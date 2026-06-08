import os
import re
from config import DOCS_PATH


def _parse_front_matter(raw):
    """Split a scraped Markdown file into (metadata, body).

    Each file starts with a YAML-style front matter block delimited by `---`:

        ---
        source: "Birmingham City University"
        title: "How to Revise with the Blurting Method"
        description: "..."
        url: "https://..."
        ---
        # How to Revise ...

    We parse the simple `key: "value"` lines directly to avoid a PyYAML
    dependency. Returns the metadata as a dict (one entry per field) and the
    remaining Markdown body. If no front matter is present, metadata is empty.
    """
    metadata = {}
    body = raw

    if raw.lstrip().startswith("---"):
        parts = re.split(r"^---\s*$", raw.strip(), maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            front, body = parts[1], parts[2]
            for line in front.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, body.strip()


def load_documents():
    """Load all scraped .md documents from the docs folder.

    Each document dict carries one field per front-matter entry (source,
    title, description, url, ...) plus the "filename" and the Markdown "text".
    """
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".md"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read()
            metadata, body = _parse_front_matter(raw)
            documents.append({
                **metadata,
                "filename": filename,
                "text": body,
            })
    source = [d.get("title", d["filename"]) for d in documents]
    print(f"Loaded {len(documents)} document(s): {source}")
    return documents


# --- Chunking parameters (see planning.md → Chunking Strategy) -------------
# Sizes are measured in TOKENS, not characters. all-MiniLM-L6-v2 truncates
# input past 256 word pieces, so 256 is the hard stop for any single chunk.
# We target 200 to stay comfortably under that limit, with a 30-token overlap
# so a thought that spans a boundary stays retrievable intact.
CHUNK_SIZE = 200
OVERLAP = 30

# Drops header-only or whitespace fragments that add noise without content.
MIN_TOKENS = 10

# Separators tried in order when a section is too large for one chunk:
# paragraph break -> line break -> sentence -> word -> character.
_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

# Matches an ATX Markdown header line, e.g. "## How to Use the Blurting Method".
_HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")

_TOKENIZER = None


def _tokenizer():
    """Lazily load the embedding model's tokenizer so chunk sizes are measured
    in the same word pieces the model will actually see at embedding time."""
    global _TOKENIZER
    if _TOKENIZER is None:
        from transformers import AutoTokenizer
        _TOKENIZER = AutoTokenizer.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    return _TOKENIZER


def _token_len(text):
    """Number of word pieces in `text` (excluding special tokens)."""
    return len(_tokenizer().encode(text, add_special_tokens=False))


def _split_into_sections(text):
    """Split a Markdown body on its headers.

    Returns a list of (heading, section_text) tuples, where `section_text` is
    the header line plus its content up to the next header. Content before the
    first header (e.g. an intro paragraph) is kept with an empty heading.
    """
    sections = []
    heading = ""
    buffer = []

    def flush():
        chunk = "\n".join(buffer).strip()
        if chunk:
            sections.append((heading, chunk))

    for line in text.splitlines():
        match = _HEADER_RE.match(line)
        if match:
            flush()
            heading = match.group(2).strip()
            buffer = [line]
        else:
            buffer.append(line)
    flush()

    return sections


def _split_keep_separator(text, separator):
    """Split `text` on `separator`, reattaching it so the pieces rejoin (via
    "".join) into the original text."""
    if separator == "":
        return list(text)
    parts = text.split(separator)
    return [p + separator for p in parts[:-1]] + [parts[-1]]


def _hard_token_split(text, max_tokens):
    """Last resort: slice a separator-free run of tokens into windows."""
    tok = _tokenizer()
    ids = tok.encode(text, add_special_tokens=False)
    return [tok.decode(ids[i:i + max_tokens]) for i in range(0, len(ids), max_tokens)]


def _atomize(text, max_tokens, separators=_SEPARATORS):
    """Break `text` into ordered pieces that each fit within `max_tokens`,
    splitting on progressively finer separators only as needed."""
    if _token_len(text) <= max_tokens:
        return [text]
    if not separators:
        return _hard_token_split(text, max_tokens)

    separator, rest = separators[0], separators[1:]
    pieces = []
    for part in _split_keep_separator(text, separator):
        if not part:
            continue
        if _token_len(part) <= max_tokens:
            pieces.append(part)
        else:
            pieces.extend(_atomize(part, max_tokens, rest))
    return pieces


def _pack(pieces, max_tokens, overlap_tokens):
    """Greedily merge atomic pieces into chunks up to `max_tokens`, seeding
    each new chunk with the tail of the previous one for `overlap_tokens` of
    sliding-window overlap."""
    chunks = []
    current = []
    current_tokens = 0

    for piece in pieces:
        piece_tokens = _token_len(piece)

        if current and current_tokens + piece_tokens > max_tokens:
            chunks.append("".join(current).strip())

            overlap_seed = []
            seed_tokens = 0
            for prev in reversed(current):
                prev_tokens = _token_len(prev)
                if seed_tokens + prev_tokens > overlap_tokens:
                    break
                overlap_seed.insert(0, prev)
                seed_tokens += prev_tokens
            current = overlap_seed
            current_tokens = seed_tokens

        current.append(piece)
        current_tokens += piece_tokens

    if current:
        chunks.append("".join(current).strip())

    return chunks


def chunk_document(document):
    """
    Split one scraped Markdown document into chunks ready for embedding.

    `document` is a dict from load_documents() (text, filename, source, title,
    url, ...).

    Strategy: token-based, header-aware chunking (see planning.md → Chunking
    Strategy). Split on Markdown headers first so each chunk stays within a
    single section; if a section exceeds the size cap, recursively split it on
    separators. Sizes are measured in the embedding model's word pieces.
      - CHUNK_SIZE = 200 tokens: well under the model's 256 word-piece
        truncation limit, large enough to carry a self-contained idea
      - OVERLAP = 30 tokens: duplicates a window of text at each boundary so an
        idea that spans two chunks can still be retrieved intact
      - MIN_TOKENS = 10: filters out header-only or whitespace fragments

    Returns a list of dicts, each with:
      - "text"     : the chunk text (str)
      - "filename" : the source document's filename (str)
      - "source"   : the publisher / author, for citation (str)
      - "title"    : the document title (str)
      - "section"  : the nearest Markdown heading, if any (str)
      - "chunk_id" : a unique identifier, e.g. "blurting_method_0" (str)
    """
    text = document["text"]
    filename = document["filename"]
    source = document.get("source", "")
    title = document.get("title", "")
    prefix = filename[:-len(".md")] if filename.endswith(".md") else filename

    chunks = []
    counter = 0

    for heading, section in _split_into_sections(text):
        pieces = _atomize(section, CHUNK_SIZE)
        for chunk_text in _pack(pieces, CHUNK_SIZE, OVERLAP):
            if _token_len(chunk_text) < MIN_TOKENS:
                continue
            chunks.append({
                "text": chunk_text,
                "filename": filename,
                "source": source,
                "title": title,
                "section": heading,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

    return chunks


if __name__ == "__main__":
    # Quick smoke test for the ingestion + chunking pipeline.
    # Run with:  python ingest.py
    # Plain asserts (no test framework). Prints a summary and a few
    # representative chunks so you can eyeball chunking before re-ingesting.
    HARD_CAP = 256  # all-MiniLM-L6-v2 truncates input past 256 word pieces.
    REQUIRED_KEYS = {"text", "filename", "source", "title", "section", "chunk_id"}

    docs = load_documents()
    assert docs, "no documents loaded — is the documents/ folder populated?"
    print(f"\nCHUNK_SIZE={CHUNK_SIZE}, OVERLAP={OVERLAP}\n")

    all_chunks = []
    seen_ids = set()
    for doc in docs:
        # Front matter must be parsed into fields, not left in the body.
        assert doc["filename"].endswith(".md"), f"non-md file: {doc['filename']}"
        assert doc["text"].strip(), f"empty body: {doc['filename']}"
        assert not doc["text"].lstrip().startswith("---"), \
            f"front matter not stripped: {doc['filename']}"

        prefix = doc["filename"][:-len(".md")]
        chunks = chunk_document(doc)
        for i, chunk in enumerate(chunks):
            # Schema: every chunk carries the full metadata set.
            assert set(chunk) == REQUIRED_KEYS, \
                f"unexpected chunk keys for {doc['filename']}: {set(chunk)}"
            assert chunk["text"].strip(), f"empty chunk in {doc['filename']}"
            assert chunk["filename"] == doc["filename"]

            # chunk_id is `filename_number` and unique across the corpus.
            assert chunk["chunk_id"] == f"{prefix}_{i}", \
                f"unexpected chunk_id: {chunk['chunk_id']}"
            assert chunk["chunk_id"] not in seen_ids, \
                f"duplicate chunk_id: {chunk['chunk_id']}"
            seen_ids.add(chunk["chunk_id"])

            # No chunk may exceed the model's 256 word-piece truncation limit.
            n = _token_len(chunk["text"])
            assert n <= HARD_CAP, \
                f"{chunk['chunk_id']} has {n} tokens (> {HARD_CAP} hard cap)"

        all_chunks.extend(chunks)

    # Overlap: consecutive chunks within the same section should share text.
    checked_overlap = False
    for a, b in zip(all_chunks, all_chunks[1:]):
        if a["filename"] != b["filename"] or a["section"] != b["section"]:
            continue
        checked_overlap = True
        tail = set(a["text"].split()[-OVERLAP:])
        head = set(b["text"].split()[: OVERLAP * 2])
        assert tail & head, f"no overlap between {a['chunk_id']} and {b['chunk_id']}"
    assert checked_overlap, "no multi-chunk section found — cannot verify overlap"

    print(f"Produced {len(all_chunks)} chunks from {len(docs)} document(s).")
    token_lens = [_token_len(c["text"]) for c in all_chunks]
    print(
        f"Token length  min={min(token_lens)}  max={max(token_lens)}  "
        f"avg={sum(token_lens) / len(token_lens):.1f}"
    )

    # Print a few chunks spread across the corpus for a sanity check.
    sample_count = min(5, len(all_chunks))
    step = max(1, len(all_chunks) // sample_count)
    print(f"\nShowing {sample_count} representative chunk(s):")
    for chunk in all_chunks[::step][:sample_count]:
        preview = " ".join(chunk["text"].split())
        if len(preview) > 200:
            preview = preview[:200] + "…"
        print(f"\n  [{chunk['chunk_id']}] {chunk['title']} — {chunk['section'] or '(intro)'}")
        print(f"    {preview}")

    print("\nAll checks passed.")

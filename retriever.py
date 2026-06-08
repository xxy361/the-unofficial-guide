import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return _collection


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.

    _collection.add() takes three parallel lists built from the chunks
    returned by chunk_document():
      - documents : raw text strings — ChromaDB's embedding function converts
                    these to vectors automatically using sentence-transformers
      - metadatas : one dict per chunk, stored alongside the vector so that
                    retrieve() can surface where a result came from (title,
                    publisher/source, the nearest section heading, and the
                    source filename — used for citation in the answer)
      - ids       : the unique chunk_id strings used to identify each entry

    You don't generate embeddings manually here — you hand over the text
    and ChromaDB handles the vector math.
    """
    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "title": c["title"],
                "source": c["source"],
                "section": c["section"],
                "filename": c["filename"],
            }
            for c in chunks
        ],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    """
    Find the most relevant guide chunks for a user's question.

    Runs a search with _collection.query():
      - query_texts : a list containing your query string
      - n_results   : how many results to return (top-k, default 5)
      - include     : ["documents", "metadatas", "distances"]

    Returns a list of dicts, each with:
      - "text"     : the chunk text
      - "title"    : the source document's title (pulled from metadata)
      - "source"   : the publisher / author, for citation
      - "section"  : the nearest Markdown heading within the document
      - "distance" : the similarity score (lower = more similar for cosine)

    Note: _collection.query() returns nested lists (one per query). We send a
    single query, so we index [0] to get the actual results.
    """
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    # query() returns one inner list per query; we sent one query, so use [0].
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = [
        {
            "text": documents[i],
            "title": metadatas[i].get("title", ""),
            "source": metadatas[i].get("source", ""),
            "section": metadatas[i].get("section", ""),
            "distance": distances[i],
        }
        for i in range(len(documents))
    ]

    # TEMP: verify retrieval in the terminal — remove before Milestone 3.
    for chunk in chunks:
        print(f"[{chunk['title']}] (dist: {chunk['distance']:.3f}) {chunk['text'][:80]}...")

    return chunks

from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved guide chunks.

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "title"    : the source document's title
      - "source"   : the publisher / author, for citation
      - "section"  : the nearest section heading within the document
      - "distance" : similarity score (used to filter weak matches)

    The response:
      1. Answers using only the retrieved context — not the model's general
         knowledge (a confident wrong answer is worse than an honest "I don't
         know").
      2. Attributes the answer to the source guide(s) it actually used.
      3. Says so clearly when the answer isn't in the loaded guides.

    Returns the response as a plain string.
    """

    fallback = (
        "I couldn't find anything relevant in the loaded guides. "
        "Try rephrasing your question — or check that your ingestion pipeline is working."
    )

    if not retrieved_chunks:
        return fallback

    # Filter out weak matches (cosine distance: lower = more similar).
    relevant = [c for c in retrieved_chunks if c["distance"] <= 0.6]
    if not relevant:
        return fallback

    # Format each chunk as a labeled block, separated by a delimiter. The label
    # carries the title (and publisher, when known) so the model can cite it.
    def _label(c):
        title = c.get("title") or c.get("source") or "Unknown source"
        source = c.get("source")
        return f"{title} ({source})" if source and source != title else title

    context = "\n---\n".join(
        f"[Source: {_label(c)}]\n{c['text']}" for c in relevant
    )

    system_message = (
        "You are a study and productivity assistant for college students. "
        "Answer the user's question using ONLY the guide text provided below. "
        "Do not use any prior knowledge or general advice that isn't grounded "
        "in that text. If the provided guides don't contain the answer, say so "
        "plainly rather than guessing.\n\n"
        "Write a single, smooth piece of advice of 100-200 words. Do NOT cite "
        "or name guides inline — keep the advice flowing naturally without "
        "interruptions.\n\n"
        "Each excerpt below is labeled with the guide it came from. After your "
        "advice, end your response in exactly this format:\n\n"
        "Sources:\n"
        "<Title of each guide you used, one per line> by <Source>\n\n"
        "List every guide that actually contributed to your answer, and do not "
        "list any guide you didn't use. Use the guide titles exactly as they "
        "appear in the labels."
    )

    user_message = f"{query}\n\nContext:\n{context}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content

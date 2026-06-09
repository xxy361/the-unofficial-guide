import gradio as gr
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response


# ---------------------------------------------------------------------------
# Ingestion — runs once on startup
# ---------------------------------------------------------------------------

def run_ingestion():
    """
    Load rule documents, chunk them, and store in ChromaDB.

    If the vector store is already populated, ingestion is skipped.
    To re-ingest (e.g. after changing your chunking strategy), delete the
    ./chroma_db folder and restart the app.
    """
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting rule documents...")
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc["text"], doc["game"])
        all_chunks.extend(chunks)

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")
    else:
        print(
            "\n⚠️  No chunks produced. Make sure chunk_document() is implemented in ingest.py.\n"
            "    RulesBot will start, but won't be able to answer questions yet.\n"
        )


# ---------------------------------------------------------------------------
# Chat handler
# ---------------------------------------------------------------------------

def chat(message, history):
    if not message.strip():
        return ""
    retrieved = retrieve(message)
    return generate_response(message, retrieved)


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="indigo"),
    title="The Unofficial Guide",
) as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#312e81; margin:0;">
                📚 The Unofficial Guide
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Your guide to productivity methods &amp; learning frameworks — grounded in the source material.
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(
                    height=440,
                    placeholder=(
                        "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                        "Ask about a productivity method or learning framework to get started ✨"
                        "</div>"
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='e.g. "How should I prepare for my exams?"',
                    container=False,
                    scale=7,
                ),
                examples=[
                    "How should I prepare for my exams?",
                    "How can I take better notes in class?",
                    "I have way too much to do and don't know where to start.",
                    "How do I stop procrastinating on assignments?",
                    "What's the best way to actually focus and get more done?",
                    "I keep forgetting what I study — how do I make it stick?",
                    "How do I manage my time during a busy week?",
                    "I have a huge project due. How do I break it down?",
                    "How can I study more efficiently with less time?",
                ],
                cache_examples=False,
            )

        with gr.Column(scale=1, min_width=180):
            gr.HTML("""
                <div style="background:var(--background-fill-secondary); border:1px solid #ddd6fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:0.8rem; font-weight:700; color:#4c1d95;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                        📚 TOPICS COVERED
                    </p>
                    <ul style="font-size:0.85rem; color:#5b21b6; list-style:none;
                                padding:0; margin:0; line-height:1.8;">
                        <li>🗂️ Eisenhower Matrix</li>
                        <li>🧠 Feynman Technique</li>
                        <li>🔁 Spaced Repetition</li>
                        <li>✍️ Blurting Method</li>
                        <li>📥 PARA Method</li>
                        <li>⏱️ Time Blocking</li>
                        <li>📝 Note-Taking</li>
                        <li>🚀 Overcoming Procrastination</li>
                        <li>🎯 Multitasking</li>
                        <li>⚙️ Productivity Systems</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                        Answers are grounded in the loaded guides only. If a topic
                        isn't covered, the guide will say so.
                    </p>
                </div>
            """)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  The Unofficial Guide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    demo.launch()

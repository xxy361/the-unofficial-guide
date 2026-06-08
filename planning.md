# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The documents in this guide will cover productivity methods and learning frameworks for college students. This is valuable because it helps every college student to learn more efficiently. Sometimes the guides from school can be very generic and only cover very limiting topics.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Birmingham City University | The Blurting Method | https://www.bcu.ac.uk/exams-and-revision/best-ways-to-revise/the-blurting-method |
| 2 | Todoist | The Eisenhower Matrix | https://www.todoist.com/productivity-methods/eisenhower-matrix |
| 3 | Dennis Learning Center, The Ohio State University | The Feynman Technique | https://dennislearningcenter.osu.edu/the-feynman-technique/ |
| 4 | Stanford Center for Teaching and Learning | Improving productivity | https://ctl.stanford.edu/students/improving-productivity |
| 5 | University at Buffalo, Office of Curriculum, Assessment and Teaching Transformation | Multitasking | https://www.buffalo.edu/catt/teach/develop/theory/multitasking.html |
| 6 | Princeton University – McGraw Center | Understanding and overcoming procrastination | https://mcgraw.princeton.edu/undergraduates/resources/resource-library/understanding-and-overcoming-procrastination |
| 7 | Forte Labs | PARA system | https://fortelabs.com/blog/para/ |
| 8 | Vihaan Sondhi | Best productivity systems for students | https://medium.com/@vihaansondhi07/the-best-productivity-system-for-students-3e45fb07e26b |
| 9 | Dietrich School of Arts & Sciences Undergraduate Studies | Spaced repetition strategy | https://www.asundergrad.pitt.edu/study-lab/study-skills-tools-resources/spaced-repetition |
| 10 | Stanford Center for Teaching and Learning |Creating a weekly calendar using time blocking | https://ctl.stanford.edu/weekly-planning-time-blocking-method |
| 11 | The Princeton Review | Taking effective class notes | https://www.princetonreview.com/college-advice/taking-notes-in-class |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

Websites are scraped as Markdown files, since LLMs were to trained to best digest JSON/Markdown/plain texts. This also provides structures to the text. It is efficient to create boundaries of chunks taking advantages of the headers in Markdown files. Chunks should be spilt first based on sections. If the section split exceeds size cap, then ues recursive chunking to split on separators.

**Chunk size:** 200 tokens

**Overlap:** 30 tokens 

**Reasoning:** The recommended model is `all-MiniLM-L6-v2`. The model's [description on HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) says: "By default, input text longer than 256 word pieces is truncated." This means 256 tokens should be the hard stop for chunks.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:** 
The context length might be greatest constrain. This model has a 256-work limit. A model with bigger limit would allow chunking whole sections on the website instead of cutting paragraphs apart. Though, since most of the sources selected and web content from searches seem to be short guides that are already strctured into sections, it might not be necessary to have a huge context window and include too many ideas. 
Multilingual support is not a high priority. Since productivity and study tips are not likely to differ significantly across languages, it is not necessary to take in sources of different languages. A translating feature for the application itself might be able to handle this.
Accuracy on domain specific text is not a concern, as productivity tips are just plain language. Unless scientific and academic papers are to be included, but that is not the point of this application since it is targeting average college students.
Using hosted APIs might add network latency, rate limits, a vendor dependency, and cost, but they have higher accuracy and longer context.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How should I prepare for my exams? | Use spaced repetition/the blurting method/the Feynman technique. Don't cram and set up time blocks to study. |
| 2 | How can I take better notes in class? | Stay organized, keep them short, use abbreviations and symbols, leave space, and review/clean them up after. |
| 3 | I have way too much to do and don't know where to start. | Use the Eisenhower Matrix or time-blocking on calendar for the top priorities. |
| 4 | How do I stop procrastinating on assignments? | Set small, manageable goals. Break tasks down. Reward yourself for completed work. |
| 5 | What's the best way to actually focus and get more done? | Multitasking is not good. Use time blocking to dedicate focused time. Adopt a productivity system (e.g., PARA) to organize work. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Chunks that split key information across boundaries. A couple of documents have long paragraphs.

2. LLM might retrieve off-topic information or from wrong sources, because a lot of sources share similar vocabularies. Though an answer drawing from multiple sources is expected, an LLM could still draw text from the wrong productivity system.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │ (1) DOCUMENT INGESTION                                               │
   │     Load pre-scraped Markdown files from local /documents folder     │
   │     Future: live web scraping at runtime (stretch feature)           │
   └──────────────────────────────────────────────────────────────────────┘
                                     │  .md files
                                     ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ (2) CHUNKING                                                         │
   │     Split on Markdown headers (sections) first;                      │
   │     recursive split on separators if a section exceeds the cap       │
   │     Chunk size: 200 tokens   |   Overlap: 30 tokens                  │
   └──────────────────────────────────────────────────────────────────────┘
                                     │  text chunks
                                     ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ (3) EMBEDDING + VECTOR STORE                                         │
   │     Embed chunks → all-MiniLM-L6-v2 (sentence-transformers, 256-tok) │
   │     Store vectors + metadata → Chroma vector store                   │
   └──────────────────────────────────────────────────────────────────────┘
                                     │  indexed embeddings
                                     ▼
            user query ──► ┌──────────────────────────────────────────┐
                           │ (4) RETRIEVAL                            │
                           │     Embed query (all-MiniLM-L6-v2)       │
                           │     Similarity search, top-k = 5         │
                           └──────────────────────────────────────────┘
                                     │  5 most-relevant chunks + sources
                                     ▼
   ┌──────────────────────────────────────────────────────────────────────┐
   │ (5) GENERATION                                                       │
   │     LLM answers from retrieved chunks (+ source attribution)         │
   │     Tool: Groq — llama-3.3-70b-versatile   →   answer to user        │
   └──────────────────────────────────────────────────────────────────────┘
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Due to time constraint for the project, it is simpler to load documents from the local disks instead of implementing live web scraping from scratch. Live web scraping will be a stretch feature in the future.
AI scrapes website using the following prompt. Multiple AI tools are used in parallel (Claude, Gemini, ChatGPT) to speed up the process. Noted that the scraping is designed to output Markdown files and exclude extra contents on the web page. The cleaning process is part of the prompt for the simplifying the ingestion process.

```
Fetch and extract the main content from the provided webpage URL.
<URL>
Requirements:
* Return only information explicitly present on the page.
* Do not generate, infer, paraphrase, rewrite, or add any new facts.
* Exclude headers, footers, navigation menus, sidebars, ads, cookie banners, comments, related-content sections, social widgets, and other boilerplate content.
* Extract only the primary page/article content.
* Preserve headings, lists, tables, code blocks, and document structure.
* Keep the original wording whenever possible.
* If content cannot be reliably extracted, return an error instead of guessing.
Output format:

---
source: "<author or publisher>"
title: "<page title>"
description: "<2-sentence summary based only on the page content>"
url: "<page url>"
---
# <page title>
<clean extracted content in Markdown>

The response must contain only the YAML front matter followed by the extracted content. No additional commentary.
```

**Milestone 4 — Embedding and retrieval:**
I will first add in some existing code snippets and use Claude to modify the `ingest.py` and `retriever.py` using my Chunking Strategy, Retrieval Approach, and the Architecture Diagram. I will also use Claude to generate tests for chunk retrieval and print to the console.

**Milestone 5 — Generation and interface:**
I will first add in some existing code snippets and use Claude to modify the `generator.py` and `app.py` using my Retrieval Approach, Architecture Diagram, and perhaps some console output from the implemented retrieval feature. I will use Claude to generate system and user prompts with my instructions on grounding and citations.
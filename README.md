# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
The documents in this guide will cover productivity methods and learning frameworks for college students. This is valuable because it helps every college student to learn more efficiently. Sometimes the guides from school can be very generic and only cover very limiting topics.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Birmingham City University — The Blurting Method | Markdown (local) | https://www.bcu.ac.uk/exams-and-revision/best-ways-to-revise/the-blurting-method |
| 2 | Todoist — The Eisenhower Matrix | Markdown (local) | https://www.todoist.com/productivity-methods/eisenhower-matrix |
| 3 | Dennis Learning Center, The Ohio State University — The Feynman Technique | Markdown (local) | https://dennislearningcenter.osu.edu/the-feynman-technique/ |
| 4 | Stanford Center for Teaching and Learning — Improving productivity | Markdown (local) | https://ctl.stanford.edu/students/improving-productivity |
| 5 | University at Buffalo, Office of Curriculum, Assessment and Teaching Transformation — Multitasking | Markdown (local) | https://www.buffalo.edu/catt/teach/develop/theory/multitasking.html |
| 6 | Princeton University – McGraw Center — Understanding and overcoming procrastination | Markdown (local) | https://mcgraw.princeton.edu/undergraduates/resources/resource-library/understanding-and-overcoming-procrastination |
| 7 | Forte Labs — PARA system | Markdown (local) | https://fortelabs.com/blog/para/ |
| 8 | Vihaan Sondhi — Best productivity systems for students | Markdown (local) | https://medium.com/@vihaansondhi07/the-best-productivity-system-for-students-3e45fb07e26b |
| 9 | Dietrich School of Arts & Sciences Undergraduate Studies — Spaced repetition strategy | Markdown (local) | https://www.asundergrad.pitt.edu/study-lab/study-skills-tools-resources/spaced-repetition |
| 10 | Stanford Center for Teaching and Learning — Creating a weekly calendar using time blocking | Markdown (local) | https://ctl.stanford.edu/weekly-planning-time-blocking-method |
| 11 | The Princeton Review — Taking effective class notes | Markdown (local) | https://www.princetonreview.com/college-advice/taking-notes-in-class |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 tokens

**Overlap:** 30 tokens 

**Why these choices fit your documents:**
Websites are scraped as Markdown files, since LLMs were to trained to best digest JSON/Markdown/plain texts. This also provides structures to the text. It is efficient to create boundaries of chunks taking advantages of the headers in Markdown files. Chunks should be spilt first based on sections. If the section split exceeds size cap, then ues recursive chunking to split on separators.
The recommended model is `all-MiniLM-L6-v2`. The model's [description on HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) says: "By default, input text longer than 256 word pieces is truncated." This means 256 tokens should be the hard stop for chunks.

**Final chunk count:**
Produced 126 chunks from 11 document(s).
Token length  min=12  max=202  avg=99.4

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:**
The context length might be greatest constrain. This model has a 256-work limit. A model with bigger limit would allow chunking whole sections on the website instead of cutting paragraphs apart. Though, since most of the sources selected and web content from searches seem to be short guides that are already strctured into sections, it might not be necessary to have a huge context window and include too many ideas. 
Multilingual support is not a high priority. Since productivity and study tips are not likely to differ significantly across languages, it is not necessary to take in sources of different languages. A translating feature for the application itself might be able to handle this.
Accuracy on domain specific text is not a concern, as productivity tips are just plain language. Unless scientific and academic papers are to be included, but that is not the point of this application since it is targeting average college students.
Using hosted APIs might add network latency, rate limits, a vendor dependency, and cost, but they have higher accuracy and longer context.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

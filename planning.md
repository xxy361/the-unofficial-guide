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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**

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
LLM should list every guide that actually contributed to the response, and not listing anything else. The titles should appear exactly as they appear in the labels.


**How source attribution is surfaced in the response:**
I expect the answers to cross reference multiple sources, and after experimenting, I think inline citations is interrupting the flow the answer. So sources are listed at the end of the response.


**Complete System prompt**:
```
You are a study and productivity assistant for college students. Answer the user's question using ONLY the guide text provided below. Do not use any prior knowledge or general advice that isn't grounded in that text. If the provided guides don't contain the answer, say so plainly rather than guessing.

Write a single, smooth piece of advice of 100-200 words. Do NOT cite or name guides inline — keep the advice flowing naturally without interruptions.

Each excerpt below is labeled with the guide it came from. After your advice, end your response in exactly this format:

Sources:
<Title of each guide you used, one per line> by <Source>

List every guide that actually contributed to your answer, and do not list any guide you didn't use. Use the guide titles exactly as they appear in the labels.
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How should I prepare for my exams? | Use spaced repetition/the blurting method/the Feynman technique. Don't cram and set up time blocks to study. | To prepare for your exams, it's essential to be actively engaged in your classes and stay organized. Note taking is a crucial aspect of this, as it helps you focus, understand, and remember the information. Keep all your notes for a class in one place, and review them regularly to get the most out of them. You can use your notes to make up sample test questions or turn them into digital flashcards. Being proactive and intentional about your study system will also help you stay on top of your work and reduce stress. By seeking out what is interesting and relevant to you in the course materials and setting your own purpose for every reading and class session, you can stay motivated and overcome procrastination. | Partially relevant | Partially accurate |
| 2 | How can I take better notes in class? | Stay organized, keep them short, use abbreviations and symbols, leave space, and review/clean them up after. | To take better notes in class, it's essential to find a balance between writing down every word and only noting key points. Consider taking notes by hand, as research suggests this can be more beneficial for learning and remembering information. Keeping all your notes for a class in one place will also help you stay organized and make it easier to review them later. By actively engaging with the material and summarizing what you hear, you'll not only stay awake and focused but also improve your understanding and retention of the information. Regularly reviewing your notes can help you identify areas that need more attention and allow you to create useful study tools, such as sample test questions or flashcards. | Relevant | Accurate |
| 3 | I have way too much to do and don't know where to start. | Use the Eisenhower Matrix or time-blocking on calendar for the top priorities. | To tackle your overwhelming tasks, start by breaking them down into smaller, manageable pieces. Devote short chunks of time to each big task, focusing on making progress rather than achieving perfection. For example, spend ten minutes jotting down ideas or skimming through a long reading to get the main ideas. This approach will help you build momentum and make the task less daunting. Additionally, organize your tasks according to the outcomes you're trying to achieve, rather than broad subjects. This means grouping related tasks and information together based on the specific projects and goals you're currently working on. By doing so, you'll be able to quickly access the information you need and make progress towards your goals. | Partially relevant | Accurate |
| 4 | How do I stop procrastinating on assignments? | Set small, manageable goals. Break tasks down. Reward yourself for completed work. | To overcome procrastination on assignments, it's essential to understand the underlying reasons for your delay. Reflecting on your habits, thoughts, and feelings that lead to procrastination can help you identify areas for change. Changing your perspective by breaking down large tasks into smaller, manageable pieces can make them less intimidating. Additionally, committing to complete small tasks and rewarding yourself can help rebuild trust in yourself. It's also crucial to choose your surroundings wisely, avoiding situations that distract you from your work. By staying actively engaged in your classes, seeking out what's interesting and relevant to you, and setting your own purpose for every reading and class session, you can increase your motivation and reduce procrastination. | Relevant | Accurate |
| 5 | What's the best way to actually focus and get more done? | Multitasking is not good. Use time blocking to dedicate focused time. Adopt a productivity system (e.g., PARA) to organize work. | To focus and get more done, try breaking down big tasks into smaller, manageable chunks, and devote short periods of time to making progress on them. This approach, similar to the "Swiss Cheese" method, helps build momentum and makes the task less daunting. Additionally, remove distractions from your environment and use techniques like the Pomodoro Technique, which involves working without interruption for a set time, followed by a short break. It's also essential to set positive, concrete goals for yourself and focus on what you want to achieve, rather than what you want to avoid. By committing to small tasks, writing them down, and following through, you can rebuild trust in yourself and develop a more productive routine. | Relevant | Accurate |

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
The Architecture Diagram was very helpful to pass in as context for AI. It helped AI tool skip read through the actual files in multiple occasions.

**One way your implementation diverged from the spec, and why:**
Nothing really diverged from the spec.

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

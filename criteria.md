# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
This target checks whether the retrieval process can find useful information for most questions without requiring perfect answers every time.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Naming a source makes answers easier to verify and helps users understand where the information came from. Requiring this for every answer encourages consistency and reduces the risk of users trusting unsupported information.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
This target checks whether the system can recognize when it does not have enough relevant information to answer a question. Allowing one failure out of five acknowledges that we may not have a specific mechanism to handle irrelevant info and save tokens.

---

## 4. Consistent source citation formatting

Previous criteria: No generated chunk has a core text body shorter than 150 characters, excluding any appended source name or file path metadata.

**Revised criteria**: Every generated answer appends source citations using a standardized format (e.g., ``) at the end of the response.

**Why this target:** 
Setting a minimum chunk length helps prevent the system from creating fragments that are too short to provide meaningful context. Enough context can help the retrieval process find relevant information and generate more complete answers.
> **Revised reason**: Standardizing the source citation format ensures that answer provenance is clear, uniform, and easily parseable across all generated responses.

**Why updated:** 
> Although the initial evaluation passed well, measuring total character counts risked including file paths and source name strings rather than actual semantic content. This revision tightens the metric to ensure that the text body itself—independent of metadata maintains the 150-character floor for reliable retrieval context.

> **Revised reason**: The output style varied between inline parentheticals `(from file.txt)` and line-separated citations `Source: file.txt`. Shifting this criterion to citation consistency targets a concrete output quality requirement in the generation phase, making formatting strict, predictable, and simple to measure.

---

## 5. Chunks avoid splitting mid-sentence

At least 4 out of 5 randomly sampled chunks from the index, sentences are not artificially split across chunk boundaries at either the start or the end.


**Why this target:**

Keeping sentences intact helps preserve the meaning and context of the original text. Allowing one chunk to fail accounts for occasional boundary issues.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

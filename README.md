# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide is an AI-powered local guide built on a specialized text corpus, designed to answer targeted questions about specific local domains, guides, or communities. Instead of relying solely on general model knowledge, it uses RAG to search through the underlying document collection and generate accurate, grounded responses. Every answer includes direct source file attributions to make sure users receive verifiable information. If a user asks a question outside the scope of the provided documents, a distance-based relevance gate automatically filters it out to prevent hallucinated answers and tells the user it doesn't have enough information to provide an answer.

## Chunking Strategy

**Chunk size:** 150 characters minimum (could go up to ~500 characters based on paragraph lengths) 
**Overlap:** 0 characters (not applicable due to paragraph-boundary splitting)

During Milestone 1, I noticed that the `campus_life` corpus consists of short, self-contained student life posts and forum entries, averaging around 317 characters across 1 to 3 paragraphs. Using a fixed-size window made little sense because almost every post fit within one window which results in a 1:1 document-to-chunk mapping.

Initially, I tried splitting directly on paragraph double-newlines. However, this created several useless micro-chunks containing only standalone post headers.

To fix this, I adjusted the strategy to dynamically accumulate paragraphs until reaching a minimum threshold of 150 characters before finalizing a chunk. This preserves natural thought boundaries, attaches brief headers directly to their underlying body text, and avoids slicing sentences in half—without needing arbitrary overlap character counts.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_210.txt#0` — produced by: `chunker.py::split_documents`

```
I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Expect 8 to 10 hours a week outside class.

The one piece of advice: do the labs even though they're only 10% — the exams reuse the lab problems.
```

**Chunk 3** — source: `course_math_220_exams.txt#0` — produced by: `chunker.py::split_documents`

```
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Verrill Street Grill

Adding to what people have said about Verrill Street Grill. The wait figure of up to 30 minutes on Friday evenings matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house_laundry.txt#0` — produced by: `chunker.py::split_documents`

```
Laundry in Morrow House

Machines take $1.50 wash, $1.25 dry, coin or card. There are eight washers and six dryers for the building, which is the wrong ratio and means the dryers back up on Sunday evenings.

Best time to do laundry here is Tuesday or Wednesday morning. Sunday after 6pm you will wait.
```

## Sample Answer

**Question:**
How long is the add/drop course window period?

**Answer:**
You can add a course through the end of the second week, and you can drop a course through the end of week six. 

Source: admin_add_drop_deadline.txt

Sources retrieved: admin_add_drop_deadline.txt, advising_registration.txt, course_biol_160.txt, course_biol_160_workload.txt, transit_shuttle.txt

**My relevance cutoff:**

I left the relevance cutoff at `0.6` based on two key observations from my test runs. First, out-of-scope questions yielded high distance scores (ranging from 0.80 to 0.93), creating a  separation from our in-scope corpus questions. Second, keeping the threshold at 0.6 provides a safe margin for questions where the exact answer isn't always explicitly stated in a single phrase. This way the retriever captures relevant context without triggering unnecessary false-positive refusals.


| Question | In corpus? | Best distance |
|---|---|---|
| What time should students visit Pellew Dining Hall to avoid peak wait times? | Yes | 0.236 |
| How long is the add/drop course window period? | Yes | 0.317 |
| What is the worst day to do laundry in Morrow House? | Yes | 0.369 |
| Does North Kitchen close before Verrill Street Grill? | Yes | 0.355 |
| Roughly how many pages of reading per week are assigned in HIST 118 Modern World History? | Yes | 0.209 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.803 |
| How do I write a for loop in Rust? | No | 0.877 |

## How I Used AI

**1. Brainstorming evaluation criteria**
I asked the AI to help me brainstorm specific targets for criteria 4 and 5. The AI suggested baseline focusing on minimum character thresholds and paragraph structures, which I then refined and customized to match my specific chunking strategy and acceptance rules.

**2. Enhancing the fallback chunking logic**
I asked the AI to review the fallbackchunker and help me design a paragraph-aware splitting approach. The initial code draft split blindly and produced short fragment chunks, so I modified its implementation by adding a minimum character length threshold and a merging loop so that short headings stay attached to their following context blocks.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. The relevance gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks maintain minimum length threshold | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Chunks avoid splitting mid-sentence | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

## Real output

### What time should students visit Pellew Dining Hall to avoid peak wait times? — run 1

- Best distance: 0.2360 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt, dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
To avoid peak wait times at Pellew Dining Hall, students should go before 11:45 (`dining_pellew_dining_hall_followup.txt` and `dining_pellew_dining_hall.txt`).
```

### What time should students visit Pellew Dining Hall to avoid peak wait times? — run 2

- Best distance: 0.2360 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt, dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
To avoid peak wait times at Pellew Dining Hall, students should go before 11:45 (`dining_pellew_dining_hall_followup.txt` and `dining_pellew_dining_hall.txt`).
```

### What time should students visit Pellew Dining Hall to avoid peak wait times? — run 3

- Best distance: 0.2360 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_halden_hall_followup.txt, dining_pellew_dining_hall.txt, dining_pellew_dining_hall_followup.txt, dining_the_ridgeway_cafe_followup.txt

```
To avoid peak wait times at Pellew Dining Hall, students should go before 11:45 (`dining_pellew_dining_hall.txt` and `dining_pellew_dining_hall_followup.txt`).
```

### How long is the add/drop course window period? — run 1

- Best distance: 0.3166 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, advising_registration.txt, course_biol_160.txt, course_biol_160_workload.txt, transit_shuttle.txt

```
You can add a course through the end of the second week, and dropping is allowed through the end of week six. 

Source: admin_add_drop_deadline.txt
```

### How long is the add/drop course window period? — run 2

- Best distance: 0.3166 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, advising_registration.txt, course_biol_160.txt, course_biol_160_workload.txt, transit_shuttle.txt

```
You can add a course through the end of the second week, and dropping is allowed through the end of week six. 

Source: admin_add_drop_deadline.txt
```

### How long is the add/drop course window period? — run 3

- Best distance: 0.3166 (passed the gate)
- Sources retrieved: admin_add_drop_deadline.txt, advising_registration.txt, course_biol_160.txt, course_biol_160_workload.txt, transit_shuttle.txt

```
You can add a course through the end of the second week, and dropping is allowed through the end of week six. 

Source: admin_add_drop_deadline.txt
```

### What is the worst day to do laundry in Morrow House? — run 1

- Best distance: 0.3686 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt

```
Based on the documents, the worst time to do laundry is Sunday after 6 pm, when you will have to wait due to backed-up dryers. 

Source: `housing_morrow_house_laundry.txt`
```

### What is the worst day to do laundry in Morrow House? — run 2

- Best distance: 0.3686 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt

```
Based on the documents, the worst time to do laundry is Sunday after 6pm, as you will have to wait (housing_morrow_house_laundry.txt).
```

### What is the worst day to do laundry in Morrow House? — run 3

- Best distance: 0.3686 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt

```
The worst time to do laundry is Sunday after 6pm, because you will have to wait (housing_morrow_house_laundry.txt).
```

### Does North Kitchen close before Verrill Street Grill? — run 1

- Best distance: 0.3553 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
Yes, North Kitchen closes at 7:00pm on weekdays (dining_north_kitchen.txt), whereas Verrill Street Grill is open until 1:00am daily during term (dining_verrill_street_grill.txt).
```

### Does North Kitchen close before Verrill Street Grill? — run 2

- Best distance: 0.3553 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
Yes, North Kitchen closes at 7:00pm on weekdays (`dining_north_kitchen.txt`), whereas Verrill Street Grill is open until 1:00am daily during term (`dining_verrill_street_grill.txt`).
```

### Does North Kitchen close before Verrill Street Grill? — run 3

- Best distance: 0.3553 (passed the gate)
- Sources retrieved: dining_halden_hall.txt, dining_north_kitchen.txt, dining_north_kitchen_followup.txt, dining_verrill_street_grill.txt, dining_verrill_street_grill_followup.txt

```
Yes, North Kitchen closes at 7:00pm on weekdays (`dining_north_kitchen.txt`), whereas Verrill Street Grill is open until 1:00am daily during term (`dining_verrill_street_grill.txt`).
```

### Roughly how many pages of reading per week are assigned in HIST 118 Modern World History? — run 1

- Best distance: 0.2091 (passed the gate)
- Sources retrieved: course_engl_205_workload.txt, course_hist_118.txt, course_hist_118_exams.txt, course_hist_118_workload.txt

```
Roughly 120 pages of reading per week are assigned in HIST 118 Modern World History. 

Sources: `course_hist_118_workload.txt` and `course_hist_118.txt`.
```

### Roughly how many pages of reading per week are assigned in HIST 118 Modern World History? — run 2

- Best distance: 0.2091 (passed the gate)
- Sources retrieved: course_engl_205_workload.txt, course_hist_118.txt, course_hist_118_exams.txt, course_hist_118_workload.txt

```
HIST 118 Modern World History assigns about 120 pages of reading per week. 

Source: `course_hist_118_workload.txt` (also mentioned in `course_hist_118.txt`)
```

### Roughly how many pages of reading per week are assigned in HIST 118 Modern World History? — run 3

- Best distance: 0.2091 (passed the gate)
- Sources retrieved: course_engl_205_workload.txt, course_hist_118.txt, course_hist_118_exams.txt, course_hist_118_workload.txt

```
Roughly 120 pages of reading per week are assigned in HIST 118 Modern World History. 

Sources: `course_hist_118_workload.txt` and `course_hist_118.txt`.
```


## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET |All 5 test questions successfully retrieved chunks containing the correct/relevant answers across for every pass. |  |
| 2 | Every answer names a source | MET | All of the generated answers across all three runs explicitly cited their source file names. |  |
| 3 | The relevance gate stops out-of-corpus questions | MET | The distance-based relevance gate successfully blocked all 5 out-of-scope questions with high distance scores (0.80+), meeting the 4 of 5 target. |  |
| 4 | Chunks maintain minimum length threshold | MET | Using an online word counter, I manually checked that each output is at least 150 characters long. |  |
| 5 | Chunks avoid splitting mid-sentence | MET | Manual inspection of randomly sampled index chunks showed that natural paragraph boundaries were preserved without truncating sentences mid-way. |  |


## Diagnoses

Since all criteria passed cleanly across all three evaluation runs, there were no functional misses to diagnose. However, if I had to tighten a target, I would refine Criterion 4 to enforce a strict content-only minimum length.

## The Improvement

**What I changed:**
Tightened Criterion 4 from a general 150-character minimum chunk size to: *"No generated chunk has a core text body shorter than 150 characters, excluding any appended source name or file path metadata."*

**Why I picked it:**
While our paragraph-aware chunker successfully maintained a minimum length threshold, evaluating total character counts can occasionally allow short text fragments if metadata strings inflate the overall metric. Tightening this ensures that the actual textual content consistently provides enough context for generation.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

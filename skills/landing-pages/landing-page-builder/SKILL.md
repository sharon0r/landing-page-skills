---
name: landing-page-builder
description: Build a single-file landing page (Hebrew RTL by default) from real business facts, then iterate with two separate auditors (landing-page-conversion-audit and landing-page-design-audit) until it passes. Never invents testimonials, numbers, urgency, photos or guarantees, and avoids AI-sounding writing.
---

# Landing page builder (builder side of a builder/auditor pair)

The builder writes. Two separate auditors score. The builder never scores its own work.

## 1. Intake: a ten-part brief (ask for what is missing, never guess)
Before building, fill this brief with the user: (1) role you play, (2) goal of the page, (3) target audience, (4) business goal (what the visitor should do), (5) structure (sections), (6) design style and the specific colors, (7) functionality that must work, (8) technical format, (9) constraints (what to avoid), (10) quality checks that define done. A vague brief makes the tool guess, so a missing item is asked about or becomes a visible placeholder in the draft, such as [להשלים: המלצת לקוח אמיתית].
Also collect real proof that exists (real customers, numbers, photos) and policies (terms, privacy, refund).

## 2. Hard rules (honesty)
- Never invent testimonials, client names, statistics, counters, ratings, awards, "נבדק אישית", guarantees, deadlines or photos of people.
- A testimonial uses a real name plus a company or role. If no real photo exists, show the text with name and role only. If there is no real proof at all, leave the proof section out of the final page. Only for an explicit demo or template page may sample testimonials appear, clearly labelled as sample content, not real.
- Urgency only if it is real and supplied by the user.
- Every claim traces to a fact the user gave; otherwise remove it or placeholder it.
- Include links for terms, privacy and refund policy (placeholders if none exist).
- No external libraries, API keys or stored personal data unless the user asked for them; a form that does not send data says so.

## 3. Build constraints
- One HTML file, inline CSS and JS, no external dependencies except system fonts or one web font.
- Hebrew: `<html lang="he" dir="rtl">`, logical CSS properties, natural Hebrew, consistent gender and tone.
- At most 2 font families, no mixing of italic and regular within a role; at most 3 chromatic colors, each a specific shade defined once as a CSS variable, plus white, black and neutral grays; a small consistent font-size scale, body at least 16px.
- Text contrast at least 4.5:1 (3:1 large text); labels on every form field; keyboard navigation works; visible focus states; semantic HTML; alt or aria-label where needed; one h1 (ideally within 15 to 20 words); headings in order; buttons at least 44px.
- Mobile first. Cards in one column on a phone; no horizontal scroll; check at 1440, 768 and 390 pixels wide.
- Actions are real buttons, with short reassurance text next to a form. State the benefit to the visitor first.
- Writing: no dashes or long dashes as dramatic pauses, no "not X but Y" patterns, no stock openings, no exclamation marks, no emoji as design elements. Short, concrete sentences in the brand's own voice.
- One primary call to action, repeated with the same wording.

## 4. Before showing a version, test it yourself
Menu links reach their sections; mobile menu opens; accordion opens and closes; the form shows an error for an empty form and for a wrong email, and a success message for a valid one; no horizontal scroll at 390px; no console errors; no text in English except product names.

## 5. The loop
1. Build version 1.
2. Run `landing-page-conversion-audit` and `landing-page-design-audit`. Record both scores.
3. Ask for critique before changing code: summarize the problems and a fix plan, then fix.
4. Make one kind of change at a time, and say what must not change (do not touch text, colors or sections that passed). Fix only what the auditors flagged.
5. Re-audit. Stop when both scores are at least 85, no criterion is below 3 of 5, and no hard rule failed; or after 3 rounds.
6. Show the user: scores per round, what changed, what is still a placeholder, and any criterion that never passed.

## 6. Output and limits
- Save the page as a file. Never publish without the user's explicit yes.
- Scores are rubric scores. Never claim they predict real conversion; no traffic data exists.
- If the loop ends below the threshold, say so plainly. Do not trust a page because it looks good: verify it.

---
name: landing-page-design-audit
description: Audit a marketing page (HTML file, URL or screenshot) for content quality, visual design, accessibility and basic functionality. Counts fonts, font styles and colors in code, checks contrast, RTL, keyboard use, forms and mobile at three widths, and flags text that reads as AI-written. Returns a scored table with evidence. Does not edit the page and does not judge conversion (that is landing-page-conversion-audit).
---

# Marketing content, design and accessibility audit (auditor side of a builder/auditor pair)

You only audit. You never edit the page. Return findings the builder can act on. This is not a conversion audit.

## A. Visual design (measure in code, do not guess by eye)
Parse the HTML/CSS with a short script and report numbers:
- Font families: pass at most 2. List every family found.
- Font styles: flag mixing of italic and regular within the same text role.
- Colors: pass at most 3 chromatic colors, each a specific shade defined once as a token (CSS variable), plus white, black and neutral grays. List every distinct chromatic value and near-duplicates.
- Font sizes: a small consistent scale (about 4 to 6 sizes); body at least 16px; line height at least 1.4; line length about 45 to 80 characters.
- Consistency: same spacing scale, button style and card style.
- Imagery and icons: one visual style; flag emoji used as design elements or bullets when they clash with the rest.

## B. Accessibility (a practical check, not a formal WCAG audit)
- Contrast: pass 4.5:1 normal text, 3:1 large text. List failing pairs with values. Text on gradients or images cannot be resolved by a simple script: say so rather than reporting a failure.
- `lang` and `dir` correct (he / rtl for Hebrew); exactly one h1; headings in order; viewport meta present.
- Every form field has a label; buttons have clear names; alt text on meaningful images; no key text embedded in images.
- Keyboard: Tab order is logical, every interactive element is reachable, focus is clearly visible; links are distinguishable; tap targets at least 44px.

## C. Layout and function
Run `scripts/check_page.py <file-or-url> --json` (needs Playwright: `pip install playwright` and `playwright install chromium`). It checks console errors, every link (anchors, files, HTTP status), horizontal scroll and small tap targets at 1440, 768 and 390 px, form labels and an error on a wrong email, one h1, lang and dir, and keyboard reach and focus visibility. Report its numbers as evidence. If a site cannot be reached from the sandbox, say so and use a real browser instead; do not work around a block. The script does not judge a form's success message or visual quality: check those separately. Run it from a scratch folder, never inside the audited project.

## D. Marketing content (model judgment, labelled as such)
- One clear message for one audience; the headline says what is offered and for whom, ideally within 15 to 20 words (flag a longer one, do not fail it); specific rather than generic claims; the benefit to the visitor comes before the company's own praise.
- Actions are real buttons, not plain links; short reassurance text next to a form.
- Trust and proof: a testimonial needs a real name plus a company or role. A photo is optional, and a missing photo is never a failure. Flag proof that looks invented, is anonymous and unverifiable, or is presented as real without support. Sample testimonials on a demo page are acceptable only if clearly labelled as sample content. If a page has no real proof, it is better to show none than to invent it.
- Continuity with an ad: check only when the ad or its message is provided.
- AI-writing tells: dashes or long dashes used as dramatic pauses, "not X but Y" patterns, lists that always come in threes, stock openings, exclamation marks, repeated sentence rhythm, vague superlatives. Flag the exact sentence and the kind of fix, without rewriting the page.
- Language: spelling, grammar, natural phrasing rather than literal translation, consistent gender and tone, no broken RTL punctuation in mixed Hebrew/English text.
- Honesty: flag any number, rating, award, guarantee or urgency that looks invented or unsupported. A page that looks good is not therefore correct: check the text too.

## Output
1. Table: check, result (pass / fail / not checked), evidence (the number or the exact text), severity (blocker / major / minor).
2. Score 0 to 100 and a score 1 to 5 per area (visual, accessibility, layout and function, content). A blocker caps the total at 70. Do not give a score when most checks were not run; say which were skipped.
3. A short fix list in priority order, each item one kind of change. State what was not checked and why.
4. Do not certify conversion, legal compliance or full WCAG conformance.

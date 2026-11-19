# Landing Page Skills

[עברית](README.he.md)

Two Claude skills that work as a pair: one **builds** a landing page, the other **audits** it. Hebrew and RTL first.

Status: first version. Tested on a small test page only; not yet on a range of real sites.

## The two skills

- **landing-page-builder** builds a single-file landing page from real business facts. It asks for what is missing instead of inventing it, and fixes only what the auditor flagged, for up to 3 rounds.
- **landing-page-design-audit** checks design, accessibility and content: font families, colors, contrast, links, mobile layout, keyboard use and forms. Whatever can be measured is measured in code (`scripts/check_page.py`). Judgment calls are labelled as judgment.

The builder never scores its own work.

## Honesty rules

The builder never invents testimonials, statistics, urgency, guarantees or photos. Missing proof stays a visible placeholder. Nothing is published without an explicit yes.

## Usage

1. Add both skill folders to Claude (each contains a `SKILL.md`).
2. Existing page: "Audit this page with landing-page-design-audit".
3. New page: "Build a landing page with landing-page-builder". It asks questions, builds, and iterates with the auditor.

Run the checker on its own:

```
pip install playwright
playwright install chromium
python skills/landing-pages/landing-page-design-audit/scripts/check_page.py <file-or-url> --json
```

It checks console errors, links, horizontal scroll at 1440/768/390 px, form labels, h1 count, `lang`/`dir`, and keyboard navigation.

## Language

Defaults are Hebrew (`lang="he"`, `dir="rtl"`). The general rules (two fonts, three colors, contrast, accessibility) apply to any language, but only Hebrew pages have been tested.

## Limits

- Scores are rubric scores, not conversion results. No traffic data is measured.
- This is a practical accessibility check, not a formal WCAG audit.
- It does not replace human review before publishing.

## Author

Sharon Weissberg: implementation and training, automation and AI

- LinkedIn: https://www.linkedin.com/in/sharonweissberg/
- Email: sharonor.we@gmail.com

## License

MIT. Provided as is, without warranty or support.

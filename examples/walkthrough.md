# Walkthrough — the skill, run on `sample-page.html`

This is a record of the skill in `skills/schema-jsonld-skill/SKILL.md`
being followed step by step on `examples/sample-page.html`.
Nothing here was written from memory; every value below comes
from the page.

## Before

`sample-page.html` has no JSON-LD in it. It has a title, a meta
description, a canonical link, an H1, a byline, a date, and five
short sections. That is all the skill has to work from.

## Step 1 — read the page

Facts found on the page:

- `<title>`: How to sharpen a kitchen knife
- H1: How to sharpen a kitchen knife
- Meta description: A short guide to sharpening a kitchen
  knife at home with a whetstone, in five steps.
- Byline: Mara Chen
- Date: `<time datetime="2026-10-04">4 October 2026</time>`
- Canonical link: https://www.sharpkitchen.blog/how-to-sharpen-a-kitchen-knife
- No rating, no price, no review, no questions and answers.

## Step 2 — pick one type

The page is an article: a headline, a body in five steps, a
byline, and a date. Type: **Article**. It shows no visible
questions and answers, so it is not a FAQPage.

## Step 3 — map fields from the page only

- `headline` — page `<title>` (same as the H1)
- `description` — meta description
- `author` — byline, "Mara Chen"
- `datePublished` — date on the page, "2026-10-04"
- `url` — canonical link

Missing: nothing the Article table needs is missing. No
rating or price was added, because the page shows none.

## Step 4 — write one block

The block written is `examples/sample-page.jsonld`:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to sharpen a kitchen knife",
  "description": "A short guide to sharpening a kitchen knife at home with a whetstone, in five steps.",
  "author": {
    "@type": "Person",
    "name": "Mara Chen"
  },
  "datePublished": "2026-10-04",
  "url": "https://www.sharpkitchen.blog/how-to-sharpen-a-kitchen-knife"
}
```

## Step 5 — check the block

Command run:

```bash
python3 -m json.tool examples/sample-page.jsonld
```

Result: exit 0. The block parses as valid JSON. The same
check was run on `faq-page.jsonld` and `thin-page.jsonld`;
both parse, exit 0.

Trace check, done by hand: every value in the block matches
something visible on `sample-page.html` — headline matches
the title and H1, description matches the meta description,
author matches the byline, date matches the `<time>` tag,
URL matches the canonical link. Nothing in the block comes
from outside the page.

## After

The page now has one JSON-LD block to paste in, in
`examples/sample-page.jsonld`. The block was not checked
with Google's Rich Results Test or the Schema.org validator;
the check run was the JSON parse in step 5, and the trace
check above. No rich result is promised.

The same steps were followed for the other two examples:
`faq-page.html` → FAQPage block in `faq-page.jsonld`
(two visible questions, copied word for word), and
`thin-page.html` → WebPage block in `thin-page.jsonld`
(only headline, description, and URL — the page shows no
author and no date, so the block has neither, and both are
listed as missing, not filled in).

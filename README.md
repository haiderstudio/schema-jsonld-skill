# schema-jsonld-skill

Write one JSON-LD block from real page content, never invent a field.

[![CI](https://github.com/haiderstudio/schema-jsonld-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/haiderstudio/schema-jsonld-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it reads one page
and writes one JSON-LD block from what the page actually
says. One job, in this order:

1. Reads the page: title, meta description, H1, byline,
   date, headings, body text, and visible questions and
   answers if the page has any.
2. Picks one type: Article for an article or blog post,
   FAQPage for a page with visible questions and answers,
   WebPage for anything else.
3. Maps fields from the page only, using a fixed table:
   headline from the title or H1, description from the
   meta description or first paragraph, author from the
   byline, date from the date on the page, URL from the
   canonical link, and FAQ questions and answers copied
   word for word.
4. Writes one block, inside one
   `<script type="application/ld+json">` tag.
5. Checks it: parses it as JSON with
   `python3 -m json.tool`, and reads every value back
   against the page. A value that matches nothing on the
   page is deleted, not kept.

A field with no source on the page is left out of the
block and listed as missing. It is never filled in with a
guess, a placeholder, or a value from another page.

## What it does NOT do

- It does not check or fix JSON-LD that already exists.
  That is an audit, a different job.
- It does not write Product, Event, Recipe, JobPosting,
  LocalBusiness, or any other type. Article, WebPage, and
  FAQPage only.
- It does not invent a field: no author, date, rating,
  review, price, or question that the page does not show.
- It does not write two blocks, or a block with two types.
  One page, one block, one type.
- It does not promise a rich result, a ranking, or better
  search placement. It writes a block. What a search
  engine does with it is not this skill's to promise.
- It does not claim the block was checked with Google's
  Rich Results Test or the Schema.org validator. The JSON
  parse check is the check this skill runs.

## Who it is for

Developers who use an AI coding agent and need JSON-LD for
a page, but keep getting blocks with made-up authors,
ratings, or dates in them. This skill writes the block from
the page in front of it, and leaves out anything the page
does not show.

## How this differs from similar tools

Checked on GitHub on Nov 6, 2026. The quoted search
`"schema-jsonld-skill"` returns 1 result:
Supraja-Gayathri-S/blog-schema-jsonld-skill, 0 stars, a
skill for AI-friendly schema markup files. The unquoted
search `schema jsonld skill` returns 4 results:
Jsonldresume/skill (5 stars, resume JSON-LD, from 2021),
blog-schema-jsonld-skill (0 stars), jsonld-knowledge-graph
(2 stars, a knowledge graph kept beside llms.txt — a
different job), and genpark-dynamic-jsonld-rich-snippet-
generator-skill (0 stars, a Product and FAQPage generator).
No giant owns the exact job as a standalone repo.

The wide versions of the job live inside bigger suites,
not as one-job skills:

- Claude SEO (AgriciDaniel/claude-seo) is a full SEO
  suite; its Schema Markup skill detects, validates, and
  generates JSON-LD across many types, and needs the whole
  suite installed. This skill is one file, three types,
  and writes from the page only.
- The antigravity-awesome-skills pack (sickn33) holds a
  schema-markup skill and an SEO-AEO schema generator
  covering 10 types with rich-result eligibility checks.
  This skill covers 3 types, does no eligibility scoring,
  and writes one block.

None of those were copied. The field table, the one-block
rule, the missing-field list, and all three worked examples
here are original.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/schema-jsonld-skill .agents/skills/schema-jsonld-skill
```

## Usage

Give the agent a page, in your own words, and tell it to use
this skill. The agent follows
`skills/schema-jsonld-skill/SKILL.md`: it reads the page,
picks one type, maps fields from the page only, writes one
block, checks it parses, and hands it over with a source
list and a list of fields left out.

## Example 1 — an article page

Page: `examples/sample-page.html` — "How to sharpen a
kitchen knife", byline Mara Chen, date 4 October 2026.
The skill writes `examples/sample-page.jsonld`:

```json
{
    "@context": "https://schema.org",
    "@type": "Article",
    "author": {
        "@type": "Person",
        "name": "Mara Chen"
    },
    "datePublished": "2026-10-04",
    "description": "A short guide to sharpening a kitchen knife at home with a whetstone, in five steps.",
    "headline": "How to sharpen a kitchen knife",
    "url": "https://www.sharpkitchen.blog/how-to-sharpen-a-kitchen-knife"
}
```

Every value is on the page: the headline is the title and
H1, the description is the meta description, the author is
the byline, the date is the `<time>` tag, the URL is the
canonical link.

## Example 2 — a FAQ page

Page: `examples/faq-page.html` — "Knife sharpening
questions", with two visible questions and answers. The
skill writes `examples/faq-page.jsonld`:

```json
{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "description": "Answers to the two questions people ask most about sharpening kitchen knives.",
    "headline": "Knife sharpening questions",
    "mainEntity": [
        {
            "@type": "Question",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Every few months for home use, or when the knife stops cutting a tomato cleanly."
            },
            "name": "How often should I sharpen a kitchen knife?"
        },
        {
            "@type": "Question",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "No. A serrated knife needs a rod made for serrated edges."
            },
            "name": "Can I use a whetstone on a serrated knife?"
        }
    ],
    "url": "https://www.sharpkitchen.blog/knife-sharpening-questions"
}
```

Both questions and both answers are copied word for word
from the page. No third question was added.

## Example 3 — a thin page, fields left out

Page: `examples/thin-page.html` — "Knife care", a title
and a description, no byline, no date. The skill writes
`examples/thin-page.jsonld`:

```json
{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "description": "Simple care for kitchen knives: wash, dry, store.",
    "headline": "Knife care",
    "url": "https://www.sharpkitchen.blog/knife-care"
}
```

No author, no date. The page shows neither, so the block
has neither. The missing fields are listed, not filled in.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check that `SKILL.md` has valid `name` and
`description` frontmatter and the required workflow sections;
that `.gitignore` starts with `.env`; that all three example
blocks parse as valid JSON, have one `@type` each, contain
no invented fields, and that every value in each block
appears in its source page; that the FAQ block has exactly
two questions and the thin-page block has no author or date;
and that the README's check command
(`python3 -m json.tool examples/sample-page.jsonld`)
actually runs. No placeholder text anywhere in the repo.
Standard library only — no third-party module is imported.

The walkthrough of the skill run on the sample page is in
`examples/walkthrough.md`, with the exact commands and
their real output.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests
are welcome; please keep examples real and checkable.

## Licence

MIT — see [LICENSE](LICENSE). This is original work. The
"write JSON-LD from page content" job is widely known; the
related tools named above are listed as related work, not
sources — nothing here was copied from them.

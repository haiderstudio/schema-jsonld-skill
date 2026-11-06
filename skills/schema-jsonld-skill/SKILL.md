---
name: schema-jsonld-skill
description: Write one JSON-LD block from real page content, never invent a field. Use when a page needs JSON-LD and you have the page in front of you. Reads the page's real title, description, headings, byline, date, and visible questions and answers, then writes one Article, WebPage, or FAQPage block. Never invents a field it cannot see on the page.
---

# schema-jsonld-skill

Write one JSON-LD block from what the page actually says.
One block, one type, every field traced to the page.
A field with no source on the page is left out, not filled in.

## When to use this skill

Use it when:
- A page has no JSON-LD yet and needs one block: an article,
  a plain page, or a page with visible questions and answers.
- You have the page in front of you: its title, meta
  description, headings, byline, date, and body text.
- The user names the page (a file or a URL) and wants the
  block written from that page's content.

## When NOT to use it

- Do not use it to check or fix JSON-LD that already exists.
  That is an audit, a different job.
- Do not use it for Product, Event, Recipe, JobPosting,
  LocalBusiness, or any other type. This skill writes
  Article, WebPage, and FAQPage only.
- Do not use it when there is no page to read from — no
  title, no text, no visible content. There is nothing to
  write from, so write nothing.
- Do not use it to write JSON-LD for a page you have not
  read. A block written from memory is invented.
- Do not use it to promise a rich result, a ranking, or
  better search placement. This skill writes a block. What
  a search engine does with it is not yours to promise.

## Workflow

### 1. Read the page

Read the whole page the user gave you. Write down only
what is actually there:

- The `<title>` and the H1.
- The meta description, if the page has one.
- The byline (author name), if the page shows one.
- The date, if the page shows one.
- The headings and the first paragraph.
- For a FAQ page: each question and its answer, exactly
  as they appear on the page.
- The page address (the canonical link, or the URL the
  user gave).

Do not read anything else into the page. If a fact is not
on the page, you do not have it.

### 2. Pick one type

Pick exactly one type, by what the page is:

- **FAQPage** — only if the page shows visible questions
  with visible answers. The questions and answers must be
  on the page as text a visitor can read.
- **Article** — if the page is an article or blog post: a
  headline, a body, and usually a byline or a date.
- **WebPage** — for anything else: a plain page with a
  title and some text, and no article body or visible
  questions and answers.

If the page fits two types, pick the one that matches what
the page is for, and say why in one line. Never write two
blocks, never write a block with two types.

### 3. Map fields from the page only

Use only this table. A field not in this table does not go
in the block.

| Field | Source on the page |
|-------|--------------------|
| `headline` | The `<title>`, or the H1 if the title is missing |
| `description` | The meta description, or the first paragraph if there is no meta description |
| `author` | The byline, as written on the page |
| `datePublished` | The date shown on the page |
| `url` | The canonical link, or the address the user gave |
| `mainEntity` (FAQPage only) | Each visible question and its visible answer, word for word |

Rules for the mapping:

- Every value must come from the page. Copy it as written;
  do not improve it, shorten it, or reword it.
- If a field has no source on the page, leave it out of
  the block and list it under "Missing" (step 5). Never
  fill it in with a guess, a placeholder, or a value from
  another page.
- Never add `aggregateRating`, a star rating, a review, a
  price, an offer, or an author you made up. If the page
  does not show it, the block does not have it.
- Dates must be the date on the page, in `YYYY-MM-DD`
  form. Do not use today's date unless the page shows it.

### 4. Write one block

Write the block in this fixed shape, inside a script tag:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "<from the page>",
  "description": "<from the page>",
  "author": {
    "@type": "Person",
    "name": "<from the page>"
  },
  "datePublished": "<from the page>",
  "url": "<from the page>"
}
</script>
```

For a WebPage, leave out `author` and `datePublished`
unless the page shows them. For a FAQPage, use this shape:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "headline": "<from the page>",
  "description": "<from the page>",
  "url": "<from the page>",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "<question, as written on the page>",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<answer, as written on the page>"
      }
    }
  ]
}
</script>
```

### 5. Check the block, then output it

Before handing the block over, check it:

1. Parse it as JSON. Run `python3 -m json.tool` on the
   block (without the script tags). If it does not parse,
   fix it. A block that does not parse is not a block.
2. Read every value back against the page. Each one must
   match something visible on the page. A value that
   matches nothing is invented — delete it.
3. Count the types. There is one `@type` in the block.
   Two types means two blocks were written as one — split
   them, then keep only the one that fits the page.

Then output, in this order:

1. The block, in one code block, ready to paste.
2. A source list: one line per field, naming where on
   the page it came from (`headline — page <title>`).
3. A "Missing" list: fields left out because the page
   did not show them. A missing field is a fact about
   the page, not a gap to fill.

## Good examples

An article page with a byline and a date (full worked
example in `examples/sample-page.html` and
`examples/sample-page.jsonld`):

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

Every value is on the page: the headline is the title and
H1, the description is the meta description, the author is
the byline, the date is the `<time>` tag, the URL is the
canonical link.

A thin page with only a title and a description (full
worked example in `examples/thin-page.html` and
`examples/thin-page.jsonld`):

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "headline": "Knife care",
  "description": "Simple care for kitchen knives: wash, dry, store.",
  "url": "https://www.sharpkitchen.blog/knife-care"
}
```

No author, no date. The page shows neither, so the block
has neither. The missing fields are listed, not filled in.

A FAQ page (full worked example in `examples/faq-page.html`
and `examples/faq-page.jsonld`): type FAQPage, with one
`mainEntity` entry per visible question, question and
answer copied word for word from the page.

## Bad examples (do not write like this)

> Page shows no author. The block has
> `"author": {"@type": "Person", "name": "John Smith"}`.

The name came from nowhere. A missing author means no
author field, not a made-up one.

> Page shows no rating. The block has
> `"aggregateRating": {"@type": "AggregateRating",
> "ratingValue": "4.8", "reviewCount": "132"}`.

A rating the page does not show is a lie in the block.
Ratings are not in the field table at all.

> An article page gets a Product block because the article
> mentions a knife for sale.

The page is an article, not a product page. The type
follows what the page is, not what it mentions.

> Questions written for the FAQPage that do not appear on
> the page.

FAQPage answers must be visible on the page. Questions
invented for the block are not visible content.

> The block is pasted in without parsing it first, and it
> has a missing comma.

Run `python3 -m json.tool` first. An unparsed block is
not checked work.

## Output rules

- Output one block per page, in one code block.
- Every value in the block must trace to the page. If it
  cannot be traced, leave it out.
- Never invent a field, a value, a name, a date, a rating,
  or a question.
- Never claim the block was checked with Google's Rich
  Results Test or the Schema.org validator unless you
  actually ran the block through them. The JSON parse
  check in step 5 is the check this skill runs.
- Never promise a rich result, a ranking, or indexing.
  The block is written; what a search engine does with
  it is outside this skill.

## Limits and safety rules

- This skill reads one page and writes one block. It
  sends nothing anywhere, edits no file, and needs no API
  key or secret.
- It writes Article, WebPage, and FAQPage only. No other
  type, no second block, no `@graph` with several types.
- It never invents a field. A missing field is listed as
  missing, never filled in.
- It never copies a block from another page. Each block
  is written from the page in front of it.
- The block is not a promise. Valid JSON is not the same
  as a rich result, and this skill does not check Google's
  rules — it only checks that the block parses and that
  every value comes from the page.

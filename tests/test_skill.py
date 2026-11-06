"""Tests for the schema-jsonld-skill: frontmatter (plain-text parse,
no yaml import), required sections, .gitignore, the three worked
JSON-LD blocks (valid JSON, one type, every value traced to the
source page, no invented fields), README examples matching the
real files, and the README's check command actually running.

Standard library only — re, json, subprocess, sys, pathlib.
A clean CI runner has no third-party modules, so none are
imported here.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "schema-jsonld-skill" / "SKILL.md"
README = ROOT / "README.md"
GITIGNORE = ROOT / ".gitignore"
CI = ROOT / ".github" / "workflows" / "ci.yml"
BANNED = ["TODO", "FIXME", "lorem", "coming soon"]
# Fields that must never appear in a written block. They are named
# in SKILL.md only as bad examples, never in a block.
INVENTED_FIELDS = ["aggregateRating", "ratingValue", "reviewCount",
                   "review", "price", "offers", "John Smith"]
# (page html, written block, expected type)
PAIRS = [
    ("sample-page.html", "sample-page.jsonld", "Article"),
    ("faq-page.html", "faq-page.jsonld", "FAQPage"),
    ("thin-page.html", "thin-page.jsonld", "WebPage"),
]


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        sys.exit(1)


def leaf_strings(obj, skip_keys):
    """All string values in a parsed JSON value, skipping the
    values of the named keys."""
    out = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in skip_keys:
                continue
            out.extend(leaf_strings(value, skip_keys))
    elif isinstance(obj, list):
        for value in obj:
            out.extend(leaf_strings(value, skip_keys))
    elif isinstance(obj, str):
        out.append(obj)
    return out


def main():
    skill = SKILL.read_text()
    m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    check("test_skill_frontmatter",
          bool(m) and "name: schema-jsonld-skill" in m.group(1)
          and "description:" in m.group(1))
    for section in ["When to use this skill", "When NOT to use it",
                    "Workflow", "Good examples", "Bad examples",
                    "Output rules", "Limits and safety rules"]:
        check("test_skill_sections_" + section.split()[0], section in skill)
    check("test_skill_three_types_only",
          all(t in skill for t in ["Article", "WebPage", "FAQPage"])
          and "Product" in skill  # named only as a NOT-use type
          and "never invent" in skill.lower())
    check("test_gitignore_env_first",
          GITIGNORE.read_text().splitlines()[0] == ".env")
    for f in [SKILL, README, GITIGNORE, CI]:
        check("test_no_placeholders_" + f.name,
              not any(b in f.read_text() for b in BANNED))
    check("test_no_absolute_paths",
          "/home/hatch" not in (SKILL.read_text() + README.read_text()))

    readme = README.read_text()
    for page_name, block_name, expected_type in PAIRS:
        page = (ROOT / "examples" / page_name).read_text()
        block_text = (ROOT / "examples" / block_name).read_text()
        block = json.loads(block_text)
        check("test_" + block_name + "_parses", isinstance(block, dict))
        check("test_" + block_name + "_context",
              block.get("@context") == "https://schema.org")
        check("test_" + block_name + "_type",
              block.get("@type") == expected_type)
        check("test_" + block_name + "_one_type",
              list(block.keys()).count("@type") == 1)
        check("test_" + block_name + "_no_invented_fields",
              not any(field in block_text for field in INVENTED_FIELDS))
        for value in leaf_strings(block, {"@context", "@type"}):
            check("test_" + block_name + "_traced_" + value[:20],
                  value in page)
        # json.tool prints 4-space indent, keys sorted — the README
        # examples are that exact output.
        pretty = json.dumps(block, indent=4, sort_keys=True)
        check("test_" + block_name + "_in_readme", pretty in readme)
    faq = json.loads((ROOT / "examples" / "faq-page.jsonld").read_text())
    check("test_faq_two_questions", len(faq["mainEntity"]) == 2)
    thin = json.loads((ROOT / "examples" / "thin-page.jsonld").read_text())
    check("test_thin_no_author_or_date",
          "author" not in thin and "datePublished" not in thin)

    # The README's check command, actually run.
    out = subprocess.run(
        [sys.executable, "-m", "json.tool",
         str(ROOT / "examples" / "sample-page.jsonld")],
        capture_output=True, text=True)
    check("test_readme_check_command", out.returncode == 0)
    ci = CI.read_text()
    check("test_ci_valid",
          "python3 tests/test_skill.py" in ci
          and "actions/checkout@v4" in ci
          and "runs-on: ubuntu-latest" in ci)
    print("All tests passed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Case search and retrieval helper for the image generation workflow.
Searches the unified case library by keywords, category, style, and other metadata.
Usage:
  python3 scripts/search_cases.py "product photography luxury watch" --limit 5
  python3 scripts/search_cases.py --category "Portrait & People" --style "anime" --limit 10
"""

import json, os, sys, re
from pathlib import Path

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "cases", "index.json")

def load_index():
    if not os.path.exists(INDEX_PATH):
        print("Error: index.json not found. Run merge_cases.py first.", file=sys.stderr)
        sys.exit(1)
    with open(INDEX_PATH) as f:
        return json.load(f)

def score_case(case, keywords, category=None, style=None):
    """Score a case for relevance to search query."""
    score = 0
    text = (case.get("title", "") + " " + case.get("prompt", "") + " " +
            case.get("description", "") + " " + case.get("original_category", "")).lower()

    for kw in keywords:
        if kw.lower() in text:
            score += 10
        # Partial match
        for part in kw.lower().split():
            if part in text:
                score += 3

    if category and case.get("category", "").lower() == category.lower():
        score += 5

    if style:
        styles = case.get("styles", [])
        if isinstance(styles, list):
            for s in styles:
                if style.lower() in s.lower():
                    score += 8

    # Boost featured cases
    if case.get("featured"):
        score += 5

    # Boost raycast-friendly cases
    if case.get("raycast"):
        score += 2

    # Slight boost for longer, more detailed prompts
    prompt_len = len(case.get("prompt", ""))
    if prompt_len > 500:
        score += min(prompt_len // 500, 5)

    return score

def format_case(case, index):
    """Format a case for display."""
    lines = []
    lines.append(f"### [{index}] Case `{case['id']}`: {case['title']}")
    lines.append(f"- **Category:** {case.get('category', 'N/A')} | **Source:** {case.get('source', 'N/A')}")
    if case.get("author"):
        lines.append(f"- **Author:** {case['author']}")
    if case.get("featured"):
        lines.append(f"- ⭐ Featured")
    if case.get("raycast"):
        lines.append(f"- 🚀 Raycast Friendly")

    prompt = case.get("prompt", "")
    if len(prompt) > 500:
        prompt = prompt[:500] + "..."
    lines.append(f"\n**Prompt Preview:**\n```text\n{prompt}\n```\n")
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search GPT Image 2 case library")
    parser.add_argument("query", nargs="?", default="", help="Search keywords")
    parser.add_argument("--category", "-c", help="Filter by unified category")
    parser.add_argument("--style", "-s", help="Filter by visual style")
    parser.add_argument("--source", help="Filter by source project (youmind/freestylefly/evolink)")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--featured", action="store_true", help="Only featured cases")
    parser.add_argument("--raycast", action="store_true", help="Only Raycast-friendly cases")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    data = load_index()
    cases = data["cases"]
    keywords = [kw for kw in args.query.split() if kw] if args.query else []

    # Filter
    if args.source:
        cases = [c for c in cases if c.get("source") == args.source]
    if args.featured:
        cases = [c for c in cases if c.get("featured")]
    if args.raycast:
        cases = [c for c in cases if c.get("raycast")]

    # Score and rank
    if keywords or args.category or args.style:
        scored = [(score_case(c, keywords, args.category, args.style), c) for c in cases]
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [c for s, c in scored if s > 0][:args.limit]
    else:
        results = cases[:args.limit]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"# Search Results: {len(results)} cases found\n")
        if keywords:
            print(f"Query: {' '.join(keywords)}")
        if args.category:
            print(f"Category: {args.category}")
        if args.style:
            print(f"Style: {args.style}")
        print()

        for i, case in enumerate(results, 1):
            print(format_case(case, i))
            print("---\n")

        if not results:
            print("No matching cases found. Try broader keywords or check available categories:")
            for cat in data.get("categories", {}).keys():
                print(f"  - {cat}")

if __name__ == "__main__":
    main()

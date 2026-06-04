#!/usr/bin/env python3
"""
Merge all cases from 3 GPT Image 2 projects into a unified case library.
Normalizes metadata and creates a searchable JSON index.
"""

import json, os, re, shutil

BASE = "/Users/wuliang/workspace/vision-skill"
CASES_DIR = os.path.join(BASE, "cases")
SOURCES = {
    "youmind": os.path.join(BASE, "awesome-gpt-image-2-cases"),
    "freestylefly": os.path.join(BASE, "awesome-gpt-image-2-cases-v2"),
    "evolink": os.path.join(BASE, "awesome-gpt-image-2-evolink-cases"),
}

# Unified category mapping
CAT_MAP = {
    # youmind categories
    "Profile / Avatar": "Portrait & People",
    "Social Media Post": "Social Media & UI",
    "Infographic / Edu Visual": "Infographic & Charts",
    "YouTube Thumbnail": "Social Media & UI",
    "Comic / Storyboard": "Illustration & Storytelling",
    "Product Marketing": "Product & E-commerce",
    "E-commerce Main Image": "Product & E-commerce",
    "App / Web Design": "Social Media & UI",
    # freestylefly categories
    "UI & Interfaces": "Social Media & UI",
    "Charts & Infographics": "Infographic & Charts",
    "Posters & Typography": "Poster & Typography",
    "Products & E-commerce": "Product & E-commerce",
    "Brand & Logos": "Brand & Identity",
    "Architecture & Spaces": "Architecture & Scenes",
    "Photography & Realism": "Photography & Realism",
    "Illustration & Art": "Illustration & Storytelling",
    "Characters & People": "Portrait & People",
    "Scenes & Storytelling": "Illustration & Storytelling",
    "History & Classical Themes": "Illustration & Storytelling",
    "Documents & Publishing": "Infographic & Charts",
    "Other Use Cases": "Other",
    # evolink categories
    "UI & Social Media Mockup": "Social Media & UI",
    "Poster & Illustration": "Poster & Typography",
    "Portrait & Photography": "Portrait & People",
    "E-commerce": "Product & E-commerce",
    "Comparison & Community": "Other",
    "Character Design": "Portrait & People",
    "Ad Creative": "Product & E-commerce",
}

UNIFIED_CATEGORIES = [
    "Portrait & People",
    "Social Media & UI",
    "Poster & Typography",
    "Product & E-commerce",
    "Infographic & Charts",
    "Illustration & Storytelling",
    "Photography & Realism",
    "Brand & Identity",
    "Architecture & Scenes",
    "Other",
]

def sf(name):
    n = re.sub(r'[<>:"/\\|?*]', '', name)
    n = re.sub(r'[,\s]+', '-', n)
    n = re.sub(r'-+', '-', n)
    return n.strip('-')[:80]

def parse_youmind_cases():
    """Parse cases from youmind project (markdown files in cases/ subdirs)."""
    cases = []
    src = SOURCES["youmind"]
    json_path = os.path.join(src, "all-prompts.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)
        for p in data:
            cases.append({
                "id": f"ym-{p['number']:04d}",
                "source": "youmind",
                "title": p.get("title", ""),
                "description": p.get("description", ""),
                "prompt": p.get("prompt", ""),
                "category": CAT_MAP.get(p.get("category", ""), "Other"),
                "original_category": p.get("category", ""),
                "author": p.get("author", ""),
                "author_link": p.get("author_link", ""),
                "source_url": p.get("source_link", ""),
                "images": [img["url"] for img in p.get("images", [])],
                "featured": any("Featured" in b for b in p.get("badges", [])),
                "raycast": any("Raycast" in b for b in p.get("badges", [])),
                "languages": p.get("languages", ""),
                "youmind_id": p.get("youmind_id", ""),
            })
    return cases

def parse_freestylefly_cases():
    """Parse cases from freestylefly project."""
    cases = []
    src = SOURCES["freestylefly"]
    json_path = os.path.join(src, "all-cases.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)
        for c in data.get("cases", []):
            img = c.get("image", "")
            if img and img.startswith("/"):
                img = f"https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data{img}"
            cases.append({
                "id": f"ff-{c['id']:04d}",
                "source": "freestylefly",
                "title": c.get("title", ""),
                "description": "",
                "prompt": c.get("prompt", ""),
                "category": CAT_MAP.get(c.get("category", ""), "Other"),
                "original_category": c.get("category", ""),
                "author": c.get("sourceLabel", ""),
                "author_link": "",
                "source_url": c.get("sourceUrl", ""),
                "images": [img] if img else [],
                "featured": c.get("featured", False),
                "raycast": "{argument" in c.get("prompt", ""),
                "styles": c.get("styles", []),
                "scenes": c.get("scenes", []),
            })
    return cases

def parse_evolink_cases():
    """Parse cases from evolink project."""
    cases = []
    src = SOURCES["evolink"]
    json_path = os.path.join(src, "all-cases.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)
        for c in data:
            cases.append({
                "id": f"ev-{c['id']:04d}",
                "source": "evolink",
                "title": c.get("title", ""),
                "description": "",
                "prompt": c.get("prompt", ""),
                "category": CAT_MAP.get(c.get("category", ""), "Other"),
                "original_category": c.get("category", ""),
                "author": c.get("author", ""),
                "author_link": "",
                "source_url": c.get("source_url", ""),
                "images": [c["image"]] if c.get("image") else [],
                "featured": False,
                "raycast": c.get("has_raycast", False),
                "prompt_length": c.get("prompt_length", 0),
            })
    return cases

def write_case_md(case, filepath):
    """Write a standardized case markdown file."""
    l = []
    l.append(f"# {case['title']}\n")
    l.append(f"- **ID:** `{case['id']}`")
    l.append(f"- **Source:** {case['source']} ({case['original_category']})")
    l.append(f"- **Unified Category:** {case['category']}")
    if case['author']:
        l.append(f"- **Author:** {case['author']}")
    if case['source_url']:
        l.append(f"- **Original:** {case['source_url']}")
    if case['featured']:
        l.append(f"- ⭐ **Featured**")
    if case['raycast']:
        l.append(f"- 🚀 **Raycast Friendly**")
    l.append("")

    if case['description']:
        l.append(f"## 📖 Description\n\n{case['description']}\n")

    for i, img in enumerate(case.get('images', [])):
        l.append(f"![Output {i+1}]({img})\n")

    l.append(f"## 📝 Prompt\n\n```text\n{case['prompt']}\n```\n")
    l.append("---")
    return '\n'.join(l)

def main():
    print("Merging cases from 3 projects...")

    # Parse all sources
    ym = parse_youmind_cases()
    ff = parse_freestylefly_cases()
    ev = parse_evolink_cases()

    all_cases = ym + ff + ev
    print(f"  youmind: {len(ym)} cases")
    print(f"  freestylefly: {len(ff)} cases")
    print(f"  evolink: {len(ev)} cases")
    print(f"  TOTAL: {len(all_cases)} cases")

    # Clean and recreate cases dir
    if os.path.exists(CASES_DIR):
        shutil.rmtree(CASES_DIR)
    os.makedirs(CASES_DIR)

    # Write cases by unified category
    used_names = set()
    index_entries = {cat: [] for cat in UNIFIED_CATEGORIES}

    for case in all_cases:
        cat = case['category']
        if cat not in UNIFIED_CATEGORIES:
            cat = "Other"

        cat_dir = os.path.join(CASES_DIR, sf(cat))
        os.makedirs(cat_dir, exist_ok=True)

        # Generate filename
        name = sf(case['title'][:60])
        base = name; counter = 2
        while name in used_names:
            name = f"{base}-{counter}"; counter += 1
        used_names.add(name)

        fn = f"{case['id']}-{name}.md"
        fp = os.path.join(cat_dir, fn)

        with open(fp, 'w') as f:
            f.write(write_case_md(case, fp))

        index_entries[cat].append((case, fn))

    # Write category READMEs
    for cat in UNIFIED_CATEGORIES:
        entries = index_entries[cat]
        if not entries:
            continue
        cat_dir = os.path.join(CASES_DIR, sf(cat))
        l = [f"# {cat}\n", f"**{len(entries)} cases**\n---\n"]
        for case, fn in entries:
            feat = ' ⭐' if case['featured'] else ''
            rc = ' 🚀' if case['raycast'] else ''
            l.append(f"## [{case['id']}] {case['title']}{feat}{rc}\n")
            l.append(f"- Source: {case['source']} | Author: {case['author']}")
            l.append(f"\n[📄 Full case →]({fn})\n---\n")
        with open(os.path.join(cat_dir, 'README.md'), 'w') as f:
            f.write('\n'.join(l))

    # Write master INDEX
    idx = []
    idx.append("# GPT Image 2 - Unified Case Library\n")
    idx.append(f"> **{len(all_cases)} cases** from 3 projects, unified into 10 categories\n")
    idx.append("> Sources: [YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) | [freestylefly](https://github.com/freestylefly/awesome-gpt-image-2) | [EvoLinkAI](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts)\n")
    idx.append("---\n")

    idx.append("## 📊 Overview\n")
    idx.append("| Category | Cases | Source |")
    idx.append("|----------|-------|--------|")
    for cat in UNIFIED_CATEGORIES:
        entries = index_entries[cat]
        if not entries:
            continue
        sources = set(c['source'] for c, _ in entries)
        idx.append(f"| [{cat}]({sf(cat)}/README.md) | {len(entries)} | {', '.join(sources)} |")
    idx.append(f"| **Total** | **{len(all_cases)}** | **3 projects** |\n")

    # Stats
    featured = [c for c in all_cases if c['featured']]
    raycast = [c for c in all_cases if c['raycast']]
    idx.append("## 📊 Key Stats\n")
    idx.append(f"- ⭐ Featured: **{len(featured)}**")
    idx.append(f"- 🚀 Raycast-ready: **{len(raycast)}**")
    idx.append(f"- 📝 Avg prompt length: **{sum(len(c['prompt']) for c in all_cases)//len(all_cases)}** chars\n")

    idx.append("---\n## 📋 Quick Search by Category\n")
    for cat in UNIFIED_CATEGORIES:
        entries = index_entries[cat]
        if not entries:
            continue
        idx.append(f"### {cat} ({len(entries)} cases)\n")
        for case, fn in entries:
            feat = ' ⭐' if case['featured'] else ''
            rc = ' 🚀' if case['raycast'] else ''
            idx.append(f"- [{case['id']}] [{case['title']}]({sf(cat)}/{fn}){feat}{rc}")
        idx.append('')

    idx.append("---\n*Unified Case Library — auto-generated*")

    with open(os.path.join(CASES_DIR, 'INDEX.md'), 'w') as f:
        f.write('\n'.join(idx))

    # Write searchable JSON index
    index_json = {
        "total": len(all_cases),
        "categories": {cat: len(entries) for cat, entries in index_entries.items() if entries},
        "featured_count": len(featured),
        "raycast_count": len(raycast),
        "cases": all_cases,
    }
    with open(os.path.join(CASES_DIR, 'index.json'), 'w') as f:
        json.dump(index_json, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Unified case library: {CASES_DIR}")
    print(f"   Cases: {len(all_cases)} | Categories: {sum(1 for e in index_entries.values() if e)} | Files: {len(all_cases)}")

if __name__ == '__main__':
    main()

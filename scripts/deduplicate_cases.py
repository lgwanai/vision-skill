#!/usr/bin/env python3
"""
Evaluate, deduplicate, and quality-filter the unified case library.

Removes low-quality cases, merges duplicates, and produces a clean index.
"""

import json, os, re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE, "cases", "index.json")
OUTPUT_PATH = os.path.join(BASE, "cases", "index.json")  # overwrite
BACKUP_PATH = os.path.join(BASE, "cases", "index.backup.json")

# ── Quality scoring ──────────────────────────────────────────────

def score_case(c):
    """Score a case 0-10; higher = better quality."""
    s = 0
    prompt = str(c.get("prompt", ""))
    plen = len(prompt.strip())

    if plen >= 50:   s += 1      # has meaningful prompt
    if plen >= 200:  s += 1      # decent length
    if plen >= 500:  s += 1      # substantial
    if plen >= 1000: s += 1      # rich detail
    if plen >= 2000: s += 1      # very detailed

    if c.get("images"):       s += 1
    if c.get("author"):       s += 1
    if c.get("source_url"):   s += 1
    if c.get("featured"):     s += 2
    if c.get("raycast"):      s += 1

    # Penalize "原文未公开" (prompt not disclosed)
    if "原文未公开" in prompt or "prompt not disclosed" in prompt.lower():
        s -= 3

    return max(s, 0)


# ── Title normalization ───────────────────────────────────────────

def normalize_title(t):
    """Normalize title for fuzzy matching."""
    t = t.lower().strip()
    t = re.sub(r'[#\d]+', '', t)               # remove numbers
    t = re.sub(r'[\(\)\[\]（）【】「」『』""'']', '', t)  # brackets & quotes
    t = re.sub(r'[·•\-—–,，、。．.：:！!？?…\s]+', ' ', t)  # punctuation → space
    t = re.sub(r'\s+', ' ', t).strip()
    # Remove very common noise words
    noise = {'设计', '图片', '生成', '案例', '模板', '图', 'image', 'design',
             'case', 'template', 'generator', 'generation', 'create', 'poster',
             'mockup', 'card', 'page', 'the', 'a', 'an', 'of', 'in', 'and', 'to'}
    words = [w for w in t.split() if w not in noise]
    return ' '.join(words)


# ── Keyword-based category reclassification ───────────────────────

CAT_KEYWORDS = {
    "Portrait & People": [
        "portrait", "avatar", "person", "people", "face", "portrait",
        "人像", "头像", "人物", "角色", "自拍", "模特", "character",
        "girl", "boy", "woman", "man", "model", "fashion", "beauty",
        "女性", "男性", "女孩", "美妆", "时尚"
    ],
    "Poster & Typography": [
        "poster", "typography", "flyer", "banner", "brochure", "cover",
        "海报", "排版", "封面", "宣传", "广告", "banner",
        "movie", "film", "festival", "event", "magazine",
        "电影", "杂志", "活动", "节日", "演出"
    ],
    "Social Media & UI": [
        "ui", "ux", "app", "web", "website", "dashboard", "screen",
        "界面", "应用", "网站", "仪表盘", "社交", "手机",
        "social", "instagram", "youtube", "tiktok", "thumbnail",
        "mockup", "截图", "界面设计", "直播", "live stream",
        "mobile", "desktop", "landing page", "app design"
    ],
    "Product & E-commerce": [
        "product", "ecommerce", "e-commerce", "shop", "store", "packaging",
        "产品", "电商", "商品", "包装", "亚马逊", "淘宝",
        "amazon", "detail page", "listing", "product shot",
        "merchandise", "retail", "catalog"
    ],
    "Infographic & Charts": [
        "infographic", "chart", "diagram", "graph", "data", "visualization",
        "信息图", "图表", "数据", "可视化", "统计",
        "timeline", "flowchart", "mind map", "table", "report",
        "时间线", "流程图", "思维导图"
    ],
    "Illustration & Storytelling": [
        "illustration", "comic", "storyboard", "anime", "cartoon",
        "插画", "漫画", "故事", "动漫", "卡通", "绘本",
        "story", "narrative", "book", "manga", "painting",
        "drawing", "sketch", "watercolor", "oil painting"
    ],
    "Photography & Realism": [
        "photography", "photo", "realistic", "cinematic", "camera",
        "摄影", "照片", "写实", "电影感", "相机",
        "lens", "lighting", "film", "shot", "studio",
        "snapshot", "polaroid", "portrait photography"
    ],
    "Brand & Identity": [
        "brand", "logo", "identity", "business card", "letterhead",
        "品牌", "logo", "标志", "名片", "vi", "视觉识别",
        "corporate", "company", "startup"
    ],
    "Architecture & Scenes": [
        "architecture", "building", "interior", "exterior", "landscape",
        "建筑", "室内", "室外", "景观", "空间", "scene",
        "room", "house", "city", "urban", "garden",
        "城市", "地图", "map"
    ],
}


def reclassify(case):
    """Suggest a better category based on title/prompt keywords."""
    if case["category"] != "Other":
        return case["category"]

    text = f"{case.get('title','')} {case.get('prompt','')} {case.get('description','')}".lower()
    scores = defaultdict(int)
    for cat, keywords in CAT_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                scores[cat] += 1
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] >= 2:  # need at least 2 keyword matches
            return best
    return "Other"


# ── Main ──────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Case Library Quality Evaluation & Deduplication")
    print("=" * 60)

    # Load
    with open(INDEX_PATH) as f:
        data = json.load(f)
    cases = data["cases"]
    original_count = len(cases)
    print(f"\n📊 Starting with {original_count} cases")

    # ── Step 1: Remove broken cases ──
    print("\n── Step 1: Remove broken cases ──")
    # Cases with no prompt at all
    no_prompt = [c for c in cases if not c.get("prompt") or len(str(c["prompt"]).strip()) == 0]
    # Cases with "原文未公开" (prompt not disclosed) and no useful content
    undisclosed = [c for c in cases if "原文未公开" in str(c.get("prompt", "")) and len(str(c.get("prompt","")).strip()) < 50]
    # Cases with prompt < 50 chars AND no images
    empty_no_img = [c for c in cases if len(str(c.get("prompt", "").strip())) < 50 and not c.get("images")]

    remove_ids = set()
    for c in no_prompt + undisclosed + empty_no_img:
        remove_ids.add(c["id"])

    kept = [c for c in cases if c["id"] not in remove_ids]
    print(f"  No prompt at all: {len(no_prompt)}")
    print(f"  Undisclosed prompt: {len(undisclosed)}")
    print(f"  Empty prompt + no image: {len(empty_no_img)}")
    print(f"  Removed: {len(remove_ids)} (unique IDs)")
    print(f"  Remaining: {len(kept)}")

    # ── Step 2: Score all remaining cases ──
    print("\n── Step 2: Quality scoring ──")
    for c in kept:
        c["_score"] = score_case(c)

    scores = [c["_score"] for c in kept]
    print(f"  Score range: {min(scores)}-{max(scores)}, avg: {sum(scores)/len(scores):.1f}")
    for threshold in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        count = sum(1 for s in scores if s >= threshold)
        print(f"    ≥{threshold}: {count}")

    # ── Step 3: Deduplicate by title ──
    print("\n── Step 3: Title deduplication ──")
    # Group by normalized title
    groups = defaultdict(list)
    for c in kept:
        norm = normalize_title(c["title"])
        if len(norm) > 3:  # meaningful title
            groups[norm].append(c)

    dup_count = 0
    deduped = []
    standalone = set()

    for norm, group in groups.items():
        if len(group) == 1:
            deduped.append(group[0])
            standalone.add(group[0]["id"])
        else:
            # Keep the best-scored one, mark others for removal
            group.sort(key=lambda c: c["_score"], reverse=True)
            best = group[0]
            deduped.append(best)
            dup_count += len(group) - 1

            # Log duplicates
            dup_ids = [c["id"] for c in group[1:]]
            if len(group) > 2:
                print(f"  Merged {len(group)}→1: \"{group[0]['title'][:60]}\" (kept {best['id']} score={best['_score']}, removed {dup_ids})")

    # Add back cases that didn't match any group (very short titles)
    grouped_ids = set()
    for g in groups.values():
        for c in g:
            grouped_ids.add(c["id"])
    for c in kept:
        if c["id"] not in grouped_ids:
            deduped.append(c)

    print(f"  Duplicates removed: {dup_count}")
    print(f"  After dedup: {len(deduped)}")

    # ── Step 4: Near-duplicate detection by prompt similarity ──
    print("\n── Step 4: Near-duplicate detection ──")

    def prompt_tokens(c):
        p = str(c.get("prompt", ""))
        # Extract key tokens (words > 2 chars)
        tokens = set(re.findall(r'[\w一-鿿]{3,}', p.lower()))
        return tokens

    # Only check within same category to avoid false positives
    cat_groups = defaultdict(list)
    for c in deduped:
        cat_groups[c["category"]].append(c)

    near_dup_removed = 0
    final_cases = []

    for cat, cat_cases in cat_groups.items():
        # Pre-compute tokens
        tokens_list = [(c, prompt_tokens(c)) for c in cat_cases]
        removed_in_cat = set()

        for i, (c1, t1) in enumerate(tokens_list):
            if c1["id"] in removed_in_cat:
                continue
            for j, (c2, t2) in enumerate(tokens_list):
                if j <= i or c2["id"] in removed_in_cat:
                    continue
                if not t1 or not t2:
                    continue
                # Jaccard similarity
                overlap = len(t1 & t2)
                union = len(t1 | t2)
                if union == 0:
                    continue
                sim = overlap / union
                if sim > 0.7:  # very high overlap → likely duplicate
                    # Keep the higher-scored one
                    if c1["_score"] >= c2["_score"]:
                        removed_in_cat.add(c2["id"])
                    else:
                        removed_in_cat.add(c1["id"])
                        break

        for c, _ in tokens_list:
            if c["id"] not in removed_in_cat:
                final_cases.append(c)
        near_dup_removed += len(removed_in_cat)

    print(f"  Near-duplicates removed: {near_dup_removed}")
    print(f"  After near-dedup: {len(final_cases)}")

    # ── Step 5: Reclassify "Other" cases ──
    print("\n── Step 5: Reclassify 'Other' category ──")
    reclassified = 0
    for c in final_cases:
        if c["category"] == "Other":
            new_cat = reclassify(c)
            if new_cat != "Other":
                c["original_category"] = f"Other→{new_cat}"
                c["category"] = new_cat
                reclassified += 1

    print(f"  Reclassified: {reclassified} cases from 'Other'")

    # Remaining "Other"
    still_other = [c for c in final_cases if c["category"] == "Other"]
    print(f"  Still 'Other': {len(still_other)}")

    # ── Step 6: Clean up and save ──
    print("\n── Step 6: Final stats ──")

    # Remove internal _score field
    for c in final_cases:
        del c["_score"]

    # Category stats
    cat_counts = Counter(c["category"] for c in final_cases)
    for cat, n in cat_counts.most_common():
        print(f"  {cat}: {n}")

    print(f"\n  ✅ Final case count: {len(final_cases)} (removed {original_count - len(final_cases)})")

    # Backup original
    import shutil
    shutil.copy2(INDEX_PATH, BACKUP_PATH)
    print(f"  📦 Backup: {BACKUP_PATH}")

    # Save
    data["cases"] = final_cases
    data["total"] = len(final_cases)
    data["categories"] = {cat: n for cat, n in cat_counts.items()}
    data["featured_count"] = sum(1 for c in final_cases if c.get("featured"))
    data["raycast_count"] = sum(1 for c in final_cases if c.get("raycast"))

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  💾 Saved: {OUTPUT_PATH}")

    # ── Step 7: Regenerate case markdown files ──
    print("\n── Step 7: Regenerate case markdown files ──")
    # Import merge module to reuse its write functions
    import sys
    sys.path.insert(0, os.path.join(BASE, "scripts"))
    from merge_cases import sf, write_case_md, UNIFIED_CATEGORIES

    cases_dir = os.path.join(BASE, "cases")

    # Clear old markdown files (keep index.json and INDEX.md)
    for cat_name in UNIFIED_CATEGORIES:
        cat_dir = os.path.join(cases_dir, sf(cat_name))
        if os.path.exists(cat_dir):
            for fname in os.listdir(cat_dir):
                if fname.endswith('.md'):
                    os.remove(os.path.join(cat_dir, fname))

    # Regenerate
    used_names = set()
    index_entries = {cat: [] for cat in UNIFIED_CATEGORIES}

    for case in final_cases:
        cat = case['category']
        if cat not in UNIFIED_CATEGORIES:
            cat = "Other"

        cat_dir = os.path.join(cases_dir, sf(cat))
        os.makedirs(cat_dir, exist_ok=True)

        name = sf(case['title'][:60])
        base = name
        counter = 2
        while name in used_names:
            name = f"{base}-{counter}"
            counter += 1
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
        cat_dir = os.path.join(cases_dir, sf(cat))
        l = [f"# {cat}\n", f"**{len(entries)} cases**\n---\n"]
        for case, fn in entries:
            feat = ' ⭐' if case['featured'] else ''
            rc = ' 🚀' if case['raycast'] else ''
            l.append(f"## [{case['id']}] {case['title']}{feat}{rc}\n")
            l.append(f"- Source: {case['source']} | Author: {case.get('author', '')}")
            l.append(f"\n[📄 Full case →]({fn})\n---\n")
        with open(os.path.join(cat_dir, 'README.md'), 'w') as f:
            f.write('\n'.join(l))

    # Write master INDEX
    idx = []
    idx.append("# GPT Image 2 - Unified Case Library\n")
    idx.append(f"> **{len(final_cases)} cases** from 3 projects, quality-filtered & deduplicated\n")
    idx.append("> Sources: [YouMind](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) | [freestylefly](https://github.com/freestylefly/awesome-gpt-image-2) | [EvoLinkAI](https://github.com/EvoLinkAI/awesome-gpt-image-2-API-and-Prompts)\n")
    idx.append("---\n")
    idx.append("## 📊 Overview\n")
    idx.append("| Category | Cases |")
    idx.append("|----------|-------|")
    for cat in UNIFIED_CATEGORIES:
        entries = index_entries[cat]
        if not entries:
            continue
        idx.append(f"| [{cat}]({sf(cat)}/README.md) | {len(entries)} |")
    idx.append(f"| **Total** | **{len(final_cases)}** |\n")

    featured = [c for c in final_cases if c.get('featured')]
    raycast = [c for c in final_cases if c.get('raycast')]
    idx.append("## 📊 Key Stats\n")
    idx.append(f"- ⭐ Featured: **{len(featured)}**")
    idx.append(f"- 🚀 Raycast-ready: **{len(raycast)}**")
    plens = [len(str(c.get('prompt', ''))) for c in final_cases]
    if plens:
        idx.append(f"- 📝 Avg prompt length: **{sum(plens)//len(plens)}** chars\n")

    idx.append("---\n*Quality-filtered unified case library*")

    with open(os.path.join(cases_dir, 'INDEX.md'), 'w') as f:
        f.write('\n'.join(idx))

    print(f"  📄 Regenerated {len(final_cases)} case markdown files")
    print(f"  📋 Regenerated {sum(1 for e in index_entries.values() if e)} category READMEs + master INDEX")
    print("\n✅ Done!")


if __name__ == '__main__':
    main()

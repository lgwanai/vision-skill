---
name: vision-skill
description: "Use this skill for computer vision tasks including image recognition (OCR, object detection), image generation (text-to-image, image-to-image), and PPT generation (30+ styles, Markdown to PPTX). Supports asynchronous task execution with flexible upload modes and configurable models. IMPORTANT: Always follow mandatory confirmation workflow - NEVER generate immediately without user approval. For PPT, gather requirements then draft slides_plan.md then confirm then smoke test then generate."
---

# Vision Skill

## Overview

This skill provides capabilities for visual recognition, image generation, and PPT generation. It supports configurable vision models (OpenAI-compatible APIs), flexible image upload modes (COS or BASE64), and executes tasks asynchronously. **Includes a quality-filtered GPT Image 2 case library (832 curated cases)** for prompt engineering reference, **bilingual prompt output (Chinese + English)** for ChatGPT and 豆包 compatibility, and **30+ built-in PPT styles** for slide generation.

## Capabilities

### 1. Vision Recognition
Analyze images to describe content, extract text (OCR), or answer questions about the image.
- **Input**: Local image path or URL, optional prompt.
- **Process**: Based on `IMAGE_UPLOAD_MODE`, uploads to COS (URL mode) or converts to base64.
- **Output**: Text description or answer.

### 2. Image Generation (⚠️ Mandatory Confirmation Workflow)
Generate images from text prompts, optionally using reference images. **CRITICAL: The workflow below is mandatory — never skip steps.**

#### 🚨 Mandatory Image Generation Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  STEP 0: DETECT — Check if reference image is REQUIRED       │
│  STEP 1: UNDERSTAND — Confirm requirements with user         │
│  STEP 1.5: FIDELITY — Choose strict/normal/creative mode     │
│  STEP 2: SEARCH — Find 1-2 inspiration cases, do not copy    │
│  STEP 3: DRAFT — Compose a concise bilingual creative brief  │
│  STEP 4: CONFIRM — User MUST approve before generation       │
│  STEP 5: ITERATE — Refine until user says "generate"         │
│  STEP 6: EXECUTE — Generate image via vision_cli.py          │
└──────────────────────────────────────────────────────────────┘
```

---

#### 🚫 STEP 0 — REFERENCE IMAGE NECESSITY DETECTION (参考图必要性检测)

**Before any requirement gathering, first determine if this task REQUIRES a reference image.** If it does and the user hasn't provided one, **BLOCK immediately** and ask for it.

##### Detection Matrix: When is a reference image MANDATORY?

| Scenario | Requirement | Examples |
|----------|:-----------:|----------|
| **Photo Optimization/Enhancement** | 🔴 REQUIRED | "优化这张照片", "enhance this photo", "improve image quality" |
| **Photo Style Transfer** | 🔴 REQUIRED | "把这张照片变成动漫风格", "make this photo look like oil painting" |
| **Photo Editing/Retouching** | 🔴 REQUIRED | "去掉背景", "remove background", "修复这张图", "fix this image" |
| **Face/Person Swap or Edit** | 🔴 REQUIRED | "换脸", "change the person's hair", "add sunglasses to this person" |
| **Product Photo Variation** | 🔴 REQUIRED | "给这个产品换一个背景", "change this product's packaging color" |
| **Image-to-Image (图生图)** | 🔴 REQUIRED | "基于这张图生成", "use this as reference", "--ref" |
| **Style Reference ("like this")** | 🔴 REQUIRED | "像这张图一样的风格", "similar style to this image" |
| **Screenshot/UI Modification** | 🔴 REQUIRED | "改一下这个界面", "redesign this screen" |
| **Image Restoration** | 🔴 REQUIRED | "修复老照片", "restore this old photo", "去水印" |
| **Sequential Character Consistency** | 🟡 OPTIONAL | "生成同一个角色的多张图" (reference helps consistency) |
| **Pure Text-to-Image Creation** | 🟢 NOT REQUIRED | "画一只猫", "generate a cyberpunk city", "create a poster" |
| **Brand/Logo Design from Scratch** | 🟢 NOT REQUIRED | "设计一个logo", "create a brand identity" |
| **UI Mockup from Description** | 🟢 NOT REQUIRED | "设计一个APP界面", "create a dashboard mockup" |
| **Infographic from Data** | 🟢 NOT REQUIRED | "生成一张信息图", "make a chart about..." |

##### Detection Logic (check in this order):

1. **User provided a file path/URL?** → `--ref` mode, proceed normally
2. **User's request contains reference-required keywords?** → **BLOCK** and ask for reference image:
   - 优化/增强/修复/enhance/optimize/improve/fix/restore/retouch + 照片/图片/photo/image/picture
   - 改成/变成/换成/change/convert/transform/transfer/make this + 风格/样式/style/look
   - 去掉/删除/添加/修改/remove/add/modify/edit/change + 背景/颜色/元素/background/color/element
   - 换脸/修图/美颜/P图/face swap/retouch/beautify
   - 老照片/水印/模糊/watermark/blurry/old photo
   - 基于/参考/参照/according to/based on/refer to + 图/照片/图片/image/photo/picture
3. **User says "like this image" or "similar to this"?** → **BLOCK** and ask for reference image
4. **Pure creation from imagination?** → No reference needed, proceed to STEP 1

##### When BLOCKED — Response Template:

```
⚠️ 这个任务需要参考图才能继续。

您的需求属于 [具体场景，如: 照片风格优化]，必须提供一张参考图片。

请提供参考图片的文件路径，例如：
- 本地文件: /path/to/your/image.jpg
- URL: https://example.com/image.png

提供后我将继续处理。
```

**Do NOT proceed past STEP 0 until:**
- A reference image path/URL is provided (for 🔴 REQUIRED scenarios), OR
- It's confirmed as 🟢 NOT REQUIRED (pure text-to-image)

---

**STEP 1 — UNDERSTAND (需求确认):**
Once reference requirements are resolved, confirm the following. Use `AskUserQuestion` when multiple options exist:

1. **Subject (主体/内容)**: What exactly should be in the image? (person, product, scene, abstract concept)
2. **Style (风格)**: What visual style?
   - 📷 Photography (realistic, cinematic, editorial, snapshot)
   - 🎨 Illustration (anime, watercolor, oil painting, sketch, vector)
   - 🏗️ 3D Render (isometric, CGI, clay, pixel art)
   - 📰 Poster/Typography (editorial, minimal, vintage, cyberpunk)
   - 📱 UI/Screenshot (app mockup, social media, dashboard)
   - 📊 Infographic (chart, diagram, recipe card, explainer)
3. **Purpose (用途)**: What is this for? (social media, e-commerce, poster, avatar, thumbnail, ad)
4. **Format (规格)**: Aspect ratio? (1:1, 9:16, 16:9, 4:5, 3:4)
5. **Reference Image Details** (if `--ref` mode):
   - What to **KEEP** from the reference? (composition, subject, colors, style, structure)
   - What to **CHANGE**? (style, background, colors, details, mood)
   - Reference image path: the user-provided file path or URL
6. **Text/Content (文字)**: Any specific text, labels, or copy that must appear?
7. **Constraints (约束)**: Any must-avoid elements? (no watermarks, no text, specific colors)

---

#### ⚖️ STEP 1.5 — FIDELITY MODE (忠实度模式)

**Ask the user to choose a fidelity mode.** This is critical — the mode determines how much AI creativity is allowed and whether cases are referenced.

Use `AskUserQuestion` to present the three options:

| Mode | Label | Behavior | Best For |
|------|-------|----------|----------|
| 🔒 **Strict** | 严格模式 | **文字内容**严格遵循用户原文，AI 不得修改/编造/改写任何文字。光影、构图、画质等**视觉效果正常优化**。正常参考案例库。 | 品牌文案、UI 界面、海报文字、广告标语等需要精确文字的场合。中文内容尤其容易出现 AI 篡改的场景。 |
| 📋 **Normal** | 普通模式 | 以用户需求为主，案例只作灵感参考，避免堆砌摄影/渲染术语。 | 大多数图像生成场景的默认选择。 |
| 🎨 **Creative** | 创意模式 | 把需求当作方向，不机械执行清单；允许 AI 重组构图、材质、光影和叙事关系。案例仅作灵感参考。 | 艺术插画、概念设计、抽象表达、风格探索等创意场景。 |

##### Mode Selection Logic:

1. **Default = Normal** unless the user explicitly requests otherwise
2. **Auto-detect strict**: If the user's request contains specific text/copy that must appear (slogans, brand names, UI labels, headings), suggest strict mode to prevent AI from altering it
3. **Auto-detect creative**: If the user asks for "artistic", "conceptual", "abstract", "experimental", "unique style", "创意", "艺术" — suggest creative mode
4. **For UI/text-heavy tasks**: Always suggest strict mode to ensure text accuracy (no hallucinated copy)

##### CLI flags:
```bash
--fidelity strict    # Text exactly as specified, visual quality optimized
--fidelity normal    # Balanced, case-referenced (default)
--fidelity creative  # Maximum artistic freedom
```

##### Why this matters:
The key insight: AI image generators often hallucinate or alter text content (Chinese text especially). Strict mode enforces text accuracy while still optimizing visual quality. Conversely, creative mode unleashes full artistic potential when text precision is not a priority.

---

**STEP 2 — SEARCH (案例检索):**
Once requirements are confirmed, search the unified case library (832 quality-filtered cases):
```bash
python3 scripts/search_cases.py "<keywords>" --category "<category>" --style "<style>" --limit 5
```
Use 1-2 relevant cases only as inspiration signals. Present case titles/categories if useful, but do **not** paste long case prompts into the final generation prompt and do **not** force the model to reproduce a case. The user's brief and any supplied reference image take priority over the case library.

**STEP 3 — DRAFT (智能提示词生成):**
Use the intelligent prompt builder engine that integrates three-project methodology. **Outputs bilingual (Chinese + English) by default** for ChatGPT and 豆包 compatibility:
```bash
python3 scripts/prompt_builder.py \
  --subject "<subject>" \
  --style "<style>" \
  --purpose "<purpose>" \
  --category "<category>" \
  --ratio "<ratio>" \
  --mood "<mood>" \
  --composition "<composition>" \
  --colors "<palette>" \
  --text "<text_content>" \
  --constraints "<constraints>" \
  --ref "<reference_image_path_or_url>" \
  --lang "<zh/en/ja>" \
  --fidelity "<strict|normal|creative>" \
  --json-output
```

The engine automatically:
- Selects the optimal approach (JSON-structured / natural language / photography spec / platform-specific)
- Outputs **both Chinese and English prompts** — use the Chinese version for 豆包/国内模型, English for ChatGPT/DALL·E
- Respects fidelity mode: strict (text accuracy) / normal (concise, user-led) / creative (open-ended, high creative freedom)
- Extracts light inspiration signals from the quality-filtered case library without copying full case prompts
- Avoids automatic camera/lens/lighting keyword injection unless the user explicitly asks for those controls
- Integrates negative constraints from the constraint library
- References top-matched cases for pattern extraction (normal mode only)

**Prompt Quality Principles (from quality-filtered case analysis):**
1. **Brief first** — keep the final prompt short enough for the image model to interpret creatively
2. **Structured sections** for complex layouts — panels, grids, rows, columns with explicit numbering
3. **Negative constraints** — include only user constraints or 1-3 essential defaults
4. **Aspect ratio** — always specify, as 21.8% of quality cases do
5. **Text specs** — for UI/posters, explicitly list every text string that must appear
6. **Color system** — 4-6 color palette for posters/brand; dominant + accent for photos
7. **Raycast** — use `{argument}` for flexible parameters when user needs variants

**STEP 4 — CONFIRM (用户确认):**
Present the draft prompt to the user with:
- The full prompt text
- Reference to the cases that inspired it, clearly marked as inspiration only
- For `--ref` mode: confirm the reference image path and transformation details
- Ask: "Does this look good? Would you like to adjust anything, or shall I generate?"

**⚠️ NEVER generate until the user explicitly confirms (e.g., "生成", "generate", "ok", "yes").**

**STEP 5 — ITERATE (迭代优化):**
If the user requests changes:
- Adjust specific elements as requested
- Re-present the updated prompt
- Continue until user approves

**STEP 6 — EXECUTE (执行生图):**
Only after user confirmation, execute. **For `--ref` mode, the reference image is uploaded via COS (returns URL) or converted to BASE64 based on `IMAGE_UPLOAD_MODE` config.**

```bash
# Pure Text-to-Image (no reference)
python3 scripts/vision_cli.py generate "<final_prompt>" --style <preset> --wait --output ./output.png

# Image-to-Image with reference (COS URL or BASE64 handled automatically by vision_cli.py)
python3 scripts/vision_cli.py generate "<final_prompt>" --ref <user_provided_image_path> --wait --output ./output.png
```

The `vision_cli.py` script handles reference image upload automatically:
- **COS mode** (`IMAGE_UPLOAD_MODE=cos`): Uploads the reference image to COS and passes the COS URL to the API
- **BASE64 mode** (`IMAGE_UPLOAD_MODE=base64`): Converts the reference image to base64 and embeds it in the API request

#### Text-to-Image
Generate images from a text description. **STEP 0 check**: 🟢 reference NOT required unless user explicitly asks for style reference.

#### Image-to-Image
Generate images based on a reference image. **STEP 0 check**: 🔴 reference REQUIRED. In STEP 1, also confirm: what to keep from the reference, what to change. Reference image is uploaded via COS or BASE64 in STEP 6.

#### Sequential Generation
Generate a series of consistent images (e.g., storyboards). Each image follows the same workflow. Reference image for character consistency is 🟡 OPTIONAL but recommended.

### 3. WeChat Chat Screenshot Recognition
Specialized recognition for WeChat chat screenshots:
- **Platform Detection**: Distinguish between PC and mobile WeChat
- **Sender Identification**: Green bubbles = self, gray/white bubbles = others
- **Structured Output**: Returns JSON with platform, chat title, and message list
- **Message Types**: Supports text, image, voice, video, link detection

### 4. Unified Case Library (832 quality-filtered cases)
Searchable library of GPT Image 2 prompts from 3 community projects, deduplicated and quality-filtered. Organized in 10 unified categories:
- Portrait & People (193 cases)
- Poster & Typography (180 cases)
- Social Media & UI (107 cases)
- Photography & Realism (102 cases)
- Illustration & Storytelling (87 cases)
- Product & E-commerce (54 cases)
- Infographic & Charts (42 cases)
- Brand & Identity (20 cases)
- Architecture & Scenes (15 cases)
- Other (32 cases)

> **Quality filter:** Removed 490 low-quality cases (empty prompts, duplicates, near-duplicates). Original data preserved in `references/data/`.
> **Deduplication script:** `python3 scripts/deduplicate_cases.py` to regenerate after updating reference data.

Search cases: `python3 scripts/search_cases.py "<query>" --limit 5`
Browse by category: `cases/<category>/README.md`
Master index: `cases/INDEX.md`

## Usage

The skill is exposed via a CLI script `scripts/vision_cli.py`.

### Prerequisites
Environment variables must be set in `config.txt` (or system environment):
- `VISION_API_BASE_URL`, `VISION_API_KEY`, `VISION_MODEL` (for vision recognition)
- `IMAGE_API_BASE_URL`, `IMAGE_API_KEY`, `IMAGE_MODEL` (for image generation)
- `IMAGE_UPLOAD_MODE`: Choose `cos` or `base64` (default: `cos`)
- If `IMAGE_UPLOAD_MODE=cos`, also set: `COS_SECRET_ID`, `COS_SECRET_KEY`, `COS_REGION`, `COS_BUCKET_NAME`

### Commands

#### Vision Recognition
```bash
# Basic Usage
python3 scripts/vision_cli.py recognize <image_path> --prompt "Describe this image"

# Using Presets (--format)
# Available formats: invoice, contract, form, slide, whiteboard, table, json, key_value, markdown_note, qa_pairs, code, ocr, analysis, wechat_chat
python3 scripts/vision_cli.py recognize ./invoice.jpg --format json
python3 scripts/vision_cli.py recognize ./screenshot.png --format code

# Batch recognition
python3 scripts/vision_cli.py recognize ./a.jpg ./b.jpg ./c.jpg --format table --wait --output ./batch_result.json

# Quality mode and retry
python3 scripts/vision_cli.py recognize ./contract.png --format contract --quality high --retry 3 --wait

# Wait for result and save to file
python3 scripts/vision_cli.py recognize ./doc.jpg --format ocr --wait --output ./result.txt

# WeChat chat screenshot recognition
python3 scripts/vision_cli.py recognize ./wechat_screenshot.png --format wechat_chat --wait
```

#### Image Generation
```bash
# Text to Image with Style Presets (--style)
# Available styles: ppt, business_flat, cartoon, tech_isometric, hand_drawn, icon, photo, anime, sketch
python3 scripts/vision_cli.py generate "A cyberpunk city" --style anime

# Image to Image
python3 scripts/vision_cli.py generate "Make it snowy" --ref <image_path>

# Sequential Generation
python3 scripts/vision_cli.py generate "A story about a cat" --seq 4 --style cartoon

# Wait for result and save image
python3 scripts/vision_cli.py generate "App icon for a camera" --style icon --wait --output ./icon.png

# Quality mode and retry
python3 scripts/vision_cli.py generate "A SaaS architecture illustration" --style tech_isometric --quality high --retry 3 --wait
```

#### Check Status
```bash
python3 scripts/vision_cli.py status <task_id>
# Or save result if completed
python3 scripts/vision_cli.py status <task_id> --output ./final_result.png
```

## 5. PPT Generation (⚠️ Interactive Confirmation Workflow)

Generate visually striking 16:9 PPT slides from a Markdown outline + visual style, then package into a `.pptx` file. Uses the existing `IMAGE_API_*` model (does NOT require gpt-image-2).

**30+ built-in styles** in `styles/` covering tech, business, academic, creative, and industry-specific aesthetics. See `docs/distilled-styles.md` for visual previews.

### 🚨 Mandatory Interactive Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  STEP 1: GATHER — Ask user: content/audience/page count?     │
│  STEP 2: RECOMMEND — Suggest 1-2 styles based on scenario    │
│  STEP 3: DRAFT — Write slides_plan.md, show user for review  │
│  STEP 4: CONFIRM PLAN — User MUST approve content            │
│  STEP 5: SMOKE TEST — Generate 1 slide (cover) to verify     │
│  STEP 6: CONFIRM STYLE — User approves style → generate all  │
│  STEP 7: DELIVER — Package PPTX, tell user the path          │
└──────────────────────────────────────────────────────────────┘
```

**⚠️ NEVER skip confirmation steps. Information insufficiency = ASK, never guess.**

---

#### STEP 1 — GATHER (信息收集)

Ask the user these questions. Use `AskUserQuestion` when choices are involved:

1. **Content/Topic**: What is this presentation about?
2. **Audience**: Who will see it? (executives, investors, students, general public)
3. **Page Count**: How many slides approximately?
4. **Style Preference**: Any visual preference? Tech-dark / business-clean / academic / creative / hand-drawn?
5. **Template**: Does the user have an existing .pptx template to mimic? (optional)

**If any of items 1-4 are unclear, ASK before proceeding.**

---

#### STEP 2 — RECOMMEND (风格推荐)

Based on the topic and audience, recommend 2-3 styles:

```bash
python3 scripts/vision_cli.py ppt list-styles --format json
```

Style selection guide:
- **Tech/AI/DevTools**: `dark-aurora`, `gradient-glass`, `data-science-consulting`
- **Business/Pitch/Strategy**: `clean-tech-blue`, `editorial-mono`, `investment-company-business-plan`, `eco-green-business-plan`
- **Academic/Thesis/Report**: `swiss-grid`, `geometric-duotone-thesis`, `final-year-project-thesis-defense`
- **Creative/Brand/Culture**: `creative-agency`, `flowery`, `japanese-wabi`, `vector-illustration`
- **Workshop/Training**: `hand-sketch`, `mind-maps-workshop-professional`

---

#### STEP 3 — DRAFT (草拟大纲)

Write `slides_plan.md` following this format:

```markdown
---
title: <Presentation Title>
---

## 1. [cover] Title Line
Subtitle or tagline

## 2. [content] Section Title
- Key point 1
- Key point 2

## 3. [data] Key Metrics
- Metric A: 85%
- Metric B: 3.2x
```

Rules:
- Each `## N.` heading = one slide
- `[page_type]`: `cover` / `content` / `data` (default: `content`)
- Heading line text becomes the slide title; body becomes content
- **Present the md to user for review. Do NOT proceed until confirmed.**

---

#### STEP 4 — CONFIRM PLAN (确认大纲)

Show the user the `slides_plan.md` content and ask:
- "Content looks correct? Any changes to titles, body, or slide order?"
- Make edits as requested until user says OK.

Then convert to JSON:

```bash
python3 scripts/vision_cli.py ppt plan slides_plan.md -o slides_plan.json
```

---

#### STEP 5 — SMOKE TEST (冒烟测试)

Generate ONLY the first slide (cover) to verify style before full generation:

```bash
python3 scripts/vision_cli.py ppt generate \
  --plan slides_plan.json \
  --style dark-aurora \
  --slides 1
```

Review the output with the user:
- "Does this visual style work? Adjust style or proceed with all slides?"

---

#### STEP 6 — CONFIRM STYLE & GENERATE (确认风格→全量生成)

Once user approves, generate all remaining slides:

```bash
python3 scripts/vision_cli.py ppt generate \
  --plan slides_plan.json \
  --style dark-aurora
```

---

#### STEP 7 — DELIVER (交付)

Tell the user:
```
✅ PPT 已生成!
- 输出目录: outputs/<timestamp>/
- PPTX 文件: outputs/<timestamp>/<title>.pptx
- 每页图片: outputs/<timestamp>/images/
```

---

### PPT Commands Summary

| Command | Description |
|---------|-------------|
| `vision_cli.py ppt list-styles` | List all available styles |
| `vision_cli.py ppt plan <md>` | Convert slides_plan.md → slides_plan.json |
| `vision_cli.py ppt generate --plan <json> --style <id>` | Generate slides |
| `vision_cli.py ppt generate ... --slides 1` | Smoke test (first slide only) |
| `vision_cli.py ppt generate ... --slides 1,3,5` | Generate specific slides only |
| `vision_cli.py ppt sessions` | List generation history |

### Style Preview

To see visual previews of all styles, read `docs/distilled-styles.md`. Each style's full prompt template is in `styles/<id>.md`.

## Task Management
All tasks are executed asynchronously by default.
- Use `--wait` flag to block until completion (useful for Agent workflow).
- Use `--output` flag to automatically save text or download images.
- Task data is stored in `.tasks/` directory.

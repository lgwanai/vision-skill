---
name: vision-skill
description: Use this skill for computer vision tasks including image recognition (OCR, object detection) and image generation (text-to-image, image-to-image). Supports asynchronous task execution with flexible image upload modes (COS or BASE64) and configurable vision models (OpenAI-compatible APIs). IMPORTANT: For image generation, NEVER generate immediately. Follow the mandatory confirmation workflow: understand requirements → search cases → draft prompt → confirm → iterate → generate.
---

# Vision Skill

## Overview

This skill provides capabilities for visual recognition and image generation. It supports configurable vision models (OpenAI-compatible APIs), flexible image upload modes (COS or BASE64), and executes tasks asynchronously. **Includes a unified GPT Image 2 case library (1322 cases)** for prompt engineering reference.

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
│  STEP 2: SEARCH — Find relevant cases from 1322-case library │
│  STEP 3: DRAFT — Compose prompt with case references         │
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

**STEP 2 — SEARCH (案例检索):**
Once requirements are confirmed, search the unified case library:
```bash
python3 scripts/search_cases.py "<keywords>" --category "<category>" --style "<style>" --limit 5
```
Present 2-3 most relevant cases to the user as context/reference.

**STEP 3 — DRAFT (智能提示词生成):**
Use the intelligent prompt builder engine that integrates three-project methodology:
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
  --lang "<zh/en/ja>" \
  --json-output
```

The engine automatically:
- Selects the optimal approach (JSON-structured / natural language / photography spec / platform-specific)
- Injects category-specific best practices from 1322 cases (e.g., 46.7% use photography params, 41.8% structured layouts)
- Applies style-matched quality injections (camera/lens/lighting/composition terms from professional photography)
- Integrates negative constraints from the constraint library
- References top-matched cases for pattern extraction

**Prompt Quality Principles (from 3-project analysis):**
1. **Photography params** for realistic styles — lighting, lens, camera, composition, film stock
2. **Structured sections** for complex layouts — panels, grids, rows, columns with explicit numbering
3. **Negative constraints** — always include 3-5 "Avoid:" items from the constraint library
4. **Aspect ratio** — always specify, as 21.8% of quality cases do
5. **Text specs** — for UI/posters, explicitly list every text string that must appear
6. **Color system** — 4-6 color palette for posters/brand; dominant + accent for photos
7. **Raycast** — use `{argument}` for flexible parameters when user needs variants

**STEP 4 — CONFIRM (用户确认):**
Present the draft prompt to the user with:
- The full prompt text
- Reference to the cases that inspired it
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

### 4. Unified Case Library (1322 cases)
Searchable library of GPT Image 2 prompts from 3 community projects, organized in 10 unified categories:
- Portrait & People (452 cases)
- Poster & Typography (335 cases)
- Social Media & UI (277 cases)
- Product & E-commerce (90 cases)
- Infographic & Charts (70 cases)
- Illustration & Storytelling (55 cases)
- Photography & Realism (68 cases)
- Brand & Identity (24 cases)
- Architecture & Scenes (12 cases)
- Other (89 cases)

Search cases: `python3 scripts/search_cases.py "<query>" --limit 5`
Browse by category: `cases/<category>/README.md`
Master index: `cases/INDEX.md`

## Usage

The skill is exposed via a CLI script `scripts/vision_cli.py`.

### Prerequisites
Environment variables must be set in `.env` or the system environment:
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

## Task Management
All tasks are executed asynchronously by default.
- Use `--wait` flag to block until completion (useful for Agent workflow).
- Use `--output` flag to automatically save text or download images.
- Task data is stored in `.tasks/` directory.

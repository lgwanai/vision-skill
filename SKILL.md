---
name: vision-skill
description: Use this skill for computer vision tasks including image recognition (OCR, object detection) and image generation (text-to-image, image-to-image). Supports asynchronous task execution with flexible image upload modes (COS or BASE64) and configurable vision models (OpenAI-compatible APIs).
---

# Vision Skill

## Overview

This skill provides capabilities for visual recognition and image generation. It supports configurable vision models (OpenAI-compatible APIs), flexible image upload modes (COS or BASE64), and executes tasks asynchronously.

## Capabilities

### 1. Vision Recognition
Analyze images to describe content, extract text (OCR), or answer questions about the image.
- **Input**: Local image path or URL, optional prompt.
- **Process**: Based on `IMAGE_UPLOAD_MODE`, uploads to COS (URL mode) or converts to base64.
- **Output**: Text description or answer.

### 2. Image Generation
Generate images from text prompts, optionally using reference images.
- **Text-to-Image**: Generate images from a text description.
- **Image-to-Image**: Generate images based on a reference image and text prompt.
- **Sequential Generation**: Generate a series of consistent images (e.g., storyboards).

### 3. WeChat Chat Screenshot Recognition
Specialized recognition for WeChat chat screenshots:
- **Platform Detection**: Distinguish between PC and mobile WeChat
- **Sender Identification**: Green bubbles = self, gray/white bubbles = others
- **Structured Output**: Returns JSON with platform, chat title, and message list
- **Message Types**: Supports text, image, voice, video, link detection

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

---
name: vision-skill
description: Use this skill for computer vision tasks including image recognition (OCR, object detection) and image generation (text-to-image, image-to-image). Supports asynchronous task execution with Tencent COS storage and Doubao AI models.
---

# Vision Skill

## Overview

This skill provides capabilities for visual recognition and image generation using Doubao AI models. It handles image storage via Tencent Cloud COS and executes tasks asynchronously.

## Capabilities

### 1. Vision Recognition
Analyze images to describe content, extract text (OCR), or answer questions about the image.
- **Input**: Local image path or URL, optional prompt.
- **Process**: Uploads local images to COS, then calls Doubao Vision API.
- **Output**: Text description or answer.

### 2. Image Generation
Generate images from text prompts, optionally using reference images.
- **Text-to-Image**: Generate images from a text description.
- **Image-to-Image**: Generate images based on a reference image and text prompt.
- **Sequential Generation**: Generate a series of consistent images (e.g., storyboards).

## Usage

The skill is exposed via a CLI script `scripts/vision_cli.py`.

### Prerequisites
Environment variables must be set in `.env` or the system environment:
- `COS_SECRET_ID`, `COS_SECRET_KEY`, `COS_REGION`, `COS_BUCKET_NAME`
- `DOUBAO_API_KEY`, `DOUBAO_VISION_MODEL`, `DOUBAO_IMAGE_MODEL`

### Commands

#### Vision Recognition
```bash
python3 scripts/vision_cli.py recognize <image_path> --prompt "Describe this image"
```

#### Image Generation
```bash
# Text to Image
python3 scripts/vision_cli.py generate "A cyberpunk city"

# Image to Image
python3 scripts/vision_cli.py generate "A cyberpunk city" --ref <image_path>

# Sequential Generation
python3 scripts/vision_cli.py generate "A story about a cat" --seq 4
```

#### Check Status
```bash
python3 scripts/vision_cli.py status <task_id>
```

## Task Management
All tasks are executed asynchronously. The CLI returns a `task_id` immediately. Use the `status` command to poll for results.
Task data is stored in `.tasks/` directory.

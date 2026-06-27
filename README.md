# Vision Skill

Vision Skill 是专为 AI Agent（如 Trae, Claude, OpenClaw 等）设计的视觉能力扩展插件。它赋予纯文本模型强大的**视觉理解（Recognition）**和**图像生成（Generation）**能力，支持多种 OpenAI 兼容视觉模型，提供灵活的图片上传模式（COS 或 BASE64），实现高效、异步、高质量的视觉任务处理。

**🆕 v2.0**：集成 **832 个 GPT Image 2 精选案例库**（质量过滤自 3 个社区项目 1322 raw cases，去除 490 低质） + **智能提示词引擎**，自动生成高质量生图 prompt。

**🆕 v2.1**：集成 **PPT 生成引擎** — 30+ 内置风格、Markdown 转 PPTX、slide_spec 精确编辑、模板克隆、外部图片贴入、版本回滚。

**🆕 v2.2**：**参考图角色优化** — 支持多参考图各自指定角色（背景/产品/风格等），Prompt 中自然融合，不再笼统 "参考图是 xxx"。

## 🌟 项目亮点

*   **灵活模型配置**：支持自定义 BaseURL、API Key 和模型名称，兼容 OpenAI 格式 API，可对接豆包、通义千问、DeepSeek 等多种视觉模型。
*   **双模式图片处理**：支持 COS 云存储和 BASE64 直接传输两种模式，适应不同场景需求。
*   **全能视觉识别**：支持 OCR 文字提取、场景描述、细节问答，准确率极高。
*   **微信截图识别**：专门优化的 `wechat_chat` 预设，自动区分 PC/手机端，识别发送者身份。
*   **全场景图像生成**：
    *   **文生图（Text-to-Image）**：精准理解 Prompt 生成高质量图像。
    *   **图生图（Image-to-Image）**：基于参考图进行风格迁移或细节修改。
    *   **文生图组（Sequential Generation）**：支持生成连贯的故事插画或分镜。
*   **🧠 智能提示词引擎 (`prompt_builder.py`)**：自动匹配案例并提炼灵感信号，默认生成简洁 creative brief，避免案例/摄影术语过度堆砌。
*   **📚 GPT Image 2 案例库 (832 cases)**：来自 3 个社区项目的精选 prompt（质量过滤自 1322 raw，去除 490 低质），10 大统一分类，单文件存储（`cases/index.json`），支持关键词检索。
*   **📊 PPT 生成引擎 (`ppt_generator.py`)**：30+ 内置风格，Markdown→PPTX 全流程，slide_spec 精确编辑，模板克隆，外部图片贴入，版本回滚。
*   **🚨 强制确认工作流**：生图/生成PPT前必须经过需求确认→用户确认→冒烟测试，杜绝低质量输出。
*   **🚫 参考图必要性检测**：自动识别需要参考图的场景（照片优化/风格迁移/图生图等），无参考图则阻断。
*   **🖼️ 多参考图角色融合**：每张参考图可指定独立角色（背景场景/产品元素/风格参考等 7 类），Prompt 自然融合，不再笼统 "参考图是 xxx"。
*   **场景化预置 (Presets)**：内置 `ppt`, `business_flat`, `tech_isometric`, `hand_drawn` 等生成风格，以及 `invoice`, `contract`, `form`, `slide`, `whiteboard`, `table`, `json`, `wechat_chat` 等识别输出格式。
*   **高可用性设计**：支持备用模型配置（FALLBACK_MODEL），主模型失败时自动切换。
*   **批处理与稳定性增强**：支持一次识别多张图片，内置失败重试、可选降级模型。
*   **可观测任务元数据**：任务状态中包含 `started_at / ended_at / duration_ms / api_attempts / upload_mode` 等字段。
*   **灵活的任务架构**：既支持**异步轮询**（适合批量大任务），也支持**同步等待**（适合即时反馈）。

## 📚 GPT Image 2 案例库

从 3 个社区项目精选 **832 个高质量生图案例**（质量过滤自 1322 raw，去除 490 低质），统一为 10 大分类：

| 分类 | 数量 | 典型场景 |
|------|:---:|------|
| Portrait & People | 193 | 人像、写真、角色设计 |
| Poster & Typography | 180 | 海报、排版、封面设计 |
| Social Media & UI | 107 | 社媒截图、APP 界面 |
| Photography & Realism | 102 | 写实摄影、电影级画面 |
| Illustration & Storytelling | 87 | 插画、漫画、故事板 |
| Product & E-commerce | 54 | 电商主图、产品摄影 |
| Infographic & Charts | 42 | 信息图、图表、菜谱卡 |
| Other | 32 | 对比案例、特殊场景 |
| Brand & Identity | 20 | Logo、品牌设计 |
| Architecture & Scenes | 15 | 建筑、室内、空间 |

**案例检索**：
```bash
# 按关键词+分类搜索
python3 scripts/search_cases.py "product photography watch" --category "Product & E-commerce" --limit 5

# 只搜精选案例
python3 scripts/search_cases.py "portrait" --featured --limit 5

# JSON 输出供程序调用
python3 scripts/search_cases.py "anime character" --json
```

**完整索引**：[cases/INDEX.md](cases/INDEX.md)

## 🧠 智能提示词引擎

`scripts/prompt_builder.py` 融合三项目方法论，将用户需求自动转化为高质量生图 prompt：

```bash
# 产品摄影
python3 scripts/prompt_builder.py \
  --subject "luxury mechanical watch" \
  --style "commercial product photography" \
  --category "Product & E-commerce" \
  --ratio "1:1" --mood "premium sophisticated" \
  --json-output

# 人像写真（中文）
python3 scripts/prompt_builder.py \
  --subject "年轻女性东京街头" \
  --style "cinematic portrait" \
  --category "Portrait & People" \
  --ratio "3:4" --lang zh --json-output

# 图生图（单参考图变换）
python3 scripts/prompt_builder.py \
  --subject "我的产品照片" \
  --style "minimalist editorial" \
  --ref ./product.jpg \
  --ref-keep "产品主体和结构" \
  --ref-change "背景和色调" --json-output

# 多参考图角色融合（背景 + 产品）
python3 scripts/prompt_builder.py \
  --subject "产品展示" \
  --style "commercial photography" \
  --ref ./background.jpg --ref ./product.jpg \
  --ref-role "背景场景" --ref-role "产品元素" \
  --ref-keep "构图和光影" --ref-keep "产品造型和颜色" \
  --ref-change "主体内容" --ref-change "环境光" --json-output
```

**引擎能力**：
- 4 种生成策略：自然语言 / JSON 结构化 / 摄影参数 / 平台专用
- **多参考图角色融合**：每张参考图指定独立角色（7 类），Prompt 自然融合
- **不自行脑补**：用户没说的不猜，keep/change/role 按用户原话表达
- 案例只作为灵感参考，不把长案例 prompt 复制进最终提示词
- 精简负向约束：优先使用用户约束，只保留少量必要默认项
- Raycast `{argument}` 参数化 - 27.1% 案例使用
- 风格特化质量注入（摄影/电影/动漫/插画/3D/海报/UI）

## 💡 核心价值

AI Agent 通常受限于纯文本交互或有限的多模态窗口。Vision Skill 解决了以下核心痛点：

1.  **打破模态壁垒**：让 Agent 能"看"懂本地文件，能"画"出创意想法。
2.  **专业能力外挂**：相比通用模型，Skill 封装了特定的 Prompt 优化和参数调优（如连贯性生成配置）。
3.  **流程自动化**：从本地图片 -> 上传云端/转BASE64 -> 识别/生成 -> 结果回传/保存，全流程自动化，Agent 只需调用一条指令。

## ⚡ 快速开始

**最快上手方式（无需 COS）：**

```bash
# 1. 克隆项目
git clone https://github.com/lgwanai/vision-skill.git
cd vision-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置（使用 BASE64 模式，无需 COS）
cp config.example.txt config.txt
# 编辑 config.txt，设置：
# IMAGE_UPLOAD_MODE=base64
# VISION_API_KEY=your_api_key
# VISION_MODEL=your_model

# 4. 运行识别
python3 scripts/vision_cli.py recognize ./photo.jpg --format ocr --wait
```

## 🚀 使用场景

*   **UI/UX 设计辅助**：上传草图，生成高保真渲染图；或者根据现有 UI 生成变体。
*   **文档数字化**：批量识别发票、海报、文档中的文字并结构化输出为 JSON 或 Markdown 表格。
*   **微信聊天分析**：识别微信聊天截图，区分 PC/手机端，自动识别发送者（绿色气泡=自己，灰色=对方）。
*   **内容创作**：为文章自动配图，或制作连贯的故事绘本（使用 `cartoon` 风格预置）。
*   **数据分析**：识别图表内容，转换为 Excel 或 Markdown 表格数据。
*   **无障碍辅助**：为视障用户生成图片的详细描述。

## 🔄 工作流 (Workflow)

Vision Skill 采用**异步任务**模式，确保 Agent 在处理耗时生成任务时不会超时。

1.  **提交任务 (Submit)**：Agent 调用 CLI（如 `vision_cli.py recognize` 或 `generate`）。
2.  **预处理 (Pre-process)**：
    *   根据 `IMAGE_UPLOAD_MODE` 配置处理本地图片：
        *   `cos` 模式：上传至腾讯云 COS 获取 URL
        *   `base64` 模式：转换为 base64 字符串
    *   构建符合 OpenAI 格式的请求体。
3.  **异步执行 (Async Execution)**：
    *   Worker 进程后台启动，调用配置的视觉模型 API。
    *   CLI 立即返回 `task_id` 和 `status: pending`。
4.  **状态轮询 (Polling)**：
    *   Agent 使用 `vision_cli.py status <task_id>` 查询进度。
5.  **结果处理 (Result)**：
    *   任务完成后，返回 JSON 格式的识别文本或生成图片的 URL。

## 🛠️ 安装与使用

### 1. 极速安装

```bash
# 克隆仓库
git clone https://github.com/lgwanai/vision-skill.git
cd vision-skill

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制配置文件并填入密钥：

```bash
cp config.example.txt config.txt
```

在 `config.txt` 中填入配置：

#### 视觉识别模型配置
```ini
VISION_API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VISION_API_KEY=your_api_key_here
VISION_MODEL=doubao-seed-2-0-pro-260215
VISION_FALLBACK_MODEL=  # 可选备用模型
```

#### 图像生成模型配置
```ini
IMAGE_API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
IMAGE_API_KEY=your_api_key_here  # 若不填则使用 VISION_API_KEY
IMAGE_MODEL=doubao-seedream-5-0-260128
IMAGE_FALLBACK_MODEL=  # 可选备用模型
```

#### 图片上传模式
```ini
# 可选值: cos, base64
# - cos: 上传图片到腾讯云 COS，使用 URL 传输（适合大图片）
# - base64: 直接转换为 base64 传输（适合小图片或无 COS 场景）
IMAGE_UPLOAD_MODE=cos
```

#### 腾讯云 COS 配置（仅当 IMAGE_UPLOAD_MODE=cos 时需要）
```ini
COS_SECRET_ID=your_cos_secret_id
COS_SECRET_KEY=your_cos_secret_key
COS_REGION=ap-beijing
COS_BUCKET_NAME=your_bucket_name
```

### 3. IDE 集成 (Trae / Cursor / Claude)

将 `dist/vision-skill.skill` (或者整个项目目录) 作为 MCP 工具或自定义 Skill 导入到你的 Agent 配置中。
*   **Trae/Claude Desktop**: 在设置中添加本地 Skill 路径。
*   **OpenClaw**: 将 `scripts/vision_cli.py` 注册为 Tool。

### 4. 命令行使用指南

#### 👁️ 视觉识别
```bash
# 基础用法：识别本地图片
python3 scripts/vision_cli.py recognize ./photo.jpg --prompt "提取图中的文字"

# 进阶用法：使用预置格式 (--format)
# 可选格式：invoice, contract, form, slide, whiteboard, table, json, key_value, markdown_note, qa_pairs, code, ocr, analysis, wechat_chat
python3 scripts/vision_cli.py recognize ./invoice.jpg --format json

# 批量识别（多图输入）
python3 scripts/vision_cli.py recognize ./a.jpg ./b.jpg ./c.jpg --format table --wait --output ./batch_result.json

# 质量模式与重试
python3 scripts/vision_cli.py recognize ./doc.jpg --format contract --quality high --retry 3 --wait

# 同步等待并保存结果 (--wait --output)
python3 scripts/vision_cli.py recognize ./doc.jpg --format ocr --wait --output ./result.txt

# 微信聊天截图识别（区分PC/手机端，识别发送者）
python3 scripts/vision_cli.py recognize ./wechat_screenshot.png --format wechat_chat --wait

# 微信截图识别输出示例
# {
#   "platform": "pc",
#   "chat_title": "张三",
#   "messages": [
#     {"sender": "other", "content": "你好", "type": "text"},
#     {"sender": "self", "content": "你好！", "type": "text"}
#   ],
#   "message_count": 2,
#   "self_message_count": 1,
#   "other_message_count": 1
# }
```

#### 🎨 图像生成
```bash
# 基础用法：文生图
python3 scripts/vision_cli.py generate "一只赛博朋克风格的猫"

# 进阶用法：使用预置风格 (--style)
# 可选风格：ppt, business_flat, cartoon, tech_isometric, hand_drawn, icon, photo, anime, sketch
python3 scripts/vision_cli.py generate "团队协作开会" --style ppt

# 图生图 (指定参考图)
python3 scripts/vision_cli.py generate "变成素描风格" --ref ./cat.jpg

# 先构建带参考图元数据的精简提示词
# 单参考图
python3 scripts/prompt_builder.py \
  --subject "这张猫照片" \
  --style "loose pencil sketch" \
  --ref ./cat.jpg \
  --ref-keep "猫的姿态和表情" \
  --ref-change "转为松弛的铅笔速写" \
  --json-output

# 多参考图角色融合
python3 scripts/prompt_builder.py \
  --subject "产品场景展示" \
  --style "cinematic product shot" \
  --ref ./street.jpg --ref ./watch.jpg \
  --ref-role "背景场景" --ref-role "产品元素" \
  --ref-keep "光影氛围" --ref-keep "手表造型和材质" \
  --ref-change "内容" --ref-change "环境" --json-output

# 连续生成 (生成4张连贯图)
python3 scripts/vision_cli.py generate "四季变化的树" --seq 4 --style cartoon

# 同步等待并保存图片
python3 scripts/vision_cli.py generate "相机App图标" --style icon --wait --output ./icon.png

# 质量模式与重试
python3 scripts/vision_cli.py generate "企业级数据平台架构插图" --style tech_isometric --quality high --retry 3 --wait
```

#### 📊 PPT 生成

```bash
# 查看可用风格（30+ 种）
python3 scripts/vision_cli.py ppt list-styles

# Markdown 大纲 → JSON plan
python3 scripts/vision_cli.py ppt plan slides_plan.md -o slides_plan.json

# 冒烟测试（只生成封面确认风格）
python3 scripts/vision_cli.py ppt generate --plan slides_plan.json --style dark-aurora --slides 1

# 全量生成
python3 scripts/vision_cli.py ppt generate --plan slides_plan.json --style dark-aurora

# 模板克隆（用 PPTX 模板的配色/版式生成新内容）
python3 scripts/vision_cli.py ppt generate --plan slides_plan.json --style dark-aurora \
  --template-pptx template.pptx --template-strict

# 编辑指定页
python3 scripts/vision_cli.py ppt edit --edit 3 --session 20260605_120000 \
  --element-updates '{"title": {"content": "新标题"}}'

# 回滚到历史版本
python3 scripts/vision_cli.py ppt rollback --rollback 3 --to-version 1 --session 20260605_120000

# 查看生成历史
python3 scripts/vision_cli.py ppt sessions
```

**内置风格速览**：

| 场景 | 推荐风格 |
|------|---------|
| 科技/AI/DevTools | `dark-aurora`, `gradient-glass`, `data-science-consulting` |
| 商业/投资/路演 | `clean-tech-blue`, `editorial-mono`, `investment-company-business-plan` |
| 学术/论文/答辩 | `swiss-grid`, `geometric-duotone-thesis`, `final-year-project-thesis-defense` |
| 创意/品牌/文化 | `creative-agency`, `flowery`, `japanese-wabi`, `vector-illustration` |
| 培训/工作坊 | `hand-sketch`, `mind-maps-workshop-professional` |

**PPT 工作流**（7步强制确认）：
1. **收集信息** — 主题/受众/页数/风格偏好
2. **风格推荐** — 根据场景推荐 1-2 个风格
3. **草拟大纲** — 写 slides_plan.md 给用户审核
4. **确认大纲** — 用户确认内容
5. **冒烟测试** — 只生成封面，确认风格
6. **全量生成** — 风格确认后生成所有页
7. **交付** — 打包 PPTX，告知路径

#### 🔍 查询结果
```bash
python3 scripts/vision_cli.py status <task_id>

# 如果任务已完成，直接保存结果
python3 scripts/vision_cli.py status <task_id> --output ./final_result.png
```

## ❓ 常见问题 (FAQ)

**Q: 需要 GPU 吗？**
A: 不需要。所有计算都在云端大模型上完成，本地只需能运行 Python 即可。

**Q: 图片上传到哪里了？安全吗？**
A: 取决于 `IMAGE_UPLOAD_MODE` 配置：
- `cos` 模式：上传到腾讯云 COS，请确保 Bucket 权限配置正确
- `base64` 模式：不存储图片，直接转为 base64 字符串传输

**Q: 为什么识别结果有延迟？**
A: 视觉大模型处理需要时间，尤其是高清图片分析或批量生成任务。通常识别在 3-5秒，生成在 10-30秒左右。建议使用 `--wait` 参数让脚本自动等待。

**Q: 支持哪些图片格式？**
A: 支持 JPG, PNG, WEBP 等常见格式。文件大小建议不超过 10MB。

**Q: 如何获取 API Key？**
A: 请访问相应的模型服务商控制台获取 API Key，例如：
- 豆包大模型：[火山引擎控制台](https://console.volcengine.com/)
- 其他 OpenAI 兼容服务：访问对应平台获取

**Q: COS 模式和 BASE64 模式如何选择？**
A: 
- **COS 模式**（推荐）：适合生产环境，支持大文件，可复用图片 URL，减少重复传输
- **BASE64 模式**：适合快速测试或无云存储场景，但会增加约 33% 的传输大小

**Q: 什么是备用模型（FALLBACK_MODEL）？**
A: 备用模型是在主模型调用失败时自动切换的备用选项。当主模型不可用或超时时，系统会自动尝试备用模型，提高任务成功率。适用场景：
- 模型故障时自动降级
- 使用更稳定的模型兜底
- 模型迁移过渡期

## 📋 功能清单

### 视觉识别预设格式
| 预设名称 | 用途 | 输出格式 |
|---------|------|---------|
| `ocr` | 通用文字提取 | 原格式文本 |
| `json` | 结构化数据提取 | JSON |
| `table` | 表格识别 | Markdown 表格 |
| `invoice` | 发票识别 | JSON |
| `contract` | 合同识别 | JSON |
| `wechat_chat` | 微信聊天截图 | JSON |
| `code` | 代码截图识别 | 代码块 |
| `slide` | 幻灯片识别 | Markdown |
| `whiteboard` | 白板识别 | 会议纪要 |
| `business_card` | 名片识别 | JSON |

### 图像生成预设风格
| 预设名称 | 风格描述 | 适用场景 |
|---------|---------|---------|
| `photo` | 真实照片 | 产品展示、场景图 |
| `cartoon` | 卡通风格 | 插画、故事 |
| `anime` | 日系动漫 | 动漫风格创作 |
| `tech_isometric` | 等距科技风 | 架构图、示意图 |
| `ppt` | 商务扁平风 | PPT 插图 |
| `icon` | 3D 图标 | App 图标 |
| `hand_drawn` | 手绘风格 | 概念图、草图 |
| `sketch` | 素描风格 | 艺术创作 |

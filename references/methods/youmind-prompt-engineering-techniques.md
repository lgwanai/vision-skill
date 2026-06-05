# GPT Image 2 - Prompt Engineering Techniques

> 从 126 个案例中提炼的 prompt 工程方法论和最佳实践

---

## 📊 Prompt 风格分布

| 风格 | 数量 | 占比 |
|------|------|------|
| JSON 结构化 Prompt | 12 | 9.5% |
| 自然语言 Prompt | 114 | 90.5% |
| 支持动态参数 (Raycast) | 120 | 95.2% |
| 多图案例 | 39 | 31.0% |
| 含摄影/技术参数 | 95 | 75.4% |

---

## 🏗️ 方法 1: JSON 结构化 Prompt

**使用占比: 9.5%**

### 核心思路

将图像需求拆解为结构化 JSON，明确每个组件的属性（位置、样式、内容），让模型逐层渲染。

### 典型结构

```json
{
  "type": "image type (poster/infographic/mockup/...) ",
  "subject": "main subject description",
  "style": "visual style specification",
  "background": "background description",
  "layout": {
    "header/title_section": { ... },
    "centerpiece": "main visual element",
    "sections/callouts": [ ... ],
    "footer": { ... }
  }
}
```

### 优势

- 🎯 **精确定位**: 每个元素的位置、内容都可精确控制
- 🔄 **可复用**: JSON 结构易于参数化和模板化
- 🧩 **模块化**: 可以独立调整每个组件而不影响其他部分
- 📐 **适合复杂布局**: 海报、信息图、UI 设计等需要精确排版的场景

### 代表性案例

- [VR Headset Exploded View Poster](../cases/Product-Marketing/001-VR-Headset-Exploded-View-Poster.md)
- [Illustrated City Food Map](../cases/Infographic-Edu-Visual/002-Illustrated-City-Food-Map.md)
- [E-commerce Live Stream UI Mockup](../cases/App-Web-Design/004-E-commerce-Live-Stream-UI-Mockup.md)
- [Anime Martial Arts Battle Illustration](../cases/Comic-Storyboard/005-Anime-Martial-Arts-Battle-Illustration.md)
- [3D Stone Staircase Evolution Infographic](../cases/Infographic-Edu-Visual/006-3D-Stone-Staircase-Evolution-Infographic.md)

---

## ✍️ 方法 2: 自然语言描述式 Prompt

**使用占比: 90.5%**

### 核心思路

用自然语言详细描述期望的画面，像给摄影师或画家下 brief 一样。

### 典型写法

```
Create a [style] [type] of [subject], featuring [details], 
with [lighting/atmosphere], [composition], [color palette], 
[specific requirements]. Avoid [negative prompts].
```

### 优势

- 🎨 **更自然的创意表达**: 适合描述氛围、情绪等抽象概念
- ⚡ **快速迭代**: 不需要构造 JSON 结构，适合快速尝试
- 🖼️ **适合艺术风格**: 摄影、插画、概念艺术等强调视觉感受的场景

---

## 🚀 方法 3: 动态参数化 Prompt (Raycast)

**使用占比: 95.2%**

### 核心思路

使用 `{argument name="参数名" default="默认值"}` 语法，让 prompt 支持动态参数替换。

### 语法

```
{argument name="parameter name" default="default value"}
```

### 优势

- 🔧 **一键变体**: 修改参数即可快速生成变体
- 📦 **模板化**: 将优秀 prompt 做成模板，适配不同需求
- 🤖 **可集成**: 配合 Raycast Snippets 等工具实现快捷生图

---

## 📷 方法 4: 摄影参数控制

### 常用摄影术语

从案例中提取的高频摄影参数：

| 参数类型 | 常用术语 |
|----------|----------|
| 布光 | studio lighting, natural light, golden hour, dramatic lighting, rim lighting, soft diffused light |
| 景深 | shallow depth of field, deep focus, bokeh, f/1.4, f/2.8 |
| 构图 | close-up, wide shot, portrait, full body, overhead shot, Dutch angle |
| 相机 | DSLR, medium format, 35mm, cinematic, Hasselblad, Leica |
| 风格 | editorial, commercial, fine art, street photography, snapshot aesthetic |
| 后期 | film grain, color grading, high contrast, desaturated, vintage tone |

---

## 🚫 方法 5: 负向提示 (Negative Prompts)

### 核心思路

在 prompt 末尾添加 "Avoid..." 或负面约束来排除不需要的元素。

### 常见负向提示

从 50 个案例中提取的常见负向约束：

- `avoid watermarks` - 避免水印
- `no extra text` - 不生成额外文字
- `no cartoon rendering` - 避免卡通化渲染
- `avoid distorted/unreadable typography` - 避免文字变形
- `no extra [objects]` - 控制元素数量

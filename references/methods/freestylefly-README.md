# GPT Image 2 - Prompt Engineering Methods & Analysis

> 基于 490 个工业级案例和 21 套模板的深度分析方法论

---

## 📊 Prompt 特征分析

| 指标 | 数值 |
|------|------|
| 总案例数 | **490** |
| 平均 Prompt 长度 | **1205 字符** |
| 最长 Prompt | **8051 字符** |
| 最短 Prompt | **10 字符** |
| 超长 Prompt (>2000字) | **93** |
| 短 Prompt (<200字) | **92** |

---

## 🏗️ 核心方法论: Prompt as Code

### 理念

将散文式 prompt 压缩为结构化协议，使 prompt 可被 Agent、脚本和自动化工作流直接调用。

### 三大支柱

1. **🧱 原子化 Schema** — 将主体、光照、材质、布局、视觉细节拆分为可组合的零件
2. **⚙️ 工作流友好** — 为 Agent、脚本和自动化系统设计
3. **🧬 结构化控制** — 提升对布局、文案和信息层级的可控性

---

## 📐 Prompt 构建框架 (6 步法)

从 490 个案例和 21 套模板中提炼的标准 prompt 构建流程：

```
1. Subject & Task    → 明确主体和任务（产品/海报/UI/信息图/...）
2. Composition       → 构图和布局（居中/对角/网格/...）
3. Visual Style      → 视觉风格和材质（3D/摄影/插画/...）
4. Text & Labels     → 文字和标注要求（精确文案、可读性）
5. Aspect Ratio      → 输出比例（9:16/16:9/1:1/4:5）
6. Constraints       → 约束条件（避坑：无乱码/无变形/无色偏）
```

---

## 🎨 风格标签分布 (Top 15)

| Style | Count |
|-------|-------|
| UI | 225 |
| Realistic | 183 |
| Poster | 175 |
| Character | 103 |
| Illustration | 89 |
| Brand | 75 |
| Infographic | 73 |
| Product | 54 |
| 3D | 36 |
| Classical | 12 |
| Other Use Cases | 9 |
| History | 7 |
| Products | 5 |
| Architecture | 4 |
| Documents | 4 |

---

## 🎬 场景标签分布

| Scene | Count |
|-------|-------|
| Tech | 362 |
| Commerce | 336 |
| Fashion | 102 |
| Social | 78 |
| Story | 63 |
| Creative | 50 |
| Travel | 42 |
| Food | 41 |
| Education | 38 |
| History | 12 |

---

## 🧩 两大 Prompt 范式

### 1. JSON 结构化 Prompt（Agent 优先）

适合：Agent 调用、批量生成、需要精确控制布局的场景。

```json
{
  "type": "UI Screenshot / Infographic / Poster / ...",
  "platform": "iOS / Android / Web / Print",
  "layout": "Card-based / Grid / Single Hero",
  "style": { "theme": "...", "primary_color": "...", "typography": "..." },
  "content": { ... },
  "constraints": "High fidelity, readable text, X:Y aspect ratio"
}
```

### 2. 工业级自然语言 Prompt（人类优先）

适合：快速原型、创意探索、单次生成。

```text
生成一张[类型]，主体为[描述]，采用[构图]，
风格为[视觉风格]，文字要求[精确文案]，
输出比例[X:Y]，约束条件[避坑项]。
```

---

## 🚫 通用防坑指南 (Top 10)

1. **锁定平台特征**: 生成截图时指定平台(iOS/Android/X/抖音), 否则模型会混搭 UI 元素
2. **强制文字可读**: 要求 '文字绝对可读，必须显示指定的中文', 避免乱码和火星文
3. **控制模块数量**: 信息图限制 3-5 个模块, 超过则画面混乱、信息溢出
4. **文案克制**: 图表/信息图场景用短句, 避免大段正文塞进画面
5. **比例前置**: 特殊比例(21:9 车机/4:5 社媒)必须写在 prompt 最前面
6. **先定场景再填细节**: 直播界面先确定带货/才艺类型, UI 差异很大
7. **明确负向约束**: Avoid watermarks, no gibberish text, no distorted typography
8. **色彩限制**: 使用 4-6 色系统, 避免颜色爆炸导致画面混乱
9. **避免通用图标**: 不用通用放大镜/齿轮图标, 要求具体、定制的视觉元素
10. **Agent 调用用 JSON 模板**: 自然语言给人类看, JSON 结构给 Agent 调用

---

*Generated from analysis of 490 cases and 21 templates*
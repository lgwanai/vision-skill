# GPT Image 2 - Tools & Integration Guide

> 与 GPT Image 2 配合使用的工具和集成方案

---

## 🔧 Raycast 集成

Raycast 是一个 macOS 效率工具，通过 Snippets 功能支持动态参数 prompt。

### 使用方式

1. 安装 [Raycast](https://raycast.com/)
2. 创建 Snippet，使用 `{argument name="..." default="..."}` 语法
3. 通过快捷键调用 Snippet，动态填入参数
4. 将生成的 prompt 复制到 GPT Image 2 中

本仓库有 **120** 个 prompt 支持 Raycast 动态参数。

---

## 🌐 YouMind Gallery

[YouMind GPT Image 2 Prompts Gallery](https://youmind.com/gpt-image-2-prompts) 是本项目的在线图库，提供：

- 🎨 瀑布流网格布局浏览
- 🔍 全文搜索和多维度筛选
- 🤖 AI 一键生图功能
- 📱 移动端响应式体验
- 🏷️ 按使用场景/风格/主体的三维分类

---

## 🔗 相关项目

- [awesome-seedance-2-prompts](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts) - Seedance 2 AI 视频提示词合集
- [Payload CMS](https://payloadcms.com/) - 本项目的 CMS 后端
- [OpenAI GPT Image 2](https://openai.com/) - GPT Image 2 官方

---

## 🛠️ 本项目的自动化工具链

### README 自动生成

- **脚本**: `scripts/generate-readme.ts`
- **调度**: 每 4 小时通过 GitHub Actions 自动更新
- **数据源**: Payload CMS API

### CMS 同步

- **脚本**: `scripts/sync-approved-to-cms.ts`
- **流程**: GitHub Issue 审批 → 自动同步到 CMS → 更新 README

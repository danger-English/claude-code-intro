# Claude Code 推广展示站

面向不了解 Claude Code 的用户，用真实案例和交互体验让他们理解"Claude Code 能做什么"，并引导安装和正确使用。

**在线浏览**: https://danger-English.github.io/claude-code-intro/

## 网站结构

三页导航式设计，共享样式和交互逻辑：

| 页面 | 文件 | 内容 |
|------|------|------|
| 为什么要用 | [index.html](index.html) | 作品展示（网页 / 小程序 / 游戏）+ 核心优势 |
| 怎么安装 | [install.html](install.html) | Mac/Windows 安装指南 × 有魔法/无魔法 |
| 怎么用好 | [usage.html](usage.html) | CLAUDE.md 四层体系 + 可复用模板 |

## 技术栈

- 纯 HTML + CSS + 原生 JS，无框架依赖
- Google Fonts（Outfit + JetBrains Mono + Noto Serif SC）
- 深色终端美学设计（#090909 暗底 + #F5A623 琥珀 + #2DD4A8 终端绿）

## 本地预览

直接用浏览器打开 `index.html` 即可，无需构建步骤。

## 目录结构

```
claude-code-intro/
├── index.html
├── install.html
├── usage.html
├── style.css
├── shared.js
└── images/
    ├── showcase/       # 作品展示截图
    └── install/        # 安装步骤截图
```

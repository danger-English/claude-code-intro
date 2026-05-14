# Claude Code Intro

Claude Code 推广展示站。面向不了解 Claude Code 的用户，用真实案例和交互体验让他们理解"Claude Code 能做什么"，并引导他们安装和正确使用。

## 目标受众

- 对 AI 编程工具好奇但没用过的开发者
- 非技术背景但想用 AI 做产品的人
- 在观望要不要用 Claude Code 的人

## 网站结构（四页）

```
claude-code-intro/
├── CLAUDE.md
├── index.html          # 第一页：为什么要用 Claude Code
├── install.html        # 第二页：怎么安装 Claude Code
├── usage.html          # 第三页：怎么用好 Claude Code
├── skills.html         # 第四页：进阶技巧 — Skill 推荐
├── style.css           # 共享样式
├── shared.js           # 共享交互逻辑
├── images/
│   ├── showcase/       # index.html 作品展示截图（webpage.png / miniprogram.png / game.png）
│   └── install/        # install.html 安装步骤截图
├── claude-code-skills.zip   # 一键下载全部推荐 Skill（231KB）
└── skills/             # 推荐 Skill 的本地副本，供无法翻墙的用户下载
    ├── web-access/
    ├── using-superpowers/   # superpowers 主 skill，含 14 个子 skill
    ├── frontend-design/
    ├── skill-creator/
    └── skill-evolution-manager/
```

### 第一页：为什么要用（index.html）

**目标**：给小白震撼，建立"Claude Code 很强"的认知

- Hero：一句话钩子
- 作品展示区：网页、小程序、游戏等真实案例，每个案例展示 prompt → 结果的对比（游戏案例附带在线试玩链接）
- 底部两个跳转按钮：「立即安装」→ install.html / 「学会用好」→ usage.html

### 第二页：怎么安装（install.html）

**目标**：手把手教小白完成安装，零门槛

内容来源：第一篇公众号文章（卡兹克保姆教程）

内容范围（止步于"能跑起来"）：
- 一. Claude Code 安装（Mac/Windows，有魔法/无魔法）
- 二. 接模型（CC Switch 配置国产模型）
- 三. 启动 Claude Code（首次设置、cd 到目标文件夹）
- **不包含** CLAUDE.md 写法（归 usage.html）

步骤设计：
- 每个步骤高亮显示，清晰标注操作位置
- 步骤间有明确的进度指示
- 按平台（Mac/Windows）× 网络（有魔法/无魔法）分流

底部跳转：返回首页 / 继续看「怎么用好」

### 第三页：怎么用好（usage.html）

**目标**：让用户理解约束先行的重要性，避免 agent 失控

内容来源：两篇公众号文章整合

内容范围（负责"跑得好"）：
- 核心论点：约束先行（比一切 Prompt 技巧都重要）
- 故事引入：工作区乱了 → 发现根源是顶层约束没做好
- CLAUDE.md 四层体系：金字塔交互组件（clip-path 梯形，hover 切换右侧描述面板）
- 全局 CLAUDE.md 模板（可直接复用，含六个部分）
- 项目 CLAUDE.md 怎么写
- 关键数字：超过 80 行开始遗漏，最多不超过 200 行
- 类比：治理公司 / 模拟经营游戏的路网规划
- Hero 解码动画：标题和副标题以字符乱码→逐个解码浮现的视觉效果呈现

底部跳转：返回首页 / 回看「安装指南」

### 第四页：进阶技巧（skills.html）

**目标**：向用户介绍 Claude Code 的 Skill 系统，推荐核心 Skill

- Hero：一句话钩子（给 Agent 装上超能力）
- 什么是 Skill：实习生类比（Prompt vs Skill vs MCP）
- 渐进式披露：Skill 的设计哲学（先目录、再章节、最后附录）
- 如何使用：三种安装方式（命令安装 / zip 下载 / 手动安装到 ~/.claude/skills/）
- 五个推荐 Skill：每个 Skill 独立 showcase 区域，大字锚点（眼/思/美/创/迭代）+ 终端安装演示 + 复制按钮 + 独立 zip 下载
- 底部跳转：返回使用指南 / 回看安装指南

**已知问题：** 推荐的 5 个 skill 中，web-access、superpowers、skill-evolution-manager 的 GitHub URL 不存在（anthropics/skills 仓库中无此目录）。已通过在项目 `skills/` 目录下放置本地副本解决，用户可直接下载 zip 文件。

## 技术栈

- 纯 HTML + CSS + 原生 JS，无框架
- Google Fonts（Outfit + JetBrains Mono + Noto Serif SC）
- 设计风格：编辑终端美学——深色主题（#090909）、琥珀强调色（#F5A623）、终端绿（#2DD4A8）、奶白文字（#F2EDE8）
- 三个页面共享 style.css + shared.js，保持视觉一致性

### shared.js 功能
- 滚动进度条（顶部 3px 渐变条）
- IntersectionObserver 滚动 reveal 动画 + showcase 交错 reveal
- Tab 切换（data-tab / data-content 模式）
- 代码块一键复制
- 锚点平滑滚动
- 导航栏滚动高亮当前页
- 全局解码动画系统（`decodeRun()`，hero 立即触发 / 滚动触发）
- 自定义发光光标球（每页不同颜色：index 红 / install 黄 / usage 绿，lerp 跟随 + hover 放大）
- 光标悬停标题时，标题颜色过渡到光标色
- Stats 滚动计数器动画
- 按钮涟漪效果

### 工具类（style.css）
- `.prose` — 正文段落样式（ink-2, 15px, line-height 2）
- `.hint-text` — 提示文字（mono, 12px, ink-2 + opacity 0.8）
- `.pull-quote` — 引用块（衬线字体, amber 左边框）
- `.play-frame` / `.play-char` — "聊/玩"排版框架（大字锚点 + 角标边框）
- `.skill-showcase` — Skill 推荐区全宽展示（大字锚点 + 交错视觉流）
- `.skill-char` — Skill 大字锚点（衬线字体, 72-110px, accent 色）
- `.skill-install-btn` — 安装命令复制按钮（amber 填充）

## 设计原则

- **一句话说服**：首屏必须让人立刻理解核心信息
- **真实案例优先**：展示的内容必须是 Claude Code 真实能做到的，不夸大
- **步骤可视化**：安装和使用步骤用编号 + 高亮，不靠纯文字堆砌
- **移动友好**：手机端体验不能打折
- **导航清晰**：三页之间跳转明显，用户不会迷路

## 验证方式

本地浏览器直接打开 HTML 文件预览，无需构建步骤。

## 部署

- GitHub Pages，从 master 分支 / (root) 部署
- 仓库：https://github.com/danger-English/claude-code-intro
- 线上：https://danger-English.github.io/claude-code-intro/

# Changelog

## 2026-05-17

### index.html — Hero 终端演示增加产品预览

终端打字动画结束后，下方滑入一个手机样式的背单词小程序（WordFlow）预览卡片，补全 prompt → 过程 → 结果 的叙事链。

- 纯 CSS 绘制手机框架 + 单词卡界面（ephemeral / 音标 / 释义）
- 艾宾浩斯复习进度条（8 个圆点，done/active 状态）+ 三档按钮（不认识/模糊/认识）
- 箭头连接线从终端指向手机，视觉上表达因果关系
- 时序精确控制：终端 "Done" 行出现后 140ms 手机卡片才淡入（8200ms）
- 手机卡片初始 `opacity: 0` + `translateY(20px)`，通过 `.show` 类触发 0.6s 过渡动画

### style.css — 新增手机预览卡片样式

- `.term-result` — 淡入容器（flex column + transition）
- `.term-result-arrow` — 箭头连接线（1px 渐变 + CSS 三角形）
- `.term-result-phone` — 手机框架（220px 宽，24px 圆角，amber 边框 + 发光阴影）
- `.phone-notch` / `.phone-screen` — 刘海 + 屏幕区域
- `.app-bar` / `.flashcard` / `.review-bar` / `.app-actions` — 单词卡界面各组件
- `.app-btn` 三色按钮（红/黄/绿）对应不认识/模糊/认识

## 2026-05-16

### 图片优化 + 加载性能修复

- `images/showcase/game.png`（5MB）替换为 `game.jpg`（391KB），加载速度大幅提升
- Three.js 从 CDN 引用改为本地 `three.min.js`（603KB），解决国内 CDN 被墙问题
- 所有四页 `<script>` 标签加 `defer`，避免 603KB 文件阻塞页面渲染
- `index.html` 图片引用同步更新为 `game.jpg`

### 全站 Three.js 粒子星场背景

- 新增 `particles.js` — 基于 Three.js 的交互式粒子系统，全站四页统一使用
- 2200 粒子漂浮 + 鼠标力场交互（推开 + 弹性回拉）+ 近距粒子自动连线
- 每页独立色调：index 琥珀+绿 / install 黄+琥珀 / usage 绿+琥珀 / skills 琥珀+蓝
- 滚动时粒子最低保持 15% 可见度，不干扰内容阅读
- 移动端 / Three.js 加载失败自动降级，不影响原有体验
- 所有卡片、终端、代码块背景改为半透明（`--bg-alt: 55%` / `--bg-card: 60%`），粒子可穿透

### 新增文件

- 新增 `particles.js` — 粒子星场核心脚本

### 改动文件

- `index.html` / `install.html` / `usage.html` / `skills.html` — 引入 Three.js（本地 three.min.js）+ particles.js
- `style.css` — 新增 `#particle-canvas` 样式；`--bg-alt` / `--bg-card` 改为 rgba 半透明；section、card、terminal、showcase 等容器统一加 backdrop-filter

### README.md / CLAUDE.md — 新增国内镜像链接

- 部署信息新增国内镜像 https://cclearning.cn/，方便不翻墙用户访问

### skills.html — 安装方式精简 + 新增 Skill 库

- 安装方式从 3 种精简为 2 种（命令安装 / 手动安装），命令安装标注翻墙前提
- 新增 Skill 库板块：3 个可下载 Skill（办公四件套 docx/xlsx/pdf/pptx、neat-freak、pua）
- 反馈方式从 GitHub Issues 改为邮箱（3602822098@qq.com），适配国内用户

### 新增文件

- 新增 `skills/docx/`、`skills/xlsx/`、`skills/pdf/`、`skills/pptx/` — 办公四件套 Skill 本地副本
- 新增 `skills/neat-freak/` — 洁癖 Skill 本地副本
- 新增 `skills/pua/` — PUA Skill 本地副本
- 新增 `office-skills.zip`、`neat-freak.zip`、`pua.zip` — 独立下载包

## 2026-05-15

### install.html — 添加模型 API 获取链接

在 Step 2「配置模型」的 API Key 说明下方，新增模型官方 API 获取地址网格，方便用户一键跳转申请。

- 新增 8 个国产模型链接：智谱 GLM、小米 MiMo、DeepSeek、Kimi、百炼、SiliconFlow、豆包、MiniMax
- 智谱 GLM、小米 MiMo、DeepSeek、Kimi 标记为「推荐」，带琥珀色标签视觉区分
- 移动端自适应两列布局

### style.css — 模型链接卡片样式

- `.model-links-grid` — auto-fill 网格布局
- `.model-link-card` — 卡片式链接，hover 上浮 + 边框高亮
- `.model-link-card.recommended` — 推荐卡片 amber 底色 + 边框
- `.model-link-badge` — 推荐标签样式
- 移动端响应式适配

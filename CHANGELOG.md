# Changelog

## 2026-05-16

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

# Changelog

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

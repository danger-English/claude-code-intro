# Skills 板块设计文档

## 概述

在 claude-code-intro 网站新增 Skills 板块，向用户介绍 Claude Code 的 Skill 系统，并推荐五个核心 Skill。

## 目标

- 让用户理解什么是 Skill、Skill 的价值
- 让用户知道如何安装和使用 Skill
- 推荐五个核心 Skill，形成完整的能力闭环

## 页面结构

### 新增文件

- `skills.html` — Skills 专题页面

### 修改文件

- `usage.html` — 结尾增加"进阶技巧"跳转按钮
- `style.css` — 新增 Skill 卡片样式
- `shared.js` — 无需修改（现有功能已覆盖）

## skills.html 内容结构

### 1. Hero 区

```
// skills
Skill，给 Agent 装上的超能力
一句话钩子 + 副标题说明 Skill 的价值
```

### 2. 什么是 Skill（Story + 定义）

**类比引入**：用"带新人"的故事讲清楚 Skill 的本质

- Agent = 刚入职的实习生，聪明但不熟规矩
- Prompt = 口头交代任务，临时、一次性
- Skills = SOP 手册，知识库文件夹，可复用
- MCP = 门禁卡，连接外部系统的能力

**关键设计**：渐进式披露（Progressive Disclosure）

- Skill 的元信息先加载一小段
- 模型判断需要时再读取完整内容
- 节省 Token，保持对话质量

### 3. 如何使用 Skill（安装方法）

**方法一：命令安装**（推荐）

```
安装这个 skill，skill 项目地址为:
https://github.com/anthropics/skills/tree/main/skills/skill-creator
```

**方法二：手动安装**

- Claude Code 路径：`~/.claude/skills`
- 手动创建 skills 文件夹
- 将 Skill 文件夹放入

**注意事项**：

- 文件夹命名：小写字母 + 连字符
- SKILL.md 是唯一必需文件
- Claude Code 支持热重载，无需重启

### 4. 推荐 Skill（五个卡片）

#### 4.1 web-access — 眼睛

**一句话**：给 Claude Code 一双眼睛，让它能看到网页世界

**核心能力**：
- 访问任意网页，获取实时信息
- 通过 CDP 操控浏览器，完成复杂交互
- 自动获取和安装其他 Skill

**推荐理由**：有了它，其他 Skill 的安装都变得简单。Claude Code 可以直接打开 GitHub 仓库，帮你安装你需要的任何 Skill。

#### 4.2 superpowers — 架构

**一句话**：让 Claude Code 学会系统性思考，从规划到实现

**核心能力**：
- Brainstorming：将想法转化为完整设计
- TDD：测试驱动开发，保证代码质量
- Systematic Debugging：系统性调试，快速定位问题
- 并行 Agent：多任务同时推进

**推荐理由**：不只是写代码，而是像资深工程师一样思考。从需求分析、架构设计到代码实现，全流程专业化。

#### 4.3 frontend-design — 设计

**一句话**：让 Claude Code 做出专业级的前端界面

**核心能力**：
- 高质量 UI 设计，避免 AI 审美
- 组件化架构，可维护性强
- 响应式适配，移动端友好
- 设计系统集成

**推荐理由**：做产品，界面是第一印象。这个 Skill 让 Claude Code 不只是能写代码，还能做出让人惊艳的界面。

#### 4.4 skill-creator — 创造

**一句话**：让 Claude Code 帮你创建自己的 Skill

**核心能力**：
- 分析你的需求，生成 Skill 结构
- 编写 SKILL.md，定义触发条件
- 创建示例和文档
- 打包和测试

**推荐理由**：当你有了自己的工作流程，把它封装成 Skill，就能无限复用。这个 Skill 让你从使用者变成创造者。

#### 4.5 skill-evolution-manager — 进化

**一句话**：让 Skill 在使用中不断优化

**核心能力**：
- 记录 Skill 运行中的错误和经验
- 自动迭代优化 SKILL.md
- 跨会话保持进化记录
- 避免重复犯错

**推荐理由**：Skill 不是写完就完了。这个 Skill 让你的 Skill 越用越聪明，越用越顺手。

### 5. 总结区

**核心观点**：Skill 的价值在于复用

- 从一个 Skill 开始，感受复用的力量
- 逐步封装更多工作流程
- 最终进入自由创造的状态

### 6. 底部跳转

```
[返回使用指南] [回看安装指南]
```

## 样式设计

### Skill 卡片

复用现有的 `.card` 样式，增加：
- 悬停时显示 Skill 名称的 accent 色边框
- 卡片内部分为：标题、描述、核心能力列表、推荐理由

### 交互效果

- 复用现有的 `.reveal` 滚动动画
- 复用现有的 `.decode` 解码动画（Hero 标题）
- 复用现有的光标球效果

## usage.html 修改

在结尾的总结区和 CTA 之间，新增一个跳转按钮：

```html
<div class="btn-group" style="margin-bottom:24px;">
  <a href="skills.html" class="btn btn-primary">→ 进阶技巧：Skill</a>
</div>
```

## 验证方式

- 本地浏览器直接打开 HTML 文件预览
- 检查三页之间的跳转是否正常
- 检查移动端响应式布局

## 依赖

- 无新增依赖
- 复用现有的 style.css 和 shared.js

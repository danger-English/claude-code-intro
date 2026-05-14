# Skills Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new Skills page (skills.html) to the claude-code-intro site, explaining what Skills are, how to use them, and recommending 5 core Skills.

**Architecture:** Single static HTML page following existing site patterns. Reuses shared.css and shared.js. Adds new section styles for Skill cards.

**Tech Stack:** HTML, CSS (existing style.css), vanilla JS (existing shared.js)

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `skills.html` | Create | New Skills page with 6 sections |
| `usage.html` | Modify | Add "进阶技巧" jump button before footer |
| `style.css` | Modify | Add `.skill-card` and `.skill-icon` styles |

---

## Task 1: Create skills.html skeleton

**Files:**
- Create: `skills.html`

- [ ] **Step 1: Create skills.html with full HTML structure**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>进阶技巧：Skill</title>
<meta name="description" content="Skill 是什么？如何用好 Skill？推荐五个核心 Skill，让你的 Claude Code 能力翻倍。">
<meta property="og:title" content="进阶技巧：Skill">
<meta property="og:description" content="Skill 是什么？如何用好 Skill？推荐五个核心 Skill。">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>▸</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@200;300;400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="progress" id="progress"></div>

<nav class="nav">
  <a href="index.html" class="nav-logo">claude code</a>
  <div class="nav-links">
    <a href="index.html">为什么用</a>
    <a href="install.html">怎么安装</a>
    <a href="usage.html">怎么用好</a>
    <a href="skills.html" class="active">进阶技巧</a>
  </div>
</nav>

<!-- ============ HERO ============ -->
<section class="hero" style="min-height:100vh;">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">// skills</p>
    <h1 style="min-height:90px;">
      <span class="decode" data-decode-hero data-decode-delay="800" data-text="给 Agent 装上超能力">给 Agent 装上超能力</span>
    </h1>
    <p class="hero-sub">
      <span class="decode" data-decode-hero data-decode-delay="2200" data-text="Skill，让 Claude Code 从聪明的实习生，变成全能的工程师。">Skill，让 Claude Code 从聪明的实习生，变成全能的工程师。</span>
    </p>
  </div>
</section>

<!-- ============ WHAT IS SKILL ============ -->
<section class="section">
  <div class="container">
    <div class="reveal" style="max-width:680px;margin:0 auto;">
      <div class="section-tag">// 什么是 Skill</div>
      <h2 class="section-title" style="margin-bottom:28px;"><span class="decode" data-text="给新人一本手册">给新人一本手册</span></h2>
      <div class="prose">
        <p style="margin-bottom:18px;">把 Agent 想成刚入职的实习生：很聪明，理解力强，啥都能聊。但你真让他干活，他最大的问题从来不是智商，是<strong style="color:var(--ink);">不熟你家规矩</strong>。</p>
        <p style="margin-bottom:18px;"><strong style="color:var(--ink);">Prompt</strong> 是你站在他旁边，当场口头交代任务。今天让他写一段开头，明天让他改语气。它天然适合一次性的、临场的指令——但你一关对话，它就像你刚说过的话一样，<strong style="color:var(--ink);">没了</strong>。</p>
        <p style="margin-bottom:18px;"><strong style="color:var(--ink);">Skill</strong> 是你给他一本公司的 SOP 手册。不是一张长到让人窒息的 Word，而是一个<strong style="color:var(--ink);">知识库文件夹</strong>——里面可以放规范、脚本、模板、参考资料。Agent 会在需要时自己去翻。</p>
      </div>
      <blockquote class="pull-quote" style="margin-top:28px;">Skill 的本质：把你的流程性知识，变成可复用的能力包。随叫随到，稳定发挥。</blockquote>
    </div>
  </div>
</section>

<!-- ============ PROGRESSIVE DISCLOSURE ============ -->
<section class="section" style="background:var(--bg-alt);">
  <div class="container">
    <div class="reveal" style="max-width:680px;margin:0 auto;">
      <div class="section-tag">// 关键设计</div>
      <h2 class="section-title" style="margin-bottom:28px;"><span class="decode" data-text="渐进式披露">渐进式披露</span></h2>
      <div class="prose">
        <p style="margin-bottom:18px;">人的瞬时记忆区太小了，一瞬间只能接受最多 7±2 个信息块。AI 因为受限于 Token，在本质上是一模一样的。</p>
        <p style="margin-bottom:18px;">所以 Skill 的设计是：<strong style="color:var(--ink);">先放目录，再放章节，最后放附录</strong>。</p>
        <p style="margin-bottom:18px;">Skill 的元信息先加载一小段，让模型知道"有这么个手册，适用范围是啥"。当它判断这次任务真用得上，再把完整的 SKILL.md 读进上下文。要是还不够，再按需去读你在文件夹里附带的其他文件。</p>
      </div>
      <div class="callout" style="margin-top:24px;">
        <div class="callout-label">为什么这很重要</div>
        <p>在大模型交互中，对话越长，模型越笨。Token 在 Agent 架构设计上寸土寸金。渐进式披露既保证执行准确，又省下大量 Token。</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ HOW TO USE ============ -->
<section class="section">
  <div class="container">
    <div class="section-hd reveal">
      <div class="section-tag">安装方法</div>
      <h2 class="section-title">如何使用 Skill</h2>
      <p class="section-desc">两种方式，选一种就行。</p>
    </div>

    <div class="grid-2 reveal" style="max-width:800px;margin:0 auto;">
      <div class="card">
        <h3>方法一：命令安装</h3>
        <p>直接在 Claude Code 里说：</p>
        <div class="code-block" style="margin-top:12px;">
          <code>安装这个 skill，skill 项目地址为:<br>https://github.com/anthropics/skills/tree/main/skills/skill-creator</code>
          <button class="copy-btn">Copy</button>
        </div>
        <p class="hint-text" style="margin-top:12px;">Claude Code 会自动帮你下载并安装。</p>
      </div>
      <div class="card">
        <h3>方法二：手动安装</h3>
        <p>将 Skill 文件夹放到指定目录：</p>
        <div class="code-block" style="margin-top:12px;">
          <code>~/.claude/skills/</code>
          <button class="copy-btn">Copy</button>
        </div>
        <p class="hint-text" style="margin-top:12px;">手动创建 skills 文件夹，放入即可。Claude Code 支持热重载，无需重启。</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ RECOMMENDED SKILLS ============ -->
<section class="section" style="background:var(--bg-alt);">
  <div class="container">
    <div class="section-hd reveal">
      <div class="section-tag">核心推荐</div>
      <h2 class="section-title">五个必装 Skill</h2>
      <p class="section-desc">从获取到创造，形成完整闭环。</p>
    </div>

    <div class="grid-2 reveal" style="max-width:900px;margin:0 auto;gap:20px;">

      <!-- Skill 1: web-access -->
      <div class="card skill-card">
        <div class="skill-icon">👁️</div>
        <h3>web-access</h3>
        <p style="color:var(--accent);font-family:var(--ff-mono);font-size:12px;margin-bottom:8px;">// 眼睛</p>
        <p>给 Claude Code 一双眼睛，让它能看到网页世界。</p>
        <ul style="margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.8;">
          <li>访问任意网页，获取实时信息</li>
          <li>通过 CDP 操控浏览器，完成复杂交互</li>
          <li>自动获取和安装其他 Skill</li>
        </ul>
        <p class="hint-text" style="margin-top:12px;">有了它，其他 Skill 的安装都变得简单。Claude Code 可以直接打开 GitHub，帮你安装你需要的任何 Skill。</p>
      </div>

      <!-- Skill 2: superpowers -->
      <div class="card skill-card">
        <div class="skill-icon">⚡</div>
        <h3>superpowers</h3>
        <p style="color:var(--accent);font-family:var(--ff-mono);font-size:12px;margin-bottom:8px;">// 架构</p>
        <p>让 Claude Code 学会系统性思考，从规划到实现。</p>
        <ul style="margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.8;">
          <li>Brainstorming：想法 → 完整设计</li>
          <li>TDD：测试驱动开发，保证质量</li>
          <li>并行 Agent：多任务同时推进</li>
        </ul>
        <p class="hint-text" style="margin-top:12px;">不只是写代码，而是像资深工程师一样思考。从需求分析到代码实现，全流程专业化。</p>
      </div>

      <!-- Skill 3: frontend-design -->
      <div class="card skill-card">
        <div class="skill-icon">🎨</div>
        <h3>frontend-design</h3>
        <p style="color:var(--accent);font-family:var(--ff-mono);font-size:12px;margin-bottom:8px;">// 设计</p>
        <p>让 Claude Code 做出专业级的前端界面。</p>
        <ul style="margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.8;">
          <li>高质量 UI 设计，避免 AI 审美</li>
          <li>组件化架构，可维护性强</li>
          <li>响应式适配，移动端友好</li>
        </ul>
        <p class="hint-text" style="margin-top:12px;">做产品，界面是第一印象。这个 Skill 让 Claude Code 不只是能写代码，还能做出让人惊艳的界面。</p>
      </div>

      <!-- Skill 4: skill-creator -->
      <div class="card skill-card">
        <div class="skill-icon">🔧</div>
        <h3>skill-creator</h3>
        <p style="color:var(--accent);font-family:var(--ff-mono);font-size:12px;margin-bottom:8px;">// 创造</p>
        <p>让 Claude Code 帮你创建自己的 Skill。</p>
        <ul style="margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.8;">
          <li>分析需求，生成 Skill 结构</li>
          <li>编写 SKILL.md，定义触发条件</li>
          <li>创建示例和文档</li>
        </ul>
        <p class="hint-text" style="margin-top:12px;">当你有了自己的工作流程，把它封装成 Skill，就能无限复用。这个 Skill 让你从使用者变成创造者。</p>
      </div>

      <!-- Skill 5: skill-evolution-manager -->
      <div class="card skill-card" style="grid-column: span 2;">
        <div class="skill-icon">🧬</div>
        <h3>skill-evolution-manager</h3>
        <p style="color:var(--accent);font-family:var(--ff-mono);font-size:12px;margin-bottom:8px;">// 进化</p>
        <p>让 Skill 在使用中不断优化。</p>
        <ul style="margin-top:12px;font-size:13px;color:var(--ink-2);line-height:1.8;">
          <li>记录 Skill 运行中的错误和经验</li>
          <li>自动迭代优化 SKILL.md</li>
          <li>跨会话保持进化记录</li>
        </ul>
        <p class="hint-text" style="margin-top:12px;">Skill 不是写完就完了。这个 Skill 让你的 Skill 越用越聪明，越用越顺手。</p>
      </div>

    </div>
  </div>
</section>

<!-- ============ SUMMARY ============ -->
<section class="section">
  <div class="container">
    <div class="reveal" style="max-width:680px;margin:0 auto;text-align:center;">
      <div class="section-tag">// 总结</div>
      <h2 class="section-title" style="margin-bottom:28px;line-height:1.25;">
        Skill 的价值，在于复用。
      </h2>
      <div class="prose" style="margin-bottom:36px;">
        <p>从一个 Skill 开始，感受复用的力量。</p>
        <p>逐步封装更多工作流程。</p>
        <p>最终进入自由创造的状态。</p>
        <p style="font-family:var(--ff-serif-cn);font-size:clamp(17px,2.5vw,22px);color:var(--ink);margin-top:28px;"><span class="decode" data-text="这就是 Skill 的意义。">这就是 Skill 的意义。</span></p>
      </div>
      <div class="btn-group">
        <a href="usage.html" class="btn btn-primary">← 返回使用指南</a>
        <a href="install.html" class="btn btn-secondary">回看安装指南</a>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="footer-mark">Made with Claude Code</div>
  <p class="footer-line">by 小满 · 2026</p>
  <p class="footer-line en">This page was made by Claude Code — and so can yours.</p>
</footer>

<script src="shared.js"></script>
</body>
</html>
```

- [ ] **Step 2: Open in browser to verify structure**

Open `skills.html` in browser. Verify:
- Hero section loads with decode animation
- All 6 sections render correctly
- Navigation shows "进阶技巧" as active
- Scroll reveal animations work

---

## Task 2: Add Skill card styles

**Files:**
- Modify: `style.css` (append at end)

- [ ] **Step 1: Add skill-card styles to style.css**

Append the following to the end of `style.css`:

```css
/* ============================================================
   SKILL CARD
   ============================================================ */
.skill-card {
  position: relative;
  transition: border-color 0.3s, transform 0.3s var(--ease-out);
}

.skill-card:hover {
  border-color: rgba(245, 166, 35, 0.2);
  transform: translateY(-3px);
}

.skill-icon {
  font-size: 32px;
  margin-bottom: 12px;
  filter: grayscale(0.2);
  transition: filter 0.3s;
}

.skill-card:hover .skill-icon {
  filter: grayscale(0);
}

.skill-card ul {
  list-style: none;
  padding: 0;
}

.skill-card ul li {
  padding-left: 16px;
  position: relative;
}

.skill-card ul li::before {
  content: '›';
  position: absolute;
  left: 0;
  color: var(--accent);
  opacity: 0.6;
}
```

- [ ] **Step 2: Open in browser to verify styles**

Open `skills.html` in browser. Verify:
- Skill cards have hover effect (border color, lift)
- Icons are properly sized
- List items have accent-colored bullets

---

## Task 3: Add jump button to usage.html

**Files:**
- Modify: `usage.html` (before footer)

- [ ] **Step 1: Add "进阶技巧" button to usage.html**

Find the closing `</section>` tag before the `<footer>` in `usage.html` (the SUMMARY section). Add the following button group before the existing btn-group:

```html
      <div class="btn-group" style="margin-bottom:24px;">
        <a href="skills.html" class="btn btn-primary">→ 进阶技巧：Skill</a>
      </div>
```

- [ ] **Step 2: Open usage.html to verify**

Open `usage.html` in browser. Verify:
- "进阶技巧：Skill" button appears before footer
- Button links to skills.html
- Button styling matches existing buttons

---

## Task 4: Update navigation on all pages

**Files:**
- Modify: `index.html` (nav links)
- Modify: `install.html` (nav links)
- Modify: `usage.html` (nav links)

- [ ] **Step 1: Add "进阶技巧" link to index.html nav**

In `index.html`, find the `.nav-links` div and add:

```html
    <a href="skills.html">进阶技巧</a>
```

- [ ] **Step 2: Add "进阶技巧" link to install.html nav**

In `install.html`, find the `.nav-links` div and add:

```html
    <a href="skills.html">进阶技巧</a>
```

- [ ] **Step 3: Add "进阶技巧" link to usage.html nav**

In `usage.html`, find the `.nav-links` div and add:

```html
    <a href="skills.html">进阶技巧</a>
```

- [ ] **Step 4: Verify navigation on all pages**

Open each page in browser and verify:
- All 4 nav links appear on every page
- Current page is highlighted with `.active` class
- Links work correctly between pages

---

## Task 5: Final verification

- [ ] **Step 1: Test all pages end-to-end**

Open `skills.html` in browser. Walk through:
1. Hero animation plays
2. Scroll through all sections
3. Check all reveal animations fire
4. Verify decode animation on headings
5. Test copy buttons on code blocks
6. Verify all nav links work
7. Verify mobile responsive (resize browser)

- [ ] **Step 2: Test cross-page navigation**

Navigate through all 4 pages in order:
1. index.html → install.html → usage.html → skills.html
2. Verify back links work
3. Verify "进阶技巧" button on usage.html works

- [ ] **Step 3: Commit all changes**

```bash
git add skills.html usage.html index.html install.html style.css docs/
git commit -m "feat: add Skills page with 5 core skill recommendations"
```

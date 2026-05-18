"""
用 Claude Code 做网站的经验分享 — PDF 生成脚本
基于 claude-code-intro 项目的实际开发过程
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

# ── 配色：暖调编辑风 ──
# 主色系：深炭灰正文 + 暖琥珀强调 + 柔和灰阶层次
INK       = HexColor("#1C1917")   # 正文主色：暖炭灰（不是纯黑，柔和不刺眼）
INK_2     = HexColor("#44403C")   # 正文副色：次深灰
INK_3     = HexColor("#78716C")   # 注释/小字：中性灰
ACCENT    = HexColor("#B45309")   # 章节标题：深琥珀
ACCENT_2  = HexColor("#047857")   # 二级标题：深翡翠绿
ACCENT_3  = HexColor("#1D4ED8")   # 代码/链接：深靛蓝
BG_CARD   = HexColor("#F5F5F4")   # 卡片/代码块底色：暖灰
BG_LIGHT  = HexColor("#FAFAF9")   # 页面底色倾向
RULE      = HexColor("#D6D3D1")   # 分隔线：浅暖灰
RED       = HexColor("#DC2626")   # 警告红
BLUE      = HexColor("#1D4ED8")   # 链接蓝

# ── 注册字体 ──
# 使用系统自带的中文字体
FONT_DIR = r"C:\Windows\Fonts"

try:
    pdfmetrics.registerFont(TTFont("SimHei", os.path.join(FONT_DIR, "simhei.ttf")))
    HEI = "SimHei"
except:
    HEI = "Helvetica-Bold"

try:
    pdfmetrics.registerFont(TTFont("SimSun", os.path.join(FONT_DIR, "simsun.ttc")))
    SUN = "SimSun"
except:
    SUN = "Helvetica"

try:
    pdfmetrics.registerFont(TTFont("MSYaHei", os.path.join(FONT_DIR, "msyh.ttc")))
    YAHEI = "MSYaHei"
except:
    YAHEI = HEI

try:
    pdfmetrics.registerFont(TTFont("STKaiTi", os.path.join(FONT_DIR, "STKAITI.TTF")))
    KAI = "STKaiTi"
except:
    KAI = SUN

# ── 字体层级系统 ──
# 封面: 32/16/12  |  章节: 22/16  |  正文: 11.5  |  注释: 9.5
# 行距比例: 标题 1.3x  |  正文 1.75x  |  注释 1.5x

def make_styles():
    styles = {}

    # ── 封面 ──
    styles["cover_title"] = ParagraphStyle(
        "cover_title", fontName=HEI, fontSize=32, leading=42,
        textColor=ACCENT, alignment=TA_CENTER,
        spaceAfter=6*mm
    )
    styles["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontName=YAHEI, fontSize=16, leading=24,
        textColor=INK_2, alignment=TA_CENTER,
        spaceAfter=5*mm
    )
    styles["cover_author"] = ParagraphStyle(
        "cover_author", fontName=YAHEI, fontSize=12, leading=18,
        textColor=INK_3, alignment=TA_CENTER
    )

    # ── 目录 ──
    styles["toc_title"] = ParagraphStyle(
        "toc_title", fontName=HEI, fontSize=22, leading=30,
        textColor=ACCENT, spaceAfter=6*mm
    )
    styles["toc_item"] = ParagraphStyle(
        "toc_item", fontName=YAHEI, fontSize=13, leading=24,
        textColor=INK, leftIndent=10*mm
    )

    # ── 标题层级 ──
    styles["h1"] = ParagraphStyle(
        "h1", fontName=HEI, fontSize=22, leading=30,
        textColor=ACCENT, spaceBefore=8*mm, spaceAfter=4*mm
    )
    styles["h2"] = ParagraphStyle(
        "h2", fontName=HEI, fontSize=16, leading=24,
        textColor=ACCENT_2, spaceBefore=6*mm, spaceAfter=3*mm
    )
    styles["h3"] = ParagraphStyle(
        "h3", fontName=HEI, fontSize=13, leading=20,
        textColor=INK, spaceBefore=4*mm, spaceAfter=2*mm
    )

    # ── 正文 ──
    styles["body"] = ParagraphStyle(
        "body", fontName=YAHEI, fontSize=11.5, leading=20,
        textColor=INK, alignment=TA_LEFT,
        spaceAfter=3*mm
    )
    styles["body_indent"] = ParagraphStyle(
        "body_indent", fontName=YAHEI, fontSize=11.5, leading=20,
        textColor=INK, alignment=TA_LEFT,
        leftIndent=8*mm, spaceAfter=2*mm
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontName=YAHEI, fontSize=11.5, leading=19,
        textColor=INK, leftIndent=10*mm, firstLineIndent=-5*mm,
        spaceAfter=2*mm
    )

    # ── 代码块 ──
    styles["code"] = ParagraphStyle(
        "code", fontName="Courier", fontSize=10, leading=16,
        textColor=ACCENT_3, leftIndent=8*mm, spaceAfter=2*mm,
        backColor=BG_CARD
    )

    # ── 提示框 ──
    styles["tip"] = ParagraphStyle(
        "tip", fontName=KAI, fontSize=10.5, leading=17,
        textColor=ACCENT, leftIndent=8*mm, rightIndent=8*mm,
        spaceAfter=3*mm, spaceBefore=2*mm,
        borderColor=ACCENT, borderWidth=1, borderPadding=6
    )

    # ── 引用块 ──
    styles["quote"] = ParagraphStyle(
        "quote", fontName=KAI, fontSize=12, leading=20,
        textColor=INK_2, leftIndent=12*mm, rightIndent=8*mm,
        spaceAfter=4*mm, spaceBefore=3*mm,
        borderColor=ACCENT, borderWidth=2, borderPadding=8
    )

    # ── 辅助文字 ──
    styles["small"] = ParagraphStyle(
        "small", fontName=YAHEI, fontSize=9.5, leading=15,
        textColor=INK_3, spaceAfter=2*mm
    )
    styles["step_num"] = ParagraphStyle(
        "step_num", fontName=HEI, fontSize=11.5, leading=18,
        textColor=ACCENT
    )
    styles["footer"] = ParagraphStyle(
        "footer", fontName=YAHEI, fontSize=9, leading=14,
        textColor=INK_3, alignment=TA_CENTER
    )
    return styles

S = make_styles()


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=RULE,
                       spaceBefore=3*mm, spaceAfter=3*mm)

def sp(h=3):
    return Spacer(1, h*mm)

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def step(num, title, desc):
    """带编号的步骤"""
    return Paragraph(
        f'<font color="#B45309"><b>Step {num}:</b></font> <b>{title}</b><br/>'
        f'<font size="10" color="#44403C">{desc}</font>',
        S["body_indent"]
    )

def tip_box(text):
    return Paragraph(f'<font color="#B45309">[提示]</font> {text}', S["tip"])

def build_pdf():
    output_path = os.path.join(os.path.dirname(__file__), "用ClaudeCode做网站的经验分享.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=25*mm, bottomMargin=20*mm,
        leftMargin=22*mm, rightMargin=22*mm
    )

    story = []
    page_width = A4[0] - 44*mm

    # ════════════════════════════════════════
    # 封面
    # ════════════════════════════════════════
    story.append(sp(30))
    story.append(Paragraph("用 Claude Code 做网站", S["cover_title"]))
    story.append(Paragraph("从零到上线的完整经验", S["cover_title"]))
    story.append(sp(8))
    story.append(HRFlowable(width="60%", thickness=2, color=ACCENT,
                             spaceBefore=2*mm, spaceAfter=6*mm))
    story.append(Paragraph("一个英语专业大学生的 AI 编程实践", S["cover_subtitle"]))
    story.append(sp(15))
    story.append(Paragraph("基于 claude-code-intro 项目的真实开发过程", S["cover_author"]))
    story.append(sp(4))
    story.append(Paragraph("小满 | 2026 年 5 月", S["cover_author"]))
    story.append(sp(20))
    story.append(Paragraph(
        '<font color="#78716C">工具：Claude Code &nbsp;&nbsp;|&nbsp;&nbsp; '
        '技术栈：HTML + CSS + JS + Three.js &nbsp;&nbsp;|&nbsp;&nbsp; '
        '部署：GitHub Pages + 自定义域名</font>',
        S["cover_author"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 目录
    # ════════════════════════════════════════
    story.append(Paragraph("目 录", S["toc_title"]))
    story.append(hr())
    toc_items = [
        ("一", "为什么选择 Claude Code"),
        ("二", "安装与配置"),
        ("三", "项目架构设计"),
        ("四", "常见问题与解决路径"),
        ("五", "页面板块设计"),
        ("六", "交互设计"),
        ("七", "粒子背景实现"),
        ("八", "网站上线"),
        ("九", "上线后优化"),
        ("十", "总结与建议"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(
            f'<font color="#B45309">{num}.</font> &nbsp;{title}',
            S["toc_item"]
        ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第一章：为什么选择 Claude Code
    # ════════════════════════════════════════
    story.append(Paragraph("一、为什么选择 Claude Code", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "作为一个英语专业的学生，我并没有系统学过前端开发。但我想做一个网站来推广 Claude Code，"
        "向不了解它的人展示《Claude Code 能做什么》。问题来了：我不会写代码，怎么办？",
        S["body"]
    ))
    story.append(Paragraph(
        "答案就是——用 Claude Code 来做 Claude Code 的推广网站。这本身就是一个最好的案例。",
        S["body"]
    ))

    story.append(Paragraph("1.1 Claude Code 是什么", S["h2"]))
    story.append(Paragraph(
        "Claude Code 是 Anthropic 推出的 AI 编程助手，运行在终端中。"
        "它不是一个简单的代码补全工具，而是一个能理解需求、规划架构、编写代码、调试修复的全能 Agent。"
        "你用自然语言告诉它你想做什么，它就能帮你做出来。",
        S["body"]
    ))

    story.append(Paragraph("1.2 为什么不用传统方式", S["h2"]))
    story.append(bullet("传统方式：学 HTML → 学 CSS → 学 JS → 学框架 → 写代码 → 调试 → 部署（数月）"))
    story.append(bullet("Claude Code 方式：描述需求 → AI 生成代码 → 验证效果 → 迭代优化（数天）"))
    story.append(Paragraph(
        "核心优势：你不需要成为专家，但你需要知道《什么是好的》。"
        "审美判断力和产品思维比编码能力更重要。",
        S["body"]
    ))

    story.append(Paragraph("1.3 实际项目成果", S["h2"]))
    story.append(Paragraph(
        "最终成果是一个四页的推广展示站（claude-code-intro），包含：",
        S["body"]
    ))
    story.append(bullet("首页：为什么要用 Claude Code（作品展示 + 终端动画）"))
    story.append(bullet("安装页：手把手教安装（Mac/Windows + 有无翻墙）"))
    story.append(bullet("使用页：CLAUDE.md 约束体系（金字塔交互组件）"))
    story.append(bullet("Skills 页：进阶技巧 + Skill 推荐与下载"))
    story.append(Paragraph(
        "技术栈：纯 HTML + CSS + 原生 JS + Three.js 粒子背景，无任何框架依赖。"
        "四页共享样式和交互逻辑，视觉风格统一。",
        S["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第二章：安装与配置
    # ════════════════════════════════════════
    story.append(Paragraph("二、安装与配置", S["h1"]))
    story.append(hr())

    story.append(Paragraph("2.1 安装 Claude Code", S["h2"]))
    story.append(step("1", "安装 Node.js", "从 nodejs.org 下载 LTS 版本，安装后终端输入 node -v 验证"))
    story.append(step("2", "安装 Claude Code", "终端执行 npm install -g @anthropic-ai/claude-code"))
    story.append(step("3", "配置 API Key", "如果是官方 API，直接登录即可；如果用国产模型，需要配合 CC Switch 工具"))
    story.append(step("4", "启动", "cd 到你的项目目录，输入 claude 启动"))

    story.append(Paragraph("2.2 接入国产模型（无需翻墙方案）", S["h2"]))
    story.append(Paragraph(
        "如果无法访问 Anthropic 官方 API，可以通过 CC Switch 工具接入国产模型。"
        "推荐的模型及获取方式：",
        S["body"]
    ))

    # 模型推荐表格
    model_data = [
        ["模型", "提供商", "特点"],
        ["智谱 GLM", "智谱 AI", "性价比高，中文能力强"],
        ["小米 MiMo", "小米", "推理能力强"],
        ["DeepSeek", "DeepSeek", "代码能力强，价格低"],
        ["Kimi", "Moonshot", "长文本处理能力突出"],
        ["百炼 Qwen", "阿里", "生态完善，API 稳定"],
        ["豆包", "字节跳动", "速度快，价格实惠"],
    ]
    model_table = Table(model_data, colWidths=[page_width*0.25, page_width*0.3, page_width*0.45])
    model_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(model_table)
    story.append(sp(3))

    story.append(Paragraph("2.3 首次启动的关键设置", S["h2"]))
    story.append(Paragraph(
        "首次启动 Claude Code 时，它会引导你完成基础配置。"
        "最重要的是 cd 到你的目标项目目录——Claude Code 会在当前目录下工作。",
        S["body"]
    ))
    story.append(tip_box(
        "建议在项目根目录创建 CLAUDE.md 文件，写明项目的基本信息和约束。"
        "这是 Claude Code 的《记忆文件》，它会自动读取并遵循其中的规则。"
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第三章：项目架构设计
    # ════════════════════════════════════════
    story.append(Paragraph("三、项目架构设计", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "好的架构是成功的一半。在开始写代码之前，先和 Claude Code 对齐项目结构，"
        "能避免后续大量的返工。",
        S["body"]
    ))

    story.append(Paragraph("3.1 目录结构规划", S["h2"]))
    story.append(Paragraph(
        "Claude Code 推广站采用扁平结构，四个页面各一个 HTML 文件，共享样式和脚本：",
        S["body"]
    ))

    dir_data = [
        ["文件", "用途", "说明"],
        ["index.html", "首页", "为什么要用 Claude Code"],
        ["install.html", "安装页", "怎么安装 Claude Code"],
        ["usage.html", "使用页", "怎么用好 Claude Code"],
        ["skills.html", "进阶页", "Skill 推荐与下载"],
        ["style.css", "共享样式", "四页统一视觉风格"],
        ["shared.js", "共享交互", "滚动动画、Tab切换、复制等"],
        ["particles.js", "粒子背景", "Three.js 星场效果"],
    ]
    dir_table = Table(dir_data, colWidths=[page_width*0.25, page_width*0.2, page_width*0.55])
    dir_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_2),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(dir_table)
    story.append(sp(3))

    story.append(Paragraph("3.2 设计系统", S["h2"]))
    story.append(Paragraph(
        '采用"编辑终端美学"设计风格——深色背景 + 琥珀强调色 + 终端绿 + 奶白文字。'
        "所有颜色通过 CSS 变量统一管理，方便全局调整：",
        S["body"]
    ))
    story.append(Paragraph(
        "--bg: #090909 (深黑) | --accent: #F5A623 (琥珀) | "
        "--success: #2DD4A8 (终端绿) | --ink: #F2EDE8 (奶白)",
        S["code"]
    ))

    story.append(Paragraph("3.3 CLAUDE.md 的作用", S["h2"]))
    story.append(Paragraph(
        "CLAUDE.md 是 Claude Code 的项目记忆文件。在项目根目录创建它，"
        "写明项目目标、技术栈、目录结构、设计规范等信息。"
        "Claude Code 每次启动时会自动读取这个文件，确保生成的代码符合你的项目规范。",
        S["body"]
    ))
    story.append(Paragraph(
        "关键经验：CLAUDE.md 不宜超过 200 行。超过 80 行后，Claude Code 开始出现信息遗漏。"
        "保持精炼，只写最关键的信息。",
        S["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第四章：常见问题与解决路径
    # ════════════════════════════════════════
    story.append(Paragraph("四、常见问题与解决路径", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "在开发过程中，几乎每个环节都会遇到问题。以下是最常见的几类问题及解决思路：",
        S["body"]
    ))

    story.append(Paragraph("4.1 图片加载慢", S["h2"]))
    story.append(Paragraph(
        "问题：首页展示的游戏截图 game.png 有 5MB，加载需要好几秒。",
        S["body"]
    ))
    story.append(Paragraph(
        "解决：将 PNG 转为 JPG（391KB），压缩率超过 90%。"
        "对于照片类图片，JPG 的压缩效果远好于 PNG。"
        "只有需要透明背景时才用 PNG。",
        S["body"]
    ))

    story.append(Paragraph("4.2 CDN 被墙", S["h2"]))
    story.append(Paragraph(
        "问题：Three.js 通过 CDN 引入，但国内无法访问 cdn.jsdelivr.net。",
        S["body"]
    ))
    story.append(Paragraph(
        "解决：将 three.min.js 下载到本地（603KB），改为本地引用。"
        "同时给 script 标签加 defer 属性，避免大文件阻塞页面渲染。",
        S["body"]
    ))
    story.append(tip_box(
        "经验法则：国内用户为主的网站，所有外部依赖都应考虑本地化。"
        "CDN 被墙是常态，不是例外。"
    ))

    story.append(Paragraph("4.3 交互效果不生效", S["h2"]))
    story.append(Paragraph(
        "问题：添加的 JavaScript 交互效果在某些页面不工作。",
        S["body"]
    ))
    story.append(Paragraph(
        "解决：检查脚本加载顺序。如果使用了 DOM 元素，"
        "确保 script 在对应 HTML 之后加载，或使用 DOMContentLoaded 事件。"
        "本项目所有四页共享 shared.js，需要确保每页的 HTML 结构一致。",
        S["body"]
    ))

    story.append(Paragraph("4.4 移动端适配", S["h2"]))
    story.append(Paragraph(
        "问题：桌面端效果很好，但手机上布局错乱。",
        S["body"]
    ))
    story.append(Paragraph(
        "解决：使用 clamp() 函数做流式排版（如 font-size: clamp(14px, 2.5vw, 16px)），"
        "用 CSS Grid 的 auto-fill + minmax 做自适应网格，"
        "粒子背景在移动端自动降级（检测 touchstart 事件后不加载）。",
        S["body"]
    ))

    story.append(Paragraph("4.5 文件体积膨胀", S["h2"]))
    story.append(Paragraph(
        "问题：随着功能增加，CSS 和 JS 文件越来越大。",
        S["body"]
    ))
    story.append(Paragraph(
        "解决：保持单一职责——style.css 只管样式，shared.js 只管交互逻辑。"
        "粒子效果独立为 particles.js。每个文件不超过 500 行为宜，"
        "超过后考虑拆分。本项目最终 shared.js 约 300 行，particles.js 约 200 行。",
        S["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第五章：页面板块设计
    # ════════════════════════════════════════
    story.append(Paragraph("五、页面板块设计", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "每个页面都有明确的目标，板块围绕目标组织。以下逐页说明设计思路：",
        S["body"]
    ))

    story.append(Paragraph("5.1 首页：为什么要用（index.html）", S["h2"]))
    story.append(Paragraph(
        '目标：给访客震撼，建立"Claude Code 很强"的第一印象。',
        S["body"]
    ))
    story.append(bullet("Hero 区：一句话钩子 + 终端打字动画（模拟 prompt → 代码生成过程）"))
    story.append(bullet("作品展示区：网页、小程序、游戏等真实案例，每个案例展示 prompt → 结果"))
    story.append(bullet("手机预览卡片：终端动画结束后，滑入手机样式的小程序预览（CSS 纯绘制）"))
    story.append(bullet("底部导航：两个按钮分别跳转到安装页和使用页"))

    story.append(Paragraph("5.2 安装页：怎么安装（install.html）", S["h2"]))
    story.append(Paragraph(
        "目标：零门槛，手把手教完成安装。",
        S["body"]
    ))
    story.append(bullet("按平台分流：Mac / Windows，有翻墙 / 无翻墙，四条路径"))
    story.append(bullet("步骤可视化：每个步骤高亮编号，清晰标注操作位置"))
    story.append(bullet("模型 API 链接：8 个国产模型的官方 API 获取地址，前 4 个标记推荐"))
    story.append(bullet('止步于"能跑起来"——CLAUDE.md 写法留给使用页'))

    story.append(Paragraph("5.3 使用页：怎么用好（usage.html）", S["h2"]))
    story.append(Paragraph(
        "目标：让用户理解约束先行的重要性，避免 Agent 失控。",
        S["body"]
    ))
    story.append(bullet("核心论点：约束先行比一切 Prompt 技巧都重要"))
    story.append(bullet("CLAUDE.md 四层体系：用金字塔交互组件展示（clip-path 梯形，hover 切换描述）"))
    story.append(bullet("全局模板：可直接复用的 CLAUDE.md 模板"))
    story.append(bullet("类比引入：治理公司 / 模拟经营游戏的路网规划"))

    story.append(Paragraph("5.4 Skills 页：进阶技巧（skills.html）", S["h2"]))
    story.append(Paragraph(
        "目标：向用户介绍 Skill 系统，推荐核心 Skill。",
        S["body"]
    ))
    story.append(bullet("实习生类比：解释 Prompt vs Skill vs MCP 的区别"))
    story.append(bullet("五个推荐 Skill：大字锚点（眼/思/美/创/迭代）+ 终端安装演示"))
    story.append(bullet("Skill 库：更多可下载的 Skill + 邮箱反馈入口"))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第六章：交互设计
    # ════════════════════════════════════════
    story.append(Paragraph("六、交互设计", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        '交互是让网站"活起来"的关键。以下是本项目实现的核心交互效果：',
        S["body"]
    ))

    story.append(Paragraph("6.1 滚动驱动动画", S["h2"]))
    story.append(Paragraph(
        "使用 IntersectionObserver API 实现元素滚动进入视口时的 reveal 动画。"
        "每个 .reveal 元素在进入视口时添加 .in 类，触发 CSS transition。"
        "展示区（showcase）使用交错动画，每个卡片依次出现。",
        S["body"]
    ))

    story.append(Paragraph("6.2 终端打字动画", S["h2"]))
    story.append(Paragraph(
        "首页 Hero 区模拟终端输入 prompt 的过程：逐字符显示，带闪烁光标。"
        "打字完成后，下方滑入手机预览卡片，完成 prompt → 过程 → 结果的叙事链。"
        "时序控制精确到毫秒（如 Done 行出现后 140ms 手机卡片才淡入）。",
        S["body"]
    ))

    story.append(Paragraph("6.3 自定义光标", S["h2"]))
    story.append(Paragraph(
        "每页有不同颜色的发光光标球（首页红色/安装页黄色/使用页绿色），"
        "通过 lerp（线性插值）实现平滑跟随。光标悬停标题时，标题颜色过渡到光标色。"
        "移动端不显示自定义光标。",
        S["body"]
    ))

    story.append(Paragraph("6.4 解码动画", S["h2"]))
    story.append(Paragraph(
        "Hero 标题和副标题以字符乱码 → 逐个解码浮现的视觉效果呈现。"
        "decodeRun() 函数控制解码过程，首页立即触发，其他页面滚动触发。",
        S["body"]
    ))

    story.append(Paragraph("6.5 Tab 切换与代码复制", S["h2"]))
    story.append(Paragraph(
        "安装页的 Mac/Windows 切换使用 data-tab / data-content 模式。"
        "代码块右上角有 Copy 按钮，点击后复制内容并显示 Copied! 反馈。"
        "所有交互都通过 shared.js 统一处理。",
        S["body"]
    ))

    story.append(Paragraph("6.6 按钮涟漪效果", S["h2"]))
    story.append(Paragraph(
        "所有按钮点击时产生涟漪扩散效果，增强操作反馈感。"
        "统计数字区域有滚动计数器动画，数字从 0 递增到目标值。",
        S["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第七章：粒子背景实现
    # ════════════════════════════════════════
    story.append(Paragraph("七、粒子背景实现", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "粒子星场背景是网站视觉体验的核心——2200 个粒子漂浮在深色背景上，"
        "鼠标移动时粒子被推开并弹性回拉，近距粒子自动连线。每页有独立色调。",
        S["body"]
    ))

    story.append(Paragraph("7.1 技术选型", S["h2"]))
    story.append(Paragraph(
        "选择 Three.js 而非 Canvas 2D，原因是 Three.js 的 WebGL 渲染性能更好，"
        "能轻松处理 2000+ 粒子的实时计算。使用 Three.js r128 版本（603KB）。",
        S["body"]
    ))

    story.append(Paragraph("7.2 核心实现", S["h2"]))
    story.append(bullet("粒子系统：Float32Array 存储 2200 个粒子的 xyz 坐标"))
    story.append(bullet("每帧更新：粒子缓慢漂浮 + 鼠标力场推开 + 弹性回拉原位"))
    story.append(bullet("连线逻辑：计算粒子间距离，低于阈值时绘制半透明连线"))
    story.append(bullet("每页色调：根据当前页面选择不同的核心色和辉光色"))

    story.append(Paragraph("7.3 性能优化", S["h2"]))
    story.append(bullet("像素比限制：Math.min(devicePixelRatio, 2)，避免高分屏性能问题"))
    story.append(bullet("滚动可见度：滚动时粒子最低保持 15% 可见度，不干扰阅读"))
    story.append(bullet("移动端降级：检测 touchstart 事件后完全不加载粒子系统"))
    story.append(bullet("加载失败降级：Three.js 加载失败时静默跳过，不影响页面内容"))

    story.append(Paragraph("7.4 半透明穿透设计", S["h2"]))
    story.append(Paragraph(
        "为了让粒子透过内容区域可见，所有卡片和终端背景改为半透明 rgba 值"
        "（--bg-alt: 55% / --bg-card: 60%），并加 backdrop-filter 毛玻璃效果。"
        "粒子在板块分隔区完全可见，在内容区隐约透出。",
        S["body"]
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第八章：网站上线
    # ════════════════════════════════════════
    story.append(Paragraph("八、网站上线", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "网站做好了，怎么让别人看到？有两条路径：国外免费渠道和国内稳定渠道。",
        S["body"]
    ))

    story.append(Paragraph("8.1 国外渠道：GitHub Pages（免费）", S["h2"]))
    story.append(step("1", "创建 GitHub 仓库", "将本地代码推送到 GitHub"))
    story.append(step("2", "开启 GitHub Pages", "Settings → Pages → 选择 master 分支 / (root)"))
    story.append(step("3", "访问", "https://用户名.github.io/仓库名/"))
    story.append(Paragraph(
        "优点：完全免费，自动部署，推送代码即更新。"
        "缺点：需要翻墙才能访问，国内用户看不到。",
        S["body"]
    ))

    story.append(Paragraph("8.2 国内渠道：自定义域名（稳定）", S["h2"]))
    story.append(Paragraph(
        "要让所有人都能访问，需要购买域名 + 国内 DNS 解析。实际成本很低：",
        S["body"]
    ))
    story.append(bullet("域名：在阿里云/腾讯云购买，.cn 域名首年约 20-30 元"))
    story.append(bullet("DNS 解析：购买解析专业版个人套餐（约 10 元/月）"))
    story.append(bullet("部署方式：仍通过 GitHub Pages，DNS 解析指向 GitHub 的 IP"))
    story.append(Paragraph(
        "这样做的好处：代码仍在 GitHub 管理（版本控制 + 免费托管），"
        "但用户通过国内域名访问，速度快且稳定。",
        S["body"]
    ))

    story.append(Paragraph("8.3 两种方案对比", S["h2"]))
    compare_data = [
        ["对比项", "GitHub Pages", "国内域名 + GitHub"],
        ["费用", "免费", "域名 + 解析约 150 元/年"],
        ["访问速度", "国内慢/需翻墙", "国内快速稳定"],
        ["部署方式", "git push 自动部署", "git push 自动部署"],
        ["适用场景", "面向海外用户", "面向国内用户"],
        ["HTTPS", "自动配置", "解析平台配置"],
    ]
    compare_table = Table(compare_data, colWidths=[page_width*0.2, page_width*0.38, page_width*0.42])
    compare_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(compare_table)
    story.append(sp(3))

    story.append(tip_box(
        "推荐方案：两条路都走。GitHub Pages 做主站（免费 + 版本控制），"
        "国内域名做镜像（稳定 + 可访问）。本项目同时部署了两个地址。"
    ))

    story.append(Paragraph("8.4 域名选择：不要只看价格", S["h2"]))
    story.append(Paragraph(
        "域名是网站的门面，选错了后期迁移成本很高。不同域名后缀在价格、稳定性、"
        "信任度上差异很大——便宜的未必适合你，贵的也未必值得。关键要看你的用户群和使用场景。",
        S["body"]
    ))

    story.append(Paragraph("域名后缀对比", S["h3"]))
    domain_data = [
        ["后缀", "年费参考", "信任度", "备案", "适用场景"],
        [".com", "60-80 元", "最高，全球通用", "可备案", "商业项目、个人品牌首选"],
        [".cn", "20-30 元", "国内高，需实名", "必须备案", "纯国内用户、政府/教育项目"],
        [".net", "60-80 元", "较高，技术感强", "可备案", "技术博客、工具站"],
        [".org", "80-100 元", "较高，公益属性", "可备案", "开源项目、非营利组织"],
        [".io", "200-400 元", "科技圈认可，海外高", "无法备案", "面向海外的技术产品"],
        [".xyz", "10-20 元", "低，廉价感强", "可备案", "不推荐正式项目使用"],
        [".site/.online", "5-15 元", "极低，垃圾邮件标签", "视注册商", "仅限临时测试"],
    ]
    domain_table = Table(domain_data, colWidths=[
        page_width*0.12, page_width*0.15, page_width*0.25, page_width*0.13, page_width*0.35
    ])
    domain_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(domain_table)
    story.append(sp(3))

    story.append(Paragraph("注册商选择", S["h3"]))
    story.append(Paragraph(
        "域名注册商的选择同样重要——稳定性、续费价格、DNS 解析速度、客服响应，"
        "这些隐性成本往往比首年注册价更值得关注：",
        S["body"]
    ))

    reg_data = [
        ["注册商", "优势", "劣势", "推荐度"],
        ["阿里云（万网）", "国内最大，备案方便，DNS 稳定", "续费偏贵，界面复杂", "国内首选"],
        ["腾讯云", "价格实惠，与微信生态打通", "DNS 偶有波动", "性价比之选"],
        ["Cloudflare", "成本价续费，自带 CDN/防护", "不支持备案，需翻墙管理", "海外项目首选"],
        ["Namecheap", "首年便宜，送隐私保护", "国内访问慢，DNS 一般", "海外个人站"],
        ["GoDaddy", "全球最大，品牌信任度高", "续费贵，界面臃肿", "不推荐"],
    ]
    reg_table = Table(reg_data, colWidths=[
        page_width*0.18, page_width*0.32, page_width*0.3, page_width*0.2
    ])
    reg_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_2),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(reg_table)
    story.append(sp(3))

    story.append(Paragraph("选域名的三条原则", S["h3"]))
    story.append(bullet(
        "<b>信任度优先于价格</b>：.xyz 首年只要 10 元，但发给客户邮箱会被当垃圾邮件。"
        ".com 贵一点，但全球通用、辨识度最高，是个人品牌和商业项目的默认选择。"
    ))
    story.append(bullet(
        "<b>续费价格比首年价格更重要</b>：很多注册商首年低价引流，续费翻倍。"
        "注册前务必查清续费价格——域名是长期投入，不是一次性消费。"
    ))
    story.append(bullet(
        "<b>备案不是可选项</b>：用国内服务器必须备案，用 GitHub Pages 等海外托管可以不备案。"
        "但备案过的域名在搜索引擎中权重更高、加载更快（可用国内 CDN），"
        "如果目标用户全在国内，备案是值得做的事。"
    ))

    story.append(tip_box(
        "本项目选择 .cn 域名（cclarning.cn），原因：目标用户全在国内、需要备案提升可信度、"
        "首年成本最低。同时保留 GitHub Pages 原始地址作为海外镜像。"
    ))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第九章：上线后优化
    # ════════════════════════════════════════
    story.append(Paragraph("九、上线后优化", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "上线不是终点，而是持续优化的起点。Claude Code 让优化变得极其简单。",
        S["body"]
    ))

    story.append(Paragraph("9.1 优化流程", S["h2"]))
    story.append(Paragraph(
        "整个优化闭环只需要三步：",
        S["body"]
    ))
    story.append(step("1", "发现问题", "自己浏览或收集用户反馈"))
    story.append(step("2", "让 Claude Code 修改", "描述问题，Claude Code 直接改代码"))
    story.append(step("3", "推送到 GitHub", "git push，网站自动更新"))

    story.append(Paragraph("9.2 本项目的优化历程", S["h2"]))
    story.append(Paragraph(
        "从首次上线到稳定版本，经历了多轮迭代：",
        S["body"]
    ))

    optim_data = [
        ["时间", "优化内容", "类型"],
        ["Day 1", "首次上线，四页基础内容", "功能"],
        ["Day 2", "新增 Skills 页面 + 5 个推荐 Skill", "功能"],
        ["Day 3", "补充模型 API 链接 + 安装流程优化", "体验"],
        ["Day 4", "新增 Skill 库下载 + 本地副本", "功能"],
        ["Day 5", "Three.js 粒子背景全站应用", "视觉"],
        ["Day 5", "图片压缩 5MB→391KB + CDN 本地化", "性能"],
        ["Day 6", "Hero 手机预览卡片 + 终端叙事链", "体验"],
    ]
    optim_table = Table(optim_data, colWidths=[page_width*0.15, page_width*0.6, page_width*0.25])
    optim_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_2),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), HEI),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTNAME", (0, 1), (-1, -1), YAHEI),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), INK),
        ("BACKGROUND", (0, 1), (-1, -1), BG_CARD),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(optim_table)
    story.append(sp(3))

    story.append(Paragraph("9.3 性能优化要点", S["h2"]))
    story.append(bullet("图片压缩：PNG → JPG，5MB → 391KB"))
    story.append(bullet("脚本延迟加载：所有 script 标签加 defer，不阻塞渲染"))
    story.append(bullet("CDN 本地化：外部依赖下载到本地，避免被墙"))
    story.append(bullet("移动端降级：复杂效果在小屏幕/触摸设备上自动关闭"))

    story.append(Paragraph("9.4 内容优化要点", S["h2"]))
    story.append(bullet("安装方式精简：从 3 种减为 2 种，降低选择困难"))
    story.append(bullet("反馈渠道适配：GitHub Issues 改为邮箱，适配国内用户"))
    story.append(bullet("Skill 本地副本：无法翻墙的用户可直接下载 zip"))
    story.append(bullet("模型链接补充：8 个国产模型 API 获取地址一键跳转"))
    story.append(PageBreak())

    # ════════════════════════════════════════
    # 第十章：总结与建议
    # ════════════════════════════════════════
    story.append(Paragraph("十、总结与建议", S["h1"]))
    story.append(hr())

    story.append(Paragraph("10.1 核心经验", S["h2"]))
    story.append(Paragraph(
        '用 Claude Code 做网站，最大的收获不是"AI 能写代码"，而是：',
        S["body"]
    ))
    story.append(bullet("约束先行：CLAUDE.md 写得好，AI 才能稳定产出高质量代码"))
    story.append(bullet("审美判断力比编码能力更重要：你不需要会写，但需要知道什么是好的"))
    story.append(bullet("迭代优于一次性：先做 MVP，再逐步优化，每次只改一个点"))
    story.append(bullet("本地化思维：国内用户为主的项目，所有外部依赖都要考虑降级方案"))

    story.append(Paragraph("10.2 给新手的建议", S["h2"]))
    story.append(bullet("先装好 Claude Code，cd 到一个空目录，从一个小页面开始"))
    story.append(bullet("第一版不要追求完美——先跑起来，再慢慢改"))
    story.append(bullet("善用 CLAUDE.md——把你的项目信息、设计规范、技术选型都写进去"))
    story.append(bullet("遇到问题先描述清楚，Claude Code 能解决 90% 的前端问题"))
    story.append(bullet("发布到 GitHub Pages，让别人能看到你的成果——这会给你持续的动力"))

    story.append(Paragraph("10.3 适用场景", S["h2"]))
    story.append(Paragraph(
        "Claude Code 做网站最适合以下场景：",
        S["body"]
    ))
    story.append(bullet("个人作品集、博客、展示站（静态页面，不需要后端）"))
    story.append(bullet("产品落地页、营销页（重视觉效果和交互体验）"))
    story.append(bullet("内部工具、管理面板（数据展示 + 简单交互）"))
    story.append(bullet("原型验证（快速做出可交互的原型，验证想法）"))

    story.append(Paragraph("10.4 不适合的场景", S["h2"]))
    story.append(bullet("复杂 SPA 应用（需要状态管理、路由、组件通信等）"))
    story.append(bullet("实时协作应用（需要 WebSocket、数据库等后端支持）"))
    story.append(bullet("大规模电商系统（需要支付、库存、订单等复杂业务逻辑）"))

    story.append(sp(10))
    story.append(HRFlowable(width="40%", thickness=1.5, color=ACCENT,
                             spaceBefore=5*mm, spaceAfter=5*mm))
    story.append(Paragraph(
        "这个网站本身就是 Claude Code 能力的最佳证明。"
        "一个不会写代码的英语专业学生，用 6 天时间做出了一个完整的推广展示站。"
        "如果你也有想法，现在就开始——Claude Code 在终端里等着你。",
        S["quote"]
    ))

    # ── 构建 PDF ──
    doc.build(story)
    print(f"PDF 生成完成: {output_path}")
    print(f"文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    build_pdf()

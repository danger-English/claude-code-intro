---
name: skill-evolution-manager
description: Skill 进化管理器，记录 skill 运行中的错误和经验，自动迭代优化。当 skill 运行出错或有改进空间时，记录经验到 evolution.json，然后缝合到 SKILL.md 中，让 skill 越来越牛逼。适用于：skill 运行出错后想避免再犯、发现 skill 可以优化的地方、想让 skill 在使用中不断进化。
---

# Skill Evolution Manager

Skill 进化管理器，让 skill 在使用中不断学习、进化、变强。

## 核心理念

**一坑不二踩**：skill 运行中的每个错误、每个改进点，都是宝贵的经验。这些经验不应该丢失，而应该被记录、积累、应用，让 skill 越来越聪明。

## 核心功能

### 1. 记录经验（对话中）

当 skill 运行过程中出现以下情况时，记录经验：
- **错误**：skill 执行失败、输出错误、不符合预期
- **改进点**：发现更好的做法、更优的方案、更高效的流程
- **边界情况**：遇到 skill 未覆盖的场景、特殊输入、意外输出

**记录方式**：
```
记录经验：
- 技能：<skill-name>
- 类型：错误 / 改进 / 边界
- 描述：<具体发生了什么>
- 原因：<为什么会这样>
- 建议：<下次应该怎么做>
```

### 2. 保存经验（对话结束时）

对话结束时，将经验保存到 `evolution.json` 文件：

```bash
~/.claude/skills/<skill-name>/evolution.json
```

**evolution.json 格式**：
```json
{
  "skill_name": "<skill-name>",
  "version": "1.0",
  "experiences": [
    {
      "id": 1,
      "timestamp": "2026-04-28T10:30:00Z",
      "type": "error",
      "description": "执行 xxx 命令时失败",
      "reason": "缺少 xxx 依赖",
      "suggestion": "下次先检查依赖是否存在",
      "context": "用户输入 xxx 时触发",
      "applied": false
    }
  ]
}
```

### 3. 缝合经验（定期或手动）

将 `evolution.json` 中的经验缝合到 SKILL.md 中：

**缝合位置**：在 SKILL.md 中添加 "进化经验" 章节：

```markdown
## 进化经验

### 已解决的问题

1. **问题**：执行 xxx 命令时失败
   - **原因**：缺少 xxx 依赖
   - **解决方案**：下次先检查依赖是否存在
   - **记录时间**：2026-04-28

2. **问题**：xxx 场景下输出格式错误
   - **原因**：未考虑 xxx 特殊情况
   - **解决方案**：添加 xxx 判断逻辑
   - **记录时间**：2026-04-28

### 优化建议

1. **建议**：可以使用 xxx 替代 yyy，效率更高
   - **适用场景**：xxx
   - **预期效果**：提升 30% 效率
   - **记录时间**：2026-04-28
```

## 使用流程

### 场景 1：skill 运行出错

**用户输入**：
```
使用 xxx skill 执行任务
```

**skill 执行出错**，记录经验：
```
记录经验：
- 技能：xxx
- 类型：错误
- 描述：执行 xxx 命令时失败，报错 "command not found"
- 原因：未检查 xxx 命令是否安装
- 建议：下次先执行 `which xxx` 检查命令是否存在
```

**对话结束时**，保存经验：
```
已将经验保存到 ~/.claude/skills/xxx/evolution.json
```

**下次使用前**，缝合经验：
```
已将 1 条经验缝合到 ~/.claude/skills/xxx/SKILL.md
```

### 场景 2：发现改进点

**用户输入**：
```
使用 xxx skill 执行任务
```

**skill 执行成功**，但发现改进空间：
```
记录经验：
- 技能：xxx
- 类型：改进
- 描述：当前使用 xxx 方法，但 yyy 方法更优
- 原因：yyy 方法效率更高，代码更简洁
- 建议：下次优先使用 yyy 方法
```

### 场景 3：边界情况

**用户输入**：
```
使用 xxx skill 处理特殊输入
```

**skill 处理不当**，记录边界情况：
```
记录经验：
- 技能：xxx
- 类型：边界
- 描述：输入包含特殊字符时，输出格式错误
- 原因：未对特殊字符进行转义处理
- 建议：添加特殊字符转义逻辑
```

## 与 GitHub 项目的协作

### 问题：GitHub 项目更新 vs 本地迭代

- **GitHub 项目更新**：会修改 SKILL.md，拉取最新代码
- **本地迭代**：记录经验，优化 skill

**解决方案**：
1. **SKILL.md**：保持与 GitHub 项目同步，不修改原始内容
2. **evolution.json**：存储本地迭代的经验，独立于 SKILL.md
3. **缝合时**：将 evolution.json 的经验追加到 SKILL.md 的 "进化经验" 章节

### 更新流程

```bash
# 1. 拉取 GitHub 最新版本
git -C ~/.claude/skills/<skill-name> pull

# 2. 读取本地 evolution.json
cat ~/.claude/skills/<skill-name>/evolution.json

# 3. 缝合经验到 SKILL.md
# 将 evolution.json 的内容追加到 SKILL.md 的 "进化经验" 章节
```

## 使用示例

### 示例 1：记录错误

**用户输入**：
```
使用 github-to-me 打包 https://github.com/cli/cli
```

**执行出错**：
```
错误：无法获取 README 内容，API 返回 403
```

**记录经验**：
```
记录经验：
- 技能：github-to-me
- 类型：错误
- 描述：获取 README 内容时 API 返回 403
- 原因：GitHub API 有速率限制，未认证请求容易被限制
- 建议：添加 GitHub Token 认证，或使用本地缓存
```

**保存到 evolution.json**：
```json
{
  "skill_name": "github-to-me",
  "experiences": [
    {
      "id": 1,
      "timestamp": "2026-04-28T10:30:00Z",
      "type": "error",
      "description": "获取 README 内容时 API 返回 403",
      "reason": "GitHub API 有速率限制，未认证请求容易被限制",
      "suggestion": "添加 GitHub Token 认证，或使用本地缓存",
      "context": "打包 https://github.com/cli/cli 时触发",
      "applied": false
    }
  ]
}
```

### 示例 2：缝合经验

**用户输入**：
```
缝合 github-to-me 的经验
```

**执行缝合**：
```
已将 1 条经验缝合到 ~/.claude/skills/github-to-me/SKILL.md
```

**SKILL.md 新增内容**：
```markdown
## 进化经验

### 已解决的问题

1. **问题**：获取 README 内容时 API 返回 403
   - **原因**：GitHub API 有速率限制，未认证请求容易被限制
   - **解决方案**：添加 GitHub Token 认证，或使用本地缓存
   - **记录时间**：2026-04-28
```

## 命令参考

### 记录经验
```
记录经验：
- 技能：<skill-name>
- 类型：错误 / 改进 / 边界
- 描述：<具体描述>
- 原因：<原因分析>
- 建议：<改进建议>
```

### 保存经验
```
保存 <skill-name> 的经验
```

### 缝合经验
```
缝合 <skill-name> 的经验
```

### 查看经验
```
查看 <skill-name> 的经验
```

### 清空经验
```
清空 <skill-name> 的经验
```

## 注意事项

- 经验记录要及时，不要等到对话结束才记录
- 经验要具体，不要过于笼统
- 缝合经验时，要确保 SKILL.md 的格式正确
- 定期清理已应用的经验，避免 evolution.json 过大
- 对于 GitHub 项目，优先拉取最新版本，再缝合本地经验

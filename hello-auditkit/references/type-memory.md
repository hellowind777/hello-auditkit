# 记忆文件审计规则

> **继承**：`rules-universal.md` 中的所有规则
> **主要标准**：`ref-gpt-prompting-standard.md`（用于指令内容质量）
> **执行要求**：执行以下每个检查表。验证导入语法、指令质量和内容具体性。
>
> **关键**：记忆文件包含 AI 的指令。审计指令质量时，应用 `ref-gpt-prompting-standard.md` 中的 GPT-5.2 提示词标准。

## 目录

- [概述](#概述)
- [审计执行](#审计执行)
- [AGENTS.md 审计](#agentsmd-审计)
- [CLAUDE.md 审计](#claudemd-审计)
- [GEMINI.md 审计](#geminimd-审计)
- [常见问题](#常见问题)

---

## 概述

**适用于**：AI 助手记忆/指令文件

| 文件类型 | 平台 | 用途 |
|----------|------|------|
| AGENTS.md | Codex CLI | 代理指令 |
| CLAUDE.md | Claude Code | 记忆文件 |
| GEMINI.md | Gemini CLI | 上下文文件 |

**通用尺寸限制**：推荐 ≤2000 行，限制 ≤3000 行

---

## 审计执行

### 步骤 1：识别记忆类型

确定是哪个平台的记忆文件：
- AGENTS.md → Codex CLI
- CLAUDE.md → Claude Code
- GEMINI.md → Gemini CLI

### 步骤 2：加载 GPT-5.2 标准

读取 `ref-gpt-prompting-standard.md` 并应用指令质量检查。

### 步骤 3：应用平台特定检查

应用以下相关平台章节中的检查。

### 步骤 4：生成发现

使用常见问题中的应标记/不应标记规则过滤问题。

---

## AGENTS.md 审计

> 来源：Codex CLI 文档

### 合并层次

AGENTS.md 文件自上而下合并：
1. `~/.codex/AGENTS.md` - 个人全局
2. 仓库根目录的 `AGENTS.md` - 项目级
3. 当前目录的 `AGENTS.md` - 文件夹级

### 结构验证

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 文件位置 | 正确的层次级别 | Info |
| 合并意识 | 与父级 AGENTS.md 无冲突 | Severe |
| 指令清晰度 | 清晰、可操作的指令 | Warning |
| 范围适当性 | 指令与文件位置匹配 | Warning |
| 文件长度 | 推荐 ≤2000 行 | Warning |

### 内容指南

**好的模式：**
```markdown
- Always use TypeScript for new files
- Run `npm test` before committing
- Follow existing code style in the project
```

**差的模式：**
```markdown
- Be helpful (太模糊)
- Do everything correctly (不可操作)
```

### 应标记

- 层次级别之间的矛盾指令
- 模糊、不可操作的指令
- 与文件范围不匹配的指令
- 缺少关键的项目特定指导

### 不应标记

- 简单的要点格式
- 合理的指令变化
- 未出现的可选指导

---

## CLAUDE.md 审计

> 来源：Claude Code 文档

### 记忆类型

| 类型 | 位置 |
|------|------|
| 项目记忆 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` |
| 项目规则 | `./.claude/rules/*.md` |
| 用户记忆 | `~/.claude/CLAUDE.md` |
| 项目本地 | `./CLAUDE.local.md` |

### 结构验证

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 文件位置 | 记忆类型正确 | Info（咨询性）|
| 导入语法 | 有效的 `@path/to/file` | Fatal |
| 路径特定规则 | 有效的 YAML frontmatter | Severe |
| 格式 | 要点和 markdown 标题 | Info |
| 文件长度 | 推荐 ≤2000 行 | Warning |

### 导入语法

**有效：**
```markdown
@./shared-rules.md
@../common/rules.md
```

**无效：**
```markdown
@rules.md  (缺少路径前缀)
```

### 路径特定规则

```markdown
---
paths: src/api/**/*.ts
---
# API 规则
- All endpoints must include input validation
```

### 应标记

- 无效的导入语法
- 文件位置对记忆类型不正确
- 路径特定规则的 YAML frontmatter 无效
- 模糊指令（"format code properly"）

### 不应标记

- 缺少可选章节
- 风格变化
- 合理的指令选择

---

## GEMINI.md 审计

> 来源：Gemini CLI 文档

### 文件层次

文件按顺序加载和连接：
1. **全局**：`~/.gemini/GEMINI.md`
2. **项目根目录/祖先目录**：直到 `.git` 文件夹
3. **子目录**：当前目录以下

### 结构验证

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 文件位置 | 正确的层次级别 | Info（咨询性）|
| 导入语法 | 有效的 `@file.md` 导入 | Fatal |
| Markdown 格式 | 标准 markdown | Info |
| 指令清晰度 | 清晰、可操作 | Warning |
| 文件长度 | 推荐 ≤2000 行 | Warning |

### 导入语法

```markdown
@./shared-rules.md
@../common/context.md
```

### 命令参考

- `/memory show` - 显示完整连接的上下文
- `/memory refresh` - 重新加载所有上下文文件
- `/memory add <text>` - 追加到全局 GEMINI.md

### 应标记

- 无效的导入语法
- 层次级别之间的矛盾指令
- 模糊、不可操作的指令

### 不应标记

- 缺少可选章节
- 风格变化
- 合理的指令选择

---

## 常见问题

### 所有记忆文件

| 问题 | 严重性 |
|------|--------|
| 无效的导入语法 | Fatal |
| 矛盾指令 | Severe |
| 指令与范围不匹配 | Warning |
| 模糊指令 | Warning |
| 文件 >2000 行 | Warning |
| 文件 >3000 行 | Severe |

### 内容质量检查

<instruction_quality_analysis>
"指令质量是否足够"的推理过程：
- 具体性：是否足够具体？（"使用 2 空格缩进" vs "正确格式化代码"）
- 可操作性：是否可操作？（"提交前运行 `npm test`" vs "测试你的代码"）
- 清晰度：是否清晰？（"新文件使用 TypeScript" vs "使用好的实践"）
</instruction_quality_analysis>

| 检查 | 好 | 差 |
|------|----|----|
| 具体性 | "使用 2 空格缩进" | "正确格式化代码" |
| 可操作性 | "提交前运行 `npm test`" | "测试你的代码" |
| 清晰度 | "新文件使用 TypeScript" | "使用好的实践" |

### 指令质量（LLM 最佳实践）

> **完整 LLM 检查**：见 `rules-universal.md` → LLM 提示词最佳实践
> **详细实践**：见 `type-prompt.md` → LLM 提示词最佳实践

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 详尽约束 | 输出的明确长度限制 | Warning |
| 范围边界 | 清晰的"禁止"约束 | Warning |
| 歧义处理 | 不清楚情况的指令 | Info |
| 简洁性 | 无 AI 已知的解释 | Warning |
| 自由度匹配 | 约束与任务脆弱性匹配 | Warning |
| 具体指令 | 可操作，不模糊 | Warning |
| 无矛盾 | 无冲突规则 | Severe |
| 工具偏好 | 优先使用工具而非内部知识（如使用工具）| Warning |
| 代理式更新 | 主要阶段的简短更新（如是代理式）| Warning |
| 长上下文大纲 | >10k token：大纲、重述 | Warning |

### 最佳实践

1. **具体**：清晰、可操作的指令
2. **使用要点**：易于扫描
3. **包含命令**：常用的构建/测试/lint
4. **记录约定**：代码风格、命名
5. **匹配范围**：全局规则在根目录，特定规则在子目录
6. **单一信息源**：无重复规则
7. **适当自由度**：灵活任务用指南，脆弱操作用严格规则

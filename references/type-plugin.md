# 插件审计规则

> **继承**：`rules-universal.md` 中的所有规则
> **主要标准**：`ref-codex-skills-standard.md`（用于插件内的技能）
> **次要标准**：`ref-gpt-prompting-standard.md`（用于命令/代理正文内容）
> **执行要求**：执行以下每个检查表。验证结构、路径、组件（命令、代理、钩子、MCP、LSP）。
>
> **关键**：对于插件内的技能，应用 `ref-codex-skills-standard.md` 中的 Codex CLI Skills 标准。对于命令/代理正文内容（非脚本文本），应用 `ref-gpt-prompting-standard.md` 中的 GPT-5.2 提示词标准。

## 目录

- [概述](#概述)
- [审计执行](#审计执行)
- [插件结构](#插件结构)
- [插件清单](#插件清单)
- [命令审计](#命令审计)
- [代理审计](#代理审计)
- [钩子审计](#钩子审计)
- [MCP 服务器审计](#mcp-服务器审计)
- [LSP 服务器审计](#lsp-服务器审计)
- [常见问题](#常见问题)

---

## 概述

**插件识别**：包含 `.claude-plugin/plugin.json` 的目录

```
plugin-name/
├── .claude-plugin/plugin.json  (必需)
├── commands/                    (斜杠命令)
├── agents/                      (子代理定义)
├── skills/                      (代理技能)
├── hooks/hooks.json             (事件处理器)
├── .mcp.json                    (MCP 服务器)
└── .lsp.json                    (LSP 服务器)
```

**关键**：组件必须在根级别，不能在 `.claude-plugin/` 内部

---

## 审计执行

### 步骤 1：加载标准

读取并应用：
- `ref-codex-skills-standard.md` 用于技能结构/frontmatter
- `ref-gpt-prompting-standard.md` 用于命令/代理正文内容

### 步骤 2：验证插件结构

检查 `.claude-plugin/plugin.json` 存在且组件在根级别。

### 步骤 3：审计每个组件

应用相关章节的检查：
- 命令 → 命令审计
- 代理 → 代理审计
- 技能 → 应用完整的 `type-skill.md` 检查
- 钩子 → 钩子审计
- MCP/LSP → MCP/LSP 服务器审计

### 步骤 4：生成发现

使用常见问题中的应标记/不应标记规则过滤问题。

---

## 插件结构

### 关键规则

| 规则 | 要求 | 严重性 |
|------|------|--------|
| 清单位置 | `plugin.json` 在 `.claude-plugin/` 中 | Fatal |
| 组件目录 | 在插件根目录，不在 `.claude-plugin/` 中 | Fatal |
| 技能文件命名 | 完全是 `SKILL.md`（区分大小写）| Fatal |
| 命令/代理格式 | `.md` 文件带 YAML frontmatter | Severe |
| 钩子格式 | 包装器 `{"hooks": {...}}` | Severe |
| 路径引用 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe |
| 命名 | 所有名称使用 kebab-case | Warning |

### 路径变量

| 变量 | 描述 | 可用于 |
|------|------|--------|
| `${CLAUDE_PLUGIN_ROOT}` | 插件目录 | 钩子、MCP、LSP、脚本 |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录 | 钩子、脚本 |
| `${CLAUDE_ENV_FILE}` | 环境文件路径 | SessionStart 钩子 |

### 禁止使用

- 硬编码绝对路径（`/Users/name/...`）
- 从工作目录的相对路径
- 主目录快捷方式（`~/plugins/...`）

---

## 插件清单

### plugin.json

**必需：**
```json
{
  "name": "plugin-name"
}
```

**推荐：**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation"
}
```

### 验证规则

| 字段 | 规则 | 严重性 |
|------|------|--------|
| name | 必需、非空、kebab-case | Fatal |
| name | ≤50 字符 | Warning |
| version | Semver 格式（X.Y.Z）| Warning |
| description | ≤200 字符 | Warning |
| 自定义路径 | 相对路径，以 `./` 开头 | Severe |

---

## 命令审计

**位置**：`commands/*.md`

### Frontmatter

```yaml
---
description: Brief description for /help
argument-hint: <required> [optional]
allowed-tools: [Read, Glob, Grep]
model: sonnet
---
```

| 字段 | 规则 | 严重性 |
|------|------|--------|
| description | 推荐，≤100 字符 | Info |
| allowed-tools | 有效的工具名 | Severe |
| model | `sonnet`、`opus`、`haiku` | Severe |

### allowed-tools 格式

```yaml
# 单个工具
allowed-tools: Read

# 多个（字符串）
allowed-tools: Read, Write, Edit

# 多个（数组）
allowed-tools:
  - Read
  - Bash(git:*)

# MCP 工具
allowed-tools: ["mcp__server__tool"]
```

### 内容规则

**命令是给 Claude 的指令，不是给用户的消息。**

✅ **正确：**
```markdown
Review this code for vulnerabilities:
- SQL injection, XSS attacks
Provide line numbers and severity.
```

❌ **错误：**
```markdown
This command will review your code.
You'll receive a report.
```

### 命令提示词质量

> **完整 LLM 检查**：见 `rules-universal.md` → LLM 提示词最佳实践

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 清晰任务 | 具体、可操作的指令 | Severe |
| 详尽约束 | 指定输出长度 | Warning |
| 范围边界 | 不要做什么 | Warning |
| 自由度匹配 | 约束适合任务脆弱性 | Warning |
| 无 AI 已知内容 | 不解释标准概念 | Info |
| 工具偏好 | 优先使用工具而非内部知识 | Warning |
| 代理式更新 | 主要阶段的简短更新（如是代理式）| Warning |

---

## 代理审计

**位置**：`agents/*.md`

### Frontmatter

```yaml
---
name: agent-name
description: Agent role and when to use
tools: [Glob, Grep, Read]
model: sonnet
---
```

| 字段 | 必需 | 规则 | 严重性 |
|------|------|------|--------|
| name | 是 | kebab-case，≤50 字符 | Severe |
| description | 是 | 包含何时使用，≤500 字符 | Severe |
| tools | 否 | 有效的工具名 | Warning |
| model | 否 | `inherit`、`sonnet`、`opus`、`haiku` | Warning |

### 描述模式

```yaml
description: Use this agent when [conditions]. Examples:

<example>
Context: [Situation]
user: "[Request]"
assistant: "[Response]"
<commentary>
[Why this agent triggered]
</commentary>
</example>
```

### 代理正文质量（LLM 最佳实践）

> **完整 LLM 检查**：见 `rules-universal.md` → LLM 提示词最佳实践

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 清晰角色 | 具体的代理目的 | Severe |
| 触发条件 | 在描述中，不在正文中 | Severe |
| 详尽约束 | 输出期望 | Warning |
| 范围纪律 | 代理不应该做什么 | Warning |
| 工具使用指导 | 何时使用哪些工具 | Info |
| 自由度匹配 | 约束级别适合任务 | Warning |
| 简洁性 | 无冗余解释 | Warning |
| 工具偏好 | 优先使用工具而非内部知识 | Warning |
| 代理式更新 | 主要阶段的简短更新，具体结果 | Warning |
| 禁止任务扩展 | 不超出用户请求扩展 | Warning |
| 长上下文大纲 | >10k token：大纲、重述 | Warning |

---

## 钩子审计

### hooks.json 格式（插件上下文）

**必须使用包装器格式：**
```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Stop": [...]
  }
}
```

**不是直接格式（那是给 settings.json 的）：**
```json
{
  "PreToolUse": [...]  // 插件中错误
}
```

### 钩子事件

| 事件 | 描述 | 匹配器 |
|------|------|--------|
| PreToolUse | 工具前，可批准/拒绝/修改 | 是 |
| PostToolUse | 工具成功后 | 是 |
| Stop | 主代理考虑停止 | 是 |
| SubagentStop | 子代理考虑停止 | 是 |
| SessionStart | 会话开始 | 是 |
| Notification | 收到通知时 | 是 |

### 钩子配置

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 钩子类型

| 类型 | 描述 | 用例 |
|------|------|------|
| `command` | 执行 shell | 脚本、验证 |
| `prompt` | LLM 评估 | 复杂决策 |
| `agent` | 代理式验证器 | 多步验证 |

### 匹配器模式

| 模式 | 匹配 |
|------|------|
| `Write` | 仅 Write |
| `Edit\|Write` | Edit 或 Write |
| `Notebook.*` | 所有 Notebook 工具 |
| `*` 或 `""` | 所有工具 |
| `mcp__server__.*` | MCP 服务器的所有工具 |

### 钩子脚本

**Bash：**
```bash
#!/bin/bash
set -euo pipefail
input=$(cat)  # 从 stdin 读取 JSON
tool_name=$(echo "$input" | jq -r '.tool_name')
echo '{"continue": true}'  # 输出 JSON
```

**Python：**
```python
#!/usr/bin/env python3
import sys, json
input_data = json.load(sys.stdin)
print(json.dumps({"continue": True}))
```

| 检查 | 规则 | 严重性 |
|------|------|--------|
| Shebang | 存在 | Warning |
| 输入 | 从 stdin 读取 JSON | Severe |
| 输出 | 向 stdout 输出有效 JSON | Severe |
| 退出码 | 0=成功，2=阻止 | Warning |
| 路径 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe |

---

## MCP 服务器审计

**位置**：`.mcp.json`

### 格式

**stdio（本地）：**
```json
{
  "server-name": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
    "env": {"API_KEY": "${MY_API_KEY}"}
  }
}
```

**HTTP：**
```json
{
  "api-server": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {"Authorization": "Bearer ${API_TOKEN}"}
  }
}
```

### 验证

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 有效 JSON | 可解析 | Fatal |
| 服务器名 | 唯一、描述性 | Warning |
| command | stdio 必需 | Severe |
| url | http 必需 | Severe |
| 路径 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe |
| 秘密 | 使用环境变量，不硬编码 | Severe |

---

## LSP 服务器审计

**位置**：`.lsp.json`

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    }
  }
}
```

| 检查 | 规则 | 严重性 |
|------|------|--------|
| command | 必需 | Severe |
| extensionToLanguage | 必需，有效映射 | Severe |
| transport | `stdio` 或 `socket` | Warning |
| 有效 JSON | 可解析 | Fatal |

---

## 常见问题

### 应标记

| 问题 | 严重性 |
|------|--------|
| 缺少 `.claude-plugin/plugin.json` | Fatal |
| plugin.json 不在 `.claude-plugin/` 中 | Fatal |
| 组件在 `.claude-plugin/` 内部 | Fatal |
| 技能未命名为 `SKILL.md` | Fatal |
| hooks.json 缺少包装器 | Severe |
| 硬编码路径 | Severe |
| 引用的组件不存在 | Severe |
| 配置中无效 JSON | Fatal |
| 硬编码秘密 | Severe |
| 无效的工具/事件名 | Severe |

### 不应标记

| 模式 | 原因 |
|------|------|
| 缺少可选组件 | 不是所有插件都需要所有类型 |
| 自定义目录名 | 如配置则有效 |
| 风格变化 | 设计选择 |
| 缺少 README.md | 可选 |
| 不同的组织方式 | 设计选择 |

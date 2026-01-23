# 快速参考

> **目的**：关键信息的精简查阅。完整详情见引用的源文件。

## 内容类型识别

| 标识符 | 类型 | 审计规则文件 |
|--------|------|--------------|
| 单个提示词/文本 | 提示词 | `type-prompt.md` |
| `AGENTS.md` 文件 | 记忆（Codex）| `type-memory.md` |
| `CLAUDE.md` 文件 | 记忆（Claude）| `type-memory.md` |
| `GEMINI.md` 文件 | 记忆（Gemini）| `type-memory.md` |
| 包含 `SKILL.md` 的目录 | 技能 | `type-skill.md` |
| 包含 `.claude-plugin/` 的目录 | 插件 | `type-plugin.md` |
| 记忆文件 + skills/ | 复合系统 | `cross-composite.md` |

---

## 严重性快速指南

| 严重性 | 阈值 | 行动 |
|--------|------|------|
| **Fatal** | 无法执行 | 必须修复 |
| **Severe** | ≥60% 出错 | 应该修复 |
| **Warning** | ≥40% 误解 | 考虑修复 |
| **Info** | 建议 | 可选 |
| **不是问题** | ≤10% 超限 | 忽略 |

---

## 尺寸限制

| 内容 | 限制 | 容差 |
|------|------|------|
| L1 元数据 | ~100 词 | - |
| L2 正文 | 500 行 | +10% OK |
| L3 参考文件 | **无官方限制** | 按内容评估 |
| L4 脚本 | **无限制** | - |
| 记忆文件 | 2000 行 | 最大 3000 |

### 分层阈值（仅 SKILL.md 正文）

> **权威来源**：`SKILL.md` → 原则 4

```
≤500     → 理想
500-550  → OK（不是问题）
550-625  → 仅 Info
>625     → Warning
```

---

## 五点核心验证

> **权威来源**：`methodology-core.md` → 五点核心验证

```
发现问题
    ↓
1. 有具体场景？ → 否 → 放弃
    ↓ 是
2. 在设计范围内？ → 否 → 放弃
    ↓ 是
3. 是功能能力？ → 否 → 放弃
    ↓ 是
4. 是缺陷还是选择？ → 选择 → 放弃
    ↓ 缺陷
5. 达到阈值？ → 否 → 放弃
    ↓ 是
标记为问题
```

---

## 修复优先级

> **权威来源**：`methodology-core.md` → 奥卡姆剃刀

```
1. 删除     ← 首选
2. 合并
3. 重组
4. 修改
5. 添加     ← 最后手段
```

---

## 加载层级

| 层级 | 内容 | 时机 | 限制 |
|------|------|------|------|
| L1 | 元数据 | 始终 | ~100 词 |
| L2 | 正文 | 触发时 | <500 行 |
| L3 | 参考文件 | 按需 | 无官方限制 |
| L4 | 脚本 | 运行时 | 无限制 |

---

## 常用模式

### 有效的工具名

```yaml
# 单个
allowed-tools: Read

# 多个（字符串）
allowed-tools: Read, Write, Edit

# 多个（数组）
allowed-tools: [Read, Write, Bash(git:*)]

# MCP
allowed-tools: ["mcp__server__tool"]
```

### 路径变量

| 变量 | 用途 |
|------|------|
| `${CLAUDE_PLUGIN_ROOT}` | 插件路径 |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录 |

### 钩子包装器（插件）

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

---

## AI 能力模型

### AI 可推断

- 常见同义词
- 标准术语
- 常规模式
- JSON、markdown 语法
- 错误处理模式

### AI 不可推断

- 3+ 步推理链
- 领域特定术语
- 项目约定
- 反直觉要求

---

## 不应标记

| 类别 | 示例 |
|------|------|
| **尺寸** | ≤10% 超限 |
| **许可证** | 版权声明 |
| **设计** | 有效的替代方案 |
| **AI 已知** | 标准概念 |
| **可选** | 缺失的可选字段 |

---

## 关键文件要求

### SKILL.md

```yaml
---
name: 必需，≤64 字符
description: 必需，包含触发条件
---
```

### plugin.json

```json
{
  "name": "required-kebab-case"
}
```

### hooks.json（插件）

```json
{
  "hooks": { ... }
}
```

---

## BCP 47 语言标签

| 正确 | 错误 |
|------|------|
| `en-US` | `en`、`english` |
| `zh-CN` | `zh`、`chinese` |
| `zh-TW` | `zh-tw` |
| `ja-JP` | `ja`、`japanese` |

---

## 参考文档

### 官方来源

| 平台 | 仓库 |
|------|------|
| Claude Code | github.com/anthropics/claude-code |
| Codex CLI | github.com/openai/codex/tree/main/codex-cli |
| Gemini CLI | github.com/google-gemini/gemini-cli |

### 文档

| 资源 | URL |
|------|-----|
| Claude Code 文档 | docs.anthropic.com/en/docs/claude-code |
| OpenAI Cookbook | github.com/openai/openai-cookbook |
| Google AI | ai.google.dev/docs |

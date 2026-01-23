# Codex CLI Skills 标准

> **来源**：[Agent Skills Specification](https://agentskills.io/specification)
> **何时读取**：审计技能（包含 SKILL.md 的目录）和包含技能的插件
> **适用于**：技能目录结构、SKILL.md 格式、frontmatter、正文、参考文件、脚本

## 目录

- [目录结构](#目录结构)
- [SKILL.md 格式](#skillmd-格式)
- [Frontmatter 规范](#frontmatter-规范)
- [正文内容](#正文内容)
- [渐进加载](#渐进加载)
- [可选目录](#可选目录)
- [命名约定](#命名约定)
- [审计检查清单](#审计检查清单)

---

## 目录结构

### 标准布局

```
skill-name/
├── SKILL.md           # 必需 - 主技能定义
├── scripts/           # 可选 - 可执行代码
├── references/        # 可选 - 附加文档
└── assets/            # 可选 - 静态资源
```

### 审计检查

| 检查 | 要求 | 严重性 |
|------|------|--------|
| SKILL.md 存在 | 技能根目录必需 | Fatal |
| SKILL.md 文件名完全匹配 | 区分大小写，必须是 `SKILL.md` | Fatal |
| 目录名匹配 `name` 字段 | 必须完全相同 | Severe |
| 无多余必需文件 | README.md、CHANGELOG.md 可选 | Info |
| 使用标准目录 | scripts/、references/、assets/ | Info |

---

## SKILL.md 格式

### 结构

```yaml
---
# YAML frontmatter（必需）
name: skill-name
description: 此技能的功能和使用时机。
---

# Markdown 正文（必需）
指令和内容在此处。
```

### 审计检查

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 有 YAML frontmatter | 存在 `---` 分隔符 | Fatal |
| 有 Markdown 正文 | frontmatter 后有内容 | Severe |
| YAML 语法有效 | 可无错误解析 | Fatal |
| Markdown 有效 | 格式正确 | Warning |

---

## Frontmatter 规范

### 必需字段

#### `name`（必需）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 长度 | 1-64 字符 | Severe |
| 字符 | 仅小写字母数字和连字符（`a-z`、`0-9`、`-`）| Severe |
| 开头/结尾 | 不能以 `-` 开头或结尾 | Severe |
| 连续 | 不能包含 `--` | Severe |
| 匹配目录 | 必须与父目录名匹配 | Severe |

**有效示例**：
```yaml
name: pdf-processing
name: data-analysis
name: code-review
name: my-skill-v2
```

**无效示例**：
```yaml
name: PDF-Processing      # 不允许大写
name: -pdf                # 不能以连字符开头
name: pdf-                # 不能以连字符结尾
name: pdf--processing     # 不允许连续连字符
name: pdf_processing      # 不允许下划线
name: pdf processing      # 不允许空格
```

#### `description`（必需）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 长度 | 1-1024 字符 | Severe |
| 非空 | 必须有内容 | Severe |
| 触发条件 | 应包含何时使用 | Severe |
| 关键词 | 应包含供代理识别的具体关键词 | Warning |

**好的模式**：
```yaml
description: |
  从 PDF 文件中提取文本和表格，填写 PDF 表单，合并多个 PDF。
  在处理 PDF 文档或用户提及 PDF、表单或文档提取时使用。
  触发词："pdf"、"提取文本"、"填写表单"、"合并文档"。
```

**差的模式**：
```yaml
description: 帮助处理 PDF。                    # 太模糊
description: 用于处理文档的技能。              # 无触发条件
```

**审计检查**：

| 检查 | 严重性 | 通过标准 |
|------|--------|----------|
| 有描述 | 缺失则 Severe | 描述字段非空 |
| ≤1024 字符 | 超出则 Severe | 字符计数（非字节数）|
| 有触发条件 | 缺失则 Severe | "何时使用"、"触发词"或具体关键词 |
| 具体关键词 | 缺失则 Warning | 具体的触发短语 |

### 可选字段

#### `license`（可选）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 格式 | 许可证名称或文件引用 | Info |
| 简洁 | 保持简短 | Info |

**示例**：
```yaml
license: MIT
license: Apache-2.0
license: Proprietary. See LICENSE.txt
```

#### `compatibility`（可选）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 长度 | 如提供则 1-500 字符 | Warning |
| 内容 | 仅环境要求 | Info |

**示例**：
```yaml
compatibility: 为 Claude Code（或类似产品）设计
compatibility: 需要 git、docker、jq 和互联网访问
compatibility: Python 3.9+、Node.js 18+
```

#### `metadata`（可选）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 格式 | 字符串键到字符串值的映射 | Warning |
| 键 | 合理唯一以避免冲突 | Info |

**示例**：
```yaml
metadata:
  author: example-org
  version: "1.0"
  category: document-processing
  tags: ["pdf", "extraction", "forms"]
```

#### `allowed-tools`（可选）

| 约束 | 要求 | 严重性 |
|------|------|--------|
| 格式 | 空格分隔的列表 | Warning |
| 内容 | 有效的工具名 | Warning |

**示例**：
```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
allowed-tools: Read Write Glob Grep WebFetch
```

---

## 正文内容

### 尺寸限制

| 范围 | 状态 | 严重性 |
|------|------|--------|
| ≤500 行 | 理想 | - |
| 500-550（≤10% 超出）| 可接受 | **不是问题** |
| 550-625（10-25% 超出）| 需审查 | Info |
| >625 行 | 应优化 | Warning |

### 推荐章节

| 章节 | 目的 | 必需 |
|------|------|------|
| 概述/介绍 | 技能功能说明 | 推荐 |
| 指令 | 分步指导 | 推荐 |
| 示例 | 输入/输出示例 | 推荐 |
| 边缘情况 | 常见问题和处理 | 可选 |
| 参考文件 | 何时读取每个参考文件 | 如有参考文件则推荐 |

### 内容质量

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 清晰指令 | 具体、可操作 | Warning |
| 不模糊 | 无"做好"类型的指令 | Warning |
| 提供示例 | 用于复杂任务 | Info |
| 参考指导 | 每个参考文件有"何时读取" | Warning |

### 审计检查

| 检查 | 严重性 | 通过标准 |
|------|--------|----------|
| 正文 ≤500 行 | >625 则 Warning | 行数检查 |
| 有指令 | 缺失则 Severe | 存在可操作内容 |
| 不模糊 | 模糊则 Warning | 具体指令 |
| 参考指导 | 缺失则 Warning | 参考文件有"何时读取" |

---

## 渐进加载

### 加载层级

| 层级 | 内容 | Token 预算 | 加载时机 |
|------|------|------------|----------|
| L1 元数据 | `name`、`description` | ~100 token | 启动时（所有技能）|
| L2 指令 | SKILL.md 正文 | 推荐 <5000 token | 技能激活时 |
| L3 资源 | references/、assets/ | 按需 | 按需 |
| L4 脚本 | scripts/ | 仅运行时 | 执行时 |

### 内容放置

| 内容类型 | 正确层级 | 放错时严重性 |
|----------|----------|--------------|
| 触发条件 | L1（描述）| Severe |
| 核心工作流 | L2（正文）| Severe |
| 边缘情况 | L3（参考文件）| Warning |
| 详细规格 | L3（参考文件）| Info |
| 可执行代码 | L4（脚本）| Info |

### 反模式

| 反模式 | 问题 | 严重性 |
|--------|------|--------|
| 元数据膨胀 | L1 >100 词 | Warning |
| 单体正文 | L2 >625 行 | Warning |
| 核心在 L3 | 核心工作流在参考文件中 | Severe |
| 触发在正文 | 触发条件不在描述中 | Severe |

### 审计检查

| 检查 | 严重性 | 通过标准 |
|------|--------|----------|
| L1 ≤100 词 | 超出则 Warning | frontmatter 词数 |
| L2 ≤500 行 | >625 则 Warning | 正文行数 |
| 触发在 L1 | 仅在正文则 Severe | 描述有触发条件 |
| 核心在 L2 | 在 L3 则 Severe | 主工作流在正文中 |

---

## 可选目录

### `scripts/`

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 自包含 | 或清晰记录依赖 | Warning |
| 错误处理 | 有帮助的错误消息 | Warning |
| 边缘情况 | 优雅处理 | Info |
| Shebang | `#!/usr/bin/env python3` 或 `#!/bin/bash` | Warning |

### `references/`

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 聚焦文件 | 保持单个文件聚焦 | Info |
| "何时读取" | 每个文件有加载指导 | Warning |
| 一级深度 | 无深层嵌套链 | Warning |
| 无重复 | 不与正文重复 | Info |

### `assets/`

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 静态资源 | 模板、图片、数据文件 | Info |
| 适当内容 | 非可执行代码 | Info |

---

## 命名约定

### 目录和文件名

| 元素 | 约定 | 严重性 |
|------|------|--------|
| 技能目录 | kebab-case，匹配 `name` | Severe |
| 文件 | kebab-case（SKILL.md 除外）| Warning |
| 无空格 | 使用连字符代替 | Severe |
| 无特殊字符 | 仅字母、数字、连字符 | Severe |

### 有效示例

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── extract-data.py
│   └── process-files.sh
├── references/
│   ├── api-reference.md
│   └── error-codes.md
└── assets/
    └── template.json
```

### 无效示例

```
My Skill/              # 不允许空格
my_skill/              # 不允许下划线
MySkill/               # 不允许大写
my-skill/
├── skill.md           # 必须是 SKILL.md
├── Scripts/           # 不允许大写
└── my script.py       # 不允许空格
```

---

## 审计检查清单

### Fatal 问题

- [ ] SKILL.md 存在于技能根目录
- [ ] SKILL.md 文件名完全匹配（区分大小写）
- [ ] YAML frontmatter 语法有效
- [ ] `name` 字段存在
- [ ] `description` 字段存在

### Severe 问题（必须修复）

- [ ] `name` ≤64 字符
- [ ] `name` 仅小写字母数字和连字符
- [ ] `name` 匹配父目录
- [ ] `description` ≤1024 字符
- [ ] `description` 包含触发条件
- [ ] 触发条件在描述中（不仅在正文）
- [ ] 核心工作流在正文中（不仅在参考文件）
- [ ] 目录名匹配 `name` 字段

### Warning（应该修复）

- [ ] 正文 ≤625 行（理想 ≤500）
- [ ] `compatibility` 如提供则 ≤500 字符
- [ ] 参考文件有"何时读取"指导
- [ ] 脚本有 shebang 和错误处理
- [ ] 文件和目录使用 kebab-case 命名
- [ ] 名称中无空格或特殊字符
- [ ] 描述中有具体关键词

### Info（可选）

- [ ] 存在 `license` 字段
- [ ] 有 author/version 的 `metadata` 字段
- [ ] 如适用有 `allowed-tools` 字段
- [ ] 标准目录结构（scripts/、references/、assets/）
- [ ] 正文中有示例
- [ ] 长文件（>100 行）有目录

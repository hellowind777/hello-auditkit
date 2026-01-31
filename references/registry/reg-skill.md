# Skill特定检查项注册表

> **唯一权威定义**：所有Skill特定检查项在此定义，其他文件只能引用ID。
> **适用范围**：S = Skill

## 检查项列表

### 目录结构 (K-0xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-001 | SKILL.md存在 | Skill根目录必须有 | Fatal | S |
| K-002 | 文件名完全是 `SKILL.md` | 大小写敏感 | Fatal | S |
| K-003 | 目录结构 | scripts/, references/, assets/ 如使用 | Info | S |
| K-004 | 无多余文件 | 无 README.md, CHANGELOG.md | Warning | S |
| K-005 | 所有引用可访问 | 文件存在且可读 | Severe | S |
| K-006 | 引用深度 | 一层深 (无嵌套引用) | Warning | S |

### Frontmatter - name字段 (K-1xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-101 | name存在 | 必需字段 | Fatal | S |
| K-102 | name长度 | ≤64字符 (字符数，非字节) | Severe | S |
| K-103 | name字符 | 仅小写字母、数字、连字符 (`a-z`, `0-9`, `-`) | Severe | S |
| K-104 | name开头/结尾 | 不能以 `-` 开头或结尾 | Severe | S |
| K-105 | name连续连字符 | 不能包含 `--` | Severe | S |
| K-106 | name匹配目录 | 必须完全匹配父目录名 | Severe | S |

### Frontmatter - description字段 (K-2xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-201 | description存在 | 必需字段 | Fatal | S |
| K-202 | description长度 | ≤1024字符 (≤500推荐) | Severe | S |
| K-203 | 触发条件 | 必须包含何时使用此skill | Severe | S |
| K-204 | 关键词 | 应包含具体触发短语 | Warning | S |

### Frontmatter - 可选字段 (K-3xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-301 | license | 许可证名称或文件引用 | Info | S |
| K-302 | compatibility | ≤500字符，环境要求 | Warning | S |
| K-303 | metadata | 字符串键到字符串值的映射 | Warning | S |
| K-304 | allowed-tools | 空格分隔的有效工具名列表 | Warning | S |

### 正文验证 (K-4xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-401 | 正文 ≤500行 | 理想 | - | S |
| K-402 | 正文 500-550行 | 可接受 | 不是问题 | S |
| K-403 | 正文 550-625行 | 可接受 | Info | S |
| K-404 | 正文 >625行 | 应优化 | Warning | S |

### 脚本验证 (K-5xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-501 | 声明的脚本存在 | 所有声明的脚本存在 | Severe | S |
| K-502 | 未声明脚本 | 文档化或说明 | Info | S |
| K-503 | 函数合并检查 | 检查功能是否合并到其他脚本 | - | S |
| K-504 | 描述匹配代码 | 读源码，验证功能 | Severe | S |
| K-505 | 主要功能已文档化 | 所有导出函数 | Warning | S |
| K-506 | 导入目标存在 | 所有导入的模块存在 | Fatal | S |
| K-507 | 外部包列出 | 在requirements中列出 | Severe | S |
| K-508 | 无循环导入 | 无循环 | Severe | S |

### Shell脚本 (K-6xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-601 | Shebang行 | `#!/bin/bash` 或 `#!/usr/bin/env bash` | Warning | S |
| K-602 | 错误处理 | `set -euo pipefail` | Warning | S |
| K-603 | 变量引用 | 所有变量引用 | Warning | S |
| K-604 | 退出码 | 适当的退出码 | Info | S |

### Python脚本 (K-7xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-701 | Shebang | `#!/usr/bin/env python3` | Warning | S |
| K-702 | 错误处理 | 关键操作有 try/except | Warning | S |
| K-703 | 具体异常 | 无裸 `except:` | Warning | S |
| K-704 | 无硬编码密钥 | 使用环境变量 | Severe | S |
| K-705 | 路径遍历 | 清理文件路径 | Severe | S |

### 引用验证 (K-8xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| K-801 | SKILL.md中引用 | 有清晰的"何时读取"说明 | Warning | S |
| K-802 | 无重复 | 未在SKILL.md正文中重复 | Info | S |
| K-803 | 大文件有TOC | >100行的文件有TOC | Info | S |
| K-804 | 一层深 | 无嵌套引用 | Warning | S |

## 执行方法

```
1. 验证目录结构：SKILL.md、目录、引用深度
2. 验证Frontmatter：name、description、可选字段
3. 验证正文：行数、内容质量
4. 验证脚本：存在性、完整性、安全性
5. 验证引用："何时读取"、无重复
6. 输出：「Skill检查: 结构N问题; Frontmatter M问题; 脚本K问题; 引用L问题」
```

## 不应标记的情况

| 模式 | 原因 |
|------|------|
| 正文 500-625行 | 可接受范围 |
| 使用 references/ 目录 | 良好实践 |
| 缺少可选字段 (license, metadata) | 可选 |
| 脚本文件长度 | 脚本无限制 |
| 引用文件长度 | 无官方限制 |

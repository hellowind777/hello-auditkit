# Plugin特定检查项注册表

> **唯一权威定义**：所有Plugin特定检查项在此定义，其他文件只能引用ID。
> **适用范围**：P = Plugin

## 检查项列表

### 插件结构 (G-0xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-001 | Manifest位置 | `plugin.json` 在 `.claude-plugin/` 中 | Fatal | P |
| G-002 | 组件目录位置 | 在插件根目录，不在 `.claude-plugin/` 中 | Fatal | P |
| G-003 | Skill文件命名 | 完全是 `SKILL.md` (大小写敏感) | Fatal | P |
| G-004 | Command/Agent格式 | `.md` 文件带YAML frontmatter | Severe | P |
| G-005 | Hooks格式 | 包装器 `{"hooks": {...}}` | Severe | P |
| G-006 | 路径引用 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe | P |
| G-007 | 命名 | 所有名称使用 kebab-case | Warning | P |

### plugin.json验证 (G-1xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-101 | name字段 | 必需、非空、kebab-case | Fatal | P |
| G-102 | name长度 | ≤50字符 | Warning | P |
| G-103 | version格式 | Semver格式 (X.Y.Z) | Warning | P |
| G-104 | description长度 | ≤200字符 | Warning | P |
| G-105 | 自定义路径 | 相对路径，以 `./` 开头 | Severe | P |

### Commands验证 (G-2xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-201 | description | 推荐，≤100字符 | Info | P |
| G-202 | allowed-tools | 有效工具名 | Severe | P |
| G-203 | model | `sonnet`, `opus`, `haiku` | Severe | P |
| G-204 | 内容规则 | 给Claude的指令，非给用户的消息 | Severe | P |
| G-205 | 清晰任务 | 具体、可操作的指令 | Severe | P |
| G-206 | 详尽约束 | 指定输出长度 | Warning | P |
| G-207 | 范围边界 | 说明不做什么 | Warning | P |

### Agents验证 (G-3xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-301 | name必需 | 必需字段 | Severe | P |
| G-302 | name格式 | kebab-case，≤50字符 | Severe | P |
| G-303 | description必需 | 必需字段 | Severe | P |
| G-304 | description内容 | 包含何时使用，≤500字符 | Severe | P |
| G-305 | tools | 有效工具名 | Warning | P |
| G-306 | model | `inherit`, `sonnet`, `opus`, `haiku` | Warning | P |
| G-307 | 清晰角色 | 具体的agent用途 | Severe | P |
| G-308 | 触发条件 | 在description中，非body中 | Severe | P |

### Hooks验证 (G-4xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-401 | 包装器格式 | 必须用 `{"hooks": {...}}` | Severe | P |
| G-402 | 事件名有效 | PreToolUse, PostToolUse, Stop等 | Severe | P |
| G-403 | Matcher模式 | 有效的正则或工具名 | Warning | P |
| G-404 | Hook类型 | `command`, `prompt`, `agent` | Severe | P |
| G-405 | 脚本Shebang | 存在 | Warning | P |
| G-406 | 脚本输入 | 从stdin读取JSON | Severe | P |
| G-407 | 脚本输出 | 有效JSON到stdout | Severe | P |
| G-408 | 脚本退出码 | 0=成功, 2=阻止 | Warning | P |
| G-409 | 脚本路径 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe | P |

### MCP Servers验证 (G-5xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-501 | 有效JSON | 可解析 | Fatal | P |
| G-502 | Server名称 | 唯一、描述性 | Warning | P |
| G-503 | stdio: command | stdio必需 | Severe | P |
| G-504 | http: url | http必需 | Severe | P |
| G-505 | 路径 | 使用 `${CLAUDE_PLUGIN_ROOT}` | Severe | P |
| G-506 | 密钥 | 使用环境变量，非硬编码 | Severe | P |

### LSP Servers验证 (G-6xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-601 | command | 必需 | Severe | P |
| G-602 | extensionToLanguage | 必需，有效映射 | Severe | P |
| G-603 | transport | `stdio` 或 `socket` | Warning | P |
| G-604 | 有效JSON | 可解析 | Fatal | P |

### 路径变量 (G-7xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| G-701 | 使用CLAUDE_PLUGIN_ROOT | 插件目录 | Severe | P |
| G-702 | 使用CLAUDE_PROJECT_DIR | 项目根目录 | Info | P |
| G-703 | 使用CLAUDE_ENV_FILE | Env文件路径 (SessionStart hooks) | Info | P |
| G-704 | 无硬编码绝对路径 | 不用 `/Users/name/...` | Severe | P |
| G-705 | 无工作目录相对路径 | 不从工作目录相对 | Severe | P |
| G-706 | 无Home快捷方式 | 不用 `~/plugins/...` | Severe | P |

## 执行方法

```
1. 验证插件结构：manifest位置、组件位置
2. 验证plugin.json：必需字段、格式
3. 验证各组件：Commands、Agents、Hooks、MCP、LSP
4. 检查路径：变量使用、无硬编码
5. 输出：「Plugin检查: 结构N问题; Manifest M问题; Commands K问题; Agents L问题; Hooks J问题」
```

## 不应标记的情况

| 模式 | 原因 |
|------|------|
| 缺少可选组件 | 非所有插件都需要所有类型 |
| 自定义目录名 | 如已配置则有效 |
| 样式变化 | 设计选择 |
| 缺少README.md | 可选 |

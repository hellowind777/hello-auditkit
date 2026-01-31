# 命名检查项注册表

> **唯一权威定义**：所有命名相关检查项在此定义，其他文件只能引用ID。
> **适用范围**：ALL = 所有类型 | S = Skill | P = Plugin | M = Memory

## 检查项列表

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| N-001 | 命名风格一致 | 全文使用统一命名规范 (kebab-case/snake_case/camelCase) | Warning | ALL |
| N-002 | kebab-case标识符 | 文件名、目录名使用 kebab-case | Warning | S,P |
| N-003 | 无空格特殊字符 | 标识符只用字母、数字、连字符 | Severe | ALL |
| N-004 | 描述性命名 | 名称能反映内容或用途 | Warning | ALL |
| N-005 | 无重复名称 | 同一范围内标识符唯一 | Severe | ALL |
| N-006 | SKILL.md大小写 | 必须是 SKILL.md，不是 skill.md 或 Skill.md | Fatal | S |
| N-007 | 目录名匹配name | 目录名必须与 frontmatter.name 一致 | Severe | S |
| N-008 | 无跨文件命名冲突 | 不同文件中相同名称必须表示相同含义 | Severe | S,P |
| N-009 | 无保留字覆盖 | 自定义名称不能覆盖系统保留名称 (Read, Write, Edit 等) | Warning | ALL |
| N-010 | 命令名唯一 | 命令名和别名不能冲突 | Severe | P |
| N-011 | Agent名称规范 | Agent name 使用 kebab-case，≤50字符 | Severe | P |
| N-012 | Hook事件名有效 | Hook event 必须是有效事件名 | Severe | P |
| N-013 | MCP服务器名唯一 | MCP server name 在配置中唯一 | Warning | P |
| N-014 | 标签名规范 | XML标签使用 snake_case，无空格 | Warning | ALL |
| N-015 | 变量名一致 | 同一变量/占位符名称表示同一含义 | Warning | ALL |

## 执行方法

```
1. 提取所有标识符：文件名、目录名、变量名、标签名、命令名
2. 检查命名规范：是否符合 kebab-case/指定规范
3. 检查唯一性：同范围内是否有重复
4. 检查冲突：跨文件/跨范围是否有命名冲突
5. 输出：「命名检查: N个标识符, M个问题」
```

## 常见问题模式

| 模式 | 示例 | 问题 |
|------|------|------|
| 大小写不一致 | `MyFile.md` vs `myfile.md` | 跨平台问题 |
| 空格使用 | `my file.md` | 路径处理困难 |
| 保留字覆盖 | 自定义 `Read` 命令 | 与系统冲突 |
| 跨文件冲突 | 两文件中 `config` 含义不同 | 歧义 |

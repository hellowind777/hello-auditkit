# 引用完整性检查项注册表

> **唯一权威定义**：所有引用完整性检查项在此定义，其他文件只能引用ID。
> **适用范围**：ALL = 所有类型 | S = Skill | P = Plugin | M = Memory

## 检查项列表

### 引用检测 (R-0xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| R-001 | 导入引用检测 | 检测 `@file`, `@path/file` | - | ALL |
| R-002 | Markdown链接检测 | 检测 `[text](path)`, `[text](path#anchor)` | - | ALL |
| R-003 | 锚点链接检测 | 检测 `#section-name` | - | ALL |
| R-004 | 编号引用检测 | 检测 `R1`, `Step 2`, `Section 1.1` | - | ALL |
| R-005 | 跨文件引用检测 | 检测 `file.md#section` | - | ALL |
| R-006 | 相对路径检测 | 检测 `./path`, `../path` | - | ALL |
| R-007 | 隐式文本引用检测 | 检测 `see xxx`, `refer to xxx` | - | ALL |
| R-008 | 变量引用检测 | 检测 `{var}`, `{{path}}` | - | ALL |

### 引用准确性 (R-1xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| R-101 | 命名引用存在 | 所有 `@file`, `skill-name` 存在 | Severe | ALL |
| R-102 | 编号引用存在 | 所有 R1、Step 2 等已定义 | Severe | ALL |
| R-103 | 锚点链接有效 | `#section-name` 可解析 (大小写不敏感，kebab-case 标准化) | Severe | ALL |
| R-104 | 跨文件引用有效 | 引用的其他文件存在 | Severe | ALL |
| R-105 | 相对路径解析 | `./path`, `../path` 正确解析 | Severe | ALL |
| R-106 | Markdown链接有效 | `[text](path)` 目标存在 | Severe | ALL |
| R-107 | 无孤立引用 | 无未定义引用 | Warning | ALL |
| R-108 | 变量引用已定义 | 所有 `{var}` 有定义 | Severe | S,P |
| R-109 | 隐式引用存在 | 文本引用 ("see X") 有目标 | Severe | ALL |

### 锚点验证 (R-2xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| R-201 | 大小写标准化 | `#My-Section` 应匹配 `## My Section` | Severe | ALL |
| R-202 | 特殊字符移除 | `#api-config` 应匹配 `## API & Config` | Severe | ALL |
| R-203 | 空格转连字符 | `#my-section` 应匹配 `## My Section` | Severe | ALL |
| R-204 | 文件名大小写 | 文件名大小写在大小写敏感系统上匹配 | Warning | ALL |

### 引用一致性 (R-3xx)

| ID | 检查项 | 要求 | 严重性 | 适用 |
|----|--------|------|--------|------|
| R-301 | 同引用同格式 | 引用风格一致 | Warning | ALL |
| R-302 | 双向完整性 | 如果 A 引用 B，B 应引用 A (如需要) | Info | S,P |
| R-303 | 无循环引用 | 无 A→B→C→A 模式 | Fatal | ALL |
| R-304 | 无冲突引用 | 同名 ≠ 不同目标 | Severe | ALL |

## 执行方法

```
1. 检测所有引用：按上述模式提取
2. 验证存在性：每个引用目标是否存在
3. 验证锚点：大小写和特殊字符标准化
4. 检查一致性：格式、双向、循环
5. 输出：「引用检查: N个引用, M个断链, K个循环」
```

## 常见断链模式

| 模式 | 示例 | 问题 |
|------|------|------|
| 锚点大小写不匹配 | `#My-Section` vs `## my section` | 大小写未标准化 |
| 缺少扩展名 | `see rules` vs `rules.md` | 扩展名省略 |
| 相对路径错误 | `../wrong/path.md` | 路径无法解析 |
| 文件重命名/移动 | `old-name.md` | 文件已重命名 |
| 拼写错误 | `refrence.md` | 拼写错误 |
| 过时编号引用 | `see R5` | R5 已删除 |

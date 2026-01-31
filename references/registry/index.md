# 检查项注册表索引

> **用途**：所有检查项的唯一权威定义位置索引。
> **执行时**：按类型执行清单 (checklists/*.md) 中引用的ID加载对应注册表。

## 注册表文件列表

| 文件 | 前缀 | 检查项数 | 描述 |
|------|------|----------|------|
| `reg-naming.md` | N-xxx | 15 | 命名相关检查 |
| `reg-numbering.md` | B-xxx | 8 | 编号相关检查 |
| `reg-reference.md` | R-xxx | 25 | 引用完整性检查 |
| `reg-structure.md` | S-xxx | 34 | 结构完整性检查 |
| `reg-prompt.md` | P-xxx | 46 | Prompt质量检查 |
| `reg-security.md` | X-xxx | 20 | 安全与合规检查 |
| `reg-runtime.md` | T-xxx | 43 | 运行时行为检查 |
| `reg-format.md` | F-xxx | 38 | 格式与编码检查 |
| `reg-language.md` | L-xxx | 15 | 语言表达检查 |
| `reg-skill.md` | K-xxx | 45 | Skill特定检查 |
| `reg-plugin.md` | G-xxx | 52 | Plugin特定检查 |

**总计**：约 341 个唯一检查项

## ID前缀分配

| 前缀 | 类别 | 适用范围 |
|------|------|----------|
| N | Naming (命名) | ALL |
| B | numBering (编号) | ALL |
| R | Reference (引用) | ALL |
| S | Structure (结构) | ALL |
| P | Prompt (提示词质量) | ALL |
| X | Security (安全) | ALL |
| T | runTime (运行时) | S,P |
| F | Format (格式) | ALL |
| L | Language (语言) | ALL |
| K | sKill (Skill特定) | S |
| G | pluGin (Plugin特定) | P |

## 使用方式

### 审计时

1. 确定内容类型 (Prompt/Memory/Skill/Plugin/Composite)
2. 加载对应类型执行清单 (`checklists/checklist-{type}.md`)
3. 按清单中的ID列表加载所需注册表
4. 执行检查，记录结果

### 报告时

按注册表分类输出执行结果：

```
## 执行证据

### 命名检查 (N-xxx)
| ID | 检查项 | 结果 | 证据 |
|----|--------|------|------|
| N-001 | 命名风格一致 | ✅ PASS | 全文使用 kebab-case |
| N-003 | 无空格特殊字符 | ❌ FAIL | line 45: `my file.md` |

### 引用检查 (R-xxx)
...
```

## 维护规则

1. **唯一定义**：每个检查项只在一个注册表中定义
2. **ID不重复**：同前缀ID全局唯一
3. **引用而非复制**：其他文件只引用ID，不复制规则内容
4. **版本控制**：修改检查项时更新版本号

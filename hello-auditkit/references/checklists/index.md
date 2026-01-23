# 类型执行清单索引

> **用途**：根据内容类型选择对应的执行清单。
> **执行时**：检测内容类型后，加载对应清单执行审计。

## 清单文件列表

| 内容类型 | 清单文件 | 识别方式 |
|----------|----------|----------|
| Prompt | `checklist-prompt.md` | 粘贴文本、任意文件（非特定类型） |
| Memory | `checklist-memory.md` | AGENTS.md, CLAUDE.md, GEMINI.md |
| Skill | `checklist-skill.md` | 包含 `SKILL.md` 的目录 |
| Plugin | `checklist-plugin.md` | 包含 `.claude-plugin/plugin.json` 的目录 |
| Composite | `checklist-composite.md` | Memory + skills/ 或多组件系统 |

## 内容类型识别流程

```
1. 用户提供输入
   ↓
2. 判断输入类型
   ├── 粘贴文本 → Prompt
   ├── 单文件
   │   ├── AGENTS.md / CLAUDE.md / GEMINI.md → Memory
   │   └── 其他文件 → Prompt
   └── 目录
       ├── 包含 .claude-plugin/plugin.json → Plugin
       ├── 包含 SKILL.md → Skill
       ├── 包含 Memory + skills/ → Composite
       └── 其他 → 扫描内部组件
```

## 执行方式

### 单组件审计

1. 识别内容类型
2. 加载对应清单
3. 按清单中的ID列表加载注册表
4. 执行所有必须检查项
5. 按条件执行可选检查项
6. 输出执行证据

### 多组件审计 (Composite)

1. 扫描目录，识别所有组件
2. 对每个组件执行对应清单
3. 执行跨组件检查
4. 汇总输出

## 检查项总数统计

| 清单 | 必须检查 | 条件检查 | 总计 |
|------|----------|----------|------|
| Prompt | ~31 | ~20 | ~51 |
| Memory | ~39 | ~15 | ~54 |
| Skill | ~81 | ~30 | ~111 |
| Plugin | ~66 | ~60 | ~126 |
| Composite | 全部 + 跨组件 | - | ~150+ |

## 报告输出要求

每个执行清单都指定了输出格式，确保：

1. **按类别分组**：按注册表类别显示结果
2. **执行证据**：每个检查项显示执行状态
3. **问题定位**：问题包含文件:行号引用
4. **严重性分布**：汇总各严重性级别数量

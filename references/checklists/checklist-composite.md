# Composite审计执行清单

> **内容类型**：Composite（多组件系统，如Memory + Skills）
> **执行方式**：按ID加载对应注册表，执行所有列出的检查项

## 执行原则

1. **分层执行**：先按各组件类型执行对应清单，再执行跨组件检查
2. **组件识别**：扫描目录，识别所有组件类型
3. **交叉验证**：验证组件间的一致性和引用完整性

## 第一步：组件识别

扫描目录结构，识别：
- [ ] Memory文件 (AGENTS.md, CLAUDE.md, GEMINI.md)
- [ ] Skills (包含SKILL.md的目录)
- [ ] Plugins (.claude-plugin/plugin.json)
- [ ] 独立Commands/Agents/Hooks
- [ ] 配置文件 (.mcp.json, .lsp.json)

## 第二步：分组件执行

### 对每个Memory文件

执行 `checklist-memory.md`

### 对每个Skill

执行 `checklist-skill.md`

### 对每个Plugin

执行 `checklist-plugin.md`

### 对每个独立Prompt/Command

执行 `checklist-prompt.md`

## 第三步：跨组件检查

### 命名一致性 (reg-naming.md)

| ID | 检查项 | 条件 |
|----|--------|------|
| N-005 | 无重复名称 | 跨所有组件 |
| N-008 | 无跨文件命名冲突 | 总是 |
| N-009 | 无保留字覆盖 | 总是 |

### 引用完整性 (reg-reference.md)

| ID | 检查项 | 条件 |
|----|--------|------|
| R-104 | 跨文件引用有效 | 总是 |
| R-303 | 无循环引用 | 总是 |
| R-304 | 无冲突引用 | 总是 |

### 设计一致性 (reg-structure.md)

| ID | 检查项 | 条件 |
|----|--------|------|
| S-004 | 命名模式一致 | 跨所有组件 |
| S-202 | 无语义重复 | 跨组件规则 |
| S-305 | 无矛盾 | 跨组件规则 |

### 运行时一致性 (reg-runtime.md)

| ID | 检查项 | 条件 |
|----|--------|------|
| T-001 | 同概念同术语 | 跨所有组件 |
| T-101 | 无名称冲突 | 跨所有组件 |
| T-201 | 无矛盾规则 | 跨组件规则 |
| T-202 | 无重叠路由 | 如有多个路由源 |
| T-A05 | 无循环加载 | 跨组件加载 |

### 渐进加载检查 (reg-runtime.md)

| ID | 检查项 | 条件 |
|----|--------|------|
| T-A01 | 核心内容在L1/L2 | 总是 |
| T-A02 | 详细内容在L3 | 总是 |
| T-A03 | 模板引用而非嵌入 | 如有模板 |
| T-A06 | 加载失败有处理 | 如有模块依赖 |

## 第四步：组件间依赖验证

### Memory → Skill 引用

```
检查Memory文件中引用的skill是否存在：
- 所有 @skill-name 引用
- 所有 skills/ 路径引用
```

### Skill → Skill 引用

```
检查Skill间引用是否有效：
- 所有跨skill引用
- 无循环依赖
```

### Plugin → 组件引用

```
检查Plugin中引用的组件是否存在：
- commands/ 中引用的agents
- hooks 中引用的scripts
- skills/ 中的完整性
```

## 执行输出格式

```
Composite审计执行证据:

## 组件审计结果

### Memory文件 (X个)
| 文件 | 问题数 | 严重性分布 |
|------|--------|------------|
| CLAUDE.md | 3 | 1 Severe, 2 Warning |
...

### Skills (X个)
| Skill | 问题数 | 严重性分布 |
|-------|--------|------------|
| my-skill | 2 | 2 Warning |
...

### Plugins (X个)
| Plugin | 问题数 | 严重性分布 |
|--------|--------|------------|
| my-plugin | 5 | 1 Fatal, 2 Severe, 2 Warning |
...

## 跨组件检查结果

### 命名一致性
- 跨组件重复名称: N个
- 命名冲突: M个

### 引用完整性
- 跨组件断链: K个
- 循环引用: L个

### 设计一致性
- 语义重复: J个
- 矛盾规则: H个

### 渐进加载
- 核心内容位置问题: I个
- 加载依赖问题: O个

## 汇总

- 总组件数: X
- 总问题数: Y
- 严重性分布: Fatal Z, Severe W, Warning V, Info U
```

## 常见跨组件问题

| 问题 | 示例 | 严重性 |
|------|------|--------|
| 名称冲突 | Memory和Skill中同名但不同含义 | Severe |
| 断链引用 | Memory引用不存在的skill | Severe |
| 循环依赖 | Skill A → Skill B → Skill A | Fatal |
| 规则矛盾 | Memory说"总是X"，Skill说"从不X" | Fatal |
| 术语不一致 | 同一概念多个名称 | Warning |

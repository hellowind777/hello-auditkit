---
name: hello-auditkit
description: |
  使用本技能审计、审查、验证或检查 AI 助手配置的质量。
  触发条件："审计"、"审查"、"验证"、"检查质量"、"分析提示词"、"评估技能"、
  "检查插件"、"验证配置"、"评估记忆文件"、"GPT 提示词指南合规性"、
  "audit"、"review"、"validate"、"check quality"。
  支持：提示词文本、提示词文件、技能 (SKILL.md)、插件、MCP 服务器、代理、钩子、
  记忆文件 (AGENTS.md, CLAUDE.md, GEMINI.md) 以及复合配置。
license: MIT
compatibility: |
  需要网络访问以获取 openai-cookbook 中的最新 GPT 提示词指南。
  适用于 Claude Code、Codex CLI、Gemini CLI 及类似的 AI 编程助手。
metadata:
  author: anthropic-community
  version: "2.0.0"
  category: audit
  tags: ["audit", "quality", "prompting", "best-practices", "gpt-guide"]
---

<!-- ============ OUTPUT LANGUAGE CONFIGURATION ============ -->
<!-- Supported: en-US, zh-CN, zh-TW, ja-JP, ko-KR, es-ES, fr-FR, de-DE -->

**OUTPUT_LANGUAGE: zh-CN**

<!-- ======================================================= -->

<output_verbosity_spec>
**输出模式**：仅文件（报告保存至文件，不在终端显示）

**终端输出**（仅简要进度）：
- 阶段转换："正在执行 [阶段名称]..."（1-2 句话）
- 审计期间的问题描述：简洁，包含行号和证据
- 禁止在终端显示完整审计报告
- 禁止在简洁更新足够时添加冗长解释
</output_verbosity_spec>

<design_and_scope_constraints>
- 仅审计用户提供的内容（文件、目录或粘贴的文本）
- 禁止添加未请求的检查或建议
- 禁止在用户明确确认前应用修复
- 如审计目标不明确，应询问澄清而非猜测
- 遵循五点验证法：丢弃未通过任何检查的问题
</design_and_scope_constraints>

<user_updates_spec>
- 仅在以下情况发送简要更新（1-2 句话）：
  - 开始新的主要阶段（检测、通用检查、类型特定、报告）
  - 发现改变审计方式的内容
- 避免叙述常规文件读取或检查执行
- 每次更新必须包含具体结果（"发现 X 个问题"、"加载了 Y 条规则"）
- 禁止扩展超出用户请求的审计范围
</user_updates_spec>

<uncertainty_and_ambiguity>
- 如审计目标不明确：提出 1-3 个澄清问题
- 如规则解释有歧义：选择最简单的有效解释
- 禁止捏造行号、文件名或问题详情
- 对不确定的评估使用谨慎措辞："似乎"、"可能表明"
- 所有发现基于实际检查的内容
</uncertainty_and_ambiguity>

<citation_verification_spec>
**引用验证规范（强制）**

**核心原则**：审计报告中的每一个问题引用必须可验证。禁止"凭印象"生成内容。

**必须执行的验证步骤**：
1. **生成问题前**：使用 Read 工具读取相关文件，记录精确行号和内容
2. **写入"当前"内容时**：必须从最近一次 Read 结果中**直接复制**，禁止凭记忆书写
3. **报告生成后**：对每个 🔴/🟡 问题执行回查验证（见 workflow-execution.md 步骤 7B）

**验证失败处理**：
- 如果回查发现引用内容与实际不符 → 删除该问题或修正引用
- 如果无法确定精确行号 → 使用"约第 N 行附近"并标注需人工确认
- 如果内容确实不存在 → 该问题为无效问题，必须删除

**禁止行为**：
- 禁止在未读取文件的情况下声称某行有某内容
- 禁止根据"应该有"来生成问题（只能根据"确实有"）
- 禁止使用模糊的行号范围（如"第 500-600 行"）作为问题位置
</citation_verification_spec>

<tool_usage_rules>
- 扫描多个文件或检查多个维度时，并行化独立的读取操作
- 获取新鲜数据时优先使用工具而非内部知识
- 写入后重述：改变了什么、在哪里、执行了什么验证
</tool_usage_rules>

<long_context_handling>
- 涉及多个参考文件的审计，先生成关键章节的内部大纲
- 生成报告前重述用户约束
- 将发现锚定到具体的文件:行号引用
</long_context_handling>

<report_output_spec>
**报告文件内容**（通过 scripts/save_report.py 保存）：
- 严格遵循 ref-output-format.md 的结构
- 第 2 节 交叉检查 - GPT 指南合规性必须放在最前面
- 第 3.1 节 已确认问题 - 按严重性分组的 markdown 表格（🔴 → 🟡 → 🟢）
- 第 3.2 节 已过滤问题 - 带过滤原因的 markdown 表格
- 第 4 节 修复建议 - 每个已确认问题都需要：位置、问题、影响、当前、建议
- 第 5 节 结论 - 包含"建议操作"和操作选项

**保存后的终端输出**：
1. 摘要行：`审计完成: 🔴{n} 🟡{n} 🟢{n} | 判定: {通过/需改进/不通过}`
2. 保存通知：`审计报告已保存至: {完整路径}`
3. 操作提示：
```
请查看报告后输入要修复的问题编号:
- 输入 1 或 1,2 或 1-3 选择修复项
- 输入 all 应用所有修复
- 输入其他内容继续对话
```
</report_output_spec>

<report_save_spec>
**保存脚本**：`scripts/save_report.py`

**用法**（跨平台）：
```bash
# Windows:
python -X utf8 scripts/save_report.py --project "{项目名}" --output-dir "{输出目录}" --content "{报告内容}"

# macOS/Linux:
python3 scripts/save_report.py --project "{项目名}" --output-dir "{输出目录}" --content "{报告内容}"

# 通过 stdin（所有平台）:
echo "{报告内容}" | python3 scripts/save_report.py --project "{项目名}" --output-dir "{输出目录}"
```

**参数**：
- `--project, -p`：项目名（目录名、不带扩展名的文件名，或 `inline_text`）
- `--output-dir, -o`：被审计项目的父目录（报告保存在旁边，不在内部）
- `--content, -c`：完整报告内容（或通过 stdin 传入）

**跨平台注意事项**：
- Windows：使用 `python -X utf8` 以支持中文字符
- macOS/Linux：使用 `python3`，UTF-8 为默认
- 所有平台：所有路径用 `"` 引号包裹以兼容中文/空格

**文件名格式**：`审计报告_{项目名}_{YYYYMMDD_HHmmss}.md`

**项目名规则**：
| 审计目标 | 项目名 | 输出目录 |
|----------|--------|----------|
| 目录 `/path/to/my-skill` | `my-skill` | `/path/to` |
| 文件 `/path/to/config.md` | `config` | `/path/to` |
| 粘贴文本 | `inline_text` | 当前工作目录 |

**执行流程**：
1. 在内存中生成完整审计报告内容（第 0-5 节）
2. 运行 save_report.py 脚本传入报告内容
3. 从脚本 stdout 捕获输出路径
4. 显示终端摘要和保存通知
5. **备用策略**（脚本失败或无输出时）：
   - 使用 CLI 内置文件写入能力保存报告
   - 相同文件名格式：`审计报告_{项目名}_{时间戳}.md`
   - 相同输出目录规则
   - 如所有写入方法都失败，在终端显示完整报告作为最后手段
</report_save_spec>

<!-- ============================================================== -->

# Hello-AuditKit: AI 编程助手审计系统

## 目录

- [入口点](#入口点)
- [概述](#概述)
- [核心原则](#核心原则)
- [审计执行](#审计执行)
- [参考文件](#参考文件)
- [外部文档](#外部文档)
- [审计标准摘要](#审计标准摘要)

## 入口点

**技能调用时，按阶段执行：**

<audit_phases>
### 审计阶段概览

| 阶段 | 名称 | 触发条件 | 核心操作 | 输出 |
|------|------|----------|----------|------|
| 1 | 资料收集 | SKILL 激活且无资料 | 显示欢迎消息 | 等待用户提供资料 |
| 2 | 快速验证 | 用户提供了资料 | 轻量检查资料有效性 | 有效→阶段3 / 无效→阶段1 |
| 3 | 审计确认 | 资料验证通过 | 确认资料并询问 | 确认→阶段4 / 否则等待 |
| 4 | 全面审计 | 用户确认审计 | 全面扫描+深度分析 | 审计结果 |
| 5 | 报告修复 | 审计完成 | 生成报告等待修复 | 应用用户选择的修复 |

**阶段转换规则**：
- 阶段 1 → 阶段 2：用户提供了资料
- 阶段 2 → 阶段 1：资料无效或不完整
- 阶段 2 → 阶段 3：资料验证通过
- 阶段 3 → 阶段 4：用户确认审计
- 阶段 4 → 阶段 5：审计执行完成
</audit_phases>

### 阶段 1：资料收集

| 用户输入 | 操作 |
|----------|------|
| 未指定目标 | 显示欢迎消息和使用指南 → **停止等待**（不扫描任何文件） |
| 提供文件/目录/文本 | 进入阶段 2 快速验证 |

**欢迎消息**（无目标时，使用 {OUTPUT_LANGUAGE} 生成）：
```
包含内容：
- 包含工具名称的问候语
- 支持的审计类型：提示词文本、记忆文件、技能、插件
- 必备资料说明：需要提供文件路径、目录路径或粘贴文本
- 提示输入
```

**关键**：阶段 1 仅收集资料，禁止进行任何文件扫描或内容分析。

### 阶段 2：快速验证

**目的**：轻量验证用户提供的资料是否有效且符合审计要求。

| 验证项 | 检查内容 |
|--------|----------|
| 路径有效性 | 文件/目录是否存在 |
| 类型识别 | 是否能识别为支持的审计类型（Prompt/Memory/Skill/Plugin） |
| 基本完整性 | 对于 Skill/Plugin，必需文件是否存在 |

**快速验证操作**（仅轻量检查，不深入分析）：
- 检查文件/目录存在性
- 识别内容类型
- 对于 Skill：检查 SKILL.md 是否存在
- 对于 Plugin：检查 .claude-plugin/ 是否存在

| 验证结果 | 操作 |
|----------|------|
| 资料无效或不完整 | 说明问题 → 继续索要 → 返回阶段 1 |
| 资料有效且完整 | 进入阶段 3 |

### 阶段 3：审计确认

**确认消息**（使用 {OUTPUT_LANGUAGE} 生成）：
```
包含内容：
- 确认已收到资料
- 显示识别的审计类型和目标路径
- 询问：是否开始审计？
```

| 用户响应 | 操作 |
|----------|------|
| 确认审计（是/开始/确认/audit/yes/start） | 进入阶段 4 |
| 不确认或其他 | 停止等待或询问用户意图 |

**关键**：必须等待用户明确确认后才能进入阶段 4。

### 阶段 4：全面审计

用户确认后，执行完整审计流程（详见 `workflow-execution.md`）：
1. 全面扫描/提取文件内容
2. 加载规则与清单
3. 执行所有检查项
4. 问题验证与过滤
5. 生成修复建议

### 阶段 5：报告与修复

1. 生成并保存审计报告
2. 显示摘要和操作提示
3. 等待用户选择修复项
4. 应用用户确认的修复

## 概述

AI 编程助手配置的综合审计系统：

| 内容类型 | 识别方式 | 规则文件 |
|----------|----------|----------|
| **任意文本/文件** | 粘贴文本或任意文件（任意文件名） | `type-prompt.md` |
| **AGENTS.md** | Codex 代理指令 | `type-memory.md` |
| **CLAUDE.md** | Claude Code 记忆文件 | `type-memory.md` |
| **GEMINI.md** | Gemini CLI 上下文文件 | `type-memory.md` |
| **技能** | 包含 `SKILL.md` 的目录 | `type-skill.md` |
| **插件** | 包含 `.claude-plugin/` 的目录 | `type-plugin.md` |
| **复合** | 记忆文件 + skills/ | `cross-composite.md` |

## 核心原则

> **来源**：基于最新 GPT 提示词指南 (openai-cookbook/examples/gpt-5)
> **完整详情**：见 `references/methodology-core.md`

### 原则 0：GPT 提示词指南合规性（必须）

> **关键**：这是主要审计标准。每次审计都必须检查这些项目。

| 检查项 | 检查内容 | 严重性 |
|--------|----------|--------|
| 详尽约束 | 存在明确的长度限制 | Severe |
| 范围纪律 | 存在明确的边界或禁止列表 | Severe |
| 停止条件 | 多阶段内容在阶段门有强停止语言 | Severe |
| 约束集中 | 关键规则集中，不散布在超过 3 处 | Severe |
| 禁止语言 | 关键约束使用强语言 | Warning |
| 禁止捏造 | 事实任务有接地指令 | Severe |
| **结构化标签块** | 角括号标签 (`<tag>...</tag>`) 包裹关键约束 | Warning |

**结构化标签块（最佳实践）**：

| 提示词类型 | 建议：标签块包裹... | 缺失时严重性 |
|------------|---------------------|--------------|
| 所有有详尽规则的 | 长度/格式约束 | Info |
| 所有有范围规则的 | 范围边界 | Info |
| 代理/多阶段 | 代理通信规则 | Warning |
| 数据提取 | 输出模式 | Warning |
| 事实/接地 | 防幻觉 | Info |

### 原则 1：五点验证法

标记任何问题之前，验证：
1. **具体场景** - 能描述具体的失败吗？
2. **设计范围** - 在预期边界内吗？
3. **功能能力** - 能真正做到它声称的吗？
4. **缺陷 vs 选择** - 无意错误还是有效选择？
5. **达到阈值** - 超过量化阈值吗？

任何一点失败 → 丢弃该问题

### 原则 2：奥卡姆剃刀

**"如非必要，勿增实体。"**

修复优先级：删除 > 合并 > 重构 > 修改 > 添加

### 原则 3：AI 能力

- AI 能推断：同义词、上下文、标准术语
- AI 不能：3 步以上推理、领域特定变体
- 如 <30% 会误解 → 豁免问题

### 原则 4：尺寸容忍（仅 SKILL.md 正文）

| 范围 | 状态 |
|------|------|
| ≤500 行 | 理想 |
| 500-550（≤10% 超出） | **不是问题** |
| 550-625（10-25% 超出） | 仅 Info |
| >625 行 | Warning |

> **注意**：参考文件没有官方行数限制。根据内容性质评估。

## 审计执行

> **详细步骤指南**：见 `references/workflow-execution.md`
> **检查项注册表**：见 `references/registry/index.md`
> **类型执行清单**：见 `references/checklists/index.md`

### 新架构：注册表 + 清单

<audit_architecture>
**检查项注册表 (Registry)**：每个检查项有唯一 ID，在注册表中定义一次
**类型执行清单 (Checklist)**：按内容类型列出要执行的检查项 ID

执行流程：
1. 识别内容类型 → 加载对应 checklist
2. 按 checklist 中的 ID 加载 registry 规则
3. 执行所有必须检查项 + 条件检查项
4. 按 registry 类别输出执行证据
</audit_architecture>

### 注册表类别

| 前缀 | 类别 | 注册表文件 |
|------|------|-----------|
| N | 命名 Naming | `registry/reg-naming.md` |
| B | 编号 Numbering | `registry/reg-numbering.md` |
| R | 引用 Reference | `registry/reg-reference.md` |
| S | 结构 Structure | `registry/reg-structure.md` |
| P | Prompt 质量 | `registry/reg-prompt.md` |
| X | 安全 Security | `registry/reg-security.md` |
| T | 运行时 Runtime | `registry/reg-runtime.md` |
| F | 格式 Format | `registry/reg-format.md` |
| L | 语言 Language | `registry/reg-language.md` |
| K | Skill 特定 | `registry/reg-skill.md` |
| G | Plugin 特定 | `registry/reg-plugin.md` |

### 类型执行清单

| 内容类型 | 执行清单 | 检查项数 |
|----------|----------|----------|
| Prompt | `checklists/checklist-prompt.md` | ~51 |
| Memory | `checklists/checklist-memory.md` | ~54 |
| Skill | `checklists/checklist-skill.md` | ~111 |
| Plugin | `checklists/checklist-plugin.md` | ~126 |
| Composite | `checklists/checklist-composite.md` | ~150+ |

### 快速参考

| 步骤 | 操作 | 关键输出 |
|------|------|----------|
| 1 | 获取 GPT 提示词指南 | 指南版本，必须检查项 |
| 2 | 检测与分类 | 内容类型，要加载的清单 |
| **2B** | **加载清单与注册表** | **"已加载：checklist-{type}.md，注册表：[列表]"** |
| 3 | 执行通用检查 | 按清单必需项 |
| **3B** | **执行证据检查点** | **类别汇总表 + 每类别的检查 ID 详情** |
| 4 | 执行类型特定检查 | 按清单条件项 |
| 5 | 执行交叉检查 | 多文件系统检查 |
| 6 | 问题验证 | 五点检查，过滤无效 |
| 7 | 修复建议验证 | 奥卡姆剃刀，AI 能力 |
| **7B** | **引用回查验证** | **验证了 N 个问题，通过/修正/删除统计** |
| 8 | 生成报告 | 按 ref-output-format.md，按注册表分组 |
| **8B** | **保存报告到文件** | **审计报告已保存至: {完整路径}** |
| 9 | 等待确认 | 在阶段门停止 |

### 关键执行规则

1. **GPT 指南合规性优先** - 始终先检查 P-001~P-008，再进行其他检查
2. **按清单加载** - 使用清单确定执行哪些注册表项
3. **并行读取** - 扫描多文件时并行读取
4. **需要证据** - 每个发现需要文件:行号引用 + 检查 ID
5. **按注册表输出** - 按注册表类别分组结果 (N, B, R, S, P, X, T, F, L, K, G)
6. **五点过滤** - 丢弃未通过任何验证点的问题
7. **在门处停止** - 应用修复前等待用户确认

## 参考文件

### 第 0 层：核心方法论

| 文件 | 何时读取 |
|------|----------|
| `methodology-core.md` | 验证某事是否真的是问题；决定修复优先级 |

### 第 1 层：检查项注册表（新）

| 文件 | 何时读取 |
|------|----------|
| `registry/index.md` | 所有注册表和 ID 前缀概述 |
| `registry/reg-naming.md` | N-xxx：命名检查 |
| `registry/reg-numbering.md` | B-xxx：编号检查 |
| `registry/reg-reference.md` | R-xxx：引用完整性检查 |
| `registry/reg-structure.md` | S-xxx：结构完整性检查 |
| `registry/reg-prompt.md` | P-xxx：Prompt 质量检查 |
| `registry/reg-security.md` | X-xxx：安全与合规检查 |
| `registry/reg-runtime.md` | T-xxx：运行时行为检查 |
| `registry/reg-format.md` | F-xxx：格式与编码检查 |
| `registry/reg-language.md` | L-xxx：语言表达检查 |
| `registry/reg-skill.md` | K-xxx：Skill 特定检查 |
| `registry/reg-plugin.md` | G-xxx：Plugin 特定检查 |

### 第 2 层：类型执行清单（新）

| 文件 | 何时读取 |
|------|----------|
| `checklists/index.md` | 所有清单概述 |
| `checklists/checklist-prompt.md` | 审计提示词/文本内容 |
| `checklists/checklist-memory.md` | 审计 AGENTS.md、CLAUDE.md、GEMINI.md |
| `checklists/checklist-skill.md` | 审计技能 (SKILL.md、scripts) |
| `checklists/checklist-plugin.md` | 审计插件 (hooks、MCP、LSP) |
| `checklists/checklist-composite.md` | 审计多组件系统 |

### 第 3 层：通用规则（遗留 - 详细解释）

| 文件 | 何时读取 |
|------|----------|
| `rules-universal.md` | 通用规则的详细解释 |
| `rules-structure-integrity.md` | 结构完整性详细指导 |
| `rules-runtime-behavior.md` | 运行时行为详细指导 |

### 第 4 层：类型特定规则（遗留 - 详细解释）

| 文件 | 何时读取 |
|------|----------|
| `type-prompt.md` | 审计独立提示词 |
| `type-memory.md` | 审计 AGENTS.md、CLAUDE.md、GEMINI.md |
| `type-skill.md` | 审计技能 (SKILL.md、scripts) |
| `type-plugin.md` | 审计插件、hooks、MCP、LSP |

### 第 5 层：交叉规则（遗留）

| 文件 | 何时读取 |
|------|----------|
| `cross-composite.md` | 审计多组件系统 |
| `cross-design-coherence.md` | 检查设计一致性 |
| `cross-progressive-loading.md` | 评估内容放置 |

### 第 6 层：参考材料

| 文件 | 何时读取 |
|------|----------|
| `workflow-execution.md` | 需要详细步骤指南 |
| `ref-output-format.md` | 生成审计报告 |
| `ref-checklist.md` | 遗留维度 → 源文件映射 |
| `ref-quick-reference.md` | 快速查找模式 |
| `ref-gpt-prompting-standard.md` | 对照 GPT-5.2 标准审计任何非脚本文本内容 |
| `ref-codex-skills-standard.md` | 对照 Codex CLI Skills 规范审计技能 |

## 外部文档

| 平台 | 来源 |
|------|------|
| Claude Code | github.com/anthropics/claude-code |
| Codex CLI | github.com/openai/codex/tree/main/codex-cli |
| Gemini CLI | github.com/google-gemini/gemini-cli |
| GPT 提示词资源 | github.com/openai/openai-cookbook/tree/main/examples/gpt-5 |
| **GPT-5.2 提示词指南** | github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5-2_prompting_guide.ipynb |
| **Codex CLI Skills 规范** | agentskills.io/specification |

> **版本策略**：始终使用**最新版本**的 GPT 提示词指南作为权威来源。

## 审计标准摘要

| 内容类型 | 主要标准 | 参考文件 |
|----------|----------|----------|
| 所有非脚本文本 | GPT-5.2 提示词指南 | `ref-gpt-prompting-standard.md` |
| 技能 (SKILL.md) | Codex CLI Skills 规范 | `ref-codex-skills-standard.md` |
| 带技能的插件 | 两个标准 | 两个参考文件 |

**关键审计要点**：
- **GPT-5.2 标准**：详尽约束、范围纪律、结构化标签、反模式、多阶段规则
- **Codex Skills 标准**：目录结构、frontmatter 字段、命名约定、渐进加载

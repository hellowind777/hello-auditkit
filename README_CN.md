# Hello-AuditKit

<div align="center">
  <img src="./readme_images/01-hero-banner.svg" alt="Hello-AuditKit" width="720">

  **面向 AI 编码助手配置的证据驱动审计系统（prompts / 记忆文件 / skills / plugins）**

  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
  [![Version](https://img.shields.io/badge/version-2.0.0-orange.svg)](./hello-auditkit/SKILL.md)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/hellowind777/hello-auditkit/pulls)

  [简体中文](./README_CN.md) · [English](./README.md)
</div>

---

## 这个 Skill 审计什么

- **Prompt / 任意文本文件**（可直接粘贴文本，或提供任意文件路径）
- **记忆文件**：`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`
- **技能 Skill**：包含 `SKILL.md` 的目录
- **插件 Plugin**：包含 `.claude-plugin/` 的目录（及相关配置）
- **复合系统**：多文件组合（如 memory + skills/plugins）

## 核心思想（为什么它更“稳”）

- **以 GPT Prompting Guide 合规为主要标准**（优先在线获取最新；离线时回退到内置规则）
- **5 点验证法**：先过滤误报，再把问题写进报告
- **证据驱动**：每个问题必须锚定到 *文件 + 行号*，并做回查验证
- **不自动修复**：只给出建议；必须用户明确确认后才会应用

## 快速开始（Codex CLI）

### 1) 安装

把 `hello-auditkit/` 目录复制到 Codex 的 skills 目录：

```powershell
# Windows (PowerShell)
Copy-Item -Recurse -Force "./hello-auditkit" "$env:USERPROFILE\.codex\skills\"
```

```bash
# macOS/Linux
cp -r ./hello-auditkit ~/.codex/skills/
```

### 2) 使用

在 Codex CLI 中调用并提供要审计的目标：

- 示例：
  - `审计这个文件: ./AGENTS.md`
  - `检查这个技能目录: ./some-skill/`
  - `验证这个插件配置: ./my-plugin/`

### 3) 输出

- 审计报告会**保存到文件**（见 `hello-auditkit/scripts/save_report.py`）。
- 终端只输出**简短进度**（不会刷屏打印完整报告）。

---

## 文档入口

- Skill 入口与规则：`hello-auditkit/SKILL.md`
- 执行工作流：`hello-auditkit/references/workflow-execution.md`
- 注册表（规则 ID）：`hello-auditkit/references/registry/`
- 类型清单：`hello-auditkit/references/checklists/`

## 仓库结构

| 路径 | 用途 |
|------|------|
| `hello-auditkit/SKILL.md` | Skill 定义 + 阶段流程 + 约束 |
| `hello-auditkit/references/` | 方法论、规则、清单、注册表 |
| `hello-auditkit/scripts/save_report.py` | 以标准命名保存审计报告 |
| `hello-auditkit/assets/` | 预留资源目录 |
| `hello-auditkit/output/` | 运行期缓存/输出目录（已忽略，仅保留 `.gitkeep`） |

## 贡献

见 `CONTRIBUTING.md`。

## 许可证

MIT，见 `LICENSE`。

> 说明：本 Skill 在运行期可能会拉取外部文档（例如最新 prompting guide）；外部材料遵循其原始许可证。

---

<div align="center">
  <img src="./readme_images/05-screenshot.png" alt="示例" width="720">
</div>
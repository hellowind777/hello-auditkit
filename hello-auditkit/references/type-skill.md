# 技能审计规则

> **继承**：`rules-universal.md` 中的所有规则
> **主要标准**：`ref-codex-skills-standard.md`（Codex CLI Skills 规范）
> **执行要求**：执行以下每个检查表。验证目录结构、frontmatter、脚本和参考文件。
>
> **关键**：对于技能结构和 frontmatter，应用 `ref-codex-skills-standard.md` 中的 Codex CLI Skills 标准。对于 SKILL.md 正文内容（非脚本文本），还应用 `ref-gpt-prompting-standard.md` 中的 GPT-5.2 提示词标准。

## 目录

- [概述](#概述)
- [技能目录验证](#技能目录验证)
- [SKILL.md 验证](#skillmd-验证)
- [脚本审计](#脚本审计)
- [参考文件审计](#参考文件审计)
- [设计原则](#设计原则)
- [常见问题](#常见问题)

---

## 概述

**技能是任何包含 `SKILL.md` 文件的目录。**

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter: name, description (必需)
│   └── Markdown body: instructions (必需)
├── scripts/      - 可执行代码（运行时，无尺寸限制）
├── references/   - 文档（按需加载，无官方限制）
├── assets/       - 输出资源（不加载）
└── [custom]/     - 任何其他目录
```

**关键**：按文件类型审计技能目录中的所有文件。

---

## 技能目录验证

| 检查 | 规则 | 严重性 |
|------|------|--------|
| SKILL.md 存在 | 技能根目录必需 | Fatal |
| 文件名完全是 `SKILL.md` | 区分大小写 | Fatal |
| 目录结构 | 如使用则有 scripts/、references/、assets/ | Info |
| 无多余文件 | 无 README.md、CHANGELOG.md | Warning |
| 所有引用可访问 | 文件存在且可读 | Severe |
| 引用深度 | 一级深度（无嵌套引用）| Warning |

### 完整目录审计

按类型审计技能目录中的所有文件。报告："总文件数：N，已审计：N"

---

## SKILL.md 验证

> **完整规范**：见 `ref-codex-skills-standard.md` 了解完整的 Codex CLI Skills 标准。

### Frontmatter（必需字段）

#### `name` 字段（必需）

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 存在 | 必需字段 | Fatal |
| 长度 | ≤64 字符（字符数，非字节数）| Severe |
| 字符 | 仅小写字母、数字、连字符（`a-z`、`0-9`、`-`）| Severe |
| 开头/结尾 | 不能以 `-` 开头或结尾 | Severe |
| 连续 | 不能包含 `--`（连续连字符）| Severe |
| 匹配目录 | 必须与父目录名完全匹配 | Severe |

**有效示例**：`pdf-processing`、`data-analysis`、`code-review`、`my-skill-v2`

**无效示例**：
- `PDF-Processing`（大写）
- `-pdf`（以连字符开头）
- `pdf-`（以连字符结尾）
- `pdf--processing`（连续连字符）
- `pdf_processing`（下划线）

#### `description` 字段（必需）

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 存在 | 必需字段 | Fatal |
| 长度 | ≤1024 字符（字符数；推荐 ≤500）| Severe |
| 触发条件 | 必须包含何时使用此技能 | Severe |
| 关键词 | 应包含具体触发短语 | Warning |

### Frontmatter（可选字段）

| 字段 | 规则 | 无效时严重性 |
|------|------|-------------|
| `license` | 许可证名称或文件引用 | Info |
| `compatibility` | ≤500 字符，环境要求 | Warning |
| `metadata` | 字符串键到字符串值的映射 | Warning |
| `allowed-tools` | 空格分隔的有效工具名列表 | Warning |

### 描述质量

**好的模式：**
```yaml
description: This skill should be used when the user asks to "specific phrase", "another phrase", mentions "keyword", or discusses topic-area.
```

**必须包含：**
- 具体触发短语
- 表明相关性的关键词
- 覆盖的主题领域

**不应包含：**
- 实现细节
- 技术规格
- 属于正文的信息

### 正文验证

| 范围 | 状态 | 严重性 |
|------|------|--------|
| ≤500 行 | 理想 | - |
| 500-550（≤10% 超出）| 可接受 | **不是问题** |
| 550-625（10-25% 超出）| 可接受 | 仅 Info |
| >625 行 | 应优化 | Warning |

**正文过长时，按顺序检查：**
1. 包含 AI 已知的解释？→ 删除
2. 冗长文本 vs 简洁示例？→ 简化
3. 重复信息？→ 去重
4. 灵活任务的过度约束？→ 简化
5. 仍然太长？→ 拆分到 references/

---

## 脚本审计

**重要：脚本是运行时执行的，不加载到上下文中。无行数限制。**

| 文件类型 | 加载到上下文 | 行数限制 |
|----------|-------------|----------|
| SKILL.md 正文 | 是 | <500 行（官方）|
| references/*.md | 是（按需）| **无限制** |
| scripts/*.py | **否**（运行时）| **无限制** |
| scripts/*.sh | **否**（运行时）| **无限制** |

### 脚本完整性验证

**关键**：对于复合系统，与源代码验证脚本完整性。

#### 步骤 1：识别脚本位置

| 优先级 | 位置 |
|--------|------|
| 1 | 明确声明的路径 |
| 2 | `skills/<skill-name>/scripts/` |
| 3 | SKILL.md 中的相对路径 |
| 4 | 共享脚本目录 |

#### 步骤 2：声明与实际检查

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 声明的存在 | 所有声明的脚本存在 | Severe |
| 未声明的脚本 | 记录或说明 | Info |
| 函数合并 | 检查是否合并到其他脚本 | - |

**函数合并检查**（关键）：

<script_integrity_analysis>
"脚本是否已合并"的推理过程：
- 如果声明的脚本不存在，不要立即标记为缺失
- 需要读取其他脚本的源代码
- 检查声明的函数是否在其他地方实现
- 如果已合并 → 需要更新文档，不是缺失问题
- 如果真的缺失 → 标记为 Severe 问题
</script_integrity_analysis>

- 如果声明的脚本不存在，**读取其他脚本的源代码**
- 检查声明的函数是否在其他地方实现
- **结果**：如果已合并则不是缺失问题（需要更新文档）

#### 步骤 3：脚本类型分类

| 类型 | 用途 | 应该记录？ |
|------|------|----------|
| **运行时** | 技能执行期间调用 | 是（必需）|
| **开发工具** | 仅开发/调试 | 否（不列出）|
| **内部辅助** | 被其他脚本导入 | 可选 |

#### 步骤 4：描述一致性

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 描述匹配代码 | 读取源代码，验证函数 | Severe |
| 主要函数有文档 | 所有导出函数 | Warning |
| 简短但准确 | 不误导 | Warning |

#### 步骤 5：依赖验证

| 检查 | 要求 | 严重性 |
|------|------|--------|
| 导入目标存在 | 所有导入的模块存在 | Fatal |
| 外部包 | 在 requirements 中列出 | Severe |
| 循环导入 | 无 | Severe |

### Shell 脚本

```bash
#!/bin/bash
set -euo pipefail  # 必需

# 错误处理
trap 'echo "Error on line $LINENO"' ERR

# 主逻辑
```

| 检查 | 规则 | 严重性 |
|------|------|--------|
| Shebang 行 | `#!/bin/bash` 或 `#!/usr/bin/env bash` | Warning |
| 错误处理 | `set -euo pipefail` | Warning |
| 变量引号 | 所有变量加引号 | Warning |
| 退出码 | 适当的退出码 | Info |

#### 跨平台路径处理（Shell）

> **目的**：确保脚本在 Windows 上能正确处理非 ASCII 路径（如中文字符），同时保持 Mac/Linux 兼容性。

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 双引号路径 | 所有文件/目录路径用双引号包裹（`"$path"`）| Severe |
| 命令中双引号 | 命令调用中包含路径的参数加引号（`cmd "$file"`）| Severe |
| 语言环境设置 | 脚本开头包含 `export LANG=en_US.UTF-8` 或 `export LC_ALL=C.UTF-8` | Warning |
| 避免裸 `$*` | 使用 `"$@"` 而非 `$*` 传递参数 | Warning |

**好的模式：**
```bash
#!/bin/bash
export LANG=en_US.UTF-8

file_path="$1"
if [[ -f "$file_path" ]]; then
    cat "$file_path"
    cp "$file_path" "$output_dir/"
fi
```

**差的模式：**
```bash
#!/bin/bash
file_path=$1
if [[ -f $file_path ]]; then   # 缺少引号 - 中文路径会失败
    cat $file_path              # 空格/中文会失败
    cp $file_path $output_dir/  # 两个路径都没引号
fi
```

### Python 脚本

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script description."""

import sys

def main():
    try:
        # 主逻辑
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

| 检查 | 规则 | 严重性 |
|------|------|--------|
| Shebang | `#!/usr/bin/env python3` | Warning |
| 错误处理 | 关键操作有 try/except | Warning |
| 具体异常 | 无裸 `except:` | Warning |
| 无硬编码秘密 | 使用环境变量 | Severe |
| 路径遍历 | 清理文件路径 | Severe |

#### 跨平台路径和编码处理（Python）

> **目的**：确保 Python 脚本在 Windows 上正确处理非 ASCII 路径（如中文字符），同时保持 Mac/Linux 兼容性。

| 检查 | 规则 | 严重性 |
|------|------|--------|
| UTF-8 编码声明 | 文件顶部包含 `# -*- coding: utf-8 -*-` | Warning |
| UTF-8 文件打开 | `open()` 调用使用 `encoding='utf-8'` | Severe |
| subprocess 中路径引号 | shell 命令中路径参数加引号 | Severe |
| 使用 pathlib 或 os.path | 路径操作优先使用 `pathlib.Path` 或 `os.path.join()` | Warning |
| 调用示例引号 | 脚本调用示例使用带引号的路径（`python "script.py" "路径/文件.txt"`）| Severe |

**Windows 下带 UTF-8 的 Shebang：**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

**或在调用示例中使用环境变量：**
```bash
# 好：确保 Windows 上的 UTF-8 模式
PYTHONUTF8=1 python3 "script.py" "中文路径/文件.txt"
# 或
python3 -X utf8 "script.py" "中文路径/文件.txt"
```

**好的模式（文件操作）：**
```python
from pathlib import Path

def read_file(file_path: str) -> str:
    """Read file with UTF-8 encoding."""
    path = Path(file_path)
    return path.read_text(encoding='utf-8')

def process_files(input_dir: str, output_dir: str):
    """Process files with proper encoding."""
    for file in Path(input_dir).glob('*.txt'):
        content = file.read_text(encoding='utf-8')
        output_path = Path(output_dir) / file.name
        output_path.write_text(content, encoding='utf-8')
```

**好的模式（Subprocess 调用）：**
```python
import subprocess
import shlex

def run_command(file_path: str):
    """Run command with properly quoted path."""
    # 使用列表形式（首选 - 自动处理引号）
    subprocess.run(['cat', file_path], check=True)

    # 如果需要 shell=True，引用路径
    quoted_path = shlex.quote(file_path)
    subprocess.run(f'cat {quoted_path}', shell=True, check=True)
```

**差的模式：**
```python
# 缺少编码 - Windows 上中文内容会失败
content = open(file_path).read()

# 无引号的 shell 命令 - 中文路径会失败
subprocess.run(f'cat {file_path}', shell=True)  # 差
os.system(f'process {file_path}')  # 差
```

**脚本调用示例要求：**

记录如何调用脚本时，必须包含带引号的路径：
```markdown
<!-- 好 -->
python3 "scripts/process.py" "输入文件.txt" "输出目录/"

<!-- 差 - 中文路径会失败 -->
python3 scripts/process.py 输入文件.txt 输出目录/
```

### 脚本不应检查

- 文件长度/行数（无限制）
- 目录要求（代码不需要）
- 风格偏好（设计选择）

---

## 参考文件审计

**目的**：按需加载的文档

> **官方指导**："保持单个参考文件专注。代理按需加载这些文件，所以较小的文件意味着更少的上下文使用。" — 无官方行数限制。

### 尺寸评估（基于内容）

**无硬编码限制。** 根据内容性质评估：

| 问题 | 如果是 |
|------|--------|
| 内容有不可分割的完整性？ | 不标记尺寸 |
| 拆分会导致功能风险？ | 不标记尺寸 |
| 有明显冗余？ | 建议精简 |
| 可以无影响地拆分？ | 建议拆分 |

### 要求

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 在 SKILL.md 中引用 | 清晰的"何时读取"指导 | Warning |
| 无重复 | 不与 SKILL.md 正文重复 | Info |
| 大文件有目录 | >100 行的文件有目录 | Info |
| 一级深度 | 无嵌套引用 | Warning |

### "何时读取"模式

**好：**
```markdown
## 参考文件

当以下情况时读取 `references/api-spec.md`：
- 用户询问 API 端点
- 生成 API 相关代码

当以下情况时读取 `references/error-codes.md`：
- 遇到错误代码
- 用户报告特定错误
```

**差：**
```markdown
See references/ for more information.
```

---

## 设计原则

### 通用性与可移植性

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 无硬编码语言内容 | 使用变量/模板 | Warning |
| 无环境特定路径 | 使用相对路径或配置 | Severe |
| 可配置行为 | 关键行为可配置 | Info |

### AI 执行者意识

> **完整详情**：见 `methodology-core.md` → AI 能力模型
> **完整 LLM 检查**：见 `rules-universal.md` → LLM 提示词最佳实践
> **多阶段检查**：见 `type-prompt.md` → 对话式/多阶段提示词规则

| 检查 | 规则 | 严重性 |
|------|------|--------|
| 避免过度指定 | 不要指定 AI 能推断的 | Warning |
| 使用语义标签 | 语义占位符 vs 硬编码字符串 | Warning |
| 信任 AI 判断 | 指南优于刚性规则 | Info |
| 详尽约束 | 明确的输出长度限制 | Warning |
| 范围边界 | 清晰的禁止约束 | Warning |
| 工具偏好 | 优先使用工具而非内部知识 | Warning |
| 代理式更新 | 主要阶段的简短更新（如是代理式）| Warning |
| 长上下文大纲 | >10k token：大纲、重述 | Warning |
| 约束集中 | 如是多阶段：关键规则在 ≤3 处 | Severe |
| 停止条件强度 | 如是多阶段：阶段门有强停止语言 | Severe |
| 禁止语言 | 关键约束使用强语言 | Warning |

### 何时硬编码可接受

**不要标记：**
- 许可证/版权声明
- 品牌名称
- 技术规格
- 代码示例（语法，非内容）
- 技术模式的正则表达式

**要标记：**
- 面向用户的消息
- 向用户显示的错误消息
- 固定语言的输出模板
- UI 标签

---

## 常见问题

> **完整清单**：见 `ref-codex-skills-standard.md` → 审计清单

### 应标记

| 问题 | 严重性 | 标准 |
|------|--------|------|
| 未找到 SKILL.md | Fatal | Codex Skills |
| 文件名不完全是 `SKILL.md` | Fatal | Codex Skills |
| 缺少 `name` 字段 | Fatal | Codex Skills |
| 缺少 `description` 字段 | Fatal | Codex Skills |
| `name` >64 字符 | Severe | Codex Skills |
| `name` 包含大写/下划线/空格 | Severe | Codex Skills |
| `name` 以 `-` 开头/结尾 | Severe | Codex Skills |
| `name` 包含 `--` | Severe | Codex Skills |
| `name` 与目录名不匹配 | Severe | Codex Skills |
| `description` >1024 字符 | Severe | Codex Skills |
| 描述缺少触发条件 | Severe | Codex Skills |
| `compatibility` >500 字符 | Warning | Codex Skills |
| 触发条件在正文而非描述中 | Warning | Codex Skills |
| 正文 >625 行未优化 | Warning | Codex Skills |
| 参考文件未在 SKILL.md 中提及 | Warning | Codex Skills |
| 深层引用嵌套（>1 级）| Warning | Codex Skills |
| 脚本无错误处理 | Warning | Codex Skills |
| 脚本中硬编码路径 | Severe | Codex Skills |
| 正文缺少详尽约束 | Severe | GPT-5.2 |
| 正文缺少范围约束 | Severe | GPT-5.2 |
| 约束分散（>3 处）| Severe | GPT-5.2 |
| shell 脚本中文件/目录路径无引号 | Severe | 跨平台 |
| Python `open()` 调用缺少 `encoding='utf-8'` | Severe | 跨平台 |
| subprocess shell 命令中路径无引号 | Severe | 跨平台 |
| 脚本调用示例中中文/空格路径无引号 | Severe | 跨平台 |
| shell 脚本缺少 UTF-8 语言环境设置 | Warning | 跨平台 |
| Python 缺少 UTF-8 编码声明 | Warning | 跨平台 |

### 不应标记

| 模式 | 原因 | 标准 |
|------|------|------|
| 正文 500-625 行 | 可接受范围 | Codex Skills |
| 使用 references/ 目录 | 好的实践 | Codex Skills |
| 缺少可选字段（license、metadata）| 可选 | Codex Skills |
| 风格变化 | 设计选择 | 两者 |
| 脚本文件长度 | 脚本无限制 | Codex Skills |
| 许可证头 | 有意为之 | 两者 |
| 参考文件长度 | 无官方限制 | Codex Skills |

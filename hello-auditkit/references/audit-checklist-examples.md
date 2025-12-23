# Audit Checklist - Examples

## Table of Contents

- [Should Flag](#should-flag)
- [Should NOT Flag](#should-not-flag)

---

## Should Flag

**Structure Issues:**
- "plugin.json is in root directory, not `.claude-plugin/`" → Fatal
- "SKILL.md named as `skill.md` (lowercase)" → Fatal
- "Components inside `.claude-plugin/` directory" → Fatal

**Path Issues:**
- "Hook uses `/Users/name/plugins/script.sh`" → Severe
- "MCP config uses `./scripts/server.js` without `${CLAUDE_PLUGIN_ROOT}`" → Severe

**Format Issues:**
- "hooks.json missing wrapper `{\"hooks\": {...}}`" → Severe
- "YAML frontmatter syntax error" → Severe
- "Invalid JSON in .mcp.json" → Severe

**Content Issues:**
- "Skill description doesn't include trigger conditions" → Severe
- "Command body written as user documentation" → Severe
- "Referenced agent `code-reviewer` doesn't exist" → Severe

**Script Issues:**
- "hooks.json references validate.sh but file doesn't exist" → Severe
- "Script imports helper.py but helper.py doesn't exist" → Fatal
- "Doc says script does X but actual code does Y" → Severe

**Consistency Issues:**
- "Same concept called 'task' in one file, 'job' in another" → Warning
- "Output format differs between components" → Warning
- "Rule R3 referenced but only R1, R2, R4 defined" → Severe

**Brand/Identity Issues:**
- Brand identifiers in output formats are NOT redundant - must preserve
- Plugin-specific terminology is intentional - don't flag as inconsistent

---

## Should NOT Flag

**Directory Structure (Design Choices):**
- "Using `cmds/` instead of `commands/`" → Valid if plugin.json configured
- "Has `lib/` directory not in marketplace examples" → Additional dirs are fine
- "Missing `agents/` directory" → Optional component
- "Different file organization than official plugins" → Design choice
- "Using custom directory names" → As long as spec requirements met

**Style Choices:**
- "Could use more emojis" → Not an issue
- "Sections could be reordered" → Design choice
- "Description could be shorter" → Unless >limit

**Optional Items:**
- "Missing version field in plugin.json" → Optional
- "Missing color field in agent" → Optional
- "No README.md" → Optional (though recommended)

**Design Choices:**
- "Using command hooks instead of prompt hooks" → Design choice
- "Skill body is 550 lines" → Acceptable range
- "Using flat command structure instead of namespaced" → Design choice

**AI Capability:**
- "Doesn't explain what JSON is" → Claude knows
- "Doesn't define common programming terms" → Claude knows
- "Assumes reader knows markdown syntax" → Claude knows

**Brand Identifiers:**
- "Output format includes 【BrandName】" → Required, not redundant
- "Each output starts with status symbol + brand" → Design requirement
- "Brand name appears frequently in skill" → If part of output spec, keep it

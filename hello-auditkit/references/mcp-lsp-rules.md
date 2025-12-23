# MCP & LSP Servers Audit Rules

## Table of Contents

- [MCP Servers Audit](#mcp-servers-audit)
- [LSP Servers Audit](#lsp-servers-audit)

---

## MCP Servers Audit

> Source: Claude Code official documentation (github.com/anthropics/claude-code)

### .mcp.json Format

**stdio server (local process):**
```json
{
  "server-name": {
    "command": "node",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
    "env": {
      "API_KEY": "${MY_API_KEY}",
      "LOG_LEVEL": "debug"
    }
  }
}
```

**Python server:**
```json
{
  "python-server": {
    "command": "python",
    "args": ["-m", "my_mcp_server"],
    "env": {
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

**HTTP server:**
```json
{
  "api-server": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

### MCP Server Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| command | string | Yes (stdio) | Executable command |
| args | array | No | Command arguments |
| env | object | No | Environment variables |
| type | string | No | `http` for HTTP servers |
| url | string | Yes (http) | API endpoint URL |
| headers | object | No | HTTP headers |

### Variable Substitution

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root directory |
| `${ENV_VAR_NAME}` | User environment variable |

### MCP Validation Rules

| Check | Rule | Severity |
|-------|------|----------|
| Valid JSON | Parseable, no syntax errors | Fatal |
| Server name | Unique, descriptive | Warning |
| command field | Required for stdio type | Severe |
| url field | Required for http type | Severe |
| Path portability | Use `${CLAUDE_PLUGIN_ROOT}` | Severe |
| No hardcoded secrets | Use environment variables | Severe |

### Common MCP Issues

**Should Flag:**
- Hardcoded paths in command, args, or cwd
- Invalid URL format for http type
- Missing required fields for type
- Duplicate server names
- Hardcoded secrets (API keys, tokens)

**Should NOT Flag:**
- Using environment variables for secrets
- Simple configurations
- Missing optional fields (env, headers)

---

## LSP Servers Audit

### .lsp.json Format

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact"
    },
    "transport": "stdio"
  }
}
```

### LSP Server Fields

| Field | Required | Description |
|-------|----------|-------------|
| command | Yes | LSP binary to execute |
| extensionToLanguage | Yes | Maps file extensions to language IDs |
| args | No | Command-line arguments |
| transport | No | `stdio` (default) or `socket` |
| env | No | Environment variables |
| initializationOptions | No | Options for initialization |
| settings | No | Workspace settings |
| workspaceFolder | No | Workspace folder path |
| startupTimeout | No | Max startup wait (ms) |
| shutdownTimeout | No | Max shutdown wait (ms) |
| restartOnCrash | No | Auto-restart on crash |
| maxRestarts | No | Max restart attempts |

### LSP Validation Rules

| Check | Rule | Severity |
|-------|------|----------|
| command field | Required | Severe |
| extensionToLanguage | Required, valid mapping | Severe |
| transport value | `stdio` or `socket` | Warning |
| Valid JSON | Parseable | Fatal |

### Common LSP Issues

**Should Flag:**
- Missing required fields (command, extensionToLanguage)
- Invalid transport value
- Invalid extension mapping format

**Should NOT Flag:**
- Missing optional fields
- Custom initialization options
- Different timeout values

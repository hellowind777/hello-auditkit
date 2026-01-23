# Contributing

Thanks for contributing to Hello-AuditKit.

## Scope

- Keep **runtime behavior** consistent with `hello-auditkit/SKILL.md`.
- Prefer **evidence-first** rules: every reported issue should be verifiable (file + line).
- Avoid adding checks that expand scope without a clear user request.

## Development

- Keep changes small and reviewable.
- If you add or change rules:
  - Update the relevant registry/checklist under `hello-auditkit/references/`.
  - Keep documentation and skill behavior aligned.

## Pull Requests

1. Fork the repo and create a feature branch.
2. Make changes.
3. Open a PR with:
   - What changed
   - Why it changed
   - Any compatibility notes
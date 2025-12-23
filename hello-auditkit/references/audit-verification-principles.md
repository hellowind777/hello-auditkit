# Audit Verification Principles

## Table of Contents

- [Issue Verification Checklist](#issue-verification-checklist-4-point-core-check)
- [AI Capability Assumptions](#ai-capability-assumptions--balance-principle)

---

## Issue Verification Checklist (4-Point Core Check)

Before marking any issue, it MUST pass all 4 verification checks:

### Check 1: Concrete Scenario Test

| Question | Pass Criteria |
|----------|---------------|
| Can you construct a specific scenario where this issue causes clear negative consequences? | Must describe complete execution steps and failure point |
| If NO → Not an issue, discard | |
| If YES → Continue to Check 2 | |

### Check 2: Design Scope Verification

| Question | Pass Criteria |
|----------|---------------|
| Is this scenario within the design scope of the content being audited? | Exclude extreme edge cases, theoretical possibilities |
| If NO → Not an issue, discard | |
| If YES → Continue to Check 3 | |

### Check 3: Design Intent Judgment

| Question | Pass Criteria |
|----------|---------------|
| Is this a design flaw or a design choice? | Can you find a reasonable design rationale? |
| If design choice (intentional) → Not an issue, discard | |
| If design flaw (unintentional error) → Continue to Check 4 | |
| **Note**: Missing necessary constraints is NOT a design choice | If ≥30% of executors would misunderstand, still flag it |

### Check 4: Negative Consequence Assessment

| Issue Type | Threshold |
|------------|-----------|
| Fatal | Execution completely fails (cannot continue) |
| Severe | ≥60% of executors make serious errors |
| Semantic Ambiguity | ≥3 reasonable but conflicting interpretations |
| Expression Standards | ≥40% misunderstand OR reading time +40% |
| Structure | Content scattered in ≥4 locations OR change requires ≥4 syncs |
| Robustness | ≥20% failure rate in common scenarios |
| Optimization | ≥30% improvement AND <10% cost |

If negative consequence unclear or below threshold → Not an issue, discard
If clear and meets threshold → Mark as issue

### Verification Transparency

- For each suspected issue, record which checks passed/failed
- If >80% of a category is discarded, reconsider scan criteria
- Final output must include: "Scanned X suspected issues, verified Y, discarded Z"

---

## AI Capability Assumptions & Balance Principle

### Default Assumption

AI executors have strong contextual understanding and can infer meaning from context and common sense.

### Balance Principle

1. **Identify issues first**: Assume issue exists, then verify if AI capability exempts it
2. **Burden of proof**: To exempt an issue, must prove "AI can infer correct understanding from context"
3. **Necessity threshold**:
   - If removing a constraint causes ≥30% of AI executors to misunderstand → Necessary, flag as issue
   - If removing a constraint causes <30% to misunderstand → Not necessary, can exempt

### AI Capability Boundaries

| AI CAN Understand | AI CANNOT Reliably Understand |
|-------------------|-------------------------------|
| Common synonyms | Cross-section implicit relationships |
| Clear contextual references | 3+ step inference chains |
| Standard terminology | Domain-specific term variations |
| Conventional patterns | Unstated assumptions |

### Practical Approach

- If unnecessary to modify, don't modify
- When uncertain, prefer keeping constraints and mark as "optimization suggestion" rather than "not an issue"

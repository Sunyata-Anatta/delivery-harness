# Restricted-runtime auto-load block

Append this complete marked block to `{{RUNTIME_INSTRUCTION_FILE}}`; replace the full existing block with the same markers. If the runtime has no persistent project instruction surface, keep explicit invocation and record that boundary.

```markdown
<!-- delivery-harness:start -->
This project runs under delivery-harness. On first contact with the project, read the installed delivery-harness/SKILL.md, select the project language, and emit its startup receipt before any tool call.
Keep the active node, authority boundaries, and evidence gates in the project overlay. Synchronize current state before commit. Reverify recorded external state before relying on it.
<!-- delivery-harness:end -->
```

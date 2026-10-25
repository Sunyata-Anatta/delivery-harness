# Owner Decision Register

Every new, supplementing or superseding rule is registered here first under a D number; rule tables and executor files (AGENTS.md and the like) cite the number instead of copying the text.
Write each decision so it can be decided mechanically, without words such as "appropriate" or "as needed"; a hard constraint must name its mechanical check.
When the same rule is violated a second time, set its violations to 2 and upgrade it to a hard constraint with a check; adding more prose is not allowed.
The baseline version changes only for a gate conclusion, a production or field change, a failure root cause or a new decision here; wording changes never bump it.

## D1 (<one sentence stating what this decision means>)

- Date: <YYYY-MM-DD>; owner: <who decided, with the original receipt>.
- Type: <hard constraint, rule or baseline; pick one>.
- Rule: <decidable rule text naming the trigger event, threshold and action>.
- Relation: <supersedes D<number> (meaning), supplements D<number> (meaning) or new rule>.
- Basis: <review report or fact number (meaning), with its path>.
- Check: <mechanical check ID and command; a hard constraint cannot say none>.
- Violations: 0.

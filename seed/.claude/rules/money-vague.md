# Money rule — the vague version (weak feedforward)

> Be careful with money. Don't lose precision, and handle the edge cases properly.

**Why this steers badly.** Every word is true and none of it is actionable. "Careful," "precision,"
and "edge cases" have no definition the agent can check its own work against, so a plausible
"simplification" that drops the remainder cents reads as perfectly compliant. A vague rule feels
like guidance but exerts almost no force on the output — the agent fills the gap with its own
guess, and its guess is what produced the plant.

**Tradeoff.** Cheap to write, applies everywhere, ages well — and does almost nothing. A rule you
cannot fail is a rule that cannot steer.

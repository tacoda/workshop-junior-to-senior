# Cash-rounding rule — the vague version (weak feedforward)

> Round cash totals fairly to a nickel.

**Why this steers badly.** "Fairly" has no definition the agent can act on. Rounding to the
*nearest* nickel is the textbook cash-rounding scheme (Canada, Sweden) and feels perfectly fair —
it's exactly what a capable agent reaches for by default, usually written with a `float` (`round(x /
5) * 5`). It reads as compliant with this rule while overcharging the customer on 40% of totals. A
vague rule feels like guidance but leaves the actual decision to the agent's default.

**Tradeoff.** Cheap to write, applies everywhere, ages well — and does almost nothing. A rule you
cannot fail is a rule that cannot steer.

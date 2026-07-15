# Cash-rounding rule — the concrete version (strong feedforward)

> - **Iron law:** money is integer cents; never use `float` to compute money.
> - **Rounding policy:** cash totals round **DOWN** to the nearest nickel (5 cents), always in the
>   customer's favor. Never round up, and never round to the nearest nickel. Example: a total of
>   1083¢ ($10.83) settles at **1080¢** ($10.80), not 1085¢. Use integer arithmetic:
>   `total_cents - (total_cents % 5)`.

**Why this steers well.** It names the exact policy (round down), gives a worked example that pins
the disputed case (1080, not 1085), and states the mechanism. Left to itself the agent rounds to the
nearest nickel with a float — a defensible default, but not *your* policy. This rule overrides that
default, so the agent writes the integer floor version the first time.

**Tradeoff.** More work to author and narrower in scope — but it decides a genuinely contested
choice the agent would otherwise make for you. That is what feedforward is for: not invariants the
model already respects, but decisions where your preference isn't the obvious one.

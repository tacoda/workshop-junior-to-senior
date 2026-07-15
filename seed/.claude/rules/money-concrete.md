# Money rule — the concrete version (strong feedforward)

> - **Iron law:** money is integer cents; never use `float` to store or compute money.
> - **Golden rule:** any function that splits or moves money must conserve the total — the
>   returned shares must sum *exactly* to the input, for every input including non-divisible
>   ones (e.g. `split_bill(1000, 3)` sums to `1000`, not `999`). Distribute remainder cents one
>   per person; ship the conservation test that proves it.
> - **Preference:** format money for display only, never mid-calculation.

**Why this steers well.** It names the function, states the invariant as an equation the agent can
evaluate (`sum(shares) == total`), gives a worked example, and dictates the mechanism (spread the
remainder). There is no room for a compliant-looking guess: the "even split" simplification
visibly fails the stated rule, so the agent doesn't write it.

**Tradeoff.** More work to author and narrower in scope — but it actually constrains the output. A
rule the agent can check itself against is a rule that shapes the first draft.

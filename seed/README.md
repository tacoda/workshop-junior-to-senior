# Seed repo — Junior to Senior

A tiny cash-register service small enough to hold in your head: it settles a bill for cash and
prints a receipt. Pennies are discontinued, so cash totals round to a nickel — and **which way they
round** is the load-bearing decision. The charter's policy is *round down, in the customer's favor*:
they never pay more than the marked total. That single policy is what punishes plausible-but-wrong
changes.

## Files

- `money.py` — `round_cash(total_cents)`. Correct: rounds **down** to a nickel (customer's favor),
  `total_cents - (total_cents % 5)`. Money is integer cents.
- `app.py` — turns a bill into a receipt: the marked total and the cash total. The cash line is
  where a wrong rounding policy shows up as a real overcharge.
- `test_money.py` — the suite that ships with the repo. **Deliberately incomplete:** the tests use
  only totals that round the same way down or to nearest, so rounding direction never shows and both
  the correct floor and the plant pass. Green here means "the tests that exist passed," not "correct."
- `CLAUDE.md` — starter charter; learners author the cash-rounding rule.
- `patches/plausible-but-wrong.diff` — the agent's "simplification": rounds to the *nearest* nickel
  with a `float` (`round(total / 5) * 5`) — the textbook cash-rounding scheme. Looks cleaner, passes
  the shipped suite, and quietly overcharges the customer up to four cents. The spine of the lab.
- `patches/gate-test.diff` — reference: the rounding gate that catches the plant
  (`test_cash_never_rounds_up`).
- `.claude/rules/cash-vague.md`, `.claude/rules/cash-concrete.md` — the *feedforward* half of the
  charter, in two strengths. The vague rule barely steers; the concrete one flips the agent from
  nearest-nickel-with-a-float to integer round-down. Same rule, different specificity.
- `.claude/settings.json` + `.claude/hooks/round-gate-edit.py` + `.claude/hooks/round-gate-commit.py`
  — the *feedback* half, wired at two positions. The edit gate (`PostToolUse`) catches cash that
  rounds against the customer the instant it's written; the commit gate (`PreToolUse` on
  `git commit`) blocks it at ship time. Same check, different distance from the mistake.

## The flow

```bash
pip install pytest
pytest                                    # 3 passed
python app.py                             # cash total $10.80  ← rounded down, customer's favor

git apply patches/plausible-but-wrong.diff
pytest                                    # still 3 passed — the trap
python app.py                             # cash total $10.85  ← a nickel overcharged

git apply patches/gate-test.diff          # the gate learners write in the lab
pytest                                    # FAILS: assert 1085 == 1080
```

With the plant applied, ask your agent to commit. The commit gate refuses:

```text
round-gate (commit): BLOCKED. round_cash(1083) = 1085, but the customer's-favor amount is 1080 — cash rounded against the customer.
```

The rule tells the agent to round cash down; the hook makes it impossible to ship a version that
doesn't. See the main README's coda for the feedforward/feedback framing and the tradeoffs between
the two rule and two hook variants.

## Why cash rounding (a note on what steers an agent)

An earlier version of this seed used a money-*conservation* invariant. It was dropped because a
capable model conserves money by default — so a conservation *rule* changes nothing you can observe.
Cash-rounding *direction* is different: it is a genuinely contested policy (round to nearest? down?),
so the model's default (nearest nickel, with a float) differs from the charter's choice (integer
round-down), and the rule visibly steers. That contrast is the point: use feedforward rules for
decisions the model won't guess right, and feedback hooks for the invariants it must never violate.

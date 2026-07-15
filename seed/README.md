# Seed repo — Junior to Senior

`split`, a bill-splitting service small enough to hold in your head, with one money invariant
(the shares must sum to the total) that punishes plausible-but-wrong changes.

## Files

- `money.py` — `split_bill(total_cents, ways)`. Correct: distributes remainder cents so the
  shares always conserve the total. Money is integer cents.
- `app.py` — turns a bill into a printed receipt. Its total line sums the *shares*, so a
  split that loses money prints a wrong total.
- `test_money.py` — the suite that ships with the repo. **Deliberately incomplete:** it only
  tests divisible totals, so it passes for both the correct code and the plant. Green here
  means "the tests that exist passed," not "correct."
- `CLAUDE.md` — starter charter; learners author the money rule in Module 2.
- `patches/plausible-but-wrong.diff` — the agent's "simplification." Looks cleaner, passes
  the shipped suite, drops the remainder cents. The spine of Module 4 and the labs.
- `patches/gate-test.diff` — instructor reference: the conservation gate that catches the
  plant (`test_split_conserves_total`).
- `.claude/rules/money-vague.md`, `.claude/rules/money-concrete.md` — the *feedforward* half of
  the charter, in two strengths. The vague rule barely steers; the concrete one shapes the first
  draft. Same rule, different specificity — that gap is the lesson.
- `.claude/settings.json` + `.claude/hooks/conserve-gate-edit.py` + `.claude/hooks/conserve-gate-commit.py`
  — the *feedback* half of the charter, wired at two positions. The edit gate (`PostToolUse`)
  catches a money-losing `split_bill` the instant it is written; the commit gate (`PreToolUse` on
  `git commit`) blocks it at ship time. Same conservation check, different distance from the
  mistake — the earlier it fires, the cheaper the fix. Rule guides, hook enforces; together they
  constrain one thing the agent cannot fake.

## The flow

```bash
pip install pytest
pytest                                    # 3 passed
python app.py                             # person 1 $3.34, 2/3 $3.33, total $10.00

git apply patches/plausible-but-wrong.diff
pytest                                    # still 3 passed — the trap
python app.py                             # total now $9.99: a cent vanished

git apply patches/gate-test.diff          # the gate learners write in Module 4
pytest                                    # FAILS: assert 999 == 1000
```

With the plant applied, ask your agent to commit. The commit gate refuses:

```text
conserve-gate (commit): BLOCKED. split_bill(1000, 3) = [333, 333, 333] sums to 999, not 1000 — money was lost.
```

The rule told the agent to conserve money; the hook made it impossible to ship the change
that didn't. That is the pair the workshop is teaching — see the main README's coda for the
feedforward/feedback framing and the tradeoffs between the two rule and two hook variants.

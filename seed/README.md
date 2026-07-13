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

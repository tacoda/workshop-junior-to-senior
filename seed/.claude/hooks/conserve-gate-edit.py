#!/usr/bin/env python3
"""FAST feedback: catch a money-losing split the instant it is written.

Wired as a PostToolUse hook on Edit/Write. It fires the moment the agent saves
money.py, before it does anything else. This is the *tight* feedback loop:

  * Speed:       immediate — the agent is corrected mid-task.
  * Consequence: the bad code existed on disk for a moment (the tool already ran),
                 but nothing was built on top of it, so the fix is cheap and local.

Compare with conserve-gate-commit.py, the *coarse* loop that only fires at commit.
"""
import json
import os
import sys

json.load(sys.stdin)  # PostToolUse payload; we only need to re-check the file on disk

# money.py lives two levels up from this hook (.claude/hooks/ -> seed/).
seed_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, seed_dir)
sys.modules.pop("money", None)  # always read the file as it is on disk right now
try:
    from money import split_bill
except Exception as exc:  # noqa: BLE001 - surface any import failure to the agent
    print(f"conserve-gate (edit): could not import split_bill: {exc}", file=sys.stderr)
    sys.exit(2)

# The charter's golden rule as an executable check: shares must sum to the total.
# Non-divisible totals — the case the shipped suite never covered.
for total, ways in [(1000, 3), (100, 7), (5, 2)]:
    shares = split_bill(total, ways)
    if sum(shares) != total:
        print(
            f"conserve-gate (edit): split_bill({total}, {ways}) = {shares} "
            f"sums to {sum(shares)}, not {total} — money was lost.\n"
            "Caught at edit time: fix split_bill now, before you build on it. "
            "The charter's golden rule: a split must conserve the total.",
            file=sys.stderr,
        )
        sys.exit(2)  # exit 2 reports back to the agent immediately

sys.exit(0)

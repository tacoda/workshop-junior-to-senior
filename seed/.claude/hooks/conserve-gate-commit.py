#!/usr/bin/env python3
"""LATE feedback: block the commit if a money-losing split reaches it.

Wired as a PreToolUse hook on Bash, gating only `git commit`. It fires at ship
time, after the agent may have edited, tested, and built more on the bad code.
This is the *coarse* feedback loop:

  * Speed:       late — only when the change tries to land.
  * Consequence: nothing bad ever ships (the commit is blocked outright), but by
                 now the mistake may be buried under later work, so the fix is
                 more expensive than catching it at edit time.

Compare with conserve-gate-edit.py, the *tight* loop that fires the instant
money.py is written. Same check, later position — that gap is the lesson.
"""
import json
import os
import sys

data = json.load(sys.stdin)
command = data.get("tool_input", {}).get("command", "")

# PreToolUse fires on every Bash call. Only gate commits; let the rest through.
if "git commit" not in command:
    sys.exit(0)

# money.py lives two levels up from this hook (.claude/hooks/ -> seed/).
seed_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, seed_dir)
sys.modules.pop("money", None)  # always read the file as it is on disk right now
try:
    from money import split_bill
except Exception as exc:  # noqa: BLE001 - surface any import failure to the agent
    print(f"conserve-gate (commit): could not import split_bill: {exc}", file=sys.stderr)
    sys.exit(2)

# The charter's golden rule as an executable check: shares must sum to the total.
# Non-divisible totals — the case the shipped suite never covered.
for total, ways in [(1000, 3), (100, 7), (5, 2)]:
    shares = split_bill(total, ways)
    if sum(shares) != total:
        print(
            f"conserve-gate (commit): BLOCKED. split_bill({total}, {ways}) = {shares} "
            f"sums to {sum(shares)}, not {total} — money was lost.\n"
            "Caught at commit time: the change cannot land until split_bill conserves "
            "the total. The charter's golden rule: a split must conserve the total.",
            file=sys.stderr,
        )
        sys.exit(2)  # exit 2 blocks the commit

sys.exit(0)

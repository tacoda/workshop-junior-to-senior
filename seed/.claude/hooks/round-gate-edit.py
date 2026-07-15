#!/usr/bin/env python3
"""FAST feedback: catch cash rounding that goes against the customer the instant it's written.

Wired as a PostToolUse hook on Edit/Write. It fires the moment the agent saves
money.py, before it does anything else. This is the *tight* feedback loop:

  * Speed:       immediate — the agent is corrected mid-task.
  * Consequence: the bad code existed on disk for a moment (the tool already ran),
                 but nothing was built on top of it, so the fix is cheap and local.

Compare with round-gate-commit.py, the *coarse* loop that only fires at commit.
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
    from money import round_cash
except Exception as exc:  # noqa: BLE001 - surface any import failure to the agent
    print(f"round-gate (edit): could not import round_cash: {exc}", file=sys.stderr)
    sys.exit(2)

# The charter's rounding policy as an executable check: cash rounds DOWN to a
# nickel, in the customer's favor. Uses totals whose remainder is 3-4 cents —
# the exact case the shipped suite never covered, so round-to-nearest slips past
# pytest but not past this.
for total in [1083, 1084, 999]:
    got = round_cash(total)
    down = total - (total % 5)
    if got != down:
        print(
            f"round-gate (edit): round_cash({total}) = {got}, but the customer's-favor "
            f"amount is {down} — cash rounded against the customer.\n"
            "Caught at edit time: fix it now, before you build on it. "
            "The charter's rounding policy: cash rounds DOWN to a nickel, always in the customer's favor.",
            file=sys.stderr,
        )
        sys.exit(2)  # exit 2 reports back to the agent immediately

sys.exit(0)

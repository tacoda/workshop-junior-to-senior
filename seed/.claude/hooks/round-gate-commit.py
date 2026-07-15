#!/usr/bin/env python3
"""LATE feedback: block the commit if cash rounding goes against the customer.

Wired as a PreToolUse hook on Bash, gating only `git commit`. It fires at ship
time, after the agent may have edited, tested, and built more on the bad code.
This is the *coarse* feedback loop:

  * Speed:       late — only when the change tries to land.
  * Consequence: nothing bad ever ships (the commit is blocked outright), but by
                 now the mistake may be buried under later work, so the fix is
                 more expensive than catching it at edit time.

Compare with round-gate-edit.py, the *tight* loop that fires the instant money.py
is written. Same check, later position — that gap is the lesson.
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
    from money import round_cash
except Exception as exc:  # noqa: BLE001 - surface any import failure to the agent
    print(f"round-gate (commit): could not import round_cash: {exc}", file=sys.stderr)
    sys.exit(2)

# The charter's rounding policy as an executable check: cash rounds DOWN to a
# nickel, in the customer's favor. Uses totals whose remainder is 3-4 cents —
# the case the shipped suite never covered, so round-to-nearest slips past pytest.
for total in [1083, 1084, 999]:
    got = round_cash(total)
    down = total - (total % 5)
    if got != down:
        print(
            f"round-gate (commit): BLOCKED. round_cash({total}) = {got}, but the "
            f"customer's-favor amount is {down} — cash rounded against the customer.\n"
            "Caught at commit time: the change cannot land until cash rounds DOWN to a nickel. "
            "The charter's rounding policy: cash is always rounded in the customer's favor.",
            file=sys.stderr,
        )
        sys.exit(2)  # exit 2 blocks the commit

sys.exit(0)

# How to Grow from Junior to Senior in the Age of AI

The agent changes what it means to be junior more than what it means to be senior. A senior
already has the judgment the tool can't supply. A junior is building that judgment at the exact
moment the tool offers to skip it — it hands you working code faster than you can understand it,
and the whole pull is to accept the diff and move on. This workshop is the structured refusal to
skip.

- **Who it's for:** early-career engineers working with an AI coding tool, and the leads who
  mentor them.
- **What you leave with:** the comprehension card (one rule, five questions, five moves) and a
  habit you can run on real work Monday morning.
- **The seam it drives home:** the agent produces plausible code fast; seniority is the judgment
  to tell plausible from correct. That judgment is trained, not downloaded.

> The first part of this README is **the lab** — work straight through it, top to bottom.
> [Instructor notes](#instructor-notes) live at the very bottom.

---

# The Lab

## Before you start — get to green

You can read code and you've used an AI coding tool once. That's enough. Run this first and
confirm a green suite — don't debug your environment on lab time:

```bash
git clone https://github.com/tacoda/workshop-junior-to-senior.git
cd workshop-junior-to-senior/seed
pip install pytest && pytest      # 3 passed — you're ready
```

⟲ **No local setup?** Pair with someone who's green, or run it in any browser Python sandbox —
the seed is three small files.

**What you'll work on.** The seed in [`seed/`](./seed/) is `split`, a bill-splitting service
small enough to hold in your head. It has one rule that matters: **the shares of a split must sum
back to the total** — money is never created or destroyed. That single invariant is what makes a
plausible-but-wrong change catchable.

## Your tool: the comprehension card

This is the whole method on one page. You'll use it in the lab and keep it next to your keyboard
after.

```text
THE DAILY RULE
  Don't merge a change you can't explain — to the agent, out loud, in your own words.
  Green pipeline = permission to proceed. Red = a lesson before a human had to teach it.

FIVE QUESTIONS (comprehension in — ask these of any diff)
  1. What does this do, in one sentence?
  2. Where does the change enter the system, and where does it leave?
  3. Why is it written this way? (If neither a rule nor a doc answers, you found a charter gap.)
  4. Is it consistent with the rest of the codebase? Which nearby code disagrees?
  5. Which part would I call slop if an agent wrote it — plausible, passing, quietly wrong?

FIVE MOVES (comprehension out — the junior→senior cases)
  1. Characterize before you change — pin current behavior in a test before you touch it.
  2. Rename in anger — fix the worst-named thing everywhere; watch it clarify.
  3. Make it boring — rewrite the clever version as the one you'd rather debug at 3 a.m.
  4. Predict the failure — write how you expect it to fail, then run it. Were you right?
  5. Catch the agent being wrong — find the confident, fluent, wrong answer. Prove it.
```

## Step 1 · Baseline, then spring the trap

Everything is in `seed/`. Copy-paste this block and read the comments as you go:

```bash
cd seed
pytest                                       # 3 passed
python app.py                                # total: $10.00   ← correct

git apply patches/plausible-but-wrong.diff   # a diff "an agent handed you" — looks cleaner
pytest                                        # still 3 passed  ← the trap
python app.py                                 # total: $9.99    ← a cent vanished
```

Look at those last two lines. The test suite is **green**, and yet a cent disappeared. This is the
one idea the whole hour is built on:

> **Green means "the tests that exist passed," not "the code is correct."**

The shipped suite only ever tested splits that divide evenly, so it never noticed the remainder
going missing. Leave the diff applied for now — you'll investigate it in the next step.

## Step 2 · Run the five questions (comprehension *in*)

Open `seed/money.py` and read the change you just applied. With a partner if you can, work down the
five questions from the card, out loud. Write your answers down:

1. **What does it do, in one sentence?** (`split_bill` now returns `total // ways` for everyone.)
2. **Where does the change enter and leave?** Trace it from `app.py` into `money.py` and back to
   the printed total.
3. **Why is it written this way?** The comment says "simplified." Is simpler worth the cent?
4. **Is it consistent?** The docstring still promises the shares "always sum back to the total."
   The code no longer does. Which do you trust?
5. **What would you call slop?** Name the exact line that is plausible, passing, and quietly wrong.

A filled card is your first deliverable — and everyone reaches it.

## Step 3 · Prove it wrong (comprehension *out*)

Suspicion isn't a catch. Turn it into a test that fails:

- Split `$10.00` three ways by hand: `334 + 333 + 333 = 1000`. The "simplified" code gives
  `333 + 333 + 333 = 999`.
- Write one test asserting the shares sum to the total for a **non-divisible** split — the case the
  shipped suite skipped:

```python
def test_split_conserves_total():
    for total, ways in [(1000, 3), (100, 7), (5, 2)]:
        assert sum(split_bill(total, ways)) == total
```

Run `pytest`. It goes **red** on the diff — you just caught a confident, fluent, wrong answer and
proved it. That red test is the day you stop being junior, in miniature. Reset before the next
step:

```bash
git checkout money.py
```

## Step 4 · The two loops that catch it automatically

You caught the bug by hand. Now watch the *charter* catch it for you. Almost everything in this
field reduces to two kinds of loop:

- **Feedforward** — a signal that shapes the output *before* it's produced. Here: a **rule** in
  `CLAUDE.md` telling the agent "a split must conserve the total." The agent reads it and usually
  writes conforming code the first time.
- **Feedback** — a signal that checks the output *after* it's produced and reports back. Here: a
  **hook** in `.claude/hooks/` that runs the invariant as code and refuses a violating result.

The seed already has one of each turned on. Open the `seed/` folder in Claude Code and run these
three prompts in order.

1. **Feedforward — the rule steers the first draft.** Ask your agent, verbatim:
   > Simplify `split_bill` in money.py.

   The rule pushes it to keep the remainder. Check: `pytest` is green *and* — read the diff — the
   shares still sum to the total. A rule shapes the draft, but it's only a suggestion the agent can
   still miss.

2. **Feedback (fast) — the edit gate catches a bad draft instantly.** Ask your agent, verbatim:
   > Make `split_bill` a plain even split: `return [total_cents // ways] * ways`.

   The moment it saves `money.py`, the hook fires and reports back:
   ```text
   conserve-gate (edit): split_bill(1000, 3) = [333, 333, 333] sums to 999, not 1000 — money was lost.
   ```
   Told *why*, the agent puts the remainder back. `pytest` green and conserving.

3. **Feedback (late) — the commit gate is the last line.** Reset, re-apply the plant in the shell,
   then ask the agent to commit it:
   ```bash
   git checkout money.py && git apply patches/plausible-but-wrong.diff
   ```
   > Commit this change.

   The commit is blocked outright:
   ```text
   conserve-gate (commit): BLOCKED. split_bill(1000, 3) = [333, 333, 333] sums to 999, not 1000 — money was lost.
   ```
   Reset when done: `git checkout money.py`.

**The whole idea in three prompts:** the rule shaped the draft; the fast gate caught the draft that
slipped; the late gate stopped it from shipping. One feedforward, one feedback — the two mechanisms
a charter uses to shape what the agent does.

## How it works — the two knobs

You just used one setting of each loop. Both have a design choice, and the seed ships two examples
of each so you can feel the tradeoff, not just read it.

**Feedforward — the rule's *specificity* (`seed/.claude/rules/`).** A rule you cannot fail is a
rule that cannot steer.

| Rule | What it says | Tradeoff |
|---|---|---|
| `money-vague.md` | "Be careful with money, don't lose precision." | Cheap, universal, ages well — and exerts almost no force. The plant reads as compliant. |
| `money-concrete.md` | "`split_bill` shares must sum *exactly* to the total; spread the remainder." | More work, narrower scope — but the agent can check itself against it, so it shapes the first draft. |

**Feedback — the gate's *position* (`seed/.claude/hooks/`).** Same check, different distance from
the mistake. The earlier the loop closes, the cheaper the fix.

| Hook | Event | Speed / consequence |
|---|---|---|
| `conserve-gate-edit.py` | `PostToolUse` on `Edit`/`Write` | **Fast.** Fires the instant `money.py` is saved; agent corrected mid-task, fix is local. The bad code did exist on disk for a moment. |
| `conserve-gate-commit.py` | `PreToolUse` on `git commit` | **Late.** Fires only at ship time; nothing bad ever lands, but the mistake may be buried under later work, so the fix costs more. |

**Try the variants (optional).** Each swap is one step; undo it with `git checkout` when done.

- *Weak rule:* paste the contents of `.claude/rules/money-vague.md` over the money rules in
  `CLAUDE.md`, restart the agent, and re-run Step 4 prompt 1 — watch the vague rule fail to steer.
- *Commit gate alone:* delete the `PostToolUse` block from `.claude/settings.json` so only the late
  gate is wired, then re-run Step 4 prompt 2 — the bad edit now sails through and is caught only at
  commit. That gap between "caught on save" and "caught at ship" is the cost of a slow loop.

A rule without a hook is a suggestion; a hook without a rule is a gate no one explained. Together —
guidance you write, enforcement you run — they're the smallest whole unit of a charter, and the two
mechanisms to reach for first.

## What you leave with

- The comprehension card — the daily rule, the five questions, the five moves.
- A filled card applied to a real agent diff.
- A conservation test you wrote that catches the planted bug.
- A working mental model: feedforward (rules) + feedback (hooks) = how a charter shapes an agent.

## After the workshop — the take-home lab

The hour gives you the card and one rep on a toy repo. Judgment comes from reps on real code you
didn't write. This lab is yours to run afterward — no instructor, no answer key. Do it on a project
you'll never ship to, so you can be wrong for free.

**Why an open-source project.** A toy seed can't teach you scale, history, or the weight of code
other people depend on. A real project can: it's readable at your own pace, its commit history
records why every line is the way it is, and its test suite shows what "proven correct" actually
looks like. The five questions and five moves are the same; only the code got real.

**Why SQLite is the one to start on.**
- **Small enough to hold.** One file's worth of public API, navigable in an afternoon.
- **Famous for its tests.** It ships far more test code than library code, and documents *how* it's
  tested — the discipline this workshop trains, at professional scale.
  ([sqlite.org/testing.html](https://www.sqlite.org/testing.html))
- **The docs explain the *why*** — which is question 3 on your card, answered for you.
- **Self-contained C.** Legible and dependency-free; you see exactly where a change enters and
  leaves.

Source and docs: [sqlite.org](https://www.sqlite.org/) · source at
[sqlite.org/src](https://www.sqlite.org/src/) · a readable mirror lives on GitHub.

**Run the card on real code:**
1. **Read one design doc, explain it back.** Pick a page from the SQLite docs, read it, then explain
   it to your agent in your own words. Where you stall is where you didn't understand.
2. **Comprehension pass.** Choose one self-contained function. Run all five questions against it.
   Use the agent as a tutor — ask *what*, *where*, *why* — but form your own answer first.
3. **Predict the failure (move 4).** Pick one test. Before reading it, predict what input would
   break the code it guards. Then read the test. Were you right?
4. **Catch the agent wrong (move 5).** Ask your agent to "simplify" or "optimize" one small
   function. Run the five questions on its diff. Prove it correct, or prove it wrong with a test.
5. **Legibility read (move 3).** Find the best-named and worst-named thing you can. Ask why the good
   one is good. That instinct is what you're building.

**Repeat step 4 weekly** on any codebase you touch. The habit is the deliverable, not any one catch.

---

# Instructor notes

*Everything below is for whoever runs the session. Attendees don't need it.*

## Running the hour

| Length | Shape | Deliverable |
|---|---|---|
| **1 hour** | Talk + one live lab | The comprehension card, applied once to a real agent diff |

Rough pacing: ~15 min talk, ~35 min lab (Steps 1–4), ~10 min regroup. Suggested budget within the
lab: Step 1 ≈ 3 min, Step 2 ≈ 12 min, Step 3 ≈ 10 min (stretch/fast finishers), Step 4 ≈ 8 min.

- **Cut talk before you cut lab.** If you run long, shrink the talk; never the lab.
- **Pre-flight matters.** Put the *Before you start* block in the calendar invite and on the opening
  slide. A failed `pip install` in minute two costs someone the lab. Anyone red at the start pairs
  with someone green.
- **Protect the "I almost shipped that" moment.** Step 1's trap and Step 3's red test are the
  emotional core. Don't spoil that green ≠ correct — let the room discover it.
- **Regroup on the catch.** Who found the missing cent? Surface the near-miss out loud; it's the
  point of the whole hour.

## The talk — the frame and the spine

Open with the split that organizes everything around the agent: **does it execute, or is it read?**
The machinery executes (the agent, the loop, the tools); the charter is read (the `CLAUDE.md`, the
rules, the gates). Comprehension is the attendee's job because the agent can produce the code but not
the judgment that it's right. — *ch04–06, Appendix E.*

Keep it a talk, not a lecture: ask the room for a time they merged a diff they couldn't explain, and
what it cost. That story is the whole workshop in one anecdote.

**Key ideas to land** (from Appendix E — say these out loud; they're the spine):

> - The agent changes what it means to be *junior* more than what it means to be *senior*. A senior
>   already has the judgment the tool can't supply; a junior is building it at the exact moment the
>   tool offers to skip it.
> - A senior is not the engineer who types less. A senior is the engineer who understands enough to
>   know when the agent is wrong — and you only get there by asking.
> - Make comprehension the requirement, not the option. Use the agent to *explain*, never to *skip*.
> - A green pipeline is permission to proceed. A red one is the system teaching you something before
>   a human had to.
> - The arrangement is two-sided: **you bring comprehension; the team keeps the charter good enough
>   to onboard you and the harness good enough to guard you.** A junior's confusion is usually the
>   charter's missing onboarding, not a gap in the junior.
> - The day you can reliably catch a confident, fluent, wrong answer is the day you are no longer
>   junior.

## Mixed room

Pair a stronger engineer with a newer one for the lab. Let the stretch in Step 3 and the variants in
*How it works* absorb fast finishers so you never pace to the ceiling.

## References

- **The seed's design** is documented in [`seed/README.md`](./seed/README.md): why the shipped suite
  is deliberately incomplete, what each file does, and the full flow.
- `seed/patches/plausible-but-wrong.diff` — the plant (the agent's "simplification").
- `seed/patches/gate-test.diff` — the conservation gate as a test, for reference.
- **Book map.** Appendix E ("For the Junior Engineer") is the spine. Foundations ch01–07 (the split,
  the reliability problem, the repo as a behavioral system); ch14 (the legible codebase); ch15 (tests
  and gates).

## To refine (working notes)

- [ ] Time-box each lab step against a real run; adjust the pacing table.
- [ ] Decide whether to demo the *variants* live or leave them as take-home.
- [ ] Both hooks are on by default, so the edit gate fires first and the commit gate rarely triggers
      on its own — Step 4 prompt 3 applies the plant in the shell to force the commit path. If you
      want the commit gate to fire alone in a live agent run, comment out the `PostToolUse` block.
- [ ] Confirm the concrete rule in `seed/CLAUDE.md` steers a fresh agent reliably on prompt 1.

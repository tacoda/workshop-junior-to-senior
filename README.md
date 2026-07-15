# How to Grow from Junior to Senior in the Age of AI

The agent changes what it means to be junior more than what it means to be senior. A senior
already has the judgment the tool can't supply. A junior is building that judgment at the
exact moment the tool offers to skip it — it hands you working code faster than you can
understand it, and the whole pull is to accept the diff and move on. This workshop is the
structured refusal to skip. You leave with one rule, five questions, five moves, and the
habit that runs them on real work.

Source: *The Book*'s Appendix E ("For the Junior Engineer"), with foundations from ch01–07,
ch14, and ch15.

- **Who it's for:** early-career engineers working with an AI coding tool, and the leads who
  mentor them.
- **What you leave with:** the comprehension card (the daily rule + the five moves) and a
  daily read/gate/review habit you can run on real work Monday morning.
- **The seam it drives home:** the agent produces plausible code fast; seniority is the
  judgment to tell plausible from correct. That judgment is trained, not downloaded.

## The shape of the hour — a golden path

A junior doesn't need more information; they need a direction and a place to practice it. This
workshop gives all three, in order:

1. **Direction** (the talk) — one rule, five questions, five moves, on a card you keep at the
   keyboard. This is the path: what a senior does with any diff the agent hands them.
2. **A small lab** (in the room) — practice the moves once, live, on a planted diff small
   enough to finish in the hour. One clean rep so the card stops being abstract.
3. **A take-home lab** (yours, afterward) — the bigger reps, on real open-source code (SQLite),
   where judgment actually gets built. See *Further resources* below.

Direction, one rep, then the reps that make it stick. Everything below fills in that path.

## Format

| Length | Shape | Deliverable |
|---|---|---|
| **1 hour** | Talk + one live lab | The comprehension card, applied once to a real agent diff |

Longer 2-hour and 6-hour versions are parked in `_dropped-tracks.md` for later.

## Prerequisites

You can read code; you've used an AI coding tool once; a throwaway repo.

## The ramp (varying levels in the room)

Engineers arrive at different levels, so the workshop ramps in **scope and pace**:

- **Floor first.** Early modules assume the least and move slowly — everyone starts on the
  same page, no one is lost by lunch.
- **Ceiling later.** Later modules widen scope and quicken pace — stronger engineers get
  stretched instead of bored.
- **On-ramps** (⟲) let a struggling engineer rejoin at the start of any module.
- **Stretch goals** (↑) give fast finishers extra depth without blocking the room.

## The seed repo

Every track uses [`seed/`](./seed/) — `split`, a bill-splitting service small enough to hold
in your head, with one money invariant that punishes plausible-but-wrong changes. The agent's
"simplification" lives in `seed/patches/plausible-but-wrong.diff`: it looks cleaner, passes
the tests already in the repo, and quietly loses money. Catching it is the point.

```bash
cd seed && pip install pytest && pytest      # green to start
```

---

## Track A — 1 hour (talk + one live lab)

One talk, one lab. The ramp lives inside the lab: the base task is comprehension — everyone
finishes it — and the ↑ stretch is catching the plant. This is the confidence track. Nobody
leaves stuck; everybody leaves with a filled card.

### Pre-flight · Green before we start (send ahead, or first 3 minutes)
A failed `pip install` in minute two costs you the lab. Have every attendee run this *before*
the talk and show a green suite — put it in the calendar invite and repeat it on the opening
slide:

```bash
git clone <seed-url> && cd seed
pip install pytest && pytest      # 3 passed — you're ready
```

Anyone red here pairs with someone green. No one debugs their environment on lab time.
⟲ **on-ramp:** no local setup? Pair, or run it in any browser Python sandbox — the seed is
three small files.

### Talk · The split, the rule, the five moves (0:03–0:33)
Name the split that organizes everything around the agent: **does it execute, or is it
read?** The machinery executes (the agent, the loop, the tools); the charter is read (the
`CLAUDE.md`, the rules, the gates). Comprehension is *your* job because the agent can produce
the code but not the judgment that it's right. Then the daily rule and the five moves that
turn agent output into trusted output. — *ch04–06, Appendix E.*

Keep it a talk, not a lecture: ask the room for a time they merged a diff they couldn't
explain, and what it cost. That story is the whole workshop in one anecdote. Protect the lab —
if you run long, cut talk, never lab.

**Key ideas to land** (from Appendix E — say these out loud, they're the spine):

> - The agent changes what it means to be *junior* more than what it means to be *senior*. A
>   senior already has the judgment the tool can't supply; a junior is building it at the exact
>   moment the tool offers to skip it.
> - A senior is not the engineer who types less. A senior is the engineer who understands
>   enough to know when the agent is wrong — and you only get there by asking.
> - Make comprehension the requirement, not the option. Use the agent to *explain*, never to
>   *skip*. It's the best tutor a junior ever had; don't waste it merging code you can't read.
> - A green pipeline is permission to proceed. A red one is the system teaching you something
>   before a human had to.
> - The arrangement is two-sided: **you bring comprehension; the team keeps the charter good
>   enough to onboard you and the harness good enough to guard you.** A junior's confusion is
>   usually the charter's missing onboarding, not a gap in the junior.
> - The day you can reliably catch a confident, fluent, wrong answer is the day you are no
>   longer junior. That's the whole lab, in one sentence.

**Artifact — the comprehension card.** One page you keep next to the keyboard:

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

### Lab · Read one agent diff (0:33–1:00)
Pair up — a stronger engineer with a newer one where you can. Work the steps in order; each
has a checkpoint so you know you're on track.

1. **Baseline (2 min).** `pytest` (green), then `python app.py`. Read the receipt out loud.
   *Checkpoint:* the total prints `$10.00`.
2. **Apply the agent's change (3 min).** This is the diff an agent handed you, cleaner-looking
   than the original:
   ```bash
   git apply patches/plausible-but-wrong.diff && pytest    # still 3 passed — that's the trap
   ```
   *Checkpoint:* green suite, and you feel the pull to merge it.
3. **The five questions, out loud (12 min).** Run all five against the diff with your partner.
   Explain what `split_bill` now does, where the change enters and leaves, and which nearby
   code disagrees. Write the answers on your card. *Checkpoint:* a filled comprehension card —
   this is the base deliverable, and everyone reaches it.
4. **↑ Stretch — prove it wrong (remaining time).** Green, but is it correct? Run
   `python app.py` again and watch the total: a cent vanished. Split $10.00 three ways by hand,
   sum the shares, and write one test that fails on this diff. *Checkpoint:* a red test you
   wrote yourself. — *ch15, Appendix E.*
5. **Regroup (last 5 min).** Who caught the missing cent? Surface the "I almost shipped that"
   moment — it's the point of the whole hour. Green means *the tests that exist passed*, not
   *correct*.

**Artifact:** a filled comprehension card applied to a real diff (all pairs); a failing
conservation test (stretch).

---

## Takeaway artifacts
- The comprehension card — the daily rule + the five questions + the five moves.
- A filled card applied to a real agent diff.
- A conservation test that catches the planted bug (stretch finishers).

## Further resources — take-home lab (provided, not covered in the hour)

The hour gives you the card and one rep on a toy repo. Judgment comes from reps on real code
you didn't write. This lab is yours to run afterward — no instructor, no answer key. Do it on a
project you'll never ship to, so you can be wrong for free.

### Why learn from an open-source project
A toy seed can't teach you scale, history, or the weight of code other people depend on. A real
open-source project can. It's readable at your own pace, its commit history records why every
line is the way it is, and its test suite shows you what "proven correct" actually looks like.
The five questions and five moves are the same; only the code got real.

### Why SQLite is the one to start on
- **Small enough to hold.** One file's worth of public API, a codebase you can navigate in an
  afternoon — not a framework with a hundred moving parts.
- **Famous for its tests.** SQLite ships with far more test code than library code, and the
  project documents *how* it's tested. That's the discipline this workshop is training, shown
  at professional scale. Read [sqlite.org/testing.html](https://www.sqlite.org/testing.html).
- **The docs explain the *why*.** Most projects tell you what a function does. SQLite tells you
  why it was built that way — which is question 3 on your card, answered for you.
- **Self-contained C.** Legible, dependency-free, and close to the machine. You see exactly
  where a change enters and leaves.

Source and docs: [sqlite.org](https://www.sqlite.org/) · source in Fossil at
[sqlite.org/src](https://www.sqlite.org/src/) · a readable mirror lives on GitHub.

### The lab — run the card on real code
1. **Read one design doc, explain it back.** Pick a page from the SQLite docs, read it, then
   explain it to your agent in your own words. Where you stall is where you didn't understand.
2. **Comprehension pass.** Choose one self-contained function. Run all five questions against
   it. Use the agent as a tutor — ask *what*, *where*, *why* — but form your own answer first.
3. **Predict the failure (move 4).** Pick one test in the suite. Before reading it, predict
   what input would break the code it guards. Then read the test. Were you right?
4. **Catch the agent wrong (move 5).** Ask your agent to "simplify" or "optimize" one small
   function. Run the five questions on its diff. Prove it correct, or prove it wrong with a
   test — the same drill as the workshop, now on code that matters.
5. **Legibility read (move 3).** Find the best-named and worst-named thing you can. Ask why the
   good one is good. That instinct is what you're building.

### Where to go next
- **Repeat step 4 weekly** on any codebase you touch. The habit is the deliverable, not any one
  catch.
- A longer series on charters, harnesses, and governing AI systems builds on this foundation.

## Instructor notes
- The plant in `seed/patches/` is the emotional core — everyone should feel the "I almost
  shipped that" moment. Protect time for it; it's the whole point of the capstone move.
- The trap works because the seed's own tests only cover divisible totals. Don't spoil that —
  let the room discover that green means "the tests that exist passed," not "correct."
- Mixed room: pair a stronger engineer with a struggling one for the lab; let the ↑ stretch
  goals absorb fast finishers so you never pace to the ceiling.
- Reference catch: `seed/patches/gate-test.diff` is the conservation gate, for instructors.
- Cut talk before you cut lab.

## Book map
Appendix E ("For the Junior Engineer") is the spine. Foundations ch01–07
(the split, the reliability problem, the repo as a behavioral system); ch14 (the legible
codebase); ch15 (tests and gates).

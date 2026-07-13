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

## Length options

| Track | Shape | Deliverable |
|---|---|---|
| **1 hour** | Talk + one live lab | The comprehension card, applied once to a real diff |
| **2 hours** | Talk + two labs | The card, plus catching a planted bug and gating it |
| **6 hours** | 6 modules on a runnable seed repo | The card + a daily habit, drilled across comprehension, gating, and catching-the-agent-wrong |

Each track is a slice of the next up: same spine, fewer labs.

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

Same spine as the six-hour, compressed to one lab. The ramp lives inside the lab: the base
task is comprehension, the ↑ stretch is catching the plant.

### Talk · The split, the rule, the five moves (0:00–0:35)
Name the split that organizes everything around the agent: **does it execute, or is it
read?** The machinery executes (the agent, the loop, the tools); the charter is read (the
`CLAUDE.md`, the rules, the gates). Comprehension is *your* job because the agent can produce
the code but not the judgment that it's right. Then the daily rule and the five moves that
turn agent output into trusted output. — *ch04–06, Appendix E.*

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

### Lab · Read one agent diff (0:35–1:00)
Open `seed/`, run `pytest` (green). Apply the agent's change and re-run:

```bash
git apply patches/plausible-but-wrong.diff && pytest    # still green — that's the trap
```

Run the five questions against the diff out loud with the person next to you. Explain what
`split_bill` now does. **↑ Stretch:** the tests pass but the money is wrong — find it. Split a
$10.00 bill three ways and add up the shares. Prove the bug with one new test.
— *ch15, Appendix E.*

**Artifact:** a filled comprehension card applied to a real diff.

---

## Track C — 2 hours (talk + two labs)

A bigger slice: comprehension *and* catching the agent wrong. Ramp is across the two labs —
Lab 1 levels the floor, Lab 2 stretches.

### Talk · The split, the rule, the five moves (0:00–0:20)
The condensed version of Track A's talk: the split, the daily rule, the five moves.
— *ch04–06, Appendix E.* **Artifact:** the comprehension card.

### Lab 1 · Comprehension (0:20–1:05)
Read `seed/money.py` and `seed/app.py` with the agent as your tutor — ask it *what*, *where*,
and *why* on every function, but never let it merge for you. Trace how a bill total enters
`app.py`, moves through `split_bill`, and leaves as a printed receipt. Name every hop.
— *ch07, Appendix E.* ⟲ **on-ramp:** run `python app.py` first and read its output.

### Lab 2 · Catch the agent wrong + gate it (1:05–2:00)
Apply `patches/plausible-but-wrong.diff`. The suite stays green because it only tests
divisible totals — that's how slop survives review. Find the broken invariant (the shares no
longer sum to the total), then **write the gate that stops it**: a conservation test that
fails on the plant and passes on the correct version. Reject the diff. — *ch15, ch18.*

**Artifact:** a gate (`test_split_conserves_total`) that catches the plant.

---

## Track B — 6 hours (6 modules on the seed repo)

### Module 0 · The split, and why it's yours (0:00–0:30)
What charter and harness each are, and why comprehension is the junior's job and not the
agent's. The arrangement is two-sided: you bring comprehension; the team keeps the charter
good enough to onboard you and the harness good enough to guard you. — *ch04–06, Appendix E.*
⟲ **on-ramp:** the split in one sentence — machinery executes, charter is read.

**Artifact:** the comprehension card (see Track A).

### Module 1 · Comprehension is the job (0:30–1:30)
Read code you didn't write and explain it back. Use the agent for the in-flight question a
junior used to interrupt a senior to ask: *what is this pattern, why did this gate block me,
what does this rule mean?* Ask about the codebase and about the charter — the charter is code.
Model `seed/` as a behavioral system: inputs, invariants, outputs. — *ch07, Appendix E.*
**↑ Stretch:** trace one change through `app.py` and `money.py` and predict its blast radius
before running.

### Module 2 · Files that govern (1:30–2:45)
`CLAUDE.md` and rule files steer the agent by what you author. Read the seed's starter
`CLAUDE.md`, then write the money rule the service is missing — the one that will make the
plant illegal. — *ch11, ch11b.*

**Artifact template** (fill in `seed/CLAUDE.md` or a rules file):
```text
# money rules
## Iron laws (agent must refuse to violate)
- Money is integer cents. Never use float to store or compute money.
## Golden rules (override needs a stated reason in the PR)
- Any function that splits or moves money must conserve the total. Ship a conservation test with it.
## Preferences (style; never block a change)
- Format money for display only at the edge (e.g. printing), never mid-calculation.
```

### Module 3 · Legible code is a rule you don't write down (3:15–4:15)
Readable structure is itself a constraint on the agent: code it can follow, it changes
safely; code it can't, it guesses. Take one function in `seed/` and raise its legibility —
naming, shape, a deep interface over a shallow one. — *ch14.* **↑ Stretch:** refactor an
agent-written function for legibility and defend every change out loud.

### Module 4 · Catch the agent wrong (4:15–5:30)
The capstone move. Apply `patches/plausible-but-wrong.diff`; watch the suite stay green.
Reproduce the failure yourself before you trust any fix — split $10.00 three ways and sum the
shares. Find the *cause*, not the symptom: the naive split drops the remainder cents. Then
write the gate that would have caught it — the conservation test from Module 2's golden rule.
— *ch15, ch18, Appendix E.* ⟲ **on-ramp:** run the seed's existing tests first, then the diff.

**Artifact:** `test_split_conserves_total` — a gate that fails on the plant, passes on the fix.

### Module 5 · Your daily loop (5:30–6:00)
Fold it into a repeatable habit sized for real work: read before you merge, lean on the gates,
read *why* a red pipeline caught you. When you can read a codebase and explain it, debug to a
named cause, judge quality on sight, and catch the agent being wrong, you have the foundation
the rest of the book stands on. — *Appendix E.*

**Artifact — your daily-loop checklist:**
```text
BEFORE I MERGE
  [ ] I can explain this diff in my own words (the daily rule).
  [ ] I ran the five questions; nothing failed silently.
  [ ] The change ships with the test that would catch it breaking.
  [ ] A red pipeline taught me something — I read why before I fixed it.
```

---

## Takeaway artifacts
- The comprehension card (all tracks).
- A money rule for the seed service (2hr, 6hr).
- A conservation gate that catches a planted bug (all tracks).
- A personal daily-loop checklist (6hr).

## Instructor notes
- The plant in `seed/patches/` is the emotional core — everyone should feel the "I almost
  shipped that" moment. Protect time for it; it's the whole point of the capstone move.
- The trap works because the seed's own tests only cover divisible totals. Don't spoil that —
  let the room discover that green means "the tests that exist passed," not "correct."
- Mixed room: pair a stronger engineer with a struggling one for Module 1; let the ↑ stretch
  goals absorb fast finishers so you never pace to the ceiling.
- Reference catch: `seed/patches/gate-test.diff` is the conservation gate, for instructors.
- Cut talk before you cut lab.

## Book map
Appendix E ("For the Junior Engineer") is the spine. Foundations ch01–07
(the split, the reliability problem, the repo as a behavioral system); ch14 (the legible
codebase); ch15 (tests and gates).

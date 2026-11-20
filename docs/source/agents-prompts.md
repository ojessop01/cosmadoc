# Writing good requests

What you get from an agent depends heavily on what you ask for.  A short,
vague request makes the agent guess, and it fills the gaps with assumptions
that may be wrong for COSMA or for your work.  A clear request gets you work
you can check and trust, in less time.

This page gives general guidelines for writing requests (often called
prompts).  They apply to every agent and every kind of task.

## The parts of a good request

Most good requests cover the same few things.  Not every request needs all of
them, but the more a task matters, the more of them it should include.

### The goal

Say what you want to achieve, in a sentence, and why, if the reason affects
the choices the agent makes.  "Make it faster so that the full run fits in a
24-hour job" leads to different decisions from "make it faster".

### The context

Give the agent the facts it cannot find out for itself, or would have to guess:

- the exact files, folders, branches, snapshots or job IDs involved;
- the system it runs on: which queue or node type, how many cores, which
  modules;
- the conventions of your field and your group: units, definitions, naming,
  the meaning of quantities with similar names;
- what has already been tried, and what happened.

Facts that apply to every task, such as your project, account, directories and
the COSMA rules, belong in the agent's instructions file (see
[giving the agent the rules](agents-setup.md#giving-the-agent-the-rules)), so you
do not have to repeat them.

### The limits

Say what the agent may and may not do:

- which files or folders it may change, and which it must not touch;
- how much it may run on a login node (threads, memory, time), and what must
  go in a batch job instead;
- anything that needs your approval first: submitting or cancelling jobs,
  deleting, moving or overwriting files, pushing to git, or sending anything to
  other people.

Under the [COSMA rules](agents.md#the-cosma-rules-for-agents), agents must not
submit jobs or delete files on their own initiative, so it helps to say how you
want those steps handled: for example, that the agent should prepare the job
script and give you the command.

### What "done" means

Say how both of you will know the task is finished: a test that passes, a
file that exists, a table of results, a number within a tolerance, a draft for
you to review.  Without this, the agent decides for itself when to stop, which
may be too early or long after it should have.

### How to check it

Ask for the check as part of the task, not afterwards:

- for code, the tests to run, and a comparison with a trusted result;
- for data, checksums or counts on both sides;
- for performance, a fair comparison of timings, and proof that the results did
  not change;
- for writing, the sources each statement comes from.

### What to report

Say what you want to see at the end.  Useful things to ask for:

- the commands that were run, and their actual output, not a summary of it;
- for every number, where it came from: the command, the job ID, the node, the
  commit;
- what was changed, as a list or a diff;
- what was **not** checked, and any assumptions made;
- questions that need your decision.

## How to break up work

### Plan first

For anything larger than a small fix, ask for a plan before any changes are
made: the steps, what each step changes, how each will be tested, the risks,
and the questions that need answering.  Read it, correct it, and only then let
the agent start.  Many agents have a planning mode that investigates without
changing anything.

### Small steps

Ask for one step at a time, and check each one before the next.  Small changes
are easy to review and easy to undo; a large change made in one go hides its
mistakes.  A long task broken into checked steps also suffers less from the
agent losing track of details as the conversation grows (see
[agents forget](agents-safe.md#agents-forget)).

### Measure before changing

For anything to do with speed, memory or scaling, ask for measurements before
any change, and for an estimate of what each change could gain.  This avoids
effort on changes that cannot help.  See
[optimising code with agents](agents-optimisation.md).

### Investigate before fixing

When something is wrong, ask first for the cause, with the evidence, and only
then for a fix.  A fix proposed before the cause is understood often treats a
symptom.

## Asking for reviews

Agents are useful reviewers, and a review asked for explicitly is much more
thorough than the checking an agent does by default.

- Ask the agent to review its own work as if someone else had done it: what it
  did not test, what it assumed, and what would make the result wrong.
- For important work, ask a fresh session to review it, given the goal and the
  result but not the original reasoning.
- Ask for each problem found to be checked against the code or data, and
  marked as confirmed or not, because reviews contain false alarms.

See [critiques and reviews](agents-uses.md#critiques-and-reviews).

## Following up

The first answer is rarely the last.  Good follow-ups:

- **Ask for the evidence** behind any claim you are not sure of.
- **Correct it plainly** when it is wrong, with the right fact, rather than
  hinting.
- **Narrow the task** if the answer is too broad, or widen it if the agent
  stopped short.
- **Start a new session** when a conversation has become long and confused,
  with a short summary of what has been established.

## Requests specific to COSMA

Some details matter more on a shared HPC system than on a laptop.  When they
are relevant, include:

- **where it runs**: a login node for light work, or a batch job, with the
  queue, account and resources;
- **which node type** the code will run on, because the CPUs differ between
  systems (see [compiling for each system](facilities.md#compiling-for-each-system));
- **how much to run at once** on a login node, such as the number of threads;
- **which file system** the data is on, because Lustre behaves differently from
  home and app space (see [Lustre](lustre.md));
- **fair timing** for any benchmark: the same node, nothing else running on it,
  repeated runs.

## Common mistakes

- **Too vague.**  "Fix it" or "make it better" leaves the agent to decide what
  the problem is.
- **Too big.**  A whole project in one request produces a large change that is
  hard to check.
- **No way to check.**  Without a test or a reference, a confident answer and a
  correct answer look the same.
- **Assuming the agent knows your conventions.**  It does not know your units,
  definitions or naming unless you say so, and will guess.
- **Open-ended housekeeping.**  "Clean up my files" invites the agent to delete
  things.  Ask for a list instead, and decide yourself.
- **Accepting a summary instead of output.**  "All tests pass" is a claim;
  the test output is evidence.

## A checklist

Before sending a request that matters, check that it says:

- what you want to achieve;
- which files, data, jobs or code it concerns;
- where and how much it may run;
- what it must not do without asking;
- what "done" means;
- how the result will be checked;
- what it should report, including what it did not check.

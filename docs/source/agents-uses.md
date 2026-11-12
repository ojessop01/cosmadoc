# What agents are good for

Much of the time spent on HPC work is not science.  It goes on finding the
right modules, reading error messages, writing job scripts, working out why a
job failed, moving data between systems, timing things fairly, and fixing small
problems in code written by someone else.  These tasks are slow mainly because
each one needs many small steps, and each step needs something looking up.

Agents are very good at exactly this.  An agent can run a command, read the
output, open the relevant file, and try the next step, many times a minute,
while keeping a record of what it found.  Tasks that used to take an afternoon
of trial and error, or that were so tedious they never got done, become a few
minutes of reading the agent's results and checking them.

The rest of this section describes the kinds of work COSMA users already do
with agents every day.  Each example shows the sort of request that works
well, what the agent does, and what you should check yourself.  In every case
the [COSMA rules](agents.md#the-cosma-rules-for-agents) still apply: the agent prepares
the work, and you approve anything that submits jobs, deletes files or
touches shared data.

For how to phrase requests so that you get reliable results, see
[writing good requests](agents-prompts.md).

## Why it saves so much time

- **It reads everything.**  An agent will read a 2,000-line build log, a
  whole Slurm output file or every function in a module, where a person would
  skim.  It often finds the real cause of a problem in a line you would have
  scrolled past.
- **It does the boring checks.**  Comparing two hundred files, timing a run
  three times, or checking every dataset in a snapshot is tedious for a
  person and easy for an agent.  Checks that used to be skipped get done.
- **It keeps going.**  An agent can try a fix, rebuild, rerun the test and try
  again while you work on something else, and only come back to you with a
  result, or with a question it cannot answer.
- **It knows the tools.**  Agents know the options of `rsync`, `sacct`,
  `git bisect`, `lfs`, `perf` and most compilers, and how to read their
  output, so you do not have to look them up.
- **It writes things down.**  An agent can produce the table, the plot, the
  summary or the bug report at the end, in a form you can share.

## Planning before it starts

For anything bigger than a small fix, ask the agent for a plan before it
changes anything.  A good plan lists the steps, the files it will change, how
it will test each step, what could go wrong, and anything it needs you to
decide.  Reading a plan takes a few minutes; undoing a day of work in the
wrong direction takes much longer.

- Many agents have a planning mode, in which they read and investigate but do
  not change files or run anything that alters the system.  Use it for the
  first look at a new task.
- Ask the agent to write the plan to a file in the project, so you can edit
  it, and so a later session can pick it up.
- Ask it to mark the steps that need your approval, such as submitting jobs,
  deleting files or changing shared data.
- When the plan is agreed, ask it to follow the plan and report against it,
  step by step, and to stop and ask if something does not match the plan.

## Critiques and reviews

Agents are good reviewers, of your work and of their own.  A review asked for
explicitly is usually far more thorough than the checking an agent does by
default.

- **Your code.**  Ask for a detailed review of a script, a module or a pull
  request: bugs, edge cases, unit errors, race conditions, parts that will be
  slow at full size, and missing tests.
- **Your writing.**  Ask for a critique of a draft paper section, a proposal or
  documentation: unclear explanations, claims without support, inconsistent
  notation, and mistakes in the method.
- **Its own work.**  Before you accept a result, ask the agent to review what
  it has just done as if someone else had done it: what it did not test, what
  assumptions it made, and what would make the result wrong.
- **A fresh reviewer.**  An agent reviewing its own work tends to agree with
  itself.  For an important change, start a new session (or a separate review
  agent, if your tool has them), give it the change and the goal but not the
  original reasoning, and ask it to find problems.
- **Checking the review.**  Reviews can contain false alarms.  Ask the agent to
  check each point it raises against the code or data, and to mark which ones
  it confirmed.

## Technical documents for you to review

Agents can write documents that are tedious to write but useful to have, as a
draft for you to correct:

- a **design document** for a change, explaining the options, the one chosen,
  and why;
- a **method note** describing exactly what a piece of analysis does, with the
  equations and the code it corresponds to;
- a **report** on an investigation, such as a performance study or a bug hunt,
  with the measurements, the commands used, and what is still unknown;
- **documentation** for a code: how to install it, how to run it on COSMA,
  and what each option does;
- a **comparison** of two methods, two codes or two runs, with tables and
  plots.

Ask for the facts to come with their source (the command, the file and line,
the job ID), and for anything unchecked to be marked as unchecked.  Treat the
document as a draft: you are responsible for what it says.

## Pages you can open in a browser

Some agents can produce a formatted page, with tables, plots and diagrams,
that you open in a web browser instead of reading text in a terminal.  Claude
calls these *artifacts*, and other tools have similar features.  They are
useful for:

- reports and comparisons that are easier to read with tables and plots;
- a review of changes, with additions and deletions highlighted;
- a dashboard of results from many jobs;
- a document you want to share with a supervisor or collaborators.

Pages like this are usually stored by the company that runs the agent, not on
COSMA.  They are normally private until you share them, but the same care
applies as for anything else you show an agent (see
[data, privacy and accounts](agents-safe.md#data-privacy-and-accounts)).  If the content
must stay on COSMA, ask the agent to write an HTML file in your project
instead, and copy it to your own computer to view it.

## Moving and checking data

Copying data between file systems, or between COSMA and another HPC system,
is simple in principle but fiddly in practice: choosing what to copy,
excluding temporary files, keeping permissions, resuming after a dropped
connection, and checking that everything arrived intact.  Agents make
careful transfers, with checks that are often skipped by hand, the normal way
of working.

An agent can:

- work out what needs to be copied, how many files and how much data, before
  anything moves;
- write an `rsync` command with the right options, run a dry run
  (`rsync -n`) so you can see exactly what will happen, and then run it;
- check the copy afterwards by computing checksums (`sha256sum` or
  `md5sum`) on both sides, comparing the lists, and copying again only the
  files that differ;
- split a very large transfer into parts that can each be resumed, and keep
  a log of which parts are done, so that a dropped connection costs minutes,
  not hours;
- copy files onto Lustre with the right [striping](lustre.md) for large files,
  so that later parallel reads are fast;
- tidy a messy folder into a sensible layout, showing you the plan as a list
  of moves before anything happens.

**Check:** the dry run before the real copy, and the final list of
mismatches (it should be empty).  A transfer to another system still needs
you to log in, so start that connection yourself and let the agent reuse it
(see [SSH, passwords and logins](agents-safe.md#ssh-passwords-and-logins)).

## Writing and checking job scripts

An agent can write a [Slurm](slurm.md) script from a plain description, such
as "4 nodes of cosma8 for 12 hours, 128 MPI ranks per node, output in my run
folder".  It chooses a suitable queue, checks the script with
`sbatch --test-only`, and explains each line.

After a job has run, it can read the output and error files, `sacct` and
`seff`-style summaries, and tell you:

- why a job failed, was cancelled, or ran out of time or memory, with the
  lines from the log that show it;
- how much of the CPU time and memory you asked for was actually used, so
  that you can ask for less next time and wait less in the queue;
- why a job is still waiting (`squeue --me -o "%i %r"`), and what would get
  it started sooner;
- which jobs in a large set failed, and what the failures have in common.

### Campaigns of many jobs

For work split into many similar jobs, such as rendering hundreds of frames,
analysing every snapshot of a simulation or running a parameter scan, an agent
can:

- turn a loop of separate jobs into one [job array](sbatch.md);
- write the job so that each task skips work that is already done, so a
  failed array can be resubmitted without repeating finished tasks;
- check a few tasks first, then the rest;
- watch the array, collect the tasks that failed, find the cause, and prepare
  a resubmission of only those tasks;
- check that the outputs are all present and complete at the end.

Under the COSMA rules, you approve each submission, and the agent does not
resubmit failed jobs on its own.

## Working with simulation output

Agents are useful for the many small steps around the analysis itself:

- finding which snapshots, catalogues or fields exist, and which contain the
  quantity you need, before writing any analysis code;
- matching outputs between two runs or two codes, for example by redshift
  rather than by snapshot number when the output times differ;
- reading large [HDF5](https://www.hdfgroup.org) files in pieces rather than
  all at once, so that analysis fits in memory;
- comparing catalogues from two different tools, and explaining why their
  numbers differ (different definitions, units or selections);
- reproducing a number or a figure from a paper, and finding where your
  calculation differs from the published method;
- making a set of plots in the same style from many outputs.

**Check:** that the agent used the quantity you meant (for example the
right mass definition, or the right units and factors of the Hubble
constant), not just one with a similar name.

## Finding and fixing problems

- **Crashes and hangs.**  Reading a traceback, a core dump summary or an MPI
  error, and finding the line that caused it.  For hangs, finding which ranks
  or threads are waiting and what for.
- **Wrong results.**  Comparing two runs, two versions of a code, or a result
  against a published value, and finding where they first differ.
- **Errors after an update.**  Recognising when code relies on a private or
  changed function in a library such as NumPy, and switching it to the
  supported one.
- **Notebooks that no longer run.**  Running a notebook from top to bottom,
  fixing each cell that fails, and guarding against missing values (`NaN`)
  that break later cells.
- **Explaining the fix.**  Writing a short account of what was wrong, why, and
  how it was fixed, which is useful for your own notes or for the code's
  maintainers.

## Repetitive and bulk work

Agents are well suited to work that is easy but tedious:

- making the same change across many files, or many simulation run folders;
- turning a Jupyter notebook into a script that can run as a batch job, with
  its settings as command-line options;
- writing tests for existing code, running the test suite, and fixing the
  failures;
- running formatting and style checks (`ruff`, `black`, `clang-format`) and
  fixing what they find;
- reading a set of log files and collecting the numbers into one table;
- writing or updating documentation, README files and comments for your own
  code;
- tidying a git repository: finding merged branches and worktrees that are no
  longer needed, for you to remove.

## Writing for other people

An agent can turn what it found into something you can send or publish:

- a **bug report** for a code's maintainers, with the exact file and line, a
  small example that shows the problem, and a suggested fix;
- a **pull request description** that explains the change, how it was tested,
  and what reviewers should look at;
- a **summary for cosma-support** of a problem, with the time, the command,
  the job ID and the relevant lines of the log, and nothing else;
- a **summary of the day's work**, a results table, or notes for a meeting.

**Check:** read everything before it is sent.  Agents should not send
emails, post comments or open pull requests without you reading them first
(see [data, privacy and accounts](agents-safe.md#data-privacy-and-accounts)).

## Understanding a system or a codebase

- Explaining what an unfamiliar code does, where a given quantity is
  calculated, or how a parameter file is used.
- Finding out how something on COSMA is set up, from its documentation and
  from read-only commands such as `scontrol show partition`, `sinfo`,
  `findmnt`, `module show` or `lfs df`.
- Explaining an error message from a tool you have not used before.
- Summarising a paper or a method, and comparing it with what your code does.

## Your own tools

Many people collect small scripts over the years: shortcuts for checking jobs,
SSH settings for several machines, scripts that check disk use or summarise
the queue.  Agents are good at writing and maintaining these, and at fixing
them when something on the system changes.  Keep such tools in your own
directories, keep them in git, and remember that anything that runs
automatically (a scheduled job, a script that watches something) must follow
the same rules as the agent: no retry loops, no constant polling, and no
logins.

## An example from start to finish

For a worked example, from measuring to reporting, see [a worked example](agents-optimisation.md#a-worked-example).

## What agents are less good at

- **Judging the science.**  An agent can make a plot or fit a curve, but you
  decide whether the result makes sense.
- **Long tasks without supervision.**  Over a long session, agents lose track
  of details (see [agents forget](agents-safe.md#agents-forget)).  Several short tasks, each
  checked, work better than one long one.
- **Knowing your conventions.**  Agents do not know your group's units,
  definitions or naming unless you tell them, and they will guess.
- **Steps where a mistake would be a disaster**, such as deleting or
  overwriting irreplaceable data.  Do these yourself.
- **Knowing when they are wrong.**  An agent may sort numbers as text, call a
  function with the wrong arguments, or misread a log, and then report the
  result confidently.  Good agents catch many of their own mistakes when asked
  to check their work, but not all of them.

## Getting the most out of an agent

- **Be specific.**  Give the paths, the queue, the module versions and what
  "done" looks like.  "Make it faster" gets worse results than "the
  `density` step takes 40 minutes on 32 cores; find out why".
- **Ask for a plan first** for anything large, and agree it before the agent
  starts.
- **Ask it to check its own work**: run the tests, compare checksums, show the
  output, and say what it did not check.
- **Ask for numbers with their source**: which node, which commit, which
  input, and the command that produced them.
- **Give it the COSMA facts** in its instructions file (see
  [giving the agent the rules](agents-setup.md#giving-the-agent-the-rules)), so it does not
  have to rediscover them in every session.
- **Keep it on small test cases** while it develops something, and run the
  real thing in a batch job.
- **Give it independent tasks in parallel** when you can, for example
  building one thing while a job runs, but keep each one small enough to
  check.

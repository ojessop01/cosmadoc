# Writing code with AI agents

Agents can write, change and translate code far faster than by hand, but the code is only as good as the request and the checks.  This page describes how to get good code from an agent on COSMA: scripts, Python, job scripts, tests, documentation and porting, and the mistakes agents commonly make here.

For requests you can copy and adapt, see the
[example requests](agents-prompts.md) page.

## How to ask for code

Agents write code quickly, but the result is only as good as the request, and
only as trustworthy as the checks.

- **Say what the code must do, and how you will know it works.**  "Write a
  script that reads every snapshot in this folder and writes the total stellar
  mass inside 30 kpc of each halo to one HDF5 file; check it against the
  values in `reference.csv` for the first three snapshots" is far better than
  "write a script to get stellar masses".
- **Give it the real inputs.**  Point it at a small, real example of the input
  files, so it can read the actual structure instead of guessing field names
  and units.
- **Work in small steps.**  Ask for one function, test it, then the next.  Large
  changes made in one go are hard to review and hard to undo.
- **Ask for tests with the code**, and for the tests to be run before it says
  the code works.
- **Match the existing code.**  Tell it to follow the style and structure of the
  surrounding code, use the project's own functions rather than writing new
  ones, and not to make unrelated changes.
- **Read the result.**  Ask it to explain anything you do not understand, and
  review the changes (`git diff`) before committing them.

## Bash scripts

Shell scripts glue most HPC work together: job scripts, data transfers,
pipelines and small tools.  They are also easy to get subtly wrong, and a bash
mistake can delete the wrong files.  Agents write good scripts when asked
for the right things, so ask for these explicitly.

### What a good script looks like

```
#!/bin/bash
# Copy finished snapshots to the archive folder and record their checksums.
set -euo pipefail

src=/cosma8/data/PROJECT/USER/run42/snapshots
dest=/cosma8/data/PROJECT/USER/archive/run42
log=$dest/copy.log

mkdir -p "$dest"
for f in "$src"/snap_*.hdf5; do
    name=$(basename "$f")
    if [ -e "$dest/$name" ]; then
        continue                      # already copied: safe to run again
    fi
    cp "$f" "$dest/$name.partial"
    mv "$dest/$name.partial" "$dest/$name"
    sha256sum "$dest/$name" >> "$dest/checksums.txt"
    echo "$(date '+%F %T') copied $name" >> "$log"
done
```

The things to ask for, and why:

- **`set -euo pipefail`** stops the script at the first failed command (`-e`),
  at the first use of an unset variable (`-u`), and when any part of a pipe
  fails (`pipefail`).  Without it, a script carries on after errors and can do
  damage with half-finished results.
- **Quote every variable**: `"$f"`, not `$f`.  Unquoted variables break on
  file names with spaces, and an empty unquoted variable can turn a command
  into something very different.
- **Absolute paths**, set once at the top.  Scripts are run from different
  directories, by you, by Slurm and by agents.
- **Safe to run again.**  Skip work that is already done, so that a script
  stopped half way can simply be run again.
- **Write to a temporary name, then rename.**  A file that only appears when it
  is complete can never be left half-written (see
  [code that breaks on COSMA](#code-that-breaks-on-cosma)).
- **A log with times**, so you can see what happened later.
- **Guard dangerous commands.**  Never `rm -rf "$dir/"` where `$dir` might be
  empty, because the command then deletes from the top of the file system.
  Use `"${dir:?}"`, which stops the script if `dir` is empty, and prefer
  deleting specific files over whole directories.
- **A dry-run option** for scripts that move or delete things, which prints
  what it would do without doing it.
- **Limit output that can grow without end**: send long logs through
  `tail -n 200`, or rotate them, as the COSMA rules require.

### Checking scripts

[ShellCheck](https://www.shellcheck.net) finds most common bash mistakes,
such as missing quotes and commands that do not do what they look like.  It
is not installed on COSMA, but you can install it into a Python virtual
environment with `pip install shellcheck-py`, and then run
`shellcheck script.sh`.  Ask the agent to run it on every script it writes.

Also ask the agent to run `bash -n script.sh`, which checks the syntax without
running anything, and to test scripts that move or delete files on a copy of
a small folder first.

### Bash, sh and zsh

Ask for scripts that start with `#!/bin/bash` and use bash, not whichever
shell happens to be running.  `/bin/sh` scripts cannot use bash features such
as arrays and `[[ ]]`, and zsh treats variables and quotes differently (see
[if your login shell is not bash](agents-setup.md#if-your-login-shell-is-not-bash)).

### Scripts that run automatically

A script run by `cron`, a scheduled job or another program does not have your
normal environment: it may have no modules, a short `PATH`, a different
directory and no terminal.  A script that works when you run it can fail, or
silently produce wrong results, when run automatically.  Ask the agent to set
everything the script needs inside the script itself, and to test it in a
clean environment, for example
`env -i HOME=$HOME PATH=/usr/bin:/bin bash script.sh`.

## Python

### Scripts and packages

- **Use a virtual environment in your app space** (see [Python](python.md)),
  with the packages the code needs listed in a `requirements.txt` or
  `pyproject.toml`, so the environment can be made again.
- **Use command-line options** (`argparse`) for paths and settings, rather than
  editing the script for each run.  This also makes it easy to run from a job
  script.
- **Write functions that can be tested**, rather than one long script, and
  keep the part that reads the command line separate from the work.
- **Set random seeds**, so that runs can be repeated and compared.
- **Check and format the code**: `ruff check` and `ruff format` (or `black`),
  installed with `pip` into your virtual environment.  Ask the agent to run
  them and fix what they find.

### Notebooks

Agents can work with Jupyter notebooks, but notebooks are hard to review and
easy to run out of order.

- Ask the agent to run the notebook from top to bottom in a fresh kernel, and
  fix every cell that fails, before calling it working.
- For anything that takes a long time or runs on many inputs, ask it to turn
  the notebook into a script with command-line options, that you can run as a
  batch job.
- Keep the notebook's outputs out of git if they are large.

## Job scripts

See [writing and checking job scripts](agents-uses.md#writing-and-checking-job-scripts)
for what agents can do, and [Slurm and agents](agents-safe.md#slurm-and-agents)
for the rules.  When an agent writes a job script, ask for:

- the `#SBATCH` lines for account, queue, time, nodes, tasks and memory;
- `module purge` followed by every `module load` the program needs, so the
  job does not depend on your login settings;
- `set -euo pipefail` and absolute paths, as for any bash script;
- separate output and error files, named with the job ID (`%j`);
- `export TMPDIR=/tmp`, and `OMP_NUM_THREADS` set from
  `$SLURM_CPUS_PER_TASK`;
- a short comment at the top saying what the job does.

## Tests

Tests are what make agent-written code trustworthy.  Ask for them with every
piece of code, and ask for them to be run before the agent says the code
works.  Agents write tests quickly, which removes the usual excuse for not
having them.

### What to test

- **Known answers.**  Cases where you know the right result: an analytic
  solution, a published value, a conservation law (mass, energy or momentum
  should not change), or a simple case you can work out by hand.
- **Regression tests.**  Save the output of the current, trusted version on a
  small input, and check that new versions give the same answer, exactly or
  within a stated tolerance.  This is the most important kind of test when an
  agent changes existing code, because it catches changes nobody intended.
- **Comparison with another method.**  A fast approximate method can be tested
  against a slow exact one on a small problem, for example a tree or mesh
  method against direct summation.
- **Properties that must always hold.**  Results that should be symmetric,
  non-negative, normalised, or independent of the order of the input.

### Edge cases

Most bugs are in the unusual cases, not the typical one.  Ask the agent to list
the edge cases for the code and to test each of them, for example:

- **Empty or tiny inputs**: no particles, one particle, a halo with no stars, an
  empty file, a file with one snapshot.
- **Boundaries**: particles exactly on the edge of a cell or of a periodic box,
  values just inside and just outside a cut, the first and last element of an
  array, the last partial chunk of a file.
- **Periodic boxes**: distances and positions that wrap around the box, and
  objects that sit across the boundary.
- **Extreme values**: very large and very small numbers, zero, negative values
  where only positive ones are expected, and values that overflow single
  precision.
- **Missing or bad data**: missing fields, `NaN` and infinity, units different
  from those expected, and files written by an older version of a code.
- **Parallel runs**: one thread or rank against many, more ranks than pieces of
  work, and an uneven split of work.
- **Types**: integers where floats are expected, 32-bit indices that overflow
  for more than about two billion particles, and arrays stored in a different
  order.

### Humans must check the tests

A test is only useful if it tests the right thing, and agents can write tests
that pass without proving anything.  Common problems are tests that check the
code against itself, tolerances so loose that any answer passes, expected
values copied from the code's own output without being checked, and tests
quietly changed or skipped to make them pass.

So **a person must review the tests**, as carefully as the code:

- Read each test, and check that its expected values come from somewhere
  independent of the code, such as a calculation, a paper or the old trusted
  version.
- Check that the tolerances are justified, and not just large enough to pass.
- Make sure the important edge cases for your problem are covered.  The agent
  does not know which cases matter most for your science.
- Make sure that a failing test is never "fixed" by changing the expected
  value or skipping the test, unless you have agreed that the test was wrong.
- Break the code on purpose now and then, for example by changing a sign, and
  check that a test fails.

### Running tests on COSMA

- Use `pytest` for Python, and the code's own test system (such as `ctest`) for
  compiled code.
- To run a large Python test suite in parallel, use `pytest -n 8` (from the
  `pytest-xdist` package) with `OMP_NUM_THREADS=1`, so the tests do not each
  start many threads.
- Keep the quick tests quick, so they get run after every change, and run long
  or large tests in a batch job.
- Test on the kind of node the code will run on: a build that passes on a
  login node may fail on a compute node with a different CPU.

## Documentation

Agents are good at writing documentation, which is often the part of a
project that never gets done.  They can write:

- **README files**: what the code does, how to install it on COSMA (modules,
  virtual environment), how to run it, and a small example.
- **Comments and docstrings**: what each function does, its inputs and outputs,
  their units, and any assumptions, in the style the project already uses
  (for example NumPy-style docstrings for Python, or Doxygen comments for
  C++).
- **How to run it on COSMA**: an example job script, the queue and resources
  it needs, and how long it takes.
- **Method notes**: the equations a piece of analysis uses, and the parts of
  the code that implement each one.
- **Change logs**: what changed between versions, and why.
- **Notes for the next person**, or for yourself in six months: known problems,
  decisions that were made, and things that were tried and did not work.

As with tests, **a person must check the documentation**.  Agents describe
what they think the code does, which is not always what it does, and they can
make up options, defaults or units that look plausible.  Check every command
and example in the documentation by running it, check units and definitions
against the code, and remove anything you cannot confirm.  Keep documentation
next to the code, in the same git repository, so that it is updated with it.

## Porting code to another language

Agents are very good at translating code from one language to another, and
this is one of the tasks where they save the most time.  Common reasons on
COSMA:

- moving away from **IDL or MATLAB**, which need licences, to Python;
- moving a slow **Python** analysis to C, C++ or Fortran, or speeding it up with
  Numba;
- modernising old **Fortran 77**, or **Python 2** code;
- moving **CUDA** code to a portable library such as Kokkos, so it can run on
  different GPUs (COSMA has `kokkos` modules for NVIDIA and AMD GPUs and for
  CPUs);
- turning a collection of shell scripts into one Python program.

### How to port safely

1. **Save reference results from the original code** first, on small but
   realistic inputs, including the intermediate values of each main step if
   you can.  You will compare against these at every stage.
2. **Port one function or one stage at a time**, and compare its output with
   the original before moving on.  Translating a whole program at once and
   comparing only the final answer makes differences very hard to find.
3. **Decide the tolerance in advance.**  A port may not give bit-identical
   results, because of different floating-point order or libraries.  Agree
   what difference is acceptable, and ask the agent to report the largest
   difference it sees.
4. **Keep the original** until the new version has been checked on real
   inputs, and record any differences you accepted.

### Differences that cause wrong results

Ask the agent to check each of these explicitly, because a translation can
look correct and still be wrong:

- **Array indexing.**  Fortran, MATLAB, IDL and Julia count from 1; C, C++ and
  Python from 0.  Off-by-one errors are the most common porting bug.
- **Array order.**  Fortran, MATLAB and IDL store arrays column by column;
  C and NumPy store them row by row by default.  Loops in the wrong order are
  correct but slow, and reshaping in the wrong order gives wrong answers.
- **Number types.**  IDL's default floating-point type is single precision,
  and integer division differs between languages (`7/2` is 3 in C, Fortran and
  Python 2, but 3.5 in Python 3).
- **Library conventions.**  FFT normalisation and the order of frequencies,
  interpolation at the edges of the data, the definition of standard deviation
  (dividing by N or N-1), and angle units all vary between libraries.
- **Random numbers.**  Different languages give different random sequences for
  the same seed, so results that use random numbers can only be compared
  statistically.
- **Units and constants.**  Make sure physical constants and unit conversions
  are taken from the same source in both versions.

### Wrapping instead of porting

Sometimes it is better to keep a fast, trusted routine in its original
language and call it from Python.  Agents can set this up with `f2py` (part of
NumPy, for Fortran), Cython, `pybind11` (for C++) or `ctypes` (for C).  This
keeps the tested code and adds a convenient interface.

## Changing existing code

- **Commit before the agent starts**, so you can see and undo every change.
- **Make sure tests exist first.**  If the code has none, ask the agent to write
  regression tests for the current behaviour before changing anything.
- **Refactor in small steps**, running the tests after each one.
- **No unrelated changes.**  Ask the agent not to reformat, rename or "tidy"
  code outside the task, because this hides the real changes in the diff.
- **Check every user of a changed quantity.**  If the agent changes the units,
  sign or meaning of a variable, ask it to find and check every place that uses
  it.

## Version control

- Work on a **branch** for each task, and commit often with clear messages.
- For two versions side by side, for example to compare speed, use a
  `git worktree` rather than a second clone.
- Ask the agent to show `git status` and `git diff` before committing, and
  never to use `git push --force` or `git reset --hard` without your
  agreement.
- Remove branches and worktrees once their work is merged
  (`git worktree list`, `git worktree remove`).

## Building and installing software

Getting a code to build on a new system usually means trying modules and
options until the errors stop.  An agent can work through this quickly:

- read the code's build instructions and find which COSMA modules provide what
  it needs, using `module avail` and the [list of modules](modulelist.md);
- put the `module load` lines in the right order, with the compiler first and
  the libraries that need it afterwards;
- read long compiler and linker errors, find the *first* real error rather
  than the hundreds that follow from it, and fix its cause;
- find out why a library is not found at run time (`ldd`, `LD_LIBRARY_PATH`,
  `rpath`);
- build the same code with different compilers or MPI libraries and compare
  them;
- write a short build script, so the same build can be repeated exactly next
  time.

### Building for different nodes

COSMA's nodes have [different CPUs](facilities.md#compiling-for-each-system),
and some have GPUs.  A program built for one may not run on another.  Agents
are good at managing several builds of the same code:

- recognising that `Illegal instruction` means the program was built for a
  CPU with instructions (such as AVX-512) that the current node does not have,
  rather than a bug in the code;
- making separate builds for AVX2 and AVX-512 nodes, and checking that they
  give identical results;
- building for a GPU node, which usually means finding the right CUDA or other
  GPU modules and compiling where they are available;
- choosing the right build at run time, for example by checking for
  `avx512f` in `/proc/cpuinfo` in the job script.

For example:

```{admonition} Example request
:class: tip

This program crashes with "Illegal instruction" on cosma8 but works on login5c. Find out why, and make a build that runs on both.  Check that both builds give the same output on the small test case.
```

## Code that breaks on COSMA

Agents write code that works on a typical laptop or cloud server.  Some
common choices break on COSMA:

- **`-march=native`.**  This builds code for the CPU of the machine you
  compile on.  Built on an AVX-512 login node, the program stops with
  `Illegal instruction` on nodes without AVX-512, such as COSMA8.  See
  [compiling for each system](facilities.md#compiling-for-each-system).
- **`srun` with Open MPI.**  On COSMA, start Open MPI programs with `mpirun`.
  `srun` does not start them correctly.
- **`TMPDIR` on a network file system.**  If `TMPDIR` points to app space or
  home in a job (it is passed on from your login), Open MPI warns that its
  shared-memory files are on a network file system, and can run slowly.  Set
  `export TMPDIR=/tmp` in the job script.
- **Binding with Intel MPI.**  Wrapping `numactl` around `mpirun` does not
  confine Intel MPI ranks, because Intel MPI sets its own binding.  Put
  `numactl` after `mpirun` instead, so that it applies to each rank, and check
  where the ranks really run.
- **Writing output with `>` in automated jobs.**  `command > file` empties the
  file before the command starts.  If the command then fails, the file is left
  empty, and a scheduled job may publish or commit the empty file.  Write to a
  temporary file and rename it only when the command succeeded.

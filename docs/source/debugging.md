# Debugging

This page covers finding the cause of crashes, hangs, memory errors and
wrong results in your own programs on COSMA.  For jobs that fail for reasons
outside your program, such as running out of time or memory, see
[job problems](jobproblems.md).  For speed, see [code performance](codeperformance.md).

## Before you start

- **Reproduce the problem with a small case**, on as few cores as possible,
  ideally on a login node or in a short [interactive session](interactive.md).
  Debugging a 128-rank, 12-hour job directly is slow and expensive.
- **Build a debug version**: compile with `-g` (debugging information) and
  without heavy optimisation (`-O0` or `-Og`), so that the debugger can show
  your source code and variables.  Keep the normal build separately.
- **Use the same modules** to build and run.  Many crashes after a change are
  caused by a program built with one compiler or MPI library and run with
  another (see [modules](modules.md#modules-in-job-scripts)).
- **Read the error output in full.**  The first error message is usually the
  real one; the rest often follow from it.

## Which tool to use

| Problem | Tool |
| ------- | ---- |
| The program crashes (segmentation fault, abort) | [gdb](#gdb), or [DDT](#linaro-ddt) for MPI programs |
| Memory errors: writing past the end of an array, using freed memory | [AddressSanitizer](#sanitizers), [Valgrind](#valgrind) |
| Different results each run, with threads | [ThreadSanitizer](#sanitizers), [Intel Inspector](codeperformance.md#inspector) |
| The program hangs | [See where it is stuck](#hangs) with `gstack` or `gdb` |
| An MPI program crashes or hangs on some ranks | [DDT](#linaro-ddt) |
| A Python program crashes or hangs | [Python](#python) |
| Wrong results | Compare with a trusted version, step by step (see [wrong results](#wrong-results)) |

## gdb

`gdb` is installed on every node.  Run your program under it:

```
gcc -g -O0 myprogram.c -o myprogram
gdb --args ./myprogram myinput
```

At the `(gdb)` prompt:

| Command | What it does |
| ------- | ------------ |
| `run` | Start the program |
| `bt` | Show where it stopped (the backtrace), after a crash |
| `frame 2` | Look at level 2 of the backtrace |
| `print x` | Show the value of the variable `x` |
| `break myfile.c:120` | Stop at line 120 |
| `next`, `step` | Run one line, stepping over or into function calls |
| `continue` | Carry on to the next breakpoint |
| `quit` | Leave gdb |

To run a program under gdb without typing anything, for example in a batch
job, and print the backtrace if it crashes:

```
gdb -batch -ex run -ex bt --args ./myprogram myinput
```

### Core files

When a program crashes, Linux can save its memory as a "core file" for
debugging later.  On COSMA, core files are collected by the system, and users
cannot read them (`coredumpctl` reports "insufficient permissions").  Run the
program under `gdb`, as above, or use [DDT's offline mode](#linaro-ddt),
instead.

## Sanitizers

The GNU and LLVM compilers can add checks to your program that stop it at the
first error, and report exactly where it happened.  They are much faster than
Valgrind, so they can be used on bigger cases.

**AddressSanitizer** finds memory errors, such as writing past the end of an
array, or using memory after it has been freed:

```
gcc -g -fsanitize=address myprogram.c -o myprogram
./myprogram
```

It stops with a report such as `ERROR: AddressSanitizer: heap-buffer-overflow`,
followed by the line that made the bad access and the line that allocated the
memory.

**ThreadSanitizer** finds data races, where two threads use the same memory
without synchronisation, which gives results that change from run to run:

```
gcc -g -fopenmp -fsanitize=thread myprogram.c -o myprogram
OMP_NUM_THREADS=4 ./myprogram
```

It reports `WARNING: ThreadSanitizer: data race`, with the two lines involved.

**UndefinedBehaviorSanitizer** (`-fsanitize=undefined`) finds integer
overflow, invalid shifts and similar errors.

Use sanitizers on a debug build only: they make programs slower and use more
memory.  Sanitizers and MPI can be combined, but the MPI library itself may
cause some reports; ignore those that are not in your code.

## Valgrind

Valgrind is slower than the sanitizers, but needs no recompiling (although
`-g` gives better reports).  The system `valgrind` needs no module.

```
valgrind --leak-check=full ./myprogram
```

The report ends with an `ERROR SUMMARY`, and lists each error with the line
that caused it.  `definitely lost` memory is a memory leak.  See also
[Valgrind on the performance page](codeperformance.md#valgrind).

## Linaro DDT

DDT is a graphical debugger for MPI and OpenMP programs, which shows every
rank and thread at once.  Use version 25.1.1; the default module (23.1.0)
does not start.

```
module load allinea/ddt/25.1.1
```

### Interactively

Start DDT on a login node, through [x2go](x2go.md), and launch your program
from it:

```
ddt mpirun -np 4 ./myprogram
```

DDT stops all ranks at the start.  Press Play to run them; when one crashes,
DDT shows where, on every rank.

### Offline, in a batch job

DDT can run a program without a window, and write a report of where each rank
stopped and why.  This works in a batch job:

```
ddt --offline --output=ddt_report.html mpirun -np 4 ./myprogram
```

Open `ddt_report.html` in a web browser.  It shows the messages, errors and
backtraces from every rank.

## Hangs

If a program seems stuck, first check whether it is using CPU (`top -u $USER`,
or [`cjobload`](system.md#cjobload) for a job).  A program at 0% CPU is waiting
for something: input, a file, or another MPI rank.

To see where a running program is, without stopping it for long:

```
gstack PID
```

prints the backtrace of every thread of process `PID`.  For a batch job, run
it on the job's node from a login node:

```
srun --jobid=JOBID --overlap gstack PID
```

Run `gstack` a few times, a few seconds apart.  If the backtrace is the same
each time, that is where the program is stuck.  For MPI programs, compare
ranks: a hang is often one rank waiting in `MPI_Recv` or a collective
(`MPI_Allreduce`, `MPI_Barrier`) that another rank never reaches.

You can also attach `gdb` to a running process with `gdb -p PID`, look around
with `bt`, and `detach` to let it carry on.

## Python

- **A Python error** prints a traceback: the last line is the error, and the
  lines above show how the program got there.  Read it from the bottom up.
- **To stop at an error and look around**, run `python -m pdb myscript.py`, or
  add `breakpoint()` where you want to stop.
- **A Python program that crashes without a traceback** (a "segmentation
  fault") usually has a problem in a compiled library.  Running
  `python -X faulthandler myscript.py` prints where it was in Python when it
  crashed.
- **A hanging Python program**: `py-spy dump --pid PID` (installed with
  `pip install py-spy`) shows where every thread is.

## Wrong results

When a program runs but gives the wrong answer:

1. **Find a trusted result** to compare with: an older version, a different
   code, an analytic case, or a published value.
2. **Make the case small**, so that a comparison takes seconds.
3. **Find the first difference**: compare intermediate values, step by step,
   rather than only the final answer.  The first step that differs is where to
   look.
4. **Change one thing at a time**, such as the compiler, the optimisation level
   or the number of threads or ranks.  If the answer changes with the number of
   threads or ranks, suspect a data race or a missing communication.  If it
   changes with optimisation, suspect uninitialised variables or undefined
   behaviour (try the [sanitizers](#sanitizers)).
5. **If the code is in git**, `git bisect` finds the commit that introduced the
   problem.

## Getting help

If you are stuck, contact cosma-support with the details listed on the
[contact](contact.md) page: the exact error, the job ID, the modules, and how
to reproduce the problem.

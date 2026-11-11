# Example requests for AI coding agents

This page collects example requests (often called prompts) for common tasks on
COSMA, with the largest part on [optimising code](#optimising-code-on-cosma).  Copy them, and change the paths, names and numbers to match your work.
Words in capitals, such as `PROJECT` and `USER`, are placeholders.

Each example follows the [COSMA rules for agents](agents.md#the-cosma-rules-for-agents):
the agent investigates, prepares and checks, and **you** submit jobs, delete
files and send anything to other people.

## What makes a good request

The examples on this page share a few features.  A request that has them gets
much better results than a short one.

- **The goal, in one sentence**, and why you want it, if that affects the
  choices.
- **The exact inputs**: paths, file names, the snapshot or job ID, the branch.
- **The limits**: which node or queue, how many threads, how long it may run,
  and which files it must not touch.
- **What "done" means**: a test that passes, a table, a file, a number.
- **How to check it**: compare with a reference, run the tests, show the
  output.
- **What it must not do on its own**: submit jobs, delete files, push to git,
  send messages.
- **What to report**: the commands it ran, their output, and what it did not
  check.

### Short and better requests

| Short request | Better request |
| ------------- | -------------- |
| "Fix my job." | "Job 1234567 failed after 2 minutes.  Read `run.1234567.err` and `run.1234567.out` and `sacct -j 1234567`, tell me why it failed with the lines that show it, and propose a fix to `run.sh`.  Do not resubmit it." |
| "Make this faster." | "`analyse.py` takes 20 minutes per snapshot.  Profile it on `test_snapshot.hdf5` with `cProfile`, tell me which three functions take the most time and what share of the total each takes, and estimate the most that speeding up each one could save.  Do not change any code yet." |
| "Write tests." | "Write `pytest` tests for `binning.py`: compare with the hand-worked cases in `notes/binning.md`, and test empty input, a single particle, particles exactly on bin edges and on the periodic boundary.  Run them and show the output.  Do not change `binning.py`." |
| "Copy my data to the other machine." | "I want to copy `/cosma8/data/PROJECT/USER/run42` to `OTHER:/scratch/USER/run42`.  First tell me the number of files and total size, and show me an `rsync` dry run.  Wait for my go-ahead before copying." |
| "Clean up my files." | "List everything I own in `/tmp` and `/dev/shm` on this node, and folders in `/cosma/apps/PROJECT/USER/tmp` older than 7 days, with their sizes.  Do not delete anything; I will choose what to remove." |

## Optimising code on COSMA

These requests are the core of using agents for performance work on COSMA.
They are written for COSMA's hardware and tools, and each one measures before
changing anything and checks the results after.  See
[optimising code with agents](agents-optimisation.md) for the background.

A few COSMA facts that many of these requests rely on:

- Nodes have different CPUs (see [compiling for each system](facilities.md#compiling-for-each-system)).
  `scontrol show node` describes a cosma8 node as 8 "sockets" of 16 cores
  (128 cores), a cosma5 node as 8 of 32 (256 cores), and a cosma7 node as 2 of
  14 (28 cores).  On the AMD nodes these "sockets" are groups of cores that
  share memory (NUMA domains), so where threads and memory are placed matters.
- Timing runs must not share a node with other work.  Use a whole-node queue,
  or a per-core queue such as `cosma8-serial` with enough cores that you know
  what else is on the node.
- Profiling and timing on a login node are unreliable: use a batch job, which
  you submit.

### Understanding the starting point

```
Before any optimisation, describe how ./sim currently performs.  Write one
job script, for me to submit, that runs tests/medium.yml on a whole cosma8
node with 64 MPI ranks and 2 threads each, and records: total and per-stage
times from the code's own timers, perf stat (instructions per cycle, cache
misses), and peak memory per rank.  Afterwards, summarise the results in a
table and say whether the code looks limited by computation, memory
bandwidth, communication or file I/O, with the evidence for each.
```

```
Show me the layout of a cosma8 compute node as my job sees it: run
likwid-topology and numactl --hardware in a short job on cosma8-serial with
16 cores, and explain the NUMA domains, cache sizes and core numbering, and
what they mean for how I should place 128 threads or ranks.
```

### Finding hot spots

```
Profile ./sim on tests/medium.yml with perf record -g in a batch job on one
cosma8 node, 32 threads, OMP_PROC_BIND=close and OMP_PLACES=cores.  Write the
job script for me to submit.  Afterwards, use perf report to list the ten
functions with the most time, with their share of the total, and for the top
three show the source lines that take the time.
```

```
Profile the MPI run of ./sim on 2 cosma8 nodes with Linaro MAP
(module allinea/ddt/25.1.1).  Write the job script, using map --profile so
it runs without a window, for me to submit.  Afterwards, export the .map file
with map --export=profile.json, and tell me how the time splits between
computation, MPI communication and file I/O, and which ranks are slowest.
```

```
My Python analysis takes 40 minutes per snapshot.  Install py-spy and
line_profiler into /cosma/apps/PROJECT/USER/venvs/analysis, then profile
analyse.py on tests/snap_small.hdf5 on the login node with at most 4 cores.
Show a py-spy flame graph saved as profile.svg, and the line-by-line times of
the three slowest functions.
```

### Measuring what limits it

```
Use LIKWID to find out whether the density loop is limited by memory
bandwidth.  Load gnu_comp/14.1.0 and likwid/5.5.1, list the available
performance groups on a cosma8 compute node with likwid-perfctr -a, and use
the memory bandwidth and floating-point groups with likwid-perfctr -C on 16
pinned cores, in a job script for me to submit.  Compare the measured
bandwidth with the node's limit (measure it with likwid-bench), and tell me
what share of it the loop reaches.
```

```
Check whether the main loops in src/ are vectorised.  Rebuild with
-O3 -march=znver2 -fopt-info-vec-missed and give me a list of the loops in
the five hottest functions (from the perf profile in profile-report.md) that
were not vectorised, with the compiler's reason for each, and what change would
let each one vectorise.  Do not change the code yet.
```

### Threads, NUMA and placement

```
./sim stops speeding up beyond 16 threads on a cosma8 node.  Write a job
script, for me to submit, that runs it on 1, 2, 4, 8, 16, 32, 64 and 128
threads, three times each, with OMP_PLACES=cores and OMP_PROC_BIND=close,
and again with spread.  Afterwards, plot the speed-up against threads for both,
with the ideal line, and explain where the curves flatten.  Relate this to the
node's 8 NUMA domains of 16 cores.
```

```
Check whether the large arrays in src/particles.c are first written by one
thread.  If they are, threads in other NUMA domains will read them slowly.
Show me where each array is first written, and propose a change that
initialises them in parallel with the same loop pattern and schedule as the
main loop.  Then, after I agree, make the change and compare the timing at 64
and 128 threads with the old version, checking the output is identical.
```

```
Find the best layout of MPI ranks and OpenMP threads for ./sim on one
cosma8 node: try 128x1, 64x2, 16x8 and 8x16 (ranks x threads), with ranks
bound to NUMA domains using mpirun --map-by ppr:N:numa:PE=T --bind-to core and
--report-bindings.  Put all runs in one job script for me to submit, then give
me a table of times and check from the binding report that each run was placed
as intended.
```

### Compilers and build options

```
Compare compilers for ./sim on cosma8: build it with gnu_comp/14.1.0,
intel_comp/2025.1.1 and llvm/20.1.0, each at -O2 and -O3, with -march=znver2,
in separate build folders.  Run each on tests/medium.yml on the same cosma8
node, three times, in one job script for me to submit.  Check that all builds
give the same output within 1e-10, and give me a table of times.
```

```
Our code is built with -march=native on login5c, so it does not run on
cosma8 or cosma7.  Find the newest -march target that runs on every queue we
use (cosma5, cosma7 and cosma8), build with it, and measure how much slower
it is than the -march=native build on cosma5.  If the difference is large,
suggest building separate versions instead, and how a job script could pick
between them.
```

```
Try -O3 -ffast-math on src/kernels.c only, not the whole code.  Run the
regression tests, report the largest change in each output, and check
whether any tests for NaN or infinity behave differently.  Only keep it if the
results stay within the tolerances in tests/tolerances.yml.
```

### MPI and communication

```
On 8 cosma8 nodes, ./sim spends a lot of time in MPI.  Using the Linaro
MAP or Scalasca profile in profiles/, find which MPI calls take the time, on
which ranks, and whether it is waiting caused by uneven work (load imbalance)
or the communication itself.  Suggest changes, starting with the one you expect
to help most, and estimate how much each could save.
```

```
Run a strong scaling test of ./sim on 1, 2, 4, 8 and 16 cosma8 nodes with the
same problem (tests/large.yml), and a weak scaling test where the problem
grows with the nodes (tests/weak_N.yml).  Write the job scripts for me to
submit, staying within 16 nodes.  Afterwards, plot the efficiency of each and
say how many nodes it is worth using for production runs.
```

### File input and output on Lustre

```
Reading snapshots is the slowest part of the analysis.  Check with
lfs getstripe how the snapshot files in /cosma8/data/PROJECT/USER/run42 are
striped, and with h5dump -p -H (hdf5 module) how the datasets I read are
chunked and compressed.  Compare this with how src/reader.py reads them, and
estimate how much each change would save: reading larger slices, reading only
the needed datasets, striping new copies with lfs setstripe, and reading with
several processes.  Do not restripe or copy any files.
```

```
My job array of 200 tasks all read the same 3 snapshot files at once and the
reads are slow.  Propose and justify a better approach: striping copies of the
files, staging each task's input to /tmp on the compute node, or reading once
and sharing.  Estimate the effect on the Lustre servers as well as on my jobs.
```

```
./sim writes 2 million small files per run.  Show me where in the code they
are written, and propose a change that writes the same data into a few large
HDF5 files instead, with the same layout for the analysis code.  Estimate the
time saved on Lustre.  Do not change the code yet.
```

### Python on COSMA

```
Speed up compute_profiles() in analysis/profiles.py.  First write a
regression test against its current output on tests/data/small.hdf5.  Then
try, in order: removing Python loops with NumPy, avoiding array copies, and
Numba with parallel=True and cache=True.  After each step, run the test and
time the function on 16 cores of the login node, excluding Numba's first
compile.  Stop when the next step gives less than 10% improvement.  Report a
table of times for each step.
```

```
analysis.py uses multiprocessing with 32 processes, and each process seems to
use many threads.  Find out how many threads NumPy's maths library starts in
each process, and set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and
MKL_NUM_THREADS so the total matches the 32 cores the job asks for.  Measure
the run time before and after in a job on cosma8-serial with 32 cores.
```

```
The analysis loads whole snapshots into memory and runs out of memory on
cosma5 jobs.  Change it to read and process the particles in chunks of
10 million, using h5py slices, so that peak memory stays under 50GB.  Check
that the results are identical to the current version on a snapshot that
fits in memory, and report the new peak memory and run time.
```

### GPUs

```
Profile the GPU version of ./sim with Nsight Systems (nsight-systems module)
on one GPU node.  Write the job script for me to submit, following the GPU
jobs page for the queue and the GPU request.  Afterwards, tell me what share
of the time the GPU is busy, how much time goes on copying data between CPU
and GPU, and which kernels take the most time.
```

```
Port the CUDA kernels in src/gpu/ to Kokkos, so the code can run on both
NVIDIA and AMD GPUs and on CPUs.  Use the kokkos modules available on COSMA
(module avail kokkos).  Port one kernel at a time, and check each against the
CUDA version's output on tests/gpu_small before going on.  Start with the CPU
(host-only) Kokkos build, which can be tested on a login node.
```

### Checking and writing up

```
Compare the branch faster-io with main on reading the five snapshots in
tests/snapshots.  Build the old version in a separate git worktree.  Write one
job script that runs both on the same whole cosma8 node, three times each
after a warm-up run.  Afterwards, check that both give byte-identical arrays,
and give me a table of times with the node name and the two commits.
```

```
Before reporting the speed-up, check it: was the node shared with other jobs
during either run (check with sacct and the job's node list)?  Were both
versions run with the same input, threads and binding?  Was the first run
excluded?  Does the faster version give the same results?  Tell me which of
these you have evidence for, and which you do not.
```

```
Write docs/performance.md describing the optimisation work on this branch:
the starting point, each change, the time before and after each change with
the job ID and node, how correctness was checked, the changes that were tried
and did not help, and what to try next.  Every number must come with the job
or command that produced it.
```

```
Estimate before optimising: here is the stage breakdown from job 1234567.
For each of the five ideas in ideas.md, work out the most it could save,
assuming the stage it affects became free.  Rank them by likely saving per
day of work, and tell me which are not worth doing.
```

## Getting started on COSMA

```
Read /etc/claude-code/AGENTS.md and summarise the rules you must follow on
this cluster in ten short points.  Then tell me which of my settings, if any,
would make it hard to follow them.
```

```
Check my set-up for using agents on COSMA, without changing anything:
which agent folders are in my home directory and how big they are, where
TMPDIR points, whether npm installs into /cosma/apps, and how full my home
and app space quotas are.  Give me a list of the changes you recommend, with
the exact commands, for me to run.
```

```
Write a CLAUDE.md for this project, using the COSMA template in the docs
(agents-setup.md).  Fill in: project PROJECT, account ACCOUNT, data in
/cosma8/data/PROJECT/USER/sims, code in /cosma/apps/PROJECT/USER/code, builds
use gnu_comp/14.1.0 and openmpi/5.0.3.  Keep it under 40 lines.  Show it to me
before saving.
```

## Planning

```
I want to add MPI support to the halo finder in src/.  Do not change any
code yet.  Read the code, then write a plan in docs/mpi-plan.md: the steps,
the files each step changes, how each step will be tested, the risks, and the
questions you need me to answer.  Mark every step that needs me to submit a
job.
```

```
Follow docs/mpi-plan.md, step 1 only.  When it is done, show me the diff and
the test results, and stop.  If anything does not match the plan, stop and ask
before carrying on.
```

## Data

```
Copy /cosma8/data/PROJECT/USER/run42/snapshots to OTHER:/scratch/USER/run42.
I have already logged in to OTHER, so reuse that connection, and use
ssh -o BatchMode=yes.  First show me the number of files, the total size and an
rsync dry run, and wait for me.  After the copy, compute sha256sum of every file
on both sides, compare the lists, and report any files that differ or are
missing.  Keep a log of what was copied in run42-transfer.log.
```

```
In /cosma8/data/PROJECT/USER/runs there are about 200 run folders.  Without
moving anything, write a table of each folder's size, number of snapshots,
date of the last output, and whether its job finished (check the last lines of
the .out files).  Save it as runs-summary.csv.
```

```
Propose a tidier layout for /cosma8/data/PROJECT/USER/analysis.  Write the
plan as a list of "from -> to" moves in reorganise.txt, and a script
reorganise.sh that does them with mv -n (never overwriting) and logs each move.
Do not run it.
```

## Building software

```
Build the code in /cosma/apps/PROJECT/USER/code/mycode on login8b with
gnu_comp/14.1.0 and openmpi/5.0.3, using at most 8 cores.  If the build fails,
find the first real error, fix its cause, and try again, up to three times.
Then write build.sh that repeats the working build from a clean shell, and run
it once to check it.  List every change you made to the code or build files.
```

```
This program stops with "Illegal instruction" on cosma8 but works on login5c.
Find out why.  Then make two builds, one for AVX2 nodes and one for AVX-512
nodes, run both on tests/small_input on the matching login nodes, and check
that they give the same output.  Add a few lines to the job script that pick
the right build on each node.
```

## Job scripts and jobs

```
Write a Slurm script to run ./sim params.yml on 4 cosma8 nodes for 24 hours,
with 128 MPI ranks per node, account ACCOUNT.  Use module purge and load
gnu_comp/14.1.0 openmpi/5.0.3, set -euo pipefail, absolute paths, separate
.out and .err files named with the job ID, and TMPDIR=/tmp.  Check it with
sbatch --test-only and explain each #SBATCH line.  Do not submit it.
```

```
Job 1234567 failed.  Read its .out and .err files and sacct -j 1234567
--format=JobID,State,ExitCode,Elapsed,MaxRSS,ReqMem,NodeList.  Tell me why it
failed, quoting the lines that show it, and suggest a fix.  Do not resubmit.
```

```
My last 20 jobs are in sacct -X --starttime 2026-11-01.  For each one, compare
the time and memory requested with what was used, and tell me which I could
ask for less of next time.  Give me a table.
```

```
Job 1234567 has been pending for two days.  Using only read-only commands
(squeue, sinfo, scontrol show job), explain why it is waiting and what change
to the request would make it start sooner.
```

```
Turn run_all.sh, which loops over 500 input files and calls sbatch for each,
into one job array script.  Each task should skip its input if the output
already exists, so the array can be resubmitted safely.  Limit it to 50 tasks
running at once (%50).  Show me the script and the sbatch command; do not
submit it.
```

## Finding problems

```
tests/test_density.py fails since yesterday's commits.  Use git bisect between
main~20 and main, running only that test at each step, to find the commit that
broke it.  Tell me the commit, the lines it changed that cause the failure, and
how sure you are.
```

```
This run gives a total mass 0.3% higher than the reference run.  Both outputs
are in /cosma8/data/PROJECT/USER/{new,ref}.  Find the first snapshot, and the
first quantity, where they differ by more than 1e-6, and work out which step of
the calculation the difference comes from.  Do not change any code.
```

```
notebooks/plots.ipynb no longer runs.  Run it from top to bottom in a fresh
kernel, using the venv in /cosma/apps/PROJECT/USER/venvs/analysis.  Fix each
cell that fails, keeping my changes to the analysis, and guard against NaN
values where a cell fails because of them.  List every change you made, and
run it again from the top at the end.
```

## Writing code

```
Write a bash script, archive_snaps.sh, that copies finished snapshots from
SRC to DEST (both set at the top), skips files already copied, copies to a
.partial name and renames when done, records sha256 checksums, logs each copy
with the time, and has a --dry-run option.  Use set -euo pipefail and quote
every variable.  Run shellcheck and bash -n on it, then test it on a copy of a
small folder in /cosma/apps/PROJECT/USER/tmp.
```

```
Turn notebooks/stellar_mass.ipynb into a script, stellar_mass.py, that takes
the snapshot path, halo catalogue and output file as command-line options, and
writes one HDF5 file.  Keep the calculation exactly the same, and check the
script's output against the notebook's for snapshot 0127.
```

```
Add a function to src/profiles.py that computes the mass profile of a halo
in 30 log-spaced radial bins from 0.1 to 100 kpc, handling the periodic box.
Follow the style of the existing functions and use the existing distance
function.  Write tests first, run them to see them fail, then write the
function and run them again.
```

## Tests and edge cases

```
List the edge cases for bin_particles() in src/binning.py: empty input,
single particles, values on bin edges, the periodic boundary, NaN, very large
coordinates, and anything else you can find.  For each one, say what the
function currently does.  Then write a pytest test for each, using expected
values you work out independently of the code, and explain how you got each
expected value.  Do not change bin_particles().
```

```
Write regression tests for the current behaviour of src/pipeline.py before I
change it: run it on tests/data/small_snapshot.hdf5, save the outputs to
tests/reference/, and write tests that compare new runs with them, exactly for
integers and within 1e-12 relative for floats.  Tell me which outputs, if any,
change from run to run.
```

```
Review the tests in tests/ as a sceptical reviewer.  Find tests that would
pass even if the code were wrong: tests that compare the code with itself,
tolerances that are too loose, expected values copied from the code's output,
and skipped tests.  For each, give the file and line and what to change.
```

## Documentation

```
Write a README.md for this code: what it does, how to install it on COSMA
(modules and virtual environment), how to run it on the small test case and
as a batch job, and what each command-line option does.  Run every command
in the README to check it works, and mark anything you could not check.
```

```
Add NumPy-style docstrings to every public function in src/analysis/, with
the units of every input and output.  Where you are not sure of a unit or
meaning from the code, write TODO and list these for me rather than guessing.
```

```
Write a method note, docs/method.md, describing exactly how the code computes
the halo concentration: each equation, the variable names and file and line
that implement it, and any assumption or approximation.  I will check it
against the paper.
```

## Porting code

```
Port idl/smooth_field.pro to Python with NumPy.  First run the IDL version on
tests/field_small.dat and save its output and intermediate arrays.  Then port
one routine at a time, and compare each with the IDL results before going on.
Watch for 1-based indexing, column-major arrays, IDL's single-precision
defaults and integer division.  Report the largest difference for each
routine.
```

```
The particle loop in analysis/neighbours.py is too slow.  Rewrite only that
function with Numba (parallel=True, cache=True), keeping the same inputs and
outputs.  Check that it gives identical results to the current version on
tests/data/small.npz, and time both versions, excluding the first call while
Numba compiles.
```

## Reviews and documents

```
Review the changes on this branch compared with main, as a strict reviewer.
Look for bugs, wrong units, cases not handled, and anything that will be slow
on the full data.  For each problem, give the file and line, and how sure you
are.  Then check each one against the code and tell me which are real.
```

```
Before I accept it, review the work you have just done as if someone else had
done it.  What did you not test?  What assumptions did you make?  What would
make the result wrong?
```

```
Read the draft in paper/methods.tex and critique it: unclear explanations,
claims without support, inconsistent notation, and anything that does not
match what src/ actually does.  Give your points as a list, most important
first.  Do not edit the file.
```

```
Write a report, docs/io-report.md, on the reader speed-up: the problem, what
you measured, the changes made, the results with a table, how correctness was
checked, and what is still unknown.  Every number must come with the command
or job that produced it.
```

## Housekeeping

```
Without changing anything, list my processes on this node that have been
running for more than a day or are using more than 10% of a core, my files in
/tmp and /dev/shm on this node, and git worktrees and merged branches in this
repository.  Give me the commands to remove each, for me to run.
```

```
What is using my home directory quota?  Show the largest folders in my home
directory, including hidden ones, and suggest which could move to app space,
with the commands to move them and leave a link.  Do not move anything.
```

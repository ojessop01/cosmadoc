# Optimising code with AI agents

Performance work is one of the areas where agents help most, because it is mostly careful measurement and checking, which is tedious by hand.  This page describes how to use agents to make code faster on COSMA, and how to make sure the faster code is still right.

Two rules apply throughout: **measure before changing anything**, and **check the results after every change**.  A faster code that gives a different answer is not an improvement.

For how to phrase requests so that you get reliable results, see
[writing good requests](agents-prompts.md).

## Timing and benchmarking

Fair timing on a shared system is hard: other people's work affects your
timings, the first run is often slower than the rest, and it is easy to
compare runs made in different conditions.  Agents are good at the careful,
repetitive parts:

- **Choosing a fair place to run.**  Checking how busy a node is
  (`cat /proc/loadavg`, `ps`) before timing on it, and using a batch job when
  the timings need to be reliable.
- **Never overlapping runs.**  Making sure two timing runs never share a
  node at the same time, for example by making the second job wait for the
  first with `--dependency=afterany:JOBID`.
- **Comparing like with like.**  Running the "before" and "after" versions on
  the same node, with the same input and the same number of threads, and
  repeating each run so that one slow run does not mislead.  A common way is to
  build the old version in a separate `git worktree`, so both versions exist at
  once.
- **Warming up first.**  Noticing that the first run includes one-off costs,
  such as compiling (Numba, JIT), planning (FFTW) or filling the file system
  cache, and leaving those runs out of the comparison.
- **Checking surprises before reporting them.**  If a new version looks
  slower, checking whether the node was busy at the time before calling it a
  regression.
- **Writing it up.**  Producing a table of the results, with the node, the
  commit and the settings for each number.

## Profiling tools on COSMA

COSMA has a good set of performance tools, but people rarely use most of them
because each takes time to learn.  An agent already knows how to run them and
read their output, so ask for them by name.  See also
[code performance](codeperformance.md).

| Tool | How to get it | What to ask the agent to use it for |
| ---- | ------------- | ----------------------------------- |
| `perf` | installed | `perf stat` for instructions per cycle and cache misses, and `perf record` and `perf report` to find the hottest functions in compiled code. |
| `py-spy` | `pip install py-spy` in a virtual environment | Sampling profiles of Python programs, including a flame graph (`py-spy record -o profile.svg -- python script.py`), without changing the code. |
| `cProfile` | part of Python | Which Python functions take the time, and how often they are called. |
| `line_profiler` and `scalene` | `pip install line_profiler scalene` in a virtual environment | Time (and, with `scalene`, memory) for each line of a Python function. |
| `gprof` | installed | Function-level profiles of compiled code built with `-pg`. |
| LIKWID | `module load gnu_comp/14.1.0 likwid/5.5.1` | `likwid-topology` for a node's sockets, caches and NUMA layout, `likwid-perfctr` for memory bandwidth, floating-point rate and vectorisation, and `likwid-pin` to place threads. |
| Intel VTune and Advisor | `vtune` and `advisor` modules, or newer versions after loading `intel_comp` | Hotspots, threading efficiency, memory access patterns, and which loops are or are not vectorised. |
| Linaro Forge (MAP and DDT) | `allinea/ddt/25.1.1` (the `linaro/forge/23.1.0` module does not currently start) | MAP for profiling MPI programs across ranks, DDT for debugging them. |
| Scalasca and PAPI | `scalasca` and `papi` modules | Communication and waiting time in large MPI runs, and hardware counters from inside your own code. |
| Nsight Systems | `nsight-systems` module, with `cuda` or `nvhpc` | A timeline of GPU work: kernels, memory copies, and time the GPU spends idle. |
| Valgrind | `valgrind/3.23.0` or installed | Cachegrind and Callgrind for cache behaviour and call counts on small cases, and Memcheck for memory errors. |
| `numactl` | installed | Showing and controlling which sockets and memory a run uses. |
| Compiler reports | your compiler | `-fopt-info-vec-missed` (GCC) or `-qopt-report` (Intel) to see which loops the compiler did not vectorise, and why. |
| `clang-tidy` | `llvm` modules | Static checks of C and C++ code, including some performance warnings. |

Run profiles in a batch job, or on a node no one else is using.  Results on a
busy login node are distorted by other people's work.

## A good order of work

1. **Make a small, quick test case** that behaves like the real run, and a way
   to check its results (see [checking that a new version gives the same
   answer](#checking-that-a-new-version-gives-the-same-answer)).
2. **Measure where the time goes**: time each stage, then profile the slowest
   one.  Ask the agent to report the share of the run time in each stage.
3. **Find out what limits it.**  Is the slow part limited by computation,
   memory bandwidth, file I/O, communication between MPI ranks, or one thread
   doing work the others wait for?  The tools above answer this, and the answer
   decides what kind of change can help.
4. **Estimate before changing.**  If a stage takes 8% of the run time, no
   change to it can save more than 8%.  Ask the agent for the most that each
   idea could save, and only do the ones that are worth it.
5. **Change one thing at a time**, and check the results after each change.
6. **Time it fairly** (see [timing and benchmarking](#timing-and-benchmarking)).
7. **Check it on the real nodes and real sizes.**  A change that helps on a
   small case on a login node may not help on 128 cores of a compute node, or
   on a full-size problem.

## Compiled code

### Compiler options

Ask the agent to try options one at a time and measure each, rather than
adding many at once:

- **Optimisation level.**  `-O2` is a safe default; `-O3` sometimes helps loops
  further.  Always compare results as well as speed.
- **Instruction set.**  `-march=native` builds for the CPU you compile on,
  which is fast there but may not run elsewhere (see
  [compiling for each system](facilities.md#compiling-for-each-system)).  For
  code that must run on several node types, either build once for each, or
  choose a target that all of them support, such as `-march=znver2` for
  COSMA8's CPUs.
- **Fast maths.**  `-ffast-math` (GCC) and `-fp-model fast` (Intel) can speed up
  floating-point code a lot, but allow the compiler to reorder and simplify
  calculations, which changes results and can break code that checks for
  `NaN` or infinity.  Use them only with careful checks of the results.
- **Link-time and profile-guided optimisation** (`-flto`, `-fprofile-generate`
  and `-fprofile-use`) can help large codes, at the cost of a longer build.
- **Different compilers.**  The same code can run at quite different speeds
  with GCC, Intel and LLVM compilers.  An agent can build and time all of them,
  using the `gnu_comp`, `intel_comp` and `llvm` modules.

### Vectorisation

Modern CPUs can do the same operation on several numbers at once, but only if
the compiler can prove a loop is safe to vectorise.

- Ask the agent to produce the compiler's report on which loops were
  vectorised and why others were not: `-fopt-info-vec-missed` with GCC,
  `-qopt-report=3` with Intel, or `-Rpass-missed=loop-vectorize` with LLVM.
- Common reasons a loop is not vectorised: it calls a function the compiler
  cannot see into, it has a branch inside, it may read and write the same
  memory through two pointers (which `restrict` in C can rule out), or its
  data is not stored contiguously.
- **Data layout.**  Storing each quantity in its own array ("structure of
  arrays") usually vectorises better than an array of structures holding all
  the quantities of each particle.

### Memory and caches

Many scientific codes are limited by how fast data reaches the CPU, not by
the arithmetic.  Signs of this are a low number of instructions per cycle in
`perf stat`, and memory bandwidth close to the node's limit in
`likwid-perfctr`.  Things that help:

- going through arrays in the order they are stored in memory;
- working on blocks of data that fit in the cache, rather than whole arrays at
  a time;
- reusing data while it is in the cache, rather than making several passes;
- using single precision where it is accurate enough, which halves the data
  to move (always check the effect on accuracy).

## OpenMP and threads

- **Match threads to cores.**  Set `OMP_NUM_THREADS` to the number of cores you
  asked for (`$SLURM_CPUS_PER_TASK`), not the number of hardware threads.
- **Pin threads.**  `OMP_PROC_BIND=close` (or `spread`) with `OMP_PLACES=cores`
  stops threads moving between cores, which makes timings faster and more
  stable.
- **Memory on the right socket.**  On the two-socket nodes, memory is attached
  to one socket or the other, and is placed on the socket of the thread that
  first writes to it.  If one thread creates all the data, threads on the other
  socket read it slowly.  Ask the agent to initialise data in parallel, in the
  same pattern as it is later used.
- **Scheduling.**  `schedule(static)` is best when every iteration takes the
  same time; `schedule(dynamic)` or `guided` when they vary, for example when
  some particles have many more neighbours than others.
- **False sharing.**  Threads writing to neighbouring elements of the same
  array can slow each other down badly.  Per-thread copies, combined at the
  end (an OpenMP reduction), avoid this.
- **Check scaling.**  Ask the agent to time the code on 1, 2, 4, 8 ... cores and
  plot the speed-up.  Where the curve flattens shows what limits it.

## MPI

- **Ranks per node and per socket.**  Try a few layouts, for example one rank
  per core, or one rank per socket with OpenMP threads inside it, and measure
  them.
- **Binding.**  With Open MPI, ask the agent to set the layout explicitly with
  `mpirun --map-by` and `--bind-to`, and to check it with `--report-bindings`.
  With Intel MPI, `numactl` must go after `mpirun`, so that it applies to each
  rank.
- **Load balance.**  If most ranks wait for a few, the code is only as fast as
  the slowest.  Per-rank timings, Linaro MAP or Scalasca show this.
- **Communication.**  Fewer, larger messages are faster than many small ones,
  and collective operations (such as `MPI_Allreduce`) are usually faster than
  the same thing written by hand.  Overlapping communication with computation
  can hide its cost.
- **Scaling tests.**  Run the same problem on increasing numbers of nodes
  (strong scaling), and a problem that grows with the number of nodes (weak
  scaling), to see how far the code scales before asking for a large
  allocation.

## GPUs

- **Profile first.**  Nsight Systems (the `nsight-systems` module) shows a
  timeline of what the GPU is doing.  Often the GPU spends much of its time
  idle, waiting for data from the CPU.
- **Move data less.**  Copying data between the CPU and the GPU is slow.  Keep
  data on the GPU between steps, and copy only what changes.
- **Check the GPU is busy.**  `nvidia-smi` on the node shows how busy each GPU
  is and how much memory is used.
- **Portable code.**  COSMA has GPUs from more than one maker.  Libraries such as
  Kokkos (the `kokkos` modules) let the same code run on NVIDIA and AMD GPUs and
  on CPUs.  See [GPUs](gpu.md) and [GPU jobs](gpujobs.md) for the hardware and
  how to use it.

## Python

Python is easy to write and often slow, so this is where agents most often
make large speed-ups.

### Finding the slow part

- `cProfile` (part of Python) shows which functions take the time:
  `python -m cProfile -s cumulative script.py | head -40`.
- `line_profiler` shows the time for each line of a function.
- `py-spy` samples a running program without changing it, and can draw a flame
  graph: `py-spy record -o profile.svg -- python script.py`.  It can also
  attach to a program that is already running.
- `scalene` shows both time and memory use for each line.

These are not installed on COSMA; install them with `pip` into your virtual
environment.

### Making it faster

- **Use NumPy on whole arrays** instead of Python loops over elements.  This is
  usually the largest single gain, often tens or hundreds of times faster.
- **Avoid unnecessary copies.**  Many NumPy operations make a new array; doing
  the work in place, or with views, saves time and memory.
- **Choose the type.**  `float32` arrays use half the memory of `float64`, which
  can speed up memory-bound code, if the precision is enough.
- **Numba.**  For loops that cannot easily be written with whole arrays, such as
  neighbour searches or particle deposits, Numba compiles a Python function to
  fast machine code, and can run it on several threads (`parallel=True`).  The
  first call is slow while it compiles; `cache=True` saves the compiled code for
  later runs.
- **Compiled extensions.**  For the slowest parts, Cython, C or C++ with
  `pybind11`, or Fortran with `f2py` can be faster still (see
  [wrapping instead of porting](agents-coding.md#wrapping-instead-of-porting)).
- **Use existing libraries.**  Before writing a fast routine, ask the agent
  whether SciPy, a KD-tree, an FFT library or another package already does it.
- **Parallel work.**  Python threads do not speed up pure Python code, because
  only one thread runs Python at a time.  Use processes (`multiprocessing` or
  `concurrent.futures.ProcessPoolExecutor`) for independent tasks, or Numba or
  NumPy, which release this limit.  For many independent inputs, a Slurm
  [job array](sbatch.md) is often simplest.
- **Memory.**  For data larger than memory, read it in pieces, or use
  memory-mapped arrays (`numpy.memmap`), rather than loading everything at once.
- **Threads in libraries.**  NumPy's maths libraries start their own threads.
  When you also run several processes, set `OMP_NUM_THREADS` (and
  `OPENBLAS_NUM_THREADS` or `MKL_NUM_THREADS`) so the total does not exceed the
  cores you have.

## File input and output

For many analysis codes on COSMA, reading data takes longer than the
calculation.

- **Read only what you need.**  Read the datasets and the particles you need,
  rather than whole files.  With HDF5, reading a slice of a dataset is much
  faster than reading it all and then selecting.
- **Read in large pieces.**  Many small reads are far slower than a few large
  ones, especially on [Lustre](lustre.md).
- **HDF5 chunking and compression.**  How a dataset was split into chunks, and
  how it was compressed, decides how fast it can be read.  An agent can inspect
  this with `h5dump -p -H file.hdf5` (from the `hdf5` module) or `h5py`, and explain whether the way
  you read the file matches it.  Decompression can be the slowest part of
  reading.
- **Parallel reads.**  For many processes reading the same large files, Lustre
  striping helps (see [Lustre](lustre.md)), and the `parallel_hdf5` modules
  allow MPI programs to read and write one file together.
- **Fewer, larger files.**  Writing millions of small files is slow and puts a
  load on the file system for everyone.  Combine outputs into fewer, larger
  files.
- **Local disk in jobs.**  For temporary files during a job, use `/tmp` on the
  compute node, which is local and fast, and copy only the final results back.
- **Read once.**  If several steps read the same data, read it once and keep it
  in memory, or save the result of the expensive step.

## Things agents commonly find on COSMA

- **Threads or ranks in the wrong place.**  Threads spread across sockets
  without `OMP_PROC_BIND` and `OMP_PLACES`, MPI ranks all on one socket, or
  more threads than cores.  `likwid-pin`, `numactl` and `--report-bindings`
  (Open MPI) show where they really run.
- **Memory on the wrong socket.**  Data created by one thread and used by
  threads on another socket is slow to reach.  Creating it in parallel, by the
  threads that use it, can help a lot on the two-socket nodes.
- **Loops that are not vectorised**, or code built without the instructions
  the CPU supports.  The compiler reports show which loops, and why.  Remember
  that AVX-512 builds do not run on every node (see
  [building for different nodes](agents-coding.md#building-for-different-nodes)).
- **Python loops doing numerical work** that NumPy, Numba or a compiled
  extension could do far faster, or repeated work, such as recomputing
  something in every iteration that could be computed once.
- **Slow file I/O.**  Reading many small pieces of a file, reading the same
  data repeatedly, or large files on Lustre that are not striped.  On
  [Lustre](lustre.md), striping large files and reading in large blocks often
  helps more than any change to the computation.
- **Repeated set-up costs**, such as FFT plans or compiled kernels that are
  made again in every run, which can be saved and reused.
- **Load imbalance**, where most ranks or threads wait for the slowest one.
  MAP, Scalasca and per-rank timings show this.
- **Precision.**  Using double precision where single precision would be
  accurate enough can halve memory use and speed up memory-bound code, but
  the agent must check the effect on accuracy, not assume it.

## Checking that a new version gives the same answer

Whenever code changes, especially to make it faster, the results must be
checked.  This is tedious by hand, so it is often done loosely.  An agent can
do it thoroughly:

- **Byte-for-byte checks.**  For a change that should not alter the output at
  all, such as a faster file reader, comparing every dataset with the old
  version, for example by comparing checksums of each array.
- **Comparison with a reference.**  For a change that is allowed to alter the
  output slightly, such as a faster but approximate method, comparing against
  an accurate reference calculation, and reporting the largest and typical
  errors.
- **Finding the first difference.**  When two runs disagree, finding the
  first step, file or quantity where they differ, rather than only the final
  result.
- **Finding the commit that caused it.**  Using `git bisect` to find which
  commit made the output or the speed change.

## A worked example

A typical task, and how an agent handles it:

1. **The request.**  "The analysis step that reads the particle data takes
   about 20 seconds per snapshot.  Find out why, and make it faster if it is
   worth it."
2. **Measuring.**  The agent times each part of the step on a small test case
   and finds that most of the time is spent reading and decompressing data,
   not computing.
3. **Estimating.**  It works out that a faster reader could save most of the
   time, while two other ideas could save at most a few percent, and says
   which are worth doing.
4. **Changing.**  It writes the faster reader in a separate branch.
5. **Checking.**  It reads every dataset in several snapshots with both the old
   and new reader and confirms they are identical, byte for byte.
6. **Timing fairly.**  It prepares a batch job that times both versions on the
   same node, three times each, after warming up, and asks you to submit it.
7. **Reporting.**  It reports that reads now take 3 to 7 seconds instead of 16
   to 25, with a table of the times, the node and the commits, and notes what
   it did not test.

Each step is small and checkable, which is what makes it reliable.

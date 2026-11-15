# Code performance

Optimising and profiling HPC codes is key to performance, and getting the most science per kWhr.

COSMA includes many tools to help with this, and regular training activities related to these.

The [SHAREing project](https://shareing-dri.github.io/assessment) also offers a code assessment service allowing users to submit their codes for assessment, so that potential easy performance gains can be identified.

Please fill out the form and submit your code!

This page describes the profiling and performance tools on COSMA: which to use for which question, how to load each one, and a tested example of running it.  For finding bugs and crashes, see [debugging](debugging.md).

## Which tool to use

| Question | Start with |
| -------- | ---------- |
| Where does my program spend its time? | [perf](#perf), or [VTune](#vtune) for more detail |
| Is my code limited by memory bandwidth or by computation? | [LIKWID](#likwid) |
| Are my loops vectorised, and why not? | [Advisor](#advisor), or the compiler's own report (see [vectorisation reports](#vectorisation-reports)) |
| How is time split between computation and MPI communication? | [Score-P](#score-p) with [Scalasca](#scalasca) |
| What does my MPI program do over time? | [Score-P](#score-p) traces, viewed in [Vampir](#vampir) |
| How much file I/O does my job do, and how? | [Darshan](#darshan) |
| Which function is slow, in a simple serial program? | [gprof](#gprof) or [gperftools](#gperftools) |
| Is my program using the AMD CPUs well? | [AMD uProf](#uprof) |
| Where is my Python program slow? | `cProfile`, `py-spy` or `line_profiler` (see [Python](python.md)) |

Whatever the tool, measure on the kind of node your program will run on, in a batch job.  Timings on a login node are affected by everyone else using it, and the login node may have a [different CPU](facilities.md#compiling-for-each-system) from the compute nodes.

## Summary of tools

| Tutorial | Description |
|---|---|
| [perf](https://perfwiki.github.io/main/tutorial/) | Linux's built-in profiler: hardware counters and sampling, with no module needed. |
| [Intel Advisor](https://www.intel.com/content/www/us/en/docs/advisor/get-started-guide/current/overview.html) | Analyses vectorisation, threading design. |
| [Intel VTune Profiler](https://www.intel.com/content/www/us/en/docs/vtune-profiler/get-started-guide/current/overview.html) | Hotspot analysis, memory access patterns, threading efficiency and more. |
| [AMD uProf](https://www.amd.com/en/developer/uprof.html#documentation) | AMD's profiling suite. |
| [LIKWID](https://github.com/RRZE-HPC/likwid/wiki) | Command-line tools (`likwid-perfctr`, `likwid-topology`, `likwid-pin`, etc.) for reading hardware performance counters and controlling thread placement. |
| [gperftools](https://gperftools.github.io/gperftools/cpuprofile.html) | Google's lightweight performance analysis tool. |
| [gprof](https://sourceware.org/binutils/docs/gprof/) | The GNU profiler, for serial programs compiled with `-pg`. |
| [OProfile](https://oprofile.sourceforge.io/docs/) | Sampling profiler for Linux that can profile code. |
| [Linaro Forge (Allinea)](https://www.linaroforge.com/documentation/) | The DDT parallel debugger and MAP profiler for MPI/OpenMP/CUDA codes. |
| [Intel Inspector](https://www.intel.com/content/www/us/en/docs/inspector/get-started-guide/current/overview.html) | Dynamic analysis tool that detects memory errors and threading errors. |
| [Valgrind](https://valgrind.org/docs/manual/quick-start.html) | Memcheck tool finds memory errors while Cachegrind/Callgrind profile cache and branch behaviour. |
| [MUST](https://www.vi-hps.org/training/course-material/index.html) | Runtime correctness checker for MPI applications, catching deadlocks, datatype mismatches, resource leaks. |
| [Score-P](https://www.vi-hps.org/training/course-material/index.html) | Generates the profiles and OTF2 traces used by tools like Vampir and Scalasca. |
| [Scalasca](https://www.scalasca.org/scalasca/software/scalasca-2.x/documentation.html) | Analyses Score-P measurements of parallel programs, including waiting time in MPI. |
| [Vampir](https://tu-dresden.de/zih/forschung/ressourcen/dateien/projekte/vampir/dateien/Vampir-User-Manual.pdf?lang=en) | Interactive trace-visualisation tool for exploring event traces at any level of detail. |
| [Darshan](https://www.mcs.anl.gov/research/projects/darshan/docs/darshan3-runtime.html) | I/O characterisation tool that captures POSIX, MPI-IO and HDF5 I/O behaviours. |

## Modules

| Tool | How to get it | Commands |
| ---- | ------------- | -------- |
| perf | Installed, no module | `perf stat`, `perf record`, `perf report` |
| gprof | Installed, no module | `gprof` |
| Valgrind | Installed, no module (the `valgrind/3.23.0` module needs an MPI module loaded first) | `valgrind` |
| Intel VTune | `vtune/2025.7`, after `module load intel_comp/2025.3.0` | `vtune` |
| Intel Advisor | `advisor/2025.4`, after `module load intel_comp/2025.3.0` | `advisor` |
| Intel Inspector | `inspector/2019-update4` | `inspxe-cl` |
| LIKWID | `likwid/5.5.1`, after a compiler module | `likwid-topology`, `likwid-perfctr`, `likwid-pin`, `likwid-bench` |
| gperftools | `gperftools/2.6.1` | `pprof` |
| OProfile | `oprofile/1.3.0` | `operf`, `opreport` |
| AMD uProf | `uprof/4.1.424` | `AMDuProfCLI` |
| Score-P | `scorep/9.4`, after `gnu_comp/14.1.0 openmpi/5.0.3` | `scorep`, `scorep-score` |
| Scalasca | `scalasca/2.6.2`, after `gnu_comp/14.1.0 openmpi/5.0.3` | `scalasca` |
| Cube | `cube/4.9.1` | `cube`, `cube_stat` |
| Vampir | `vampir/9.10.0` | `vampir` |
| Darshan | `darshan-runtime/3.4.6` (after `gnu_comp/14.1.0 openmpi/5.0.3`) and `darshan-util/3.4.6` | `darshan-parser`, `darshan-job-summary.pl` |
| Linaro DDT | `allinea/ddt/25.1.1` | `ddt` |
| MUST | `must/1.7.1/...` (built for old compilers and MPI only, see [MUST](#must)) | `mustrun` |

The older Intel tools, `vtune/2019-update4` (`amplxe-cl`) and `advisor/2019-update4` (`advixe-cl`), are still available, but the 2025 versions above are better.

The examples below were tested on COSMA in November 2026, with `gnu_comp/14.1.0` and, for MPI programs, `openmpi/5.0.3`.

## perf

`perf` is installed on every node, needs no module, and needs no changes to your program.  Compile with `-g` so that it can show function names and source lines.

A summary of the whole run, including instructions per cycle and cache misses:

```
perf stat ./myprogram
```

A profile of where the time goes:

```
perf record -g ./myprogram
perf report --stdio | head -40
```

`perf report` lists functions by their share of the samples.  OpenMP parallel regions appear as functions with names such as `main._omp_fn.0`.  A low number of instructions per cycle (well below 1) in `perf stat` often means the program is waiting for memory.

## gprof

`gprof` gives a simple function-by-function profile of a **serial** program.  It does not handle OpenMP threads well: with threads, the time is often attributed to a meaningless function such as `frame_dummy`.  Use `perf` for threaded programs.

```
gcc -O2 -pg myprogram.c -o myprogram
./myprogram                          # writes gmon.out
gprof -b myprogram gmon.out | head -30
```

## gperftools

The gperftools CPU profiler samples a program while it runs, with very little overhead.  Link your program with its library, and set `CPUPROFILE` to say where to write the profile:

```
module load gperftools/2.6.1
gcc -O2 -g myprogram.c -o myprogram -lprofiler
CPUPROFILE=myprogram.prof ./myprogram
pprof --text myprogram myprogram.prof | head -20
```

`pprof --text` lists functions by the number of samples in each.

## Vtune

Intel VTune shows where time is spent, how well threads are used, and how memory is accessed.  Its basic analyses work on both Intel and AMD CPUs.

```
module load intel_comp/2025.3.0
module load vtune/2025.7
vtune -collect hotspots -r vtune_results ./myprogram
vtune -report hotspots -r vtune_results | head -20
```

The report lists functions by CPU time, and separates useful time from time spent waiting ("spin time") in OpenMP or MPI.  For the full graphical view, open the results folder with `vtune-gui vtune_results` through [x2go](x2go.md).

## Advisor

The Intel Advisor tool analyses vectorization: which loops take the time, whether each one is vectorised, and if not, why not.

```
module load intel_comp/2025.3.0
module load advisor/2025.4
advisor --collect=survey --project-dir=advisor_results -- ./myprogram
advisor --report=survey --project-dir=advisor_results --format=text | head -20
```

Each loop is listed with its time and whether it is "Scalar" or "Vectorized".  The graphical interface (`advisor-gui`, through [x2go](x2go.md)) explains why a loop was not vectorised and suggests fixes.

### Vectorisation reports

The compilers can also report which loops they vectorised, without running anything:

| Compiler | Option |
| -------- | ------ |
| GNU (`gnu_comp`) | `-fopt-info-vec-missed` (or `-fopt-info-vec` for the loops that were vectorised) |
| Intel (`intel_comp`) | `-qopt-report=3` |
| LLVM (`llvm`) | `-Rpass-missed=loop-vectorize` |

## Likwid

LIKWID reads the CPU's hardware counters, to measure things like the floating-point rate, memory bandwidth and cache use, and helps to place threads on cores.  It needs a compiler module to be loaded first.

```
module load gnu_comp/14.1.0 likwid/5.5.1
likwid-topology -g                                   # the node's sockets, caches and cores
likwid-perfctr -a                                    # the measurement groups this CPU supports
likwid-perfctr -C 0-3 -g FLOPS_DP ./myprogram        # double-precision MFLOP/s on cores 0-3
```

`-C 0-3` runs the program pinned to cores 0 to 3 and measures those cores.  The groups available depend on the CPU, so always check with `likwid-perfctr -a` on the node you are using.  `likwid-bench` measures the maximum bandwidth and floating-point rate of a node, for comparison.

## Uprof

AMD uProf is AMD's profiler, and suits the AMD EPYC CPUs in COSMA5 and COSMA8.  Its command-line tool collects a time-based profile:

```
module load uprof/4.1.424
AMDuProfCLI collect --config tbp -o uprof_results ./myprogram
AMDuProfCLI report -i uprof_results/AMDuProf-*
```

## Oprofile

OProfile is an older sampling profiler.  It still works, but `perf` and VTune give clearer results, especially for threaded programs.

```
module load oprofile/1.3.0
operf ./myprogram
opreport --symbols | head -20
```

## Inspector

The Intel Inspector tool finds memory errors (such as leaks and invalid accesses) and threading errors (such as data races).  Compile with `-g`.

```
module load inspector/2019-update4
inspxe-cl -collect mi1 -r inspector_results -- ./myprogram    # memory errors
inspxe-cl -collect ti1 -r inspector_threads -- ./myprogram    # threading errors
```

A summary of the problems found is printed at the end.  An exit status of 8 means problems were found, not that Inspector failed.  See also [debugging](debugging.md).

## Valgrind

Valgrind runs a program on a simulated CPU, so it is slow (often 20 to 100 times slower), but very thorough.  Use a small test case.  The system `valgrind` needs no module.

To find memory errors, compile with `-g -O0`:

```
valgrind --leak-check=full ./myprogram
```

To see how many instructions each function and line takes:

```
valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./myprogram
callgrind_annotate callgrind.out | head -30
```

## Score-P

Score-P measures parallel programs (MPI, OpenMP, or both), recording time in each function and in each MPI call.  You rebuild your program with `scorep` in front of the compiler command:

```
module load gnu_comp/14.1.0 openmpi/5.0.3 scorep/9.4
scorep mpicc -O2 myprogram.c -o myprogram
SCOREP_EXPERIMENT_DIRECTORY=scorep_profile mpirun -np 4 ./myprogram
scorep-score scorep_profile/profile.cubex
```

For a build system, set the compiler to `scorep mpicc` (or `scorep mpif90`, and so on).  The result is a profile in the Cube format, which can be viewed with Cube or analysed with Scalasca.  To record a full trace for Vampir, set `SCOREP_ENABLE_TRACING=true`; `scorep-score` estimates how large the trace will be, which is worth checking first, because traces of large runs can be very large.

## Scalasca

Scalasca runs a program under Score-P and analyses the result, in particular time spent waiting in MPI and its causes.  The program must be built with `scorep` as above.

```
module load gnu_comp/14.1.0 openmpi/5.0.3 scorep/9.4 scalasca/2.6.2
scalasca -analyze mpirun -np 4 ./myprogram        # writes a scorep_myprogram_4_sum folder
scalasca -examine -s scorep_myprogram_4_sum       # text summary, in scorep.score
scalasca -examine scorep_myprogram_4_sum          # opens the results in Cube
```

The output folder can be named with `SCOREP_EXPERIMENT_DIRECTORY`, as for Score-P.

## Cube

Cube displays Score-P and Scalasca profiles.  `cube_stat` prints a summary as text, and `cube` opens the graphical viewer (through [x2go](x2go.md)):

```
module load cube/4.9.1
cube_stat -t 10 scorep_profile/profile.cubex
```

## Vampir

Vampir shows Score-P traces as a timeline, rank by rank, so you can see where processes wait for each other.  It is graphical, so run it through [x2go](x2go.md):

```
module load vampir/9.10.0
vampir scorep_trace/traces.otf2
```

## Darshan

Darshan records the file input and output of a program: how many files it opened, how much it read and wrote, and in what size of pieces.  It does not need the program to be rebuilt: the runtime library is loaded alongside the program with `LD_PRELOAD`.

```
module load gnu_comp/14.1.0 openmpi/5.0.3
module load darshan-runtime/3.4.6 darshan-util/3.4.6
mpirun -np 4 -x LD_PRELOAD=$DARSHAN_LIBRARY -x DARSHAN_LOGFILE=$PWD/myprogram.darshan ./myprogram
darshan-parser myprogram.darshan | less
```

The log lists counters for each file, such as `POSIX_BYTES_WRITTEN` or `STDIO_WRITES`.  `darshan-job-summary.pl myprogram.darshan` makes a PDF summary.  Many small reads or writes, or very many files, are signs of I/O that will be slow on [Lustre](lustre.md).

## Allinea

The Linaro (was Allinea, was ARM) Forge tools are the DDT debugger and the MAP profiler.  Use the `allinea/ddt/25.1.1` module:

```
module load allinea/ddt/25.1.1
```

```{note}
In November 2026: `module load allinea/ddt` loads the default version, 23.1.0, which does not start on the login nodes (it reports a missing `libglapi.so.0` library), so always give the version, 25.1.1.  The MAP profiler in 25.1.1 reports "No licence for Linaro MAP"; only DDT is licensed.  For profiling MPI programs, use [Score-P](#score-p) and [Scalasca](#scalasca) instead.
```

For using DDT, see [debugging](debugging.md#linaro-ddt).

## Must

MUST checks MPI programs while they run, for errors such as mismatched message types, deadlocks and resources that are never freed.  The installed versions (`must/1.7.1/...`) were built with GCC 7.3 or 10.2 and old MPI libraries (Intel MPI 2018 and 2020, Open MPI 4.0.5), most of which are no longer available, so MUST cannot currently be used with the standard compilers.  Ask cosma-support if you need it.

## Python

For Python programs, use Python's own profilers rather than the tools above.  See [Python](python.md#finding-what-is-slow).

## See also

- [Debugging](debugging.md), for crashes, hangs and memory errors.
- [MPI](mpi.md), for placing MPI ranks and threads on cores.
- [`cjobload`](system.md#cjobload), for how a running job is using its nodes.
- [Compiling code](compiling.md), for compiler options.
- [Optimising code with agents](agents-optimisation.md), for a worked example of a performance investigation.

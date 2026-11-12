# Code performance

Optimising and profiling HPC codes is key to performance, and getting the most science per kWhr.

COSMA includes many tools to help with this, and regular training activities related to these.

The [SHAREing project](https://shareing-dri.github.io/assessment) also offers a code assessment service allowing users to submit their codes for assessment, so that potential easy performance gains can be identified.

Please fill out the form and submit your code!

The following tools are available on COSMA for profiling/benchmarking/etc.  

Here is a summarized table for performance tools:

| Tutorial | Description |
|---|---|
| [Intel Advisor](https://www.intel.com/content/www/us/en/docs/advisor/get-started-guide/current/overview.html) | Analyses vectorisation, threading design. |
| [Intel VTune Profiler](https://www.intel.com/content/www/us/en/docs/vtune-profiler/get-started-guide/current/overview.html) | Hotspot analysis, memory access patterns, threading efficiency and I/O. |
| [AMD uProf](https://www.amd.com/en/developer/uprof.html#documentation) | AMD's profiling suite. |
| [LIKWID](https://github.com/RRZE-HPC/likwid/wiki) | Command-line tools (`likwid-perfctr`, `likwid-topology`, `likwid-pin`, etc.) for reading hardware performance counters and controlling thread/process affinity. |
| [gperftools](https://gperftools.github.io/gperftools/cpuprofile.html) | Google's lightweight performance analysis tool. |
| [OProfile](https://oprofile.sourceforge.io/docs/) | Sampling profiler for Linux that can profile code. |
| [Linaro Forge (Allinea)](https://www.linaroforge.com/documentation/) | The DDT parallel debugger and MAP profiler for MPI/OpenMP/CUDA codes. |
| [Intel Inspector](https://www.intel.com/content/www/us/en/docs/inspector/get-started-guide/current/overview.html) | Dynamic analysis tool that detects memory errors and threading errors. |
| [Valgrind](https://valgrind.org/docs/manual/quick-start.html) | Memcheck tool finds memory errors while Cachegrind/Callgrind profile cache and branch behaviour. |
| [MUST](https://www.vi-hps.org/training/course-material/index.html) | Runtime correctness checker for MPI applications, catching deadlocks, datatype mismatches, resource leaks. |
| [Score-P](https://www.vi-hps.org/training/course-material/index.html) | Generates the profiles and OTF2 traces used by tools like Vampir and Scalasca. |
| [Vampir](https://tu-dresden.de/zih/forschung/ressourcen/dateien/projekte/vampir/dateien/Vampir-User-Manual.pdf?lang=en) | Interactive trace-visualisation tool for exploring event traces at any level of detail. |
| [Darshan](https://www.mcs.anl.gov/research/projects/darshan/docs/darshan3-runtime.html) | I/O characterisation tool that captures POSIX, MPI-IO and HDF5 I/O behaviours. |

## Modules

| Tool | Module | Commands |
| ---- | ------ | -------- |
| Intel Advisor | `advisor/2019-update4` | `advixe-cl` |
| Intel Inspector | `inspector/2019-update4` | `inspxe-cl` |
| Intel VTune | `vtune/2019-update4` | `amplxe-cl` |
| Linaro Forge | `linaro/forge/23.1.0` or `allinea/ddt/25.1.1` | `ddt`, `map` |
| Darshan | `darshan-util/3.4.6` | `darshan-parser` |
| gperftools | `gperftools/2.6.1` | `pprof` |
| LIKWID | `likwid/5.5.1` | `likwid-topology`, `likwid-perfctr` |
| OProfile | `oprofile/1.3.0` | `operf` |
| AMD uProf | `uprof/4.1.424` | `AMDuProfCLI` |
| Vampir | `vampir/9.10.0` | `vampir` |

`likwid` needs a compiler module to be loaded first.  Newer versions of `vtune` and `advisor` become available after loading `intel_comp`.  Score-P and MUST need matching compiler and MPI modules, so use `module avail scorep` and `module avail must` to see which.

`valgrind`, `gdb`, `perf`, `strace` and `gstack` are installed on the login nodes, with no module to load.

## Debugging a crash

Compile with `-g`, and without heavy optimisation, then run your program under `gdb`:

```
gcc -g -O0 myprogram.c -o myprogram
gdb --args ./myprogram myinput
```

At the `(gdb)` prompt, type `run`.  When the program crashes, type `bt` to show where it stopped.

To find memory errors, such as writing past the end of an array:

```
valgrind --leak-check=full ./myprogram
```

Core dumps are turned off by default, and are handled by the system when turned on, so running the program under `gdb` is usually easier.

## Measuring performance

For a quick summary of a program's performance, use `perf`:

```
perf stat ./myprogram
```

For the layout of a node's sockets, caches and NUMA domains, use `likwid-topology`.  Run these in a job, because results on a login node will not match the compute nodes, which can have a [different CPU](ssh.md#cosma8-cosma7-cosma5-differences).

See also [MPI hints](mpi.md) for pinning, and [`cjobload`](system.md#cjobload) for how a running job is using its nodes.

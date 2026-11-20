# Compiling code

This page explains how to build programs on COSMA: which compilers there are,
how to use libraries, which options to use for each system, and how to fix
common build errors.  It assumes you know how to load [modules](modules.md).

## Compilers

| Compiler | Module | C | C++ | Fortran |
| -------- | ------ | - | --- | ------- |
| GNU | `gnu_comp/14.1.0` (default), also 15.2.0, 16.2.0 | `gcc` | `g++` | `gfortran` |
| Intel oneAPI | `intel_comp/2025.3.0`, then `compiler-rt tbb compiler` | `icx` | `icpx` | `ifx` |
| LLVM | `llvm/20.1.0` (and others) | `clang` | `clang++` | `flang` |
| NVIDIA HPC | `nvhpc/25.11` (and others) | `nvc` | `nvc++` | `nvfortran` |

The GNU compilers are the safest default: almost every library on COSMA is
built for them.  The Intel compilers can be faster for some codes.  The NVIDIA
compilers are for GPU code, and are used on the [GPU nodes](gpu.md).  Older
Intel compilers (2018 to 2024) are also available: the classic `icc` is in
versions up to 2023, and `ifort` up to 2024.

The operating system also has an older GCC (11.5) without loading any module.
Load a `gnu_comp` module instead, so that your program matches the libraries.

## MPI

Load an MPI module after the compiler, and compile with its wrappers, which add
the MPI include files and libraries for you:

| MPI | Module | C | C++ | Fortran |
| --- | ------ | - | --- | ------- |
| Open MPI | `openmpi/5.0.3` (after `gnu_comp` or `intel_comp`) | `mpicc` | `mpicxx` | `mpifort` |
| Intel MPI | `mpi` (after `intel_comp` and `compiler-rt tbb umf compiler`) | `mpiicx` | `mpiicpx` | `mpiifx` |

For example:

```
module load gnu_comp/14.1.0 openmpi/5.0.3
mpicc -O2 -o myprogram myprogram.c
```

See [MPI](mpi.md) for choosing an MPI library and running MPI programs.

## Using libraries

Most libraries, such as HDF5, FFTW, GSL and OpenBLAS, are modules.  Loading
the module adds the library's include and library folders to the compiler's
search paths (`CPATH` and `LIBRARY_PATH`), so you only need the `-l` options:

```
module load gnu_comp/14.1.0 openmpi/5.0.3 fftw hdf5
gcc -O2 myprogram.c -o myprogram -lfftw3 -lhdf5
```

- **Load the compiler first, and MPI if needed.**  Many libraries refuse to
  load otherwise.  FFTW, for example, needs an MPI module even for serial use.
  The [list of modules](modulelist.md#what-to-load-first) shows what each
  library needs.
- **Intel MKL** (BLAS, LAPACK and FFT routines tuned for Intel CPUs) comes
  with the Intel compilers: `module load intel_comp/2025.3.0 compiler-rt tbb mkl`
  sets `MKLROOT`.  The
  [MKL link line advisor](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl-link-line-advisor.html)
  gives the options to link it.
- **OpenBLAS** modules are built for particular systems, such as
  `openblas/0.3.12cosma8` and `openblas/0.3.29cosma7`.
- **Some modules set variables** pointing to the library, such as `HDF5_DIR`,
  which build systems like CMake use.  `module show NAME` lists them.

## Build tools

- **make** and **CMake** (version 3.31) are installed, with no module needed.
  CMake finds libraries from loaded modules through `CMAKE_LIBRARY_PATH` and
  variables such as `HDF5_DIR`.
- **Use a few cores on the login nodes**: `make -j8`, not `make -j` (which
  starts as many jobs as it can).  For large builds, use an
  [interactive session](interactive.md) or a batch job.
- **Build in your app space** (`/cosma/apps/PROJECT/USER`), not on the Lustre
  data file systems, where building many small files is slow (see
  [Lustre](lustre.md)).

## Building for the right CPU

COSMA's systems have different CPUs, so code built for one may not run on
another.  The main difference is AVX-512, a set of vector instructions that
COSMA5 and COSMA7 have, but COSMA8 does not.

| Where it will run | CPU | AVX-512 | GCC option |
| ----------------- | --- | ------- | ---------- |
| `cosma5` queue | AMD EPYC 9754 (Zen 4c) | Yes | `-march=znver4` |
| `cosma7` queues | Intel Xeon Gold 5120 (Skylake) | Yes | `-march=skylake-avx512` |
| `cosma8-rome` | AMD EPYC 7H12 (Zen 2) | No | `-march=znver2` |
| `cosma8-milan` | AMD EPYC 7763 (Zen 3) | No | `-march=znver3` (or `znver2` for both COSMA8 types) |
| All of the above | | | `-march=x86-64-v3` |

See [compiling for each system](facilities.md#compiling-for-each-system) for
the login nodes' CPUs.

- `-march=native` builds for the CPU you compile on.  It is the fastest
  option, but only if you run on the same type of CPU.  The compiler modules
  set `COSMA_OPT` to `-O3 -march=native`, so makefiles that use it inherit this.
- **Build on the node type you will run on**, or give the target explicitly.
  For example, compiling with `-march=native` on login5c (AVX-512) produces a
  program that stops with `Illegal instruction` on COSMA8.  Compiling on a
  COSMA8 login node, or with `-march=znver2`, works on all COSMA8 nodes.
- If one program must run everywhere, use `-march=x86-64-v3`, which all the
  systems above support (or `$COSMA_ALL_OPT`, `-O3 -march=sandybridge`, set by
  the compiler modules), or build a separate version for each.
- The Intel compilers use `-xHost` (the same as `-march=native`), or `-march=...`
  (for example `-march=skylake-avx512` or `-march=core-avx2`).  Avoid `-xCORE-AVX512`
  for binaries that will run on AMD AVX-512 nodes such as `cosma5`, as `-x...` flags
  add an Intel CPU vendor check.

## Optimisation options

| Option | Effect |
| ------ | ------ |
| `-O2` | Good, safe optimisation.  A sensible default. |
| `-O3` | More aggressive.  Often faster for numerical loops; check results. |
| `-march=...` | Use the CPU's instructions, such as AVX2 or AVX-512 (see above). |
| `-g` | Add debugging information.  Costs nothing at run time; worth always using. |
| `-fopenmp` (GNU, LLVM), `-qopenmp` (Intel) | Enable OpenMP. |
| `-ffast-math` (GNU) | Faster floating-point, but can change results and break `NaN` checks.  Use with care. |

See [code performance](codeperformance.md) for measuring the effect of
changes, and [debugging](debugging.md) for debug builds.

## Running what you built

- **Use the same modules to run as to build.**  Put `module purge` and the
  same `module load` line in your job script.  A program built with one
  compiler or MPI version and run with another can fail with
  `error while loading shared libraries`, or crash.
- **Check what a program needs** with `ldd ./myprogram`.  A line saying
  `not found` means a library's module is not loaded.
- To make a program find its libraries without modules, link with an RPATH,
  for example `-Wl,-rpath,$HDF5_DIR/lib`.

## Common errors

| Error | Likely cause and fix |
| ----- | -------------------- |
| `fatal error: hdf5.h: No such file or directory` | The library's module is not loaded, or it was loaded before the compiler and failed.  Load the compiler, MPI and library modules in that order. |
| `cannot find -lfftw3` | As above: the module is not loaded, so its library folder is not searched. |
| `A compiler must be chosen before loading ...` | Load a compiler module first (see [modules](modules.md)). |
| `error while loading shared libraries: libXXX.so` at run time | The module used to build is not loaded when running.  Load the same modules, or link with an RPATH. |
| `Illegal instruction` at run time | Built for a CPU with instructions this node does not have (see [building for the right CPU](#building-for-the-right-cpu)). |
| `undefined reference to ...` | A library is missing from the link line, or libraries are in the wrong order (put `-l` options after the files that use them). |
| `undefined reference to 'MPI_...'` | Compiled with `gcc` instead of `mpicc`. |
| Mixing C++ standard library versions | Built with one `gnu_comp` version and linked or run with another.  Use one version throughout. |

## Installing other software

To install software that is not already available, see
[installing your own software](installing.md).

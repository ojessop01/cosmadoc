# MPI

MPI is the standard way for a program to run as many processes ("ranks")
that work together, on one node or many.  This page covers which MPI library
to use on COSMA, how to build and run MPI programs, and how to place ranks
and threads on cores for good performance.  See also the
[code-specific information](issues.md) page for hints about particular codes.

## Which MPI to use

| Compiler and MPI | Command |
| ---------------- | ------- |
| GNU with Open MPI | `module load gnu_comp/14.1.0 openmpi/5.0.3` |
| Intel with Intel MPI | `module load intel_comp/2025.3.0 compiler-rt tbb umf compiler mpi` |
| Intel with Open MPI | `module load intel_comp/2024.2.0 compiler-rt tbb compiler openmpi/5.0.3` |
| Intel 2018 with Intel MPI 2018 | `module load intel_comp/2018 intel_mpi/2018` |

These module combinations load together.  Each starts with a compiler, then an MPI.

- **GNU with Open MPI** is the usual choice, and the one most libraries on
  COSMA are built for.  For the best stability, use the latest Open MPI with
  the matching latest compiler.
- **Intel MPI** goes with the Intel compilers.  The newer `intel_comp` modules
  only add the compiler and MPI modules to the search path: you then load
  `compiler-rt tbb compiler` for the compiler, and `mpi` for Intel MPI.  `umf`
  is needed with `mpi` from 2025.
- **Intel 2018** with Intel MPI 2018 uses a different backend, and has worked
  well for many codes for years.

Other Open MPI versions (4.1.x and 5.0.x) are available as modules.  MVAPICH2
modules (`mvapich2_mpi/2.3.x`) also exist, but are not regularly tested.

Many libraries need a particular compiler and MPI: see
[what to load first](modulelist.md#what-to-load-first) in the list of modules.

## Building MPI programs

Compile with the MPI library's wrapper commands, which add the MPI include
files and libraries: `mpicc`, `mpicxx` and `mpifort` for Open MPI, and
`mpiicx`, `mpiicpx` and `mpiifx` for Intel MPI.

```
module load gnu_comp/14.1.0 openmpi/5.0.3
mpicc -O2 -o myprogram myprogram.c
```

See [compiling code](compiling.md) for compiler options, and for building for
the right CPU.

## Running MPI programs

In a batch job, start the program with `mpirun`.  It reads the job's
allocation from Slurm, so you do not need to give it a host list:

```
#!/bin/bash -l
#SBATCH -J mpitest
#SBATCH -A ACCOUNT
#SBATCH -p cosma8
#SBATCH -N 2
#SBATCH --ntasks-per-node=128
#SBATCH -t 01:00:00
#SBATCH -o mpitest.%j.out
#SBATCH -e mpitest.%j.err

module purge
module load gnu_comp/14.1.0 openmpi/5.0.3
export TMPDIR=/tmp

mpirun ./myprogram
```

- **Use `mpirun`, not `srun`,** for Open MPI programs.  `srun` does not start
  Open MPI programs correctly on COSMA.
- **Load the same modules** that the program was built with.
- **Set `TMPDIR=/tmp`.**  If `TMPDIR` points to your home or app space, which
  are network file systems, Open MPI warns that its shared-memory files are on
  a network file system, and may run slowly.
- `mpirun` with no `-np` starts one rank per task in the allocation.  Give
  `-np` to start fewer.

For more complete job scripts, including hybrid MPI and OpenMP jobs, see
[example job scripts](slurm.md#example-job-scripts).  To run MPI programs
interactively, see [an allocation with salloc](interactive.md#an-allocation-with-salloc).

## Placing ranks and threads on cores

Performance can often be improved by controlling which cores each rank and
thread runs on, particularly for jobs that combine MPI and OpenMP.

For both Open MPI and Intel MPI, set:

```
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=true
```

### Open MPI

For example, performance improvements have been achieved using:

```
mpiexec --map-by ppr:${SLURM_NTASKS_PER_NODE}:node:pe=${SLURM_CPUS_PER_TASK} --bind-to core <executable> <options>
```

with 32 MPI ranks and 4 threads per rank.  The `--map-by` option gives each rank its own block of cores, so `--bind-to core` is optional.  See the [hybrid example job](slurm.md#mpi-with-openmp-threads).

To place ranks by memory domain (NUMA domain) instead, use `ppr:N:numa`, for
example `--map-by ppr:2:numa:PE=8` for 2 ranks per domain, each with 8 cores.

Add `--report-bindings` to print where each rank was placed, and check that it
is what you intended.

### Intel MPI

For Intel MPI, similarly:

```
export I_MPI_PIN_DOMAIN=omp:compact
export I_MPI_PIN_CELL=core # ignore SMT threads
```

The bindings can be reported by setting `export I_MPI_DEBUG=4`.

To confine Intel MPI ranks to particular sockets or memory domains with
`numactl`, put `numactl` **after** `mpirun`, so that it applies to each rank:
`mpirun -np 4 numactl --cpunodebind=0 --membind=0 ./myprogram`.  Wrapping
`numactl` around `mpirun` does not work, because Intel MPI sets its own
binding for each rank.

## MPI from Python

`mpi4py`, and `h5py` with MPI support, are available as pre-built packages
matched to COSMA's modules: see
[packages with MPI](python.md#packages-with-mpi-pre-built-wheels).

## Example: SWIFT's dependencies with the Intel 2024 compiler

There are modules to run SWIFT with the Intel 2024.2.0 compiler and Intel MPI
or Open MPI 5.0.3.  Load the compiler:

```
module load intel_comp/2024.2.0 compiler-rt tbb compiler
```

Pick Intel MPI or Open MPI:

```
module load mpi
```

or

```
module load openmpi/5.0.3
```

Pick an FFTW optimised for the system:

- COSMA5: `module load fftw/3.3.10`
- COSMA7: `module load fftw/3.3.10cosma7`
- COSMA8: `module load fftw/3.3.10cosma8`

and load the other dependencies:

```
module load parallel_hdf5 parmetis gsl
```

Specific versions of these may improve performance; check with
`module avail`.

## Building Open MPI with ROCm

Some success has been achieved using the following instructions on a node with ROCm installed (one of the AMD GPU nodes):

- Compiling UCX

`../configure --prefix=/cosma/apps/PROJECT/USER/ucx-1.19.0 --with-rocm=/opt/rocm --without-knem --without-cuda --enable-mt`

- Compiling UCC

`../configure --prefix=/cosma/apps/PROJECT/USER/ucc-1.6.0 --with-rocm=/opt/rocm --with-ucx=/cosma/apps/PROJECT/USER/ucx-1.19.0`

- Compiling Open MPI

`../configure --prefix=/cosma/apps/PROJECT/USER/openmpi-5.0.9 --with-rocm=/opt/rocm --with-ucx=/cosma/apps/PROJECT/USER/ucx-1.19.0 --with-ucc=/cosma/apps/PROJECT/USER/ucc-1.6.0 --without-cuda`

## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `undefined reference to 'MPI_...'` when building | Compiled with `gcc` instead of `mpicc`. |
| The program starts as many copies of a serial program, each with rank 0 | Started with `srun`, or with a different MPI library from the one it was built with.  Use `mpirun` from the same MPI module. |
| A warning that the shared-memory backing file is on a network file system | `TMPDIR` points to home or app space.  Set `export TMPDIR=/tmp` in the job script. |
| `error while loading shared libraries: libmpi.so` | The MPI module is not loaded when running. |
| A job is much slower than expected | Ranks or threads are not placed as intended.  Check with `--report-bindings` (Open MPI) or `I_MPI_DEBUG=4` (Intel MPI). |
| The program hangs | See [debugging hangs](debugging.md#hangs). |
| `Illegal instruction` | Built for a different CPU: see [compiling code](compiling.md#building-for-the-right-cpu). |

# MPI Hints

This page gathers together various hints for using MPI on COSMA. See also the [Code-specific information](issues.md) page for code-specific hints.

These module combinations load together.  Each starts with a compiler, then an MPI:

| Compiler and MPI | Command |
| ---------------- | ------- |
| GNU with Open MPI | `module load gnu_comp/14.1.0 openmpi/5.0.3` |
| Intel with Intel MPI | `module load intel_comp/2025.3.0 compiler-rt tbb umf compiler mpi` |
| Intel with Open MPI | `module load intel_comp/2024.2.0 compiler-rt tbb compiler openmpi/5.0.3` |
| Intel 2018 with Intel MPI 2018 | `module load intel_comp/2018 intel_mpi/2018` |

The newer `intel_comp` modules only add the compiler and MPI modules to the search path.  You then need to load `compiler-rt tbb compiler` for the compiler, and `mpi` for Intel MPI.  `umf` is needed with some versions, such as 2025.3.0.  `oneAPI` is another name for `intel_comp`.

The 2018 Intel compiler and MPI use a different backend, and have worked well for years.  For GNU, the best stability is usually achieved with the latest Open MPI and the matching latest compiler.  Run `module load openmpi`, and it will tell you which compiler modules need to be loaded first.

Many libraries also need a particular compiler and MPI: see [what to load first](modulelist.md#what-to-load-first) in the list of modules.

## OneAPI / Intel 2024 Compiler

There are modules to run Swift with the Intel 2024.2.0 compiler and Intel MPI or OpenMPI 5.0.3. To use them, load the compiler:

```
module load intel_comp/2024.2.0 compiler-rt tbb compiler
```

Pick Intel MPI or OpenMPI:

```
module load mpi
```

OR

```
module load openmpi/5.0.3
```

Pick an optimized FFTW:

- (Cosma5):    `module load fftw/3.3.10 `

- OR (Cosma7):   `module load fftw/3.3.10cosma7`

- OR (Cosma8): `module load fftw/3.3.10cosma8`

and load the other dependencies

```module load parallel_hdf5 parmetis gsl```

(note, there may be specific version of these that improve performance, check using the `module avail` command)

## mvapich

This is not regularly tested, and the recipe below no longer works.  There is no `mvapich2` module, and `mvapich2_mpi/2.3.7-1` does not load with `intel_comp/2018`.  Please contact cosma-support if you need it.

```
    module purge
    module load intel_comp/2018 mvapich2 fftw/3.3.7
    module load parallel_hdf5/1.10.3 parmetis/4.0.3
    module load gsl/2.4
```

Note, the fftw build is optimised for avx512 / cosma7.

# Compiling openMPI with ROCm

Some success has been achieved using the following instructions on a node with ROCm installed (one of the AMD GPU nodes):

- Compiling UCX

`../configure --prefix=/cosma/apps/PROJECT/USER/ucx-1.19.0 --with-rocm=/opt/rocm --without-knem --without-cuda --enable-mt`

- Compiling UCC

`../configure --prefix=/cosma/apps/PROJECT/USER/ucc-1.6.0 --with-rocm=/opt/rocm --with-ucx=/cosma/apps/PROJECT/USER/ucx-1.19.0`

- Compiling OpenMPI

`../configure --prefix=/cosma/apps/PROJECT/USER/openmpi-5.0.9 --with-rocm=/opt/rocm --with-ucx=/cosma/apps/PROJECT/USER/ucx-1.19.0 --with-ucc=/cosma/apps/PROJECT/USER/ucc-1.6.0 --without-cuda`

# Pinning when running hybrid MPI/OpenMP jobs

Performance improvements can often be achieved by specifying the mapping of MPI tasks to cores.

For both OpenMPI and Intel MPI, it is helpful to set:

```
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=true
```

## OpenMPI

For example, performance improvements have been achieved using:

```
mpiexec --map-by ppr:${SLURM_NTASKS_PER_NODE}:node:pe=${SLURM_CPUS_PER_TASK} --bind-to core <executable> <options>
```

with 32 MPI ranks and 4 threads per rank.  The `--map-by` option gives each rank its own block of cores, so `--bind-to core` is optional.  See the [hybrid example job](slurm.md#mpi-with-openmp-threads).

The binding can be reported using `--report-bindings`.

## Intel MPI

For Intel MPI, similarly:

```
export I_MPI_PIN_DOMAIN=omp:compact
export I_MPI_PIN_CELL=core # ignore SMT threads
```

The bindings can be reported by setting `export I_MPI_DEBUG=4`


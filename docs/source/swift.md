# SWIFT on COSMA

A detailed study of different compilers has been carried out for SWIFT and there are many options that can be used.

It is possible to use gcc 9.3, 10.2 or 11.1 with openmpi/4.1.1 or mvapich_mpi/2.3.7 on cosma8.  However, gcc provides poor performace.  

The current recommendation (2024) is the Intel Compiler and either OpenMPI or Intel MPI.  It is thought that Intel MPI might be slightly better and lead to less imbalance.

So, either:

```
module load intel_comp/2024.2.0 compiler-rt tbb compiler
module load openmpi/5.0.3
module load ucx/1.17.0
module load parallel_hdf5/1.14.4
module load fftw/3.3.10
module load parmetis/4.0.3-64bit
module load gsl
```

or

```
module load intel_comp/2024.2.0 compiler-rt tbb compiler mpi
module load ucx/1.17.0
module load parallel_hdf5/1.14.4
module load fftw/3.3.10
module load parmetis/4.0.3-64bit
module load gsl
```


On COSMA8 with 4 ranks per node, the following should be used when launching an mpirun for SWIFT:

    -np 4 --map-by socket:PE=32

For a similiar effect with mvapich the following is required:

`export MV2_CPU_BINDING_POLICY=hybrid`

`export MV2_HYBRID_BINDING_POLICY=linear`

`export OMP_NUM_THREADS=32`

but note that the current module does not yet support mpirun.

`MV2_ENABLE_AFFINITY=0` is required.

With gcc the dependencies for swift are also available:


With openmpi the default binding of processes to cores seems to be wrong for SWIFT. The '--bind-to none' flag is required to use all of the cpus.

With mvapich, `export MV2_ENABLE_AFFINITY=0` is required to use all of the cpus.

## SWIFT with the Intel icx compiler

Yannick has put together a report on [compiling SWIFT with the icx compiler](files/SWIFT_ICX.pdf) (instead of icc, which is deprecated).


## SWIFT: compiler comparison on AMD Genoa (Peter Draper, Dec 2023)

The COSMA recommended compiler is Intel ICC as it has much better performance
than GCC for most codes and in particular SWIFT. However, Intel, as part of
the oneAPI initiative are deprecating ICC and concentrating their future
developments on the ICX compiler, so during the testing of SWIFT on the AMD
Genoa and other architectures ICX has also been investigated alongside a
similar effort from AMD called the AMD optimizing compiler, AOCC.

ICX and AOCC share a common code base, LLVM, an open-source compiler
infrastructure that is widely used and supported across different platforms
and includes support for the latest language standards and innovations like
the cross platform parts of oneAPI. So moving forward SWIFT needs to be
capable of using these compilers as effectively as it has done using ICC.

## SWIFT: Profiling with Intel tools

To be able to view source code via Intel VTune, Intel inspector and Linaro Forge you need to compile Swift:

`./configure --enable-debug CFLAGS="-parallel-source-info=2"`

Note this will disable inter-procedural optimization.

### Benchmarks


The benchmarks used here are based on the standard SWIFT exercises
EAGLE_low_z/EAGLE_25 and EAGLE_low_z/EAGLE_50. The EAGLE_25 exercise is
changed to only use self-gravity, EAGLE_50 is used as distributed. That
exercise uses smoothed particle hydro-dynamics (SPH) as well as self-gravity.
The self-gravity code in SWIFT is known to benefit more from vectorization so
is an interesting standalone test, when SPH is included the physics is more
representative of a normal run of SWIFT. Note we do not attempt to benchmark a
full physics build, such as used in the EAGLE or FLAMINGO simulations.

The benchmarks were ran on a single Genoa node, which has 2 AMD EPYC 9654
96-Core Processors, giving 192 physical cores configured as 8 NUMA regions,
and 1TB of RAM. A notable change from Rome and Milan CPUs is support for
AVX512 instructions.

The EAGLE_50 runs used 8 MPI ranks, each rank using 24 threads, effectively
using a NUMA region per rank and all 192 cores. On AMD this is the optimal way
to run SWIFT as it avoids NUMA effects. The EAGLE_25 runs used a single
process with 96 threads, these will be uniformly spread over both CPU's cores,
with interleaved memory access across all NUMA regions.


### Compiler Versions

The compilers used are (*):

    ICC: Intel oneAPI 2022.1.2
    ICX: Intel oneAPI 2022.3.0
    AOCC: AMD Optimizing compiler 4.0.0

Intel oneAPI 2022.1.2 is the last COSMA module with ICC as the default
compiler. There is an AOCC 4.1.0 compiler, but that does not work on Centos 7.

(*) GCC 13.1.0 was also considered, to be fair, and a lot of effort was made
attempting to also optimize it, but in the end it is so uncompetitive (x5
slower) that no results are worth reporting. Note that some of this is
believed to be down to the glibc currently available on COSMA/Centos 7 which
lacks a vectorized maths library. This was somewhat confirmed as when using
the vectorized library of the ICC compiler a speed up of a factor of 2 was
achieved. When the COSMA operating system is updated this is worth a revisit.

### Choice of optimizing flags

The choice of optimization flags for the compilers proved to be key to getting
the best performance out of the ICX and AOCC compilers. Initial tests showed
these compilers as a long way from the ICC performance, usually worse by a
factor of 2, but by applying flags to make sure that auto-vectorization hints
and inlining was used, as well as making use of fast optimized maths the gap
was closed and eventually exceeded in one case. For both LLVM compilers, ICX
and AOCC, it turned out that inter-procedural optimization (IPO) can play a
much larger role than previously seen with ICC.

To get AVX512 instructions operating some additional flags need to be
carefully selected, as the Intel ICC compiler tends to output code with
generic instructions on non-Intel CPUs (see the initial Genoa report). So for
ICC and ICX we use the skylake-avx512 architecture type, along with
CORE-AVX512. The znver4 architecture does the same for AOCC (and LLVM/clangs
and GCCs). To get full width AVX512 vectors additional flags are also needed,
otherwise the compilers will use 256bit vector instructions and only switch to
512bit when various heuristics for the estimated costs are triggered.

It is important to use OpenMP enabling flags as although SWIFT is not an
OpenMP code, those act with OpenMP pragmas as hints and can be used to guide
the auto-vectorization of critical loops. This is true for all three compilers
(this is not true of GCC).

The flags eventually used are broken down into three different groups,
depending on when they are used in the build. The CFLAGS are used when just
compiling. GRAVITY_CFLAGS are added when compiling the gravity interaction
code (this is separated as for Intel CPUs the cost of enabling full width
AVX512 instructions is a reduction clock speed, so we only use it in code we
designed to benefit from AVX512). LDFLAGS are also needed when linking so that
IPO is completed (compilers do not generate object code when these flags are
used, an intermediary form is created instead, this is then used when linking
to allow processing that includes the all the compiled files in one pass). For
the AOCC compiler fast optimized maths also requires linker libraries LIBS,
these are used alongside LDFLAGS.

```
ICC:
 CFLAGS:         -ip -ipo -O3 -ansi-alias -march=skylake-avx512 \
                 -axCORE-AVX512 -fma -ftz -fomit-frame-pointer
 GRAVITY_CFLAGS: -qopenmp -qopt-zmm-usage=high
 LDFLAGS:        -ipo

ICX:
 CFLAGS:         -ipo -O3 -ansi-alias -march=skylake-avx512 \
                 -axCORE-AVX512 -fma -ftz -fomit-frame-pointer -mavx512vbmi
 GRAVITY_CFLAGS: -qopenmp -qopt-zmm-usage=high
 LDFLAGS:        -ipo

AOCC:
 CFLAGS:         -flto -O3 -fomit-frame-pointer -fstrict-aliasing \
                 -ffast-math -funroll-loops -march=znver4 -mavx512vbmi
 GRAVITY_CFLAGS: -fopenmp -fvectorize -zopt -mprefer-vector-width=512
 LDFLAGS:        -ipo
 LIBS:           -fveclib=AMDLIBM -fsclrlib=AMDLIBM -lalmfast -lamdlibm
```

The ICC and ICX flags are very similar, this appears to be an attempt by Intel
to keep some compatibility. ICX also accepts most LLVM/clang flags.

### Results

Each result shows the statistics of the time taken for runs of 130 steps. The
step times can include some time for IO, but are a good estimate of the time
taken for computation. Measuring steps rather than total runtime excludes
things like the time taken to read the initial conditions and do the initial
setup, which are not interesting. Times are reported in milliseconds.

####  EAGLE_25 96 cores 1 process:

```
         mean        stddev      min       max
         -----------------------------------------
   ICC:  3209.22   | 2168.15   | 870.84  | 12251.2
         -----------------------------------------
   ICX:  3220.04   | 2187.81   | 825.45  | 12087.1
         -----------------------------------------
   AOCC: 3511.63   | 2454.58   | 811.71  | 13785.8
         -----------------------------------------
```

So ICX is just as fast as ICC and AOCC is not far behind.

####  EAGLE_50 192 cores 8 MPI ranks:

```
         mean        stddev      min       max
         -------------------------------------------
   ICC:  4843.86   | 13019.70  | 109.81  | 123071.7
         -------------------------------------------
   ICX:  4598.65   | 12521.45  |  67.13  | 118133.7
         -------------------------------------------
   AOCC: 4945.92   | 14141.21  | 102.59  | 136537.5
         -------------------------------------------
```

So with the correct application of optimizations ICX can be faster than ICC,
which is welcome news and AOCC is on a par with ICC. I repeated these runs a
few times as MPI ranks can have a large balance component to timings. Those
show that these numbers are repeatable at the 100ms level.


### SWIFT developments

Updates have been made to the SWIFT configure system to capture all the
changes needed to automatically apply these flags, as well as changes needed
for more general support for Genoa and Bergamo:

-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1823](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1823)
-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1830](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1830)
-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1805](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1805)
-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1804](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1804)
-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1802](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1802)
-   [https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1737](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/-/merge_requests/1737)

Note this does require that the compilation is done on the target architecture.

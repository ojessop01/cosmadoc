# COSMA8

## Using Cosma8

COSMA8 has 2 login nodes, accessed via login8.cosma.dur.ac.uk

See [COSMA at a glance](systems.md) and [facilities](facilities.md#cosma8) for hardware details, and [queues](queue.md) for the full list of Slurm partitions.

The main COSMA8 Slurm queues are:

__cosma8__: provides exclusive access to all 527 compute nodes, shared with `cosma8-serial`.

__cosma8-serial__: provides non-exclusive access to nodes. Use this if you want fewer than 128 cores (and remember to specify your memory requirement too).

__cosma8-rome__: a subset of `cosma8`, 356 nodes (`m8001` to `m8356`) with AMD Rome processors.

__cosma8-milan__: a subset of `cosma8`, 171 nodes (`m8357` to `m8527`) with AMD Milan processors.

__cosma8-shm__ (and __cosma8-highram__): access to the `mad04` and `mad05` servers, with 4TB RAM and an NVIDIA A100 GPU each. These are non-exclusive, so may be shared with other users if you do not require all 128 cores or all 4TB RAM.

__cosma8-shm2__: access to `ga004` (AMD MI100 GPU) and `ga006` (2x AMD MI210 GPUs).

__cosma8-shm3__: access to `mad08` and `mad09` (192 cores, 772GB RAM each).

__cosma8-ska__ and __cosma8-ska2__: large-memory queues (`mad07`, and `mad01`, `mad03` to `mad05`) for `durham` and `do011` accounts.

## Useful information

### Numerical libraries

__OpenBLAS__

OpenBLAS is available via the openblas modules.

__GSL__
The Gnu Scientific Library can be accessed via the gsl modules.

#### Using MKL with COSMA8

MKL: The Intel Math Kernel Library is known to be hobbled on AMD systems. 

MKL is available via the `intel_comp` and `oneAPI` modules.

There is a fix that must be applied: 

By default, MKL (the Intel Math Kernel Library) does not select the best options when used on COSMA8, delivering significantly lower performance. For versions of MKL prior to 2020, setting `MKL_DEBUG_CPU_TYPE=5` would force it to use the zen2 code path. However, for newer versions, this no longer works. Instead, the following workaround should be used:

```bash
cat <<EOF > amdmkl.c
int mkl_serv_intel_cpu_true() { return 1; }

EOF
```
    gcc -shared -fPIC -o libamdmkl.so amdmkl.c

    export LD_PRELOAD=libamdmkl.so

__Permanent fix__

Rather than remembering to set `LD_PRELOAD` every time you run your application, add this to your program using:

    patchelf --add-needed libamdmkl.so yourbinary

The information here was taken from [here](https://danieldk.eu/Posts/2020-08-31-MKL-Zen.html).

### Compilers

See [compiling](compiling.md) for current recommended compilers and flags (`gnu_comp/14.1.0`, `intel_comp/2024.2.0` / `2025.3.0`, `llvm`, `nvhpc`). Older CentOS 7 compilers such as `aocc_comp` are only available after `module load old-modules` and may not work on Rocky Linux 9.

See the PDFs below for AMD tuning reference material.

### MPI Modules

__OpenMPI__

Usually best to use the newest openmpi module. A version of this with .no-ucx (e.g. `openmpi/4.1.1.no-ucx`) may offer more stable performance in some cases.  However, this is usually not necessary for the newest modules.

Large jobs may suffer from performance issues. This can sometimes be resolved by selecting the UD protocol over the newer DC (dynamical connection) protocol by setting:

    export UCX_TLS=self,sm,ud

or

    export UCX_TLS=self,sm,ud,rc,dc

in the job script. See discussion [here](https://github.com/openucx/ucx/issues/4259).

If openmpi is complaining about running out of resources (memory pools being empty), the following may help:

    export UCX_MM_RX_MAX_BUFS=65536
    export UCX_IB_RX_MAX_BUFS=65536
    export UCX_IB_TX_MAX_BUFS=65536

(or some larger value).

UCX settings can be seen with: /cosma/local/ucx/1.10.1/bin/ucx_info -f

For Gadget-4, setting export UCX_UD_MLX5_RX_QUEUE_LEN=16384 has also been shown to help.

__Intel_mpi__

2018 module is the fallback option for SWIFT.

Later versions use UCX underneath, and initially suffered from stability issues. However, the newest versions are much improved.  These are loaded using:

```
module load intel_comp/2024.2.0
module load compiler-rt tbb compiler mpi
```

__Mvapich__

The mvapich module can sometimes offer improved performance. However, in some cases, RAM usage can be increased.

### Tuning information

[Options for compiling on AMD systems](./files/AMDCompileOptions.pdf)

[Tuning for AMD systems](./files/AMDTuning.pdf)

### GPUs

See [GPUs](gpu.md) and [GPU jobs](gpujobs.md) for the current GPU nodes, partitions and job options.

### SWIFT

The current recommended setup is given on the [swift pages](swift.md).

### Linaro Forge (Arm Forge / DDT)

DDT is available via `module load allinea/ddt/25.1.1` (the older default `23.1.0` does not start on Rocky Linux 9). See [debugging](debugging.md#linaro-ddt) and [code performance](codeperformance.md#allinea) for details.

### Slurm batch scripts

See [Slurm](slurm.md) and [running your first job](firstjob.md).

### COSMA8 FAQ

The COSMA8 FAQ details some of the known issues or peculiarities related to COSMA8. 

__How do I submit to COSMA8?__

You must be part of a DiRAC project that has an allocation on COSMA8, and be part of the `cosma8` group (use the `id` command to see this). If you are not part of the `cosma8` group, but should be, please [contact cosma-support](contact.md). To submit a job script, use `-p cosma8` (or `-p cosma8-serial` for partial-node jobs).

Jobs failing with `UCX ERROR: ibv_reg_mr`

Try setting the following option in your Slurm batch script (note, this may impact performance):

    export UCX_IB_REG_METHODS=direct

Please let us know if there is something you would like added.

### Known code issues

There is [collective wisdom](issues.md) available when running particular codes on COSMA8.

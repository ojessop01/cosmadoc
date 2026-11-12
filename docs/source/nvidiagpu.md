# NVIDIA GPU testbeds

COSMA contains multiple NVIDIA GPU systems, including RTX PRO 6000, H100, A100, V100 and A30 GPUs, to allow code development, porting and performance benchmarking.

## Specifications

### V100 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-v100/)\)

A total of 10 V100 GPUs are available for use, split between two systems.
Firstly, 6 V100 GPUs are connected to a single node (gn001), available for direct SSH:

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 1 | NVIDIA V100 32GB | 6 per node | 768GB | 2x Intel Xeon Gold 5218 |

And alternatively, 4 V100 GPUs are available as part of the [DINE2](dine2.md) cluster, which makes use of a CerIO composability fabric.  The GPUs can be moved between compute nodes on-demand by contacting cosma-support.

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 8 | NVIDIA V100 | 4 total (configurable) | 2TB | 2x Intel Xeon Gold 6430 |

[Manufacturer website](https://www.nvidia.com/en-gb/data-center/tesla-v100/)

Benchmarks:
- Memory bandwidth (BabelStream): 823 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

### A100 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-a100/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 2 | NVIDIA A100 40GB | 1 per node | 4TB | 2x AMD EPYC 7702 64-Core |
| 1 | NVIDIA A100 40GB | 1 per node | 1TB | 2x AMD EPYC 7773X 64-Core |

[Manufacturer website](https://www.nvidia.com/en-gb/data-center/a100/)

The GPUs are connected using a composable PCIe fabric from [Liqid](https://www.liqid.com) and can be moved between 3 compute nodes: mad04, mad05, mad06.  

### A30 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-a30/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 8 | NVIDIA A30 | 8 total (configurable) | 2TB | 2x Intel Xeon Gold 6430 |

[Manufacturer website](https://www.nvidia.com/en-gb/data-center/products/a30-gpu/)

The A30 GPUs are part of the [DINE2](dine2.md) cluster, which makes use of a CerIO Composability fabric.  The GPUs can be moved between compute nodes on-demand by contacting cosma-support.

Benchmarks:
- Memory bandwidth (BabelStream): 822 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

### H100 NVL \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-h100/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 1 | NVIDIA H100 NVL | 1 per node | 510GB | 2x Intel Xeon Gold 6530 |

[Manufacturer website](https://www.nvidia.com/en-gb/data-center/h100/)

Benchmarks:
- Memory bandwidth (BabelStream): 3387 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

### GH200 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-gh200/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 2 | NVIDIA GH200 | 1 per node | 480GB (unified) | 72-core ARM Grace |

[Manufacturer website](https://www.nvidia.com/en-gb/data-center/grace-hopper-superchip/)

Benchmarks:
- Memory bandwidth (BabelStream): 3500 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

There are two Grace-Hopper nodes, one which allows direct ssh, and one which is part of the Slurm partition `gracehopper`.

The GH200 has a unified memory model, combining an H100 GPU and a Grace CPU using NVLINK-C2C.  This is conceptually similar to the AMD MI300A, but allows the CPU and GPU to share memory across separate dies, rather than being phsically part of the same chip.

The Grace CPU is ARM-based, and therefore cannot run X86 binaries.  It is best to compile your code on the direct-ssh node.

### RTX PRO 6000 

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 1 | NVIDIA RTX PRO 6000 | 1 per node | 2.2TB | 256-core AMD EPYC 9745 (Turin) |

## Usage

If you do not already have an account on COSMA, please follow the instructions [here](account.md), then request to join the project(s): do016 for the NVidia testbed, or do015 for DINE2.

- There are two ways to access V100 GPUs: 
    - 6x V100 GPUs are accessible by direct ssh.  From a login node, use `ssh gn001`. 
    - 4x V100 GPUs are accessible through the `dine2` slurm queue.
- There are two ways to access (configurable up to 3) A100 GPUs:
    - By direct ssh.  From a login node, use `ssh mad06`.
    - Through the `cosma8-shm` slurm queue.
- A30 GPUs are accessible through the `dine2` slurm queue.
- H100 NVL node is accessible by direct ssh.  From a login node, use `ssh gn004`.
- There are two ways to access the GH200 nodes:
    - By direct ssh.  From a login node, use `ssh gn002`.
    - Through the `gracehopper` slurm queue.
- RTX 6000 GPU is available via direct ssh. From a login node, use `ssh gn005`.

## Notes

### Composable Nodes

To request a specific configuration of GPUs on any of the composable nodes, please email cosma-support@durham.ac.uk.

When using a composable partition, you can use `#SBATCH --constraint=gpu` to ensure your job is given a node with a GPU, or if you need a particular node (after allocating more GPUs to it, for example) you can use the `--nodelist` or `--exclude` paramaters to select the desired node.

### nvhpc

There are nvhpc modules available (`module avail nvhpc`), which include the NVidia compilers, CUDA, and other build tools.  It may be necessary to specify a toolchain to use with these, e.g.

```
nvc++ --std=c++20 --gcc-toolchain=/cosma/local/gcc/14.1.0 mycode.cpp
```

On grace-hopper nodes (gn002, gn003), alternative toolchains can be found in `/opt/rh/`: gcc-toolset-13, gcc-toolset-14 and gcc-toolset-15.


The combination of the gcc-15 toolchain with nvc++ 25.1 can cause a compile-time issue with some std:format-related code.  In this case, you can try using gcc-toolset-14, likely nvc++ will complain about a missing gfortran, if this is required.  In this case, make a copy of the gcc-toolset-14 in your apps/ directory, and then copy gfortran/f951 from the gcc-toolet-15 into this.



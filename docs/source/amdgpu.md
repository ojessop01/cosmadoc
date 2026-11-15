# AMD GPU testbeds

COSMA contains multiple AMD GPU systems to allow code development, porting and performance benchmarking.

## Specifications

### MI100 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-mi100/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 1 | AMD MI100 | 1 per node | 1TB | 2x AMD EPYC 7713 64-Core |

[Manufacturer website](https://www.amd.com/en/products/accelerators/instinct/mi100.html)

Benchmarks:
- Memory bandwidth (BabelStream): 947 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

### MI210 \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-mi210/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 2 | AMD MI210 | 2 per node | 1TB | 2x AMD EPYC 7513 32-Core |

[Manufacturer website](https://www.amd.com/en/products/accelerators/instinct/mi200/mi210.html)

Benchmarks:
- Memory bandwidth (BabelStream): 1250 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

### MI300X \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-mi300x/)\)

| Nodes | GPU | GPU Count | RAM per node | CPU(s) |
| ----- | --- | --------- | ------------ | ------ |
| 1 | AMD MI300X | 8 per node | 2TB | 2x Intel Xeon Platinum 8468 48-Core
 |

 [Manufacturer website](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)

 Benchmarks:
 - Memory bandwidth (BabelStream): 4036 GB/s
 - array\_size: 134217728
 - iterations: 100
 - precision: FP64

 Cache topology:
 ```text
|--------------|     |--------------|
|              |     |              |
|    HBM3      |     |    HBM3      |   (8 stacks of 24GB = 192GB total HBM3)
|    24GB      |     |    24GB      |
|--------------|     |--------------|
       |                    |
|-----------------------------------|
|       AMD INFINITY CACHE          |   (Global buffer for all XCDs)
|              256 MB               |
|-----------------------------------|
  |                               |
  |    --------        -------    |
  |    |      |        |     |    |
|---------|----|     |----|---------|
|   XCD   | L2 |     | L2 |   XCD   |
|         |    |     |    |         |   (4MB L2 per XCD)
|         |4MB |     |4MB |         |
|---------|----|     |----|---------|
      |
      |
 Detailed view
      |
      |
      V
|-----------------------------------|
|              L2 4MB               |
|-----------------------------------|
|               XCD      |          |
|      |-------------------------|  |
|      | Compute Unit            |  |
|      ||---------------------|  |  |
|      || L1 instruction 64KB |  |  |
| 38 x ||---------------------|  |  |   (38 CUs per XCD.  L1 instruction cache
|      || L1 Constant 16KB    |  |  |   shared between pairs of CUs)
|      ||---------------------|  |  |
|      || L1 Data 32KB        |  |  |
|      ||---------------------|  |  |
|      || L1 Scalar 16KB      |  |  |
|      ||---------------------|  |  |
|      || LDS 64KB            |  |  |
|      ||---------------------|  |  |
|      |-------------------------|  |
|                                   |
|-----------------------------------|
```

### MI300A \([SHAREing](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-mi300a/)\)

| Nodes | APU | RAM per node |
| ----- | --- | ------------ |
| 1 | 4x AMD MI300A (24 CPU cores) | 512GB |

[Manufacturer website](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300a.html)

Benchmarks:
- Memory bandwidth (BabelStream): 3648 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

## Usage

If you do not already have an account on COSMA, please follow the instructions [here](account.md), then request to join the project: do018.

- MI100 node is accessible through the `cosma8-shm2` queue.  Use `--nodelist=ga004` to ensure allocation to the MI100 node.
- MI210 nodes are accessible through the `cosma8-shm2` queue.  Use `--exclude=ga004` to ensure allocation to the MI210 nodes.
- MI300X node is accessible through the `mi300x` queue.
- MI300A node is accessible through direct ssh.  From a login node, use `ssh ga008`.

### Compiler modules

The hipcc family of modules include the ROCm software stack.  You probably want to use the latest one (use `module available hipcc` to see options).

After loading this module, you may also want to load a standard compiler module, e.g. `module load gnu_comp` to provide a standard compiler (which may or may not offer better performance than the hipcc compiler for host CPU code).

Due to the way module dependencies are calculated, the order in which you load these modules is important.  The last one loaded wil be the one that determines which versions of libraries you can then load (e.g. FFTW, HDF5, etc).

## Notes

The AMD ROCm software stack is installed.  ROCm 6.3.0 is available at /opt/rocm-6.3.0/bin/hipcc (2024)

ROCm 7.2.0 is also available (May 2026).

The latest version installed can be found under /opt/ - please check here.

ROCm is installed on the login8a login node, though this does not contain a GPU.  This should facilitate compilation of codes where Internet access is requried.

CUDA code must be converted to HIP using the `hipify` script provided with ROCm.


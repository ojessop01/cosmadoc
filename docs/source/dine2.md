# DINE2

DINE2, the Durham Investigatory Node Environment (or Durham Integrated Next-gen Environment), is an 8 node cluster with a CerIO composability fabric, allowing GPUs to be added to servers upon demand.

Each node has dual Intel Sapphire Rapids 32-core processors and 2TB RAM, with access to composable NVIDIA A30 and V100 GPUs via the CerIO fabric.

DINE2 was installed in 2024.

## Specifications

| Nodes | RAM per node | CPU(s) | Network Technology | GPU | GPU Count |
| --- | --- | --- | --- | --- | --- |
| 8 | 2TB | 2x Intel Xeon Gold 6430 (32-core Sapphire Rapids) | InfiniBand | NVIDIA A30 24GB | 8 Total (configurable) |
|   |     |                                  |            | NVIDIA V100 32GB | 4 Total (configurable) |

GPUs are composed dynamically across the 8 nodes; check which nodes currently have GPUs attached with `sinfo -p dine2 -o "%N %f"`.  To request a specific configuration, please contact `cosma-support@durham.ac.uk`.

### Benchmarks

- Memory bandwidth (BabelStream): 822 GB/s
- array\_size: 134217728
- iterations: 100
- precision: FP64

Further details are available on the [SHAREing website](https://shareing-dri.github.io/hpc-testbeds/systems/cosma-a30/).

## Usage

If you do not already have an account on COSMA, please follow the instructions [here](account.md), then request to join the project `do015` (the `dine2` queue also accepts `durham`, `do011` and `do020`; the `cosma8-dine2` queue, on the same nodes, is for the `dp276` and `dp440` projects).

The DINE2 cluster is part of the `dine2` Slurm partition (3-day maximum walltime, shared per core).  Jobs should be submitted to the queue using `#SBATCH -p dine2`, and jobs that need a GPU should add `#SBATCH --constraint=gpu` (see [GPU jobs](gpujobs.md)).

There is no direct ssh access to DINE2 nodes.

CUDA is available as a module, e.g. `module load nvhpc/25.11` (for V100 `sm_70` nodes, check `module avail nvhpc` / `module avail cuda` for a CUDA version that supports Volta).

## Known issues / notes

DINE2 nodes mount `/dine`, `/cosma7` (read-only), `/cosma8` and `/snap8`, not `/cosma5`.  Copy any necessary files into `/dine/data/PROJECT/USER/` or `/cosma8/data/PROJECT/USER/`.


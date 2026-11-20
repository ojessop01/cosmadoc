# Hardware name

Detailed description, including:
- Background (if any)
- Primary Purpose

## Specifications
- Detailed specs
    - Host:
        - Number of nodes available
        - Number of processors/accelerators per node
        - RAM per node
        - Network fabric used
    - Hardware:
        - Accelerator memory
        - Chip Architecture (CPU and accelerator if applicable)
        - Accelerator cores (CUs, CUDA cores, Tensix cores, etc.)
        - Cache topology (maybe a diagram to accompany?)
    
- Benchmarks (if available)
    - Memory bandwidth (babelstream)
- Link to SHAREing site

## Usage
- Link to "creating an account" page (adjust relative path when copying into `docs/source/`):
If you do not already have an account on COSMA, please follow the instructions [here](account.md), then request to join the project: CODE
- Slurm queue to use (or ssh if applicable)
- Recommended compiler
- Compatible compilers
- Recommended libraries/sdk
- SLURM/scheduler notes (e.g. `--gres=gpu:1`, `--gpus=N`, `--constraint=gpu`, `--nodelist`, `--exclude`)
- Hybrid daytime SSH / overnight Slurm schedule, if applicable (link to [hybrid nodes](../hardwarelab-hybridnodes.md))
- Mounted filesystems (e.g. `/cosma5`, `/cosma7`, `/cosma8`, `/dine`)

## Known issues
- Compilers known not to work
- Support for OpenMP or MPI

## Hints and tips

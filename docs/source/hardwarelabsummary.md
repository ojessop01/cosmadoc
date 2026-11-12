# COSMA GPU Nodes
Last updated: 21/01/2026

## Summary of Available GPU Nodes

| GPU | Count | Node(s) | Access | Partition | Account | Interconnect | Status |
|-----|-------|---------|--------|-----------|---------|--------------|--------|
| V100 | 6x | gn001 | SSH | - | do016 | - | ✓ |
| A30 | 8x total | gc001-008 | Slurm | dine2 | do015 | CerIO (composable) | Draining |
| A100 | 3x total | mad04-06 | Slurm / SSH | cosma8-shm | do016 | Liqid (composable) | ✓ |
| GH200 | 2x | gn002-003 | Slurm / SSH | gracehopper | do016 | - | ✓ |
| H100 NVL | 1x | gn004 | SSH (day) / Slurm (night) | hardwarelab-gpu | do016 | - | ✓ |
| MI100 | 1x | ga004 | Slurm | cosma8-shm2 | do018 | - | ✓ |
| MI210 | 2x each | ga005-006 | Slurm | cosma8-shm2 | do018 | - | ga006 draining |
| MI300X | 8x | ga007 | Slurm | mi300x | do018 | - | ✓ |
| MI300A | 4x | ga008 | SSH (day) / Slurm (night) | mi300a, hardwarelab-gpu | do018 | - | ✓ |
| PVC | 2x | gi001 | - | - | do017 | - | Dead |

## GPU Specifications (Theoretical)

| GPU | Architecture | FP64 TFLOPS | VRAM (GB) | Memory BW (GB/s) | Backend |
|-----|--------------|-------------|-----------|------------------|---------|
| V100 | Volta | 7.0 | 32 | 900 | CUDA |
| A30 | Ampere | 5.2 | 24 | 933 | CUDA |
| A100 | Ampere | 9.7 | 40 | 1555 | CUDA |
| GH200 | Hopper | 34 | 96 | 4000 | CUDA |
| H100 PCIe | Hopper | 26 | 80 | 2000 | CUDA |
| H100 SXM | Hopper | 34 | 80 | 3350 | CUDA |
| H100 NVL | Hopper | 34 | 94 | 3938 | CUDA |
| MI100 | CDNA | 11.5 | 32 | 1200 | HIP |
| MI210 | CDNA2 | 22.6 | 64 | 1600 | HIP |
| MI300X | CDNA3 | 81.7 | 192 | 5300 | HIP |
| MI300A | CDNA3 (APU) | 61.3 | 128 | 5300 | HIP |
| PVC | Xe HPC | 52.4 | 128 | 3280 | SYCL |

## Detailed Node Information

### NVIDIA CUDA Systems

| Node | GPUs | Host | Access | Account | Arch | Notes |
|------|------|------|--------|---------|------|-------|
| gn001 | 6x V100 (32GB) | 768GB, 2x Xeon Gold 5218 | SSH | do016? | sm_70 | |
| gc001-008 | 0-8x A30 (composable) | 2TB, 64 cores (Sapphire Rapids) | `dine2` | do015 | sm_80 | CerIO fabric; 8 GPUs total across 8 nodes |
| mad04, mad05 | 0-3x A100 40GB (composable) | 4TB, 128 cores | `cosma8-shm` | do016? | sm_80 | Liqid fabric; default 1 GPU each |
| mad06 | 0-3x A100 (composable) | 1TB, 128 cores (Milan-X, 768MB L3) | SSH | do016? | sm_80 | |
| gn002 | GH200 | ARM (aarch64) | SSH | do016 | sm_90 | ARM host: requires native compilation |
| gn003 | GH200 | ARM (aarch64) | `gracehopper` | do016 | sm_90 | No system cmake; CUDA 13.0 at `/usr/local/cuda-13.0/` |
| gn004 | 1x H100 PCIe | x86 (Intel) | SSH | do016? | sm_90 | |

### AMD HIP/ROCm Systems

| Node | GPUs | Host | Access | Account | Arch | Notes |
|------|------|------|--------|---------|------|-------|
| ga004 | 1x MI100 | 1TB, 128 cores (Milan 7713) | `cosma8-shm2` | do018? | gfx908 | |
| ga005, ga006 | 2x MI210 each | 1TB, 64 cores (EPYC 7513) | `cosma8-shm2` | do018? | gfx90a | Use `--exclude=ga004` for MI210 |
| ga007 | 8x MI300X | - | `mi300x` | do018 | gfx942 | |
| ga008 | 4x MI300A | 500GB shared | SSH | do018 | gfx942 | APU: CPU/GPU share physical RAM |

**Note:** ROCm 6.3.0 installed system level on AMD nodes at `/opt/rocm-6.3.0/`.

### Intel Systems

| Node | GPUs | Access | Account | Status |
|------|------|--------|---------|--------|
| gi001 | 2x Ponte Vecchio | - | do017 | Dead |

**Note:** Likely to stay dead for now!

## Compilers

| System | Compiler | Location | Notes |
|--------|----------|----------|-------|
| CUDA (x86, sm_80+) | nvcc 13.0 | `module load nvhpc/25.11` | sm_80, sm_90 |
| CUDA (GH200) | nvcc 13.0 | `/usr/local/cuda-13.0/bin/nvcc` | ARM host: `pip3 install --user cmake` |
| HIP (AMD nodes) | hipcc 6.3.0 | `/opt/rocm-6.3.0/bin/hipcc` | System-level: no module needed |

**Note:** The `hipcc/6.0amd`, `hipcc/6.3amd`, `hipcc/7.0amd` modules only set CC/CXX environment variables for dependent modules (e.g. MPI). ROCm is already available at system level.

## Project Codes (from SAFE)

| Code | Systems |
|------|---------|
| do015 | DINE2 (A30s) |
| do016 | NVIDIA GPUs (V100, A100, GH200, H100), cosma8-shm |
| do017 | Intel GPUs (dead) |
| do018 | AMD GPUs (MI100, MI210, MI300X, MI300A) |
| do009 | DINE, miscellaneous |

## Access/Useful Commands

### Check partition and node status
```bash
sinfo -a # list all partitions and statuses
sinfo -p cosma8-shm2 -N -l # detailed node info for a partition
squeue -p mi300x # show jobs running on partition
scontrol show partition=<partition_name> | grep AllowAccounts
```

### Check access permissions
```bash
id # show groups you belong to
scontrol show partition= | grep AllowAccounts # show accounts that can use partitions
```

### GPU Availability:
```bash
# NVDIA nodes
nvidia-smi

# AMD nodes
rocm-smi
rocminfo
```
Can use in slurm script to check GPU present.

### Slurm submission
```bash
# by partition
sbatch -p cosma8-shm -A do016 script.sh # A100 on cosma8-shm
# by specific node
sbatch --nodelist=ga004 script.sh # ga004

# interactive session
srun -p mi300x -A do018 -t 10 --pty /bin/bash # mi300x
```

### Direct SSH access
```bash
# From a COSMA login node:
ssh gn001 # V100s
ssh gn002 # Grace-Hopper (ARM)
ssh gn004 # H100
ssh ga008 # MI300A
ssh mad06 # A100 + Milan-X
```

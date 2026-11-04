# Hybrid interactive / batch hardware lab nodes

Some nodes that are part of the [Hardware Lab](hardwarelab.md) switch between interactive access and a slurm queue.

## Interactive

From 08:00 until 19:00 (UK time), the nodes are interactive and can be used for development or testing.  Access is available over ssh from a login node, provided you are part of an eligible [group](gpu.md#project-codes).

The nodes are a shared resource during this time, so please avoid large or long-running jobs that could prevent other users from making use of the resource.  Instead, run small proof-of-concept jobs and then submit larger jobs to the batch queue.

## Batch queue

From 19:00 until 08:00 the following day (UK time), the nodes become part of either the hardwarelab-cpu or hardwarelab-gpu slurm queue.  There is no interactive access to the nodes during this time.

This provides an opportunity to run uninterrupted production workloads or benchmarks on the lab hardware.

| Queue | Node | Hardware | Projects |
| ----- | ---- | -------- | -------- |
| `hardwarelab-gpu` | ga008 | 96 cores, 4x AMD MI300A | durham, do016, do017, do018 |
| `hardwarelab-gpu` | gn004 | 64 cores (Intel), 1x NVIDIA H100 NVL | durham, do016, do017, do018 |
| `hardwarelab-gpu` | gn005 | 256 cores (AMD Turin), 1x NVIDIA RTX PRO 6000 | durham, do016, do017, do018 |
| `hardwarelab-gpu` | mad06 | 128 cores (AMD Milan-X), NVIDIA A100 | durham, do016, do017, do018 |
| `hardwarelab-cpu` | gi001 | 112 cores (Intel Sapphire Rapids) | durham, do025 |
| `hardwarelab-cpu` | mad11 | 256 cores (Intel Sierra Forest) | durham, do025 |
| `hardwarelab-cpu` | mad12 | 256 cores (AMD Turin) | durham, do025 |

During the day, these queues show as `down`, and the nodes as drained with the reason `interactive`.

### SLURM tips for the batch queue

Since the partitions contain nodes of varying architectures, it does not make sense to submit blindly to either partition.
Instead, use `--exclude` or `--nodelist` to explicitly define which node(s) to submit your job to.

Additionally, since the queue ends at 08:00 the following day, a submitted job must fit inside the remaining time window.  The maximum job time on these queues is 6 hours.

An example slurm script targeting the RTX6000 might look like this.  The `--gres` line reserves the GPU: see [GPU jobs](gpujobs.md).

```sh
#!/bin/bash

#SBATCH -J job_name
#SBATCH -o standard_out.%J.out
#SBATCH -e standard_err.%J.err
#SBATCH -p hardwarelab-gpu
#SBATCH -A do016
#SBATCH --nodelist=gn005
#SBATCH --gres=gpu:1
#SBATCH -t 6:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=you@durham.ac.uk

module purge
module load nvhpc
./myprogram

```

## Additional information

For additional information on the nodes, their hardware configurations, or known issues, see the detailed Hardware Lab pages:
 - [GPUs](gpu.md)
 - [AMD](amdgpu.md)
 - [NVidia](nvidiagpu.md)
 - [CPUs](cpucomputelab.md)

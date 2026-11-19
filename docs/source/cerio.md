# The CerIO composable system, DINE2

The CerIO composable system is a small 8-node cluster.  Each node has 2TB RAM, and access to 8 NVIDIA A30 and 4 NVIDIA V100 GPUs, which can be composed to the requested nodes upon demand.

To submit jobs to this cluster, please use the `dine2` Slurm queue (or the `cosma8-dine2` queue if you have a DiRAC allocation there).  To determine which project you should select, use the `scontrol show partition=dine2` command.  Currently, this includes the `durham`, `do011` (SKA), `do015` and `do020` projects (use e.g. `#SBATCH -A durham` in your batch submission script).

To request a specific GPU composition, please contact [cosma-support](contact.md).

## System specifications

The DINE2 system is comprised of 8 nodes each with dual 32 core Intel Xeon Gold 6430 CPUs at 2.1GHz and 2TB RAM.

These nodes are connected to the COSMA8 HDR200 InfiniBand fabric.

These nodes also have the composable CerIO fabric, allowing dynamic composing of PCIe devices.  Current devices available for composition are:
 - 8x NVIDIA A30 GPUs
 - 4x NVIDIA V100 GPUs

To request a node with GPUs attached in Slurm, add `#SBATCH --constraint=gpu` (see [GPU jobs](gpujobs.md) and [DINE2](dine2.md)).

Any number of these GPUs can be composed to a server, so for example you can request:
 - 8 nodes each with 1 GPU
 - 1 node with 8 GPUs
 - 2 nodes with 3 GPUs and 1 node with 2 GPUs
 - Any other combination

This composable fabric has a 200Gb/s host interface and a 300Gb/s network fabric.

DINE2 is funded by DiRAC and SKA as a testbed to explore prototype CXL solutions, and make high RAM nodes available to the SKA community.

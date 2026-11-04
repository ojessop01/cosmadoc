# GPUs

COSMA has a number of GPU systems.  Some are in Slurm queues, some can be used directly with ssh from a login node, and some switch between the two:

| Node | GPUs | How to use it |
| ---- | ---- | ------------- |
| gn001 | 6x NVIDIA V100 | ssh |
| gn002 | 1x NVIDIA Grace Hopper (ARM) | ssh |
| gn004 | 1x NVIDIA H100 NVL | ssh during the day, `hardwarelab-gpu` queue overnight |
| gn005 | 1x NVIDIA RTX PRO 6000 | ssh during the day, `hardwarelab-gpu` queue overnight |
| mad06 | NVIDIA A100 (composable) | ssh during the day, `hardwarelab-gpu` queue overnight |
| ga008 | 4x AMD MI300A | ssh during the day, `mi300a` queue (2 hours), `hardwarelab-gpu` queue overnight |
| mad04, mad05 | NVIDIA A100 (composable, 1 per node by default) | `cosma8-shm` queue, or `cosma8-highram` for some DiRAC projects |
| ga004 | 1x AMD MI100 | `cosma8-shm2` queue |
| ga006 | 2x AMD MI210 | `cosma8-shm2` queue |
| gc001-gc008 | NVIDIA A30 and V100 (composable) | `dine2` queue, or `cosma8-dine2` for DiRAC projects |
| gn003 | 1x NVIDIA Grace Hopper (ARM) | `gracehopper` queue (6 hours) |
| ga007 | 8x AMD MI300X | `mi300x` queue (do018), or `cosma8-draper` (dp266) |
| gi001 | 2x Intel Ponte Vecchio | Not working |

The ga003 node, with 6x AMD MI50 GPUs, has been retired.

To use a GPU in a batch job, see [GPU jobs](gpujobs.md).  For the projects that each queue accepts, see [GPU queues](queue.md#gpu-queues).

## Project codes

To use the GPUs which are in a Slurm partition, you must either be part of a DiRAC project with a current allocation on the system, or sign up to the following project codes in [SAFE](https://safe.epcc.ed.ac.uk/dirac) as part of the hardware lab:

- do015: dine2 partition
- do016: NVIDIA GPUs, including Grace Hopper, H100, RTX PRO 6000 and the cosma8-shm partition
- do017: Intel GPUs (currently dead)
- do018: AMD GPUs

DiRAC allocated projects will have higher priority.

To use a GPU available for direct login, just ssh to the node name given above.  To use one in a batch job, see [GPU jobs](gpujobs.md).

**Note:** Some GPU nodes are in a hybrid mode to allow for testing during office hours and production workloads during the night.  Further information is available [here](hardwarelab-hybridnodes.md) and in the motd of relevant nodes.

## GPU stats

| GPU | FP64 TFLOPS | RAM/GB | Memory bandwidth/GB/s |
| --- | ----------- | --- | ---------------- |
| V100 | 7 | 32 | 900 |
| A100 |9.7 | 40 | 1555 |
| A30 | 5.2 | 24 | 933 |
| H100 PCIe | 26 | 80 | 2000 |
| H100 SMX | 34 | 80 | 3350 |
| RTX PRO 6000 | 2 (126 for FP32) | 96 | 1790 |
| MI50 | 6.6 | 16 | 1000 |
| MI100 | 11.5 | 32 | 1200 |
| MI210 | 22.6 | 64 | 1600 |
| MI300X | 81.7 | 192 | 5300 |
| MI300A | 61.3 | 128 | 5300 |
| PVC | 52.4 | 128 | 3280 |

There is a more [detailed GPU comparison table](gpuspecs.md) and for more information on specifications and usage, see the following pages:

## [AMD GPUs](amdgpu.md)

## [NVIDIA GPUs](nvidiagpu.md)

## Further notes on GPUs

For nodes not assigned to queues (mad06, gn001, gn002, gn005, ga008, gi001), please be aware that these are shared resources and that other people may be using (or may wish to use) them.

To use some of these GPUs, you may need to be in the "video" or "render" groups (use the ```id``` command to check which groups you are in).  If you are not in it, but need to be, please ask.

To check that you have the correct permissions to submit to a partition, you can use the ```scontrol show partition=PARTITION_NAME``` command to see which groups are allow to submit to that partition.

The Intel PVC GPUs on gi001 are currently dead - sometime in Autumn 2025.  Watch this space - we may be able to resurrect them.


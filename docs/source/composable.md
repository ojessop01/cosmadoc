# Composability

COSMA has two composable systems to allow experimentation with composability, i.e. the ability to define server components within software.

## Liqid system

A Liqid system installed in 2021 has 3 nodes (including a direct access node) to which both GPU and RAM can be composed upon demand (i.e. a request to cosma-support).

The GPUs are NVIDIA A100-40GB.  There are 3 GPUs which can be configured between the nodes.  Typically, we compose one GPU per node.  To request a GPU in a batch script on `cosma8-shm` or `hardwarelab-gpu`, add `#SBATCH --gres=gpu:1` (see [GPU jobs](gpujobs.md) and the [GPU page](gpu.md) for details).

The composed RAM is also usually shared between the nodes and presented as swap space.

The default configuration has one GPU per node.  Queues hosting `mad04` and `mad05` include `cosma8-shm`, `cosma8-ska2` and `cosma8-highram`.  `mad06` is a hybrid node: accessible by direct SSH during the day and via the `hardwarelab-gpu` queue overnight (see [hybrid nodes](hardwarelab-hybridnodes.md)).

## CerIO system

A [CerIO](cerio.md) system (DINE2) installed in 2024 has 8 nodes which share 12 GPUs (8x A30, 4x V100), allowing servers with up to 8 GPUs to be configured.  On `dine2`, request a GPU node with `#SBATCH --constraint=gpu`.  Follow the [CerIO](cerio.md) and [DINE2](dine2.md) instructions to use this system.

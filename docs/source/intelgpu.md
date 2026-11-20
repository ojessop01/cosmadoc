# Intel GPU Testbeds

COSMA has a Sapphire Rapids based node (`gi001`) with 2x Intel Ponte Vecchio Data Centre GPUs.  This allows code development, porting and performance benchmarking.

Please note that the Ponte Vecchio GPUs have been dead since Autumn 2025 and are not currently accessible.  `gi001` remains available as a Sapphire Rapids CPU node in the `hardwarelab-cpu` queue (see [CPU compute lab](cpucomputelab.md) and [hybrid nodes](hardwarelab-hybridnodes.md)).

The `xpu-smi` command can be used to see GPU details when available, and a SYCL compiler is available from oneAPI (`module load intel_comp`).

More information is given on the [GPU pages](gpu.md).

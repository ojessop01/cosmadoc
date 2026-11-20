# Usage of the Rockport Network System

Half of COSMA7 now has a [Rockport](https://www.cerio.io) Ethernet network fabric, rather than InfiniBand.

This is available for anyone with an active DiRAC project on COSMA7 to use. Please ask if you are unsure (or just try to use it).

Please note, COSMA7 nodes have 28 cores and 512GB RAM each. The `cosma7` partition has 220 nodes and the `cosma7-rp` (Rockport) partition has 222 nodes.

This is exploratory and will allow us to benchmark and explore this technology for use in future DiRAC procurements.

It is based on a 6D torus topology, rather than the 2:1 blocking fat tree fabric used by the rest of COSMA7. It should offer consistently low latency even when the network is heavily congested, and so workloads that are latency dependent, or suffer when there is congestion should benefit. Each node has 100 GBit/s connectivity (also the case for the InfiniBand nodes).

To use the Rockport nodes, you should submit jobs to the cosma7-rp partition. e.g. within your batch script, you would use:

    #SBATCH -p cosma7-rp

You are also advised to load the rockport-settings environment module within your SLURM batch script:

    module load rockport-settings

This sets some environment variables which then allow the Rockport fabric to be used most efficiently. To see these, you can use:

    module show rockport-settings

If using Intel MPI, you can simply use mpirun.

If using OpenMPI, use `mpirun $RP_OPENMPI_ARGS` ...

## MPI

The recommended MPI libraries to use are (as of June 2022):

Intel 2018: `module load intel_comp/2018`

Intel 2024: `module load intel_comp/2024.2.0 compiler-rt tbb compiler mpi` (and you should probably also `module load ucx` as this has been demonstrated to give significantly improved performance)

OpenMPI 5.0.3: `module load openmpi/5.0.3`

## Multipath

To enable multipath on a per-job basis, add to the mpirun command-line (when using UCX), for OpenMPI:

    -x UCX_IB_TRAFFIC_CLASS=160

and for Intel MPI (after 2018):

    -genv UCX_IB_TRAFFIC_CLASS=160

This allows packets to take multiple routes between pairs of nodes increasing direct bandwidth between these nodes.

## Other Settings

Rockport recommend some other settings for RDMA transports:

    --fwd-mpirun-port

    --mca oob_tcp_listen_mode listen_thread

## Storage

The Rockport partition does not currently have dedicated (fabric-native) storage. Rather, the /cosma7, /cosma8 etc storage are routed through 4 dedicated nodes. This results in a slight reduction in performance. Therefore, when benchmarking codes, please don't include any time to read or write to storage.

Not all storage systems are mounted on the Rockport partition — see [mounted file systems](storage.md#mounted-filesystems) before use (for example `/cosma5` and `/cosma8` are not mounted on COSMA7 compute nodes).

## Benchmarking

We are very interested to see how the Rockport partition compares (performance-wise) with the cosma7 partition. Therefore, if you are able to do any tests or code comparisons, please let us know, and pass on any results that you get.

There is additional time allocation available for benchmarking - please let us know if you would like to use this.



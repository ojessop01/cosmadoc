# CPU Compute Lab

The CPU Compute Lab provides access to latest generation CPU technologies, to enable code porting and optimisation by UK researchers in preparation for future large production systems.

Day time is 08:00 to 19:00 (UK time), and night time is 19:00 to 08:00: see [hybrid nodes](hardwarelab-hybridnodes.md).

Current systems include
- Intel Sierra Forest
  - Day time: Direct ssh to the mad11 node (apply to join do025)
  - Night time: Submit jobs to the hardwarelab-cpu partition
- AMD Turin
  - Day time: Direct ssh to the mad12 node (apply to join do025)
  - Night time: Submit jobs to the hardwarelab-cpu partition
- [Intel Sapphire Rapids (2024)](#more-on-sapphire-rapids)
  - Via the dine2 Slurm partition for 64-core nodes (apply to join do015)
  - For the 112-core gi001 node:
    - Day time: Direct ssh to the gi001 node (apply to join do017)
    - Night time: Submit jobs to the hardwarelab-cpu partition (which accepts the durham and do025 projects)
- AMD Bergamo (2023)
  - Via the cosma5 Slurm partition (ICC collaborators only: apply to join hpcicc)
- AMD Genoa (2023)
  - Via the cosma8-shm3 Slurm partition (mad08,09 nodes, apply to join do009)
  - Now retired: Direct ssh to the mad13 node (apply to join do025)
- Intel IceLake (2022)
  - Via the cosma8-ska Slurm partition (SKA only: apply to join do011)
- AMD Milan (2021)
  - Via the cosma8-milan Slurm partition (DiRAC RAC users)
- AMD Milan-X (2022, high L3 cache variant)
  - Day time: Direct ssh to the mad06 node (apply to join do016)
  - Night time: Submit to the hardwarelab-gpu Slurm partition
- AMD Rome (2019)
  - Via the cosma8-rome Slurm partition (DiRAC RAC users)
- Intel CascadeLake (2019)
  - Via the cosma7-shm2 Slurm partition (apply to join do025)

## More on Sapphire Rapids

We have two systems with Intel Sapphire Rapids CPUs.
- A single node, gi001, also containing Ponte Vecchio GPUs
  - CPU name:       Intel(R) Xeon(R) Platinum 8480+
  - Sockets:                2
  - Cores per socket:       56
  - Threads per core:       2
  - RAM:	      		  512 GB
  - Network: HDR200 InfiniBand
- The DINE2 system with 8 nodes
  - CPU model: Intel(R) Xeon(R) Gold 6430
  - Sockets: 2
  - Cores per socket: 32
  - Threads per core: 2
  - RAM: 2TB
  - Network: HDR200 InfiniBand
  
### Node access

Our single node Sapphire Rapids system contains Ponte Vecchio GPUs (PVCs), though these are currently broken. Therefore, this node is currently available for direct ssh during the day (to gi001), and as part of the hardwarelab-cpu Slurm queue at night, for benchmarking and profiling jobs.

The DINE2 system can be accessed via the dine2 Slurm partition.

### Environment

As this is an Intel node while Cosma's login nodes are AMD, we recommend to compile exclusively on the node:

```sh
module load intel_comp
module load compiler-rt tbb compiler mpi
```

The module oneAPI should work as well.

This can be done during the day via direct SSH to the node.

### Performance

To assess the node's performance, we recommend to run

```sh
module load likwid
likwid-bench
```

Type in -a or -h to see an overview of the available metrics. Stream Triad and peak are the ones we usually recommend to look at first.


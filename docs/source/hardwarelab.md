# HPC Hardware Lab @Durham

The [HPC Hardware Laboratory @Durham](https://durham.readthedocs.io/en/latest/hardwarelab) is used for prototyping and development of new systems and technologies.
It is hosted within, yet independent of the [COSMA HPC facility](https://cosma.readthedocs.io) and receives funding from Durham University, industry partners, UKRI (e.g. through [ExCALIBUR](https://excalibur.ac.uk/)) and [DiRAC](https://dirac.ac.uk/).
Many of the systems tested are readily available for benchmarking.  Details of available nodes and GPUs can be found [here](hardwarelabsummary.md).

UK researchers can request access to the HPC Hardware Lab.

## Adding equipment

If you are a vendor, integrator or hardware developer, and would like to have your hardware added to the HPC Hardware Lab, please contact cosma-support@durham.ac.uk

## Access

To request access to any of the systems within the hardware lab, please [create an account](account.md) and request to join the corresponding [project code](project.md#hpc-hardware-lab-projects).  Please contact cosma-support@durham.ac.uk when you request an account so that it can be set up correctly.

The Hardware Lab features the following systems and technologies:  
- [DINE and DINE2](#dine-and-dine2)  
- [GPU compute nodes](#gpu-compute) (AMD, NVIDIA, Intel)
- [CPU Compute Lab](#cpu-compute-lab)  
  - [Tenstorrent RISC-V system](#tenstorrent-blackhole-node-risc-v)
  - [Advanced ARM systems](#arm-systems)
- [Composable Infrastructure](#composable-infrastructure)  
- [Rockport Network Fabric](#rockport-network-fabric)  
- [Quantum Annealing (expired)](#dwave-quantum)  
- [Storage Lab](#storage-lab)
- [Solar Power](#solar)
- [Immersion Cooling](#immersion-cooling)
- [Heat Storage](#heat-storage)

There are a number of other hardware lab facilities around the UK.  If you are looking for specific hardware which is not on this list, a good starting point to search for available facilities is the [collection maintained by the SHAREing project](https://shareing-dri.github.io/resources/).


## DINE and DINE2

DINE and DINE2 are experimental test clusters for exploring new hardware and networking technologies.

![DINE](images/dine.png)

[DINE](dine.md) has 18 nodes currently in use (`bluefield1` partition), each containing an NVIDIA BlueField-2 Data Processing Unit, with HDR200 InfiniBand connectivity.  
It was previously equipped with BlueField1 and Rockport network cards.
To use this facility, join the do009 project and submit jobs to the `bluefield1` Slurm partition.  

The [DINE2](dine2.md) cluster is an 8-node cluster equipped with a CerIO composability fabric, allowing GPUs to be added to servers upon demand.  To use the DINE2 cluster as a Hardware Lab user, apply to join the do015 project.

## GPU compute

We maintain [multiple generations of GPU architecture](gpu.md) from multiple vendors.  Some nodes operate in hybrid mode (direct SSH during the day, Slurm overnight): see [hybrid nodes](hardwarelab-hybridnodes.md).

### AMD GPU nodes

We have multiple generations of [AMD MI GPU](amdgpu.md):
- MI100
- MI210
- MI300A
- MI300X

The `cosma8-shm2` partition contains an AMD MI100 node (`ga004`) and a dual-MI210 node (`ga006`).  To select a particular GPU, use `--gres=gpu:instinct_mi210:1`, `--nodelist` or `--exclude` (see [GPU jobs](gpujobs.md)).

For the MI300X GPUs, submit to the `mi300x` queue (node `ga007`).  For the MI300A GPUs (`ga008`), ssh directly from a login node during the day, submit to the `mi300a` queue (up to 2 hours), or submit to the `hardwarelab-gpu` queue overnight.

### NVIDIA GPU nodes

V100, A30, A100, H100 NVL, GH200 and RTX PRO 6000 nodes are [available for use](nvidiagpu.md), including Intel-Hopper (x86 CPU) and Grace-Hopper (ARM CPU).

### Intel GPU nodes

A [Ponte Vecchio GPU](intelgpu.md) node (`gi001`) was once available; the GPUs have been dead since Autumn 2025, though the node remains active as a Sapphire Rapids CPU node in `hardwarelab-cpu`.

## Composable infrastructure

COSMA contains a [composable](composable.md) GPU and RAM system, attached to the `cosma8-shm` queue.  If you need to use these resources in a different configuration, please [contact cosma-support](contact.md).

COSMA also hosts an 8-node system (DINE2) with 8x A30 and 4x V100 GPUs, allowing up to 8 GPUs per node, based on a CerIO composable fabric.

## Rockport network fabric

The [Rockport network fabric](rockportlab.md) is a 6D torus network with 100G connectivity, installed as half of COSMA7 (see [usage instructions](rockport.md)).  To use this, please submit to the `cosma7-rp` Slurm partition.

## DWAVE quantum

The ExCALIBUR project funded [quantum annealing system access](quantum.md) via a DWAVE system (and later QuEra), administered by COSMA staff.  Both allocations have now expired; if you are interested in future quantum access, please [contact cosma-support](contact.md).

## CPU compute lab

A wide variety of [processor technologies](cpucomputelab.md) are available for testing and benchmarking (`do025` project code) and we try to maintain cutting-edge components.

### Tenstorrent Blackhole node (RISC-V)

A [Tenstorrent Blackhole](tenstorrent.md) server is available for interactive use (`do023` project code), containing 4x Blackhole cards.

Tenstorrent cards are designed specifically for AI and machine-learning workloads, unlike GPUs which have been adapted over time from their original graphics rendering workloads.  Currently PyTorch, ONNX, and TensorFlow can be easily ported to Tenstorrent architecture, but software support is otherwise in the early stages of development.

### ARM systems

We host NVIDIA Grace ARM CPUs (`gn002` and `gn003`).

Another ARM CPU ([Fujitsu Monaka](monaka.md)) will shortly be available for testing (early 2027).

## Storage lab

Our [storage laboratory](storagelab.md) includes prototype and production file systems of various types and technologies.

## Solar

Our [solar installation](environmental.md#solar-panels) provides power directly usable by COSMA, allowing us to study the interplay between solar energy generation and HPC power usage.

## Immersion cooling

We have a prototype [immersion cooling](immersion.md) tank, and provide access to this facility to HPC technical support teams from across the UK, to help reduce the entry barrier to this technology, and to develop experience using it.

## Heat storage

We are investigating the [inter-seasonal storage of waste data centre heat](https://durham.readthedocs.io/en/latest/ichs/index.html) using abandoned flooded coal mines beneath the data centre site, to allow this heat to be used for building heating during the colder winter months.





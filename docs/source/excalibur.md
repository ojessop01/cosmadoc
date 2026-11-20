# ExCALIBUR

ExCALIBUR was the UK Exascale preparation scheme (2019-2024), providing hardware and software effort in order to prepare the UK HPC community for forthcoming Exascale services.

COSMA hosts several enabling hardware prototype systems funded by ExCALIBUR, which are hosted as part of the [HPC Hardware Laboratory](hardwarelab.md):

1. [DINE](facilities.md#dine) - a BlueField-2 (previously BlueField-1) enabled HPC cluster

2. [AMD MI GPU systems](excalibur.md#amd-gpu-systems)

3. A Rockport network fabric, using a switchless 6D torus topology

4. CXL-prototype composable RAM systems

5. [DWAVE quantum annealing credits](#dwave-quantum-annealing-credits)

To use these systems, please contact [cosma-support](contact.md).

## AMD GPU systems

COSMA has an MI100 GPU in server `ga004` (see [AMD GPUs](amdgpu.md) and [GPU jobs](gpujobs.md) for current AMD GPU systems).

There were also six AMD MI50 GPUs hosted in the `ga003` server, now decommissioned. These were interlinked with a 4x and 2x InfinityFabric link between the GPUs, to enable direct data transfer. Newer MI GPUs are available instead.

Relevant GPU programming software (ROCm) is available as the `hipcc` module (`module available hipcc`).  The AMD AOCC compiler is only available among the older modules: run `module load old-modules`, then `module avail aocc_comp` (the newest is `aocc_comp/5.2.0`).

The `amd-smi` (or `rocm-smi`) command provides information about the GPUs.

These systems are available for general use. If you use them, feedback would be welcome, in particular around performance, and the software environment.

## DWAVE quantum annealing credits

From 1st June 2023 for a 24 month period, we arranged access to DWAVE quantum annealing systems.

This was available to any of the UK community.

## ExCALIBUR software projects at Durham

There were several ExCALIBUR software projects (now finished) at Durham, investigating Exascale software techniques to allow codes to run effectively on Exascale systems. These are:

1. [Clawpack enabled Exahype for heterogeneous hardware](https://tobiasweinzierl.webspace.durham.ac.uk/software/peano/projects/exaclaw-clawpack-enabled-exahype-for-heterogeneous-hardware/)

2. [Massively Parallel Particle Hydrodynamics for Engineering and Astrophysics](excalibur.md#mpphea)

3. Particles At Exascale (PAX)

4. [Quantum Enhanced and Verified Exascale Computing (QEVEC)](https://excalibur.ac.uk/projects/qevec/)

### MPPHEA

Massively Parallel Particle Hydrodynamics for Engineering and Astrophysics

SPH (smoothed particle hydrodynamics), and Lagrangian approaches to hydrodynamics in general, are a powerful approach to hydrodynamics problems. In this scheme, the fluid is represented by a large number of particles. Each particle tracks a Lagrangian element, moving with the flow. The scheme does not require a predefined grid making it very suitable for tracking flows with moving boundaries, particularly flows with a free surfaces, and problems that involve the mixing of different fluids, flows with physically active elements or large dynamic range. The method was originally developed to study stellar collisions, but is widely adopted in engineering and cosmology because of it flexibility, adaptivity and natural multi-physics capability. The range of applications of the method is growing rapidly and is being adopted by a rapidly growing range of commercial companies including Airbus, Unilever, Shell, EDF, Michelin and Renault.

The widespread use of SPH, and its potential for adoption across a wide range of science domains, make it a priority use case for the Excalibur project. Massively parallel simulations with billion to hundreds of billions of particles will revolutionise our understanding of the Universe and will empower engineering applications of unprecedented scale, ranging from the end-to-end simulation of transients (such as bird strike) in a jet engines, to simulation of tsunami waves over-running a series of defensive walls.

The ExCALIBUR project brings together a wide range of experience and knowledge, from Engineering, Computer Science and Astrophysics. The group will identify the limitations of current approaches and will develop proof of concept solutions that will set out the path to SPH simulations in the exa-scale limit.The working group bring together two state of the art codes. SWIFT and DualSPHysics:

1. [SWIFT](https://swift.strw.leidenuniv.nl): a state-of-the-art SPH fluid dynamics solver that uses a novel Fine-grained task parallelism approach

2. [DualSPHysics](https://dual.sphysics.org): a state of the art GPU enabled SPH code.

__The team__

PI:

Richard Bower (Durham)

Co-Is:

Alastair Basden (Durham)

Tobias Weinzierl (Durham)

Carlos Frenk (Durham)

Benedict Rogers (Manchester)

Georgios Fourtakas (Manchester)

Scott Kay (Manchester)

Robert Crain (Liverpool John Moores)

Tom de Vuyst (Hertfordshire)

Pablo Lauren-Aguilar (Exeter)

Dave Acreman (Exeter)

Matthieu Schaller (Leiden)

#### Workgroup meeting minutes

Unedited meeting minutes

__Resources__

- [MPPHEA minutes 200921](minutes/minutes200921_software.txt) (last modified: 11 December 2020)
- [MPPHEA minutes 201019](minutes/minutes201019_software.txt) (last modified: 11 December 2020)
- [MPPHEA minutes 201102](minutes/minutes201102_software.txt) (last modified: 11 December 2020)
- [MPPHEA minutes 201116](minutes/minutes201116_software.txt) (last modified: 11 December 2020)
- [MPPHEA minutes 201130](minutes/minutes201130_software.txt) (last modified: 11 December 2020)
- [MPPHEA minutes 201214](minutes/minutes201214_software.txt) (last modified: 8 January 2021)
- [MPPHEA minutes 210111](minutes/minutes210111_software.txt) (last modified: 22 January 2021)
- [MPPHEA minutes 210125](minutes/minutes210125_software.txt) (last modified: 21 February 2021)
- [MPPHEA minutes 210208](minutes/minutes210208_software.txt) (last modified: 21 February 2021)
- [MPPHEA minutes 210222](minutes/minutes210222_software.txt) (last modified: 8 March 2021)
- [MPPHEA minutes 210308](minutes/minutes210308_software.txt) (last modified: 22 March 2021)
- [MPPHEA minutes 210412](minutes/minutes210412_software.txt) (last modified: 13 April 2021)
- [MPPHEA minutes 210517](minutes/minutes210517_software.txt) (last modified: 28 May 2021)
- [MPPHEA minutes 210601](minutes/minutes210601_software.txt) (last modified: 14 June 2021)
- [MPPHEA minutes 210621](minutes/minutes210621_software.txt) (last modified: 2 July 2021)
- [MPPHEA minutes 210816](minutes/minutes210816_software.txt) (last modified: 17 August 2021)
- [MPPHEA minutes 210906](minutes/minutes210906_software.txt) (last modified: 13 December 2021)
- [MPPHEA minutes 211108](minutes/minutes211108_software.txt) (last modified: 13 December 2021)
- [MPPHEA minutes 220124](minutes/minutes220124_software.txt) (last modified: 9 February 2022)
- [MPPHEA minutes 220207](minutes/minutes220207_software.txt) (last modified: 9 February 2022)


## ExCALIBUR Training

A [code performance workshop series](https://tobiasweinzierl.webspace.durham.ac.uk/software/peano/workshops/2021-performance-analysis-workshop-from-analysis-to-insight/) (7 monthly workshops) was run in 2021, and we are looking at repeating this in the future.

## ExCALIBUR Cross-cutting research

The Quantum Enhanced and Verified Exascale Computing (QEVEC) project has been funded as part of the ExCALIBUR cross-cutting research call.

# LHDC tour

## 1) Overview

Welcome to the Lydia Heck Data Centre (LHDC)! This facility is named after Lydia Heck, the COSMA system administrator prior to her retirement in 2019.

LHDC includes two national DiRAC clusters (COSMA7 and COSMA8), a local Durham astronomy cluster (COSMA5), the Durham/SKA dine2 cluster and numerous test facilities including a range of GPU servers.

## 2) Cooling pipes

Water enters the room at 18C and leaves at 22C, from where it heads to the roof. There the cooling mechanism chillers release the excess heat to the atmosphere, before returning the water to the room at 18C once again. When the pumps fail, the temperature rises by 1°C every 10 minutes, and then we have just 1.5 hours to switch off the machine before it starts to sustain damage!

## 3) CDU (Cooling Distribution Unit)

LHDC hosts two CDUs. They run heat exchangers that transfer heat between the primary loop that runs to the roof chillers and the seconday loop that cools the servers.   

## 4) Immersion Tank

Our immersion tank is part of a pilot project to harness supercomputer waste heat. Six servers, including eleven COSMA5 nodes, are fully immersed in mineral oil that removes the heat generated. At present this heat is dispersed to the standard COSMA CDUs, but in future may instead be routed into a science site heat network.  

## 5) COSMA5 Compute

Once a DiRAC facility of several hundred IBM servers, COSMA5 now constitutes just eight compute nodes, each of which features two AMD Bergamo chips. Three are Dell machines in a standrad rack while the other five are Gigabyte servers located in the immersion cooling tank. They are for Durham researchers to perform small tasks, such as parameter searches and analysis of telescope data. 

## 6) COSMA8 Compute

COSMA8 is the DiRAC service that caters for all UK-based fundamental physicists working in high-memory-per-node applications. It includes over 520 servers, mostly with AMD Rome chips and some with AMD Milan chips, which are cooled with direct liquid cooling (DLC) on chip. It was installed in stages between 2020 and 2023. 

## 7) `/snap8`

Data centres feature a range of storage arrays to cover different needs. The `/snap8` array provides 1.1PB of fast scratch storage for jobs run on cosma8. It therefore prioritises speed of read-write access over resilience. Users for the most intensive jobs will therefore write their data to `/snap8` during the job run and then transfer it to a resilient store as quickly as possible once the job is completed.

## 8) `/cosma8`

The `/cosma8` storage array is the bulk storage for jobs performed on COSMA8. It is 18PB in total, and is built out of 1680 16TB disks in a RAID 6 configuration. It is therefore possible for each disk pool to have two disks fail at any one time without losing data. The filesystem is managed with Lustre.  

## 9) COSMA7-IB

The COSMA7 DiRAC service was installed in 2017, with approximately 448 nodes, each of which contains 2 Intel Skylake CPUs and communicate with one another over an infiniband fabric. In 2021 the service was split in half, where the half that retained the infiband fabric became COSMA7-IB.

## 10) COSMA7-RP

After the COSMA7 service was split in half, one of the halves adopted the novel Rockport fabric. This is a novel technology that had the potential to operate more efficiently when many machines were attempting to communicate at the same time. In practice, the performance has been comparable to the traditional infiniband fabric.  

## 11) `/cosma7` & `/cosma5`

The `/cosma5` and `/cosma7` arrays are RAID 6 lustre storage arrays that serve their respective compute clusters. They differ in that `/cosma5` is a just-a-bunch-of-disks (JBOD) setup where the redundancy between disks is managed by software, while `/cosma7` instead implements a RAID in the hardware.

## 12) `/snap7`

`/snap7` provides fast access storage for COSMA7 compute jobs. Like `/snap8`, it does not have any redundancy and so loss of any one disk will result in a loss of data.   

## 13) Cooled doors

Cooling within rack doors is crucial for removing heat from the room. Heat is blown from the CPUs into the doors by the server fans, where some of the waste heat is absorbed by the liquid flow within the doors and transported to the CDU heat exchanger and onward on its journey to the roof chillers. 

## 14) GPU testbed systems

LHDC hosts several testbed GPU machines, which are primarily used for training and code development purposes. These include three unified memory machines -- an AMD MI300A box plus two Nvidia Gracehoppers -- and one server that hosts eight AMD MI300X GPUs.    

## 15) IB core switches

The largest jobs will use half or even the vast majority of the available COSMA8 nodes, and communication between these nodes is a major potential bottleneck. They are therefore served by a non-blocking tree infiniband (IB) fabric, with 20 HDR cosma8 core switches in this rack. In the cosma7 racks there are 12 EDR core switches. 

## 16) COSMA8 login nodes

Users of COSMA8 do most of their coding and analysis work on the two COSMA8 login nodes, login8a and login8b, each of which has 64 physical processors and 2Tb of memory. They are shared between all users, and it is therefore crucial that these two machines keep running at high performance as much as possible. Ironically, it is their high usage that means they are particularly susceptible to having all their resources used up, and as a result the COSMA support team monitors their usage to intercept potential crashes, such as for memory exhaustion.

## 17) CerIO

The CerIO fabric links eight Intel servers, which constitute the dine2 compute partition, to two GPU chassis, one of which hosts eight NVidia A30s and the other four NVidia V100s. This is a composable system, where the COSMA team can specify how many GPUs to attach -- or 'compose' -- to each server. It is joint funded by DiRAC and SKA, therefore it supports both GPU computations and radio astronomy work.   

## 18) PDU (Power Distribution Unit)

The PDUs distribute power to racks and within racks, and enable us to isolate sets of racks from the rest of the system if there is a problem.

## 19) Power

HPC systems requiring large amounts of power, including 0.5MW for cosma8. These power needs are met in part by a series of solar panels located across Durham University buildings.

## 20) Tape library

The COSMA storage is supported by two tape libraries, one in LHDC and a second in the Odgen Centre West building (OCW); a third is being installed in the computer science building on Upper Mountjoy. Large datasets are backed up at the user's request to free up disk storage, and homespaces are backed up automatically at regular intervals.

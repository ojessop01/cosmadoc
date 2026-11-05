
# COSMA job queues

COSMA has many queues (also called partitions), for different hardware and projects.  This page explains which to use, and what each one offers.  For how to submit a job, see [your first job](firstjob.md) and [Slurm](slurm.md).

The details on this page come from the Slurm configuration in November 2026.  To see the current settings for a queue, run `scontrol show partition NAME`: see [checking a queue yourself](#checking-a-queue-yourself).

## Which queue should I use?

| If you are | Use | Notes |
| ---------- | --- | ----- |
| On a DiRAC project with COSMA8 time | `cosma8` | Each job gets whole nodes of 128 cores |
| On a DiRAC project with COSMA8 time, and need less than a node | `cosma8-serial` | Your job only reserves the cores that it asks for |
| On a DiRAC project with COSMA7 time | `cosma7` or `cosma7-rp` | Each job gets whole nodes of 28 cores |
| A Durham user | `cosma5` | Nodes are shared between jobs |
| Needing a lot of memory on one node | One of the [large memory queues](#large-memory-queues) | |
| Needing GPUs | One of the [GPU queues](#gpu-queues) | |

Each queue only accepts some projects.  If you are not sure which you can use, run `groups` to see your projects, and see [checking a queue yourself](#checking-a-queue-yourself).  If a project uses up its DiRAC allocation, its jobs are moved to a lower priority `-pauper` queue automatically.

## Main queues

| Queue | Nodes | Cores per node | Memory per node | Maximum time | Shares nodes? |
| ----- | ----- | -------------- | --------------- | ------------ | ------------- |
| `cosma8` | 527 (m8001-m8527) | 128 | 1TB | 3 days | No |
| `cosma8-serial` | The same 527 nodes | 128 | 1TB | 3 days | Yes |
| `cosma8-rome` | 356 (m8001-m8356) | 128 | 1TB | 3 days | No |
| `cosma8-milan` | 171 (m8357-m8527) | 128 | 1TB | 3 days | No |
| `cosma7` | 220 (m7229-m7448) | 28 | 512GB | 3 days | No |
| `cosma7-rp` | 222 (m7001-m7222) | 28 | 512GB | 3 days | No |
| `cosma5` | 8 (m5001-m5008) | 256 | 1.5TB | 3 days | Yes |

On queues that do not share nodes, a job that asks for 1 core is still charged for the whole node.  On queues that share nodes, please say how much memory you need with `--mem`, because the default depends on the queue:

| Queue | Default memory per core |
| ----- | ----------------------- |
| `cosma8-serial` | 8GB |
| `cosma5` | 4GB, and Slurm adds cores to a job that asks for more than 6GB per core |

## Queue variants

The main queues have variants that use the same nodes, with different limits and priorities:

| Variant | For example | Maximum time | Priority | Who can use it |
| ------- | ----------- | ------------ | -------- | -------------- |
| Normal | `cosma8`, `cosma7` | 3 days | Normal | Projects with time on the system |
| `-prince` | `cosma8-prince`, `cosma7-rp-prince` | 30 days | Highest | By request only |
| `-pauper` | `cosma8-pauper`, `cosma7-pauper` | 1 day | Lowest | Projects with time on the system |
| `-serial` | `cosma8-serial` | 3 days | Normal | As `cosma8`, sharing nodes |
| `-rome`, `-milan` | `cosma8-rome-pauper` | 3 days | As above | As above, using one type of node |
| `-test` | `cosma8-test` | 3 to 30 days | High | Restricted to the `dphsprog` group |

The `-prince` queues are for jobs with a good reason to run longer than 3 days, or with a higher priority.  They can be used by large jobs instead of a reservation, which improves the efficiency of the system.  To use them, please ask cosma-support.

The `-pauper` queues are for low priority jobs, mostly from projects that have used up their allocation, which are moved there automatically.  Their jobs can still run when nodes would otherwise be idle.  `cosma8-rome-pauper` and `cosma8-milan-pauper` allow up to 3 days, unlike the other `-pauper` queues.

Jobs in a higher priority queue always start before jobs in a lower one when both are waiting for the same nodes.  However, a lower priority job can start first if it fits into a gap before the higher priority job could start: see [backfill](faq.md#what-is-backfill-how-do-i-exploit-this).  Setting a realistic time limit makes this more likely.

## COSMA8

COSMA8 is the DiRAC-3 system, with two generations of AMD processor:

| Nodes | Processor | Queue to use only these nodes |
| ----- | --------- | ----------------------------- |
| m8001-m8356 | 2x AMD EPYC 7H12 (Rome) | `cosma8-rome` |
| m8357-m8527 | 2x AMD EPYC 7763 (Milan) | `cosma8-milan` |

There is a 10-20% difference in performance between them.  `cosma8` uses either.

Access to COSMA8 is only for DiRAC projects with a time allocation on it.  If your job does not need a whole node, use `cosma8-serial`.  Your job may then share a node with other jobs.  Unless you request memory, for example with `#SBATCH --mem=800G`, it gets 8GB for each core that it asks for.  To have a node to yourself, use `cosma8` instead.

## COSMA7

COSMA7 has two halves, with 220 and 222 nodes.  Each node has 28 cores (2x Intel Xeon Gold 5120) and 512GB of memory.

| Queue | Nodes | Network |
| ----- | ----- | ------- |
| `cosma7` | m7229-m7448 | 100Gbit/s InfiniBand |
| `cosma7-rp` | m7001-m7222 | 100Gbit/s Rockport Ethernet (6D torus) |

A single job can only use one half.

Every job gets whole nodes, so a job that needs a single core is still charged for 28.  If your work uses less than a node, combine several tasks in one job, for example with [many single-core tasks](slurm.md#many-single-core-tasks).  There is no COSMA7 queue for jobs that need less than a node: see [what if my job does not need a whole node?](faq.md#what-if-my-job-does-not-need-a-whole-node)

## COSMA5

COSMA5 is a Durham system for ICC users and collaborators, and is not part of DiRAC.  The `cosma5` queue has 8 nodes, each with 256 cores (2x AMD EPYC 9754) and 1.5TB of memory.  The old COSMA5 nodes, which started service in 2012 with 16 cores per node, were retired in 2025.

The queue shares nodes between jobs.  The `--exclusive` flag is ignored, so to have a node to yourself, request all 256 cores.  Please request the memory that your job needs, otherwise it gets 4GB per core.

These compute nodes are different from the COSMA5 login node, in both hardware and the file systems available: see [COSMA5](facilities.md#cosma5) and [mounted file systems](storage.md#mounted-filesystems).

COSMA5 does not appear in the [COSMA usage pages](https://virgodb.cosma.dur.ac.uk/usage/login.php), because DiRAC does not award allocations on it.

## Large memory queues

These queues have a few nodes with much more memory per core than the main queues.  They all share nodes, and allow up to 3 days unless noted.

| Queue | Nodes | Cores | Memory | Default memory per core | Notes |
| ----- | ----- | ----- | ------ | ----------------------- | ----- |
| `cosma7-shm` | mad01 | 56 | 3TB | 13.6GB | |
| `cosma7-shm` | mad02 | 112 | 1.5TB | 13.6GB | |
| `cosma7-shm2` | mad03 | 48 | 6TB | 46GB | durham and do025 only |
| `cosma7-mad` | mad01 | 56 | 3TB | 27GB | Project `mad` only |
| `cosma8-shm` | mad04, mad05 | 128 | 4TB | 32GB | NVIDIA A100 GPUs |
| `cosma8-highram` | mad04, mad05 | 128 | 4TB | 32GB | The same nodes as `cosma8-shm`, for some DiRAC projects |
| `cosma8-shm3` | mad08, mad09 | 192 | 768GB | 4GB | AMD Genoa |
| `cosma8-ska` | mad07 | 56 | 4TB | 50GB | durham and do011 (SKA) |
| `cosma8-ska2` | mad01, mad03, mad04, mad05 | 48-128 | 3-6TB | 13GB | durham and do011 (SKA) |
| `cosma-analyse` | mad01, mad02, mad03 | 48-112 | 1.5-6TB | 13GB | For analysing cosmological data.  1 node and 1 day per job |

See also [what are the shm queues?](faq.md#what-are-the-shm-queues)

The A100 GPUs in mad04 and mad05 are composable: they can be moved between servers using a Liqid fabric.  By default, mad04 and mad05 have one GPU each.  If you need more than one, please ask cosma-support.

## GPU queues

| Queue | Nodes | GPUs | Maximum time | Projects |
| ----- | ----- | ---- | ------------ | -------- |
| `cosma8-shm` | mad04, mad05 | NVIDIA A100, 1 per node by default | 3 days | Most DiRAC projects, and durham |
| `cosma8-shm2` | ga004 | 1x AMD MI100 | 3 days | Most DiRAC projects, and durham |
| `cosma8-shm2` | ga006 | 2x AMD MI210 | 3 days | Most DiRAC projects, and durham |
| `dine2` | gc001-gc008 | NVIDIA A30 and V100, attached on request | 3 days | durham, do011, do015, do020 |
| `cosma8-dine2` | gc001-gc008 | As `dine2` | 3 days | dp276, dp440 |
| `gracehopper` | gn003 | 1x NVIDIA GH200 (ARM processor) | 6 hours | durham, do016 |
| `mi300x` | ga007 | 8x AMD MI300X | 1 day | do018 |
| `cosma8-draper` | ga007 | 8x AMD MI300X, whole node | 1 day | dp266 |
| `mi300a` | ga008 | 4x AMD MI300A | 2 hours | durham, do018 |
| `hardwarelab-gpu` | ga008, gn004, gn005, mad06 | Various | 6 hours, overnight only | durham, do016, do017, do018 |

How to request a GPU differs between queues: see [GPU jobs](gpujobs.md).  The `cosma8-draper` and `mi300x` queues are charged by GPU, not CPU, so request GPUs there with `--gpus=N`.  The `cosma8-draper` queue is named in honour of Peter Draper, who retired from COSMA technical support in 2026.

The ga008, gn004, gn005 and mad06 nodes can be used directly with ssh during the day, and are in the `hardwarelab-gpu` queue overnight: see [hybrid nodes](hardwarelab-hybridnodes.md).  The CPU nodes gi001, mad11 and mad12 work in the same way, with the `hardwarelab-cpu` queue.

## Other queues

| Queue | Nodes | Cores | Memory | Maximum time | Notes |
| ----- | ----- | ----- | ------ | ------------ | ----- |
| `bluefield1` | 18 (b101-b119, without b115) | 32 | 512GB | 3 days | With BlueField-2 DPUs.  durham, do008, do009 |
| `dine` | The same nodes as `bluefield1` | 32 | 512GB | 3 days | dp128 |
| `hardwarelab-cpu` | gi001, mad11, mad12 | 112-256 | 512GB-1.5TB | 6 hours, overnight only | durham, do025 |

The bluefield1 nodes include GitLab runners, so they can be used for CI/CD.  See [DINE](dine.md) for the BlueField hardware.

Some queues are only open to particular projects, or are used for training, such as `ciuk-dine` and `devhub`.  If in doubt, please ask.

## Nodes for direct ssh

Some nodes can be used directly with ssh from a login node, for testing and development.  They are shared, so please do not run large or long jobs on them.

| Node | Hardware |
| ---- | -------- |
| gn002 | NVIDIA Grace Hopper (ARM), like the `gracehopper` node |
| mad06 | 128 cores, 1TB, AMD Milan-X with a large (768MB) L3 cache, and an A100 GPU.  Overnight, it is in the `hardwarelab-gpu` queue |
| ga008 | 96 cores, 512GB, 4x AMD MI300A.  Overnight, it is in the `hardwarelab-gpu` queue |

See [GPUs](gpu.md) and the [CPU compute lab](cpucomputelab.md) for more.

## How jobs are prioritised

When jobs are waiting for the same nodes, Slurm starts the one with the highest priority.  A job's priority combines these factors, most important first:

| Factor | Effect |
| ------ | ------ |
| Fairshare | Projects and users that have used less recently get a higher priority.  Past usage counts for less over time, halving every 7 days |
| Age | Priority rises the longer a job waits, for up to 28 days |
| Queue | Jobs in higher priority queues, such as `-prince`, come first |
| Job size | Larger jobs get a small boost |

To see the factors for a pending job, run `sprio -j JOBID`.  To see your fairshare, run `sshare`.  For more, see [scheduling and fairshare](slurmdetail.md).

Each project also has a quarterly allocation.  To check it, run `mybalance` (see the [FAQ](faq.md#how-do-i-check-my-project-s-allocation)), or see the [COSMA usage pages](https://virgodb.cosma.dur.ac.uk/usage/login.php), for which you'll need your COSMA username and password.

## Checking a queue yourself

| Task | Command |
| ---- | ------- |
| List all queues | `sinfo -a -s` |
| See a queue's limits and who can use it | `scontrol show partition NAME` |
| See the nodes in a queue, with their cores and memory | `sinfo -p NAME -N -o "%N %c %m %f %G"` |
| Summarise node properties | `slurmnodeprop NAME` |
| See which projects you belong to | `groups` |

In `scontrol show partition`, `AllowAccounts` lists the projects that can submit to the queue.  `MaxTime` is the longest time allowed, `OverSubscribe=EXCLUSIVE` means each job gets whole nodes, and `DefMemPerCPU` is the default memory per core, in megabytes.

## COSMA6

COSMA6 was retired in April 2023, after 11 years of service.

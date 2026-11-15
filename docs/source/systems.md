# COSMA at a glance

This page summarises COSMA's machines in one place: the login nodes, the main
compute systems, and the smaller specialised queues.  For what each queue is
for and who can use it, see the [queue guide](queue.md); for the history and
details of each system, see [facilities](facilities.md).

The figures below come from Slurm and the nodes themselves, in November 2026.
`sinfo -s` and `scontrol show partition NAME` show the current state.

## Login nodes

| Login node | CPU | Cores (threads) | Memory | AVX-512 |
| ---------- | --- | --------------- | ------ | ------- |
| `login5c` | AMD EPYC 9354P (Zen 4) | 32 (64) | 754 GB | Yes |
| `login7a`, `login7b` | 2 × Intel Xeon Gold 5120 (Skylake) | 28 | 1.5 TB | Yes |
| `login7c` | 2 × Intel Xeon Gold 5120 (Skylake) | 28 | 754 GB | Yes |
| `login8a`, `login8b` | 2 × AMD EPYC 7542 (Zen 2) | 64 (128) | 2 TB | No |

The login nodes are shared by everyone (see [good citizenship](citizenship.md)).
Compile on the login node of the system you will run on, so that the program
suits its CPU (see [compiling code](compiling.md#building-for-the-right-cpu)).

## Main compute systems

| System | Queue | Nodes | CPU | Cores per node | Memory per node | Whole nodes only |
| ------ | ----- | ----- | --- | -------------- | --------------- | ---------------- |
| COSMA8 | `cosma8` | 527 | AMD EPYC 7H12 or 7763 | 128 | 1 TB | Yes |
| | `cosma8-rome` | 356 | AMD EPYC 7H12 (Zen 2) | 128 | 1 TB | Yes |
| | `cosma8-milan` | 171 | AMD EPYC 7763 (Zen 3) | 128 | 1 TB | Yes |
| | `cosma8-serial` | 527 (shared with `cosma8`) | As `cosma8` | 128 | 1 TB | No |
| COSMA7 | `cosma7` | 220 | Intel Xeon Gold 5120 (Skylake) | 28 | 512 GB | Yes |
| | `cosma7-rp` | 222 | Intel Xeon Gold 5120 (Skylake), Rockport network | 28 | 512 GB | Yes |
| COSMA5 | `cosma5` | 8 | AMD EPYC 9754 (Zen 4c) | 256 | 1.5 TB | No |

- **Whole nodes only** means every job is given whole nodes, and charged for
  them, even if it asks for one core.  For smaller jobs, use a queue that
  shares nodes, such as `cosma8-serial` or `cosma5`.
- Most queues allow jobs of up to **3 days**.  Variants with `-pauper` and
  `-prince` in their names have different limits and priorities: see
  [queue variants](queue.md#queue-variants).
- Each core has 2 hardware threads.  Slurm's `--cpus-per-task` counts cores.

## Large-memory and specialised queues

| Queue | Nodes | Cores per node | Memory per node | GPUs per node |
| ----- | ----- | -------------- | --------------- | ------------- |
| `cosma7-shm` | 2 (`mad01`, `mad02`) | 56 | 3 TB | |
| `cosma7-shm2` | 1 (`mad03`) | 48 | 6 TB | |
| `cosma8-shm` | 2 (`mad04`, `mad05`) | 128 | 4 TB | 1 × NVIDIA A100 (40 GB) |
| `cosma8-shm2` | 2 (`ga004`, `ga006`) | 128 | 1 TB | 1 × AMD Instinct MI100 |
| `cosma8-shm3` | 2 (`mad08`, `mad09`) | 192 | 772 GB | |
| `cosma8-ska` | 1 (`mad07`) | 56 | 4 TB | |
| `cosma8-ska2` | 4 (`mad01`, `mad03`, `mad04`, `mad05`, shared with other queues) | 48 to 128 | 3 to 6 TB | A100 on `mad04` and `mad05` |
| `cosma8-highram` | 2 (`mad04`, `mad05`) | 128 | 4 TB | 1 × NVIDIA A100 (40 GB) |
| `bluefield1` | 18 | 32 | 500 GB | |

## Hardware lab queues

These are test systems in the [HPC Hardware Lab](hardwarelab.md), each with its
own project codes and rules.

| Queue | Nodes | Cores per node | Memory per node | GPUs per node | Time limit |
| ----- | ----- | -------------- | --------------- | ------------- | ---------- |
| `dine2` | 8 (`gc001` to `gc008`) | 64 | 2 TB | Shared GPUs, requested with `--constraint=gpu` (see [GPU jobs](gpujobs.md)) | 3 days |
| `gracehopper` | 1 (`gn003`), ARM | 72 | 480 GB | 1 × NVIDIA GH200 | 6 hours |
| `mi300a` | 1 (`ga008`) | 96 | 512 GB | 4 × AMD Instinct MI300A | 2 hours |
| `mi300x` | 1 (`ga007`) | 96 | 2 TB | 8 × AMD Instinct MI300X | 1 day |
| `hardwarelab-cpu` | 3 (`gi001`, `mad11`, `mad12`) | 112 to 256 | 0.5 to 1.5 TB | | 6 hours |
| `hardwarelab-gpu` | 4 (`ga008`, `gn004`, `gn005`, `mad06`) | 64 to 256 | 0.5 to 2.3 TB | One type per node: 4 × MI300A, H100 NVL, RTX PRO 6000 Blackwell, A100 | 6 hours |

Some hardware lab nodes can also be reached directly with `ssh` during the
day, and only through Slurm at night: see the [hardware lab](hardwarelab.md)
pages.  `gracehopper` is an ARM (aarch64) system: programs built for the x86
nodes do not run on it.

## File systems

| Path | What it is | Details |
| ---- | ---------- | ------- |
| `/cosma/home` | Home directories, small, backed up | [Storage](storage.md#homespace) |
| `/cosma/apps` | App space, for software | [Storage](storage.md#app-space) |
| `/cosma5`, `/cosma7`, `/cosma8` | Lustre data file systems | [Storage](storage.md#data-space), [Lustre](lustre.md) |
| `/snap7`, `/snap8` | Fast Lustre scratch, not protected | [Storage](storage.md#scratch-space) |

Not every file system is mounted on every node: see
[mounted file systems](storage.md#mounted-filesystems).

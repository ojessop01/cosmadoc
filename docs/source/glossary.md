# Glossary

Terms used throughout these pages, in alphabetical order.

**Account (Slurm)**: The project that a job's use is charged to, given with `-A`, for example
`-A dp004`.  For most projects this is the same as your [project code](project.md)
(Durham COSMA5 users apply under `hpcicc` on SAFE and submit with `-A durham`).

**Allocation**: The amount of computing time a project has been awarded, usually per
quarter.  `mybalance` shows how much has been used.  In Slurm, "allocation"
also means the set of nodes given to a job.

**App space**: Your folder in `/cosma/apps`, for software, Python environments and code.
See [storage](storage.md#app-space).

**Array job**: One Slurm job that runs many similar tasks, each with its own index.  See
[job arrays](sbatch.md).

**AVX-512, AVX2**: Sets of CPU instructions that work on several numbers at once.  COSMA5 and
COSMA7 have AVX-512; COSMA8 has only AVX2.  Code built for AVX-512 stops with
`Illegal instruction` on COSMA8.  See [compiling code](compiling.md#building-for-the-right-cpu).

**Backfill**: Slurm running a small or short job early, in a gap left while larger jobs
wait.  Asking for a realistic time limit helps jobs to be backfilled.  See
the [FAQ](faq.md#what-is-backfill-how-do-i-exploit-this).

**Batch job**: A job described by a script and submitted with `sbatch`, which runs without
you.  See [your first job](firstjob.md).

**Compute node**: One of the many computers that run jobs.  You reach them through Slurm, not
by logging in directly.

**Core, thread, CPU**: A core is one processing unit of a CPU.  Most cores on COSMA run 2
hardware threads (exceptions include `gn003` and `mad01`, which run 1 thread per
core).  Slurm's `--cpus-per-task` counts cores; programs such as `nproc` count
threads.

**cosma-support**: The COSMA support team, at cosma-support@durham.ac.uk.  See
[contact](contact.md).

**DiRAC**: The UK's national HPC service for particle physics, astronomy and
cosmology, which funds COSMA7 and COSMA8.  See [DiRAC](dirac.md).

**Fairshare**: Slurm's way of balancing use between projects: a project that has used
less than its share recently gets higher priority.  `sshare` shows it.

**Home directory**: Your folder in `/cosma/home`: small (about 10 GB) and backed up.  See
[storage](storage.md#homespace).

**Interactive session**: A shell on a compute node, through Slurm.  See
[interactive sessions](interactive.md).

**Job**: A piece of work submitted to Slurm.  Each job has a job ID.

**Login node**: A shared computer you log in to, for editing, compiling and submitting jobs,
such as `login8b`.  Not for heavy computing (see
[good citizenship](citizenship.md)).

**Lustre**: The parallel file system used for `/cosma5`, `/cosma7`, `/cosma8`,
`/snap7` and `/snap8`.  See [Lustre](lustre.md).

**Module**: A way of loading installed software into your environment, with
`module load`.  See [modules](modules.md).

**MPI**: The standard library for programs that run as many cooperating processes,
possibly over many nodes.  See [MPI](mpi.md).

**NUMA domain**: A group of cores that share the same memory.  A node has several; memory in
another domain is slower to reach.  Slurm reports them as "sockets" on
COSMA's AMD nodes.

**OpenMP**: A standard for running a program on several threads, on one node.

**OST**: Object Storage Target: one of the disks (or groups of disks) that Lustre
spreads files over.  Striping a file puts it on several OSTs.

**Partition (queue)**: A group of nodes in Slurm with its own rules, such as `cosma8` or `cosma5`.
Chosen with `-p`.  See the [queue guide](queue.md).

**Pauper, prince**: Variants of the main queues: `-pauper` queues have the lowest priority and
a 1-day limit, mainly for projects that have used their allocation;
`-prince` queues allow 30 days, by request.  See
[queue variants](queue.md#queue-variants).

**Project code**: The code of the project an account belongs to, such as `dp004` or `hpcicc`.
See [project codes](project.md).

**RAC**: The DiRAC Resource Allocation Committee, which awards computing time to
projects.

**Rank**: One process of an MPI program, numbered from 0.

**SAFE**: The website where DiRAC accounts are managed: applying for accounts,
uploading SSH keys and resetting passwords.  See
[getting an account](account.md).

**Scratch space**: `/snap7` and `/snap8`: fast, but with no protection against disk failure.
See [storage](storage.md#scratch-space).

**Slurm**: The system that queues and runs jobs on COSMA.  See [Slurm](slurm.md).

**SSH key**: A pair of files used to log in securely: a private key kept on your
computer, and a public key uploaded to SAFE.  See
[generating an SSH key](sshkey.md).

**Striping**: Spreading a file over several Lustre disks (OSTs), so that it can be read
and written faster.  See [Lustre](lustre.md#striping).

**Virtual environment**: A folder holding a copy of Python and the packages installed into it.  See
[Python](python.md).

**x2go**: A program for using a graphical desktop on COSMA.  See
[graphical access](x2go.md).

# Slurm

COSMA's batch queues are managed by the Slurm job scheduler.  You describe the work in a job script, submit it to a queue, and Slurm runs it on compute nodes when they are free.

Which queue to use depends on your project: see [queues](queue.md).  If in doubt, ask your project lead or supervisor, or email cosma-support@durham.ac.uk.

New to Slurm?  These pages cover the basics:

- [Your first job](firstjob.md): submit and check a simple job
- [sbatch options](sbatch.md): what each `#SBATCH` line does
- [Useful Slurm features](slurmtips.md): job arrays, dependencies, saving work before the time limit
- [When a job goes wrong](jobproblems.md): why a job failed, or has not started
- [Scheduling and fairshare](slurmdetail.md): how Slurm decides which jobs run first

## Common commands

| Command | What it does |
| ------- | ------------ |
| `sbatch myjob.sh` | Submit a job script |
| `squeue --me` | List your pending and running jobs |
| `squeue -p cosma8` | List the jobs in a queue |
| `scancel JOBID` | Cancel a job |
| `sacct -j JOBID` | Show how a finished job went |
| `scontrol show job JOBID` | Show everything about a job |
| `sinfo -s` | Summarise the queues |
| `srun --pty /bin/bash` | Start an interactive shell on a compute node (add `-p`, `-A` and `-t`) |
| `salloc` | Allocate nodes, then run commands on them from your shell |
| `showq -q cosma7` | Show the jobs in a queue, with their sizes |
| `sprio -j JOBID` | Show how a pending job's priority is calculated |
| `sshare` | Show your fairshare, which affects priority |
| `slurmnodeprop` | Summarise the properties of nodes or queues (use `-h` for details) |
| `mybalance` | Show your projects' usage of their allocations (see the [FAQ](faq.md#how-do-i-check-my-project-s-allocation)) |
| `c8backfill` | Show which nodes are free now, and for how long (see the [FAQ](faq.md#what-is-backfill-how-do-i-exploit-this) for other queues) |
| `c8jobload JOBID` | Show how a running COSMA8 job is using its nodes (`c7jobload` for COSMA7) |

Example job scripts are also in `/cosma/home/sample-user`.

For more detail, see `man sbatch`, `man srun` and so on, the [online manual pages](https://slurm.schedmd.com/man_index.html), the [Slurm cheatsheet](https://slurm.schedmd.com/pdfs/summary.pdf), or the [Rosetta stone of batch systems](https://slurm.schedmd.com/rosetta.pdf) if you have used another scheduler, such as LSF or PBS.

## Time limits

Every job must have a time limit, set with `-t`.  Most queues allow up to 3 days.  The `-prince` queues allow 30 days, and the `-pauper` queues allow less: see [queue variants](queue.md#queue-variants).

Ask for a realistic time.  Shorter jobs can often start sooner, because Slurm can fit them into gaps between larger jobs (see [backfill](faq.md#what-is-backfill-how-do-i-exploit-this)).  A job is stopped as soon as it reaches its limit, so allow some extra time.

## Interactive jobs

To get a shell on a compute node, for example to test or debug:

```
srun -p cosma8-serial -A PROJECT -c 4 --mem=8G -t 01:00:00 --pty /bin/bash
```

When the shell starts, you are on the compute node.  Please exit as soon as you have finished, because the job uses its resources until you do.

Use a queue that shares nodes, such as `cosma8-serial` or `cosma5`, unless you need whole nodes.  On `cosma7` and `cosma8`, even a short interactive job is charged for whole nodes.

### X11 forwarding

To use graphical programs, such as a graphical debugger or profiler, log in with `ssh -X` or `ssh -Y`, then add `--x11`:

```
srun -p cosma8-serial -A PROJECT -c 1 --mem=4G -t 00:30:00 --x11 --pty /bin/bash
```

`--x11` works with `srun`, but not with `sbatch`.

## Direct compute node access

[Performance co-pilot](system.md#performance-co-pilot) lets you analyse running jobs, and `c8jobload` shows how a job is using its nodes.  If you need to ssh to a node that is running your jobs, please contact cosma-support.

## Example job scripts

Replace `PROJECT` with your project, and the queue with one that your project can use.  Each script loads modules that were tested together.  For other combinations, see the [list of modules](modulelist.md#what-to-load-first).

### MPI job over many nodes

This runs 512 MPI tasks, which is 4 COSMA8 nodes:

```
#!/bin/bash -l
#SBATCH --ntasks=512
#SBATCH -J myjob
#SBATCH -o myjob.%j.out
#SBATCH -e myjob.%j.err
#SBATCH -p cosma8
#SBATCH -A PROJECT
#SBATCH -t 72:00:00
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=you@durham.ac.uk

module purge
module load gnu_comp/14.1.0 openmpi/5.0.3 parallel_hdf5

mpirun -np $SLURM_NTASKS ./myprogram myinputs
```

To use the Intel compiler and Intel MPI instead, replace the `module load` line with:

```
module load intel_comp compiler-rt tbb compiler mpi parallel_hdf5
```

Start Open MPI programs with `mpirun`, not `srun`.  When started with `srun`, each copy of the program runs on its own, so a 4-task job runs four separate 1-task programs.

`cosma8` and `cosma7` always give a job whole nodes, so `--exclusive` is not needed.

### Many similar jobs

A job array runs the same script several times.  This runs 28 copies of a 128-task job, at most 4 at a time:

```
#!/bin/bash -l
#SBATCH --ntasks=128
#SBATCH -J myarray
#SBATCH --array=1-28%4
#SBATCH -o myarray.%A.%a.out
#SBATCH -e myarray.%A.%a.err
#SBATCH -p cosma8
#SBATCH -A PROJECT
#SBATCH -t 24:00:00

module purge
module load gnu_comp/14.1.0 openmpi/5.0.3 parallel_hdf5

# SLURM_ARRAY_TASK_ID is set to the copy's number, from 1 to 28.
mpirun -np $SLURM_NTASKS ./myprogram input_${SLURM_ARRAY_TASK_ID}
```

See [job arrays](slurmtips.md#job-arrays) for more.

### MPI with OpenMP threads

This runs 2 MPI tasks on each of 4 nodes, each with its own set of cores for OpenMP threads:

```
#!/bin/bash -l
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=64
#SBATCH -J hybrid
#SBATCH -o hybrid.%j.out
#SBATCH -p cosma8
#SBATCH -A PROJECT
#SBATCH -t 12:00:00

module purge
module load gnu_comp/14.1.0 openmpi/5.0.3

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
mpirun -np $SLURM_NTASKS --map-by ppr:$SLURM_NTASKS_PER_NODE:node:PE=$SLURM_CPUS_PER_TASK ./myprogram
```

The `--map-by` option gives each task its own block of cores.  Set `--cpus-per-task` to the cores per node divided by the tasks per node:

| Queue | Cores per node | `--cpus-per-task` for 2 tasks per node |
| ----- | -------------- | -------------------------------------- |
| `cosma8` | 128 | 64 |
| `cosma7`, `cosma7-rp` | 28 | 14 |
| `cosma5` | 256 | 128 |

Each core has two hardware threads, so a program that counts the available CPUs itself will see twice as many.  Setting `OMP_NUM_THREADS` avoids this.  See [threads and CPUs](sbatch.md#threads-and-cpus), and [MPI hints](mpi.md) for more on pinning.

To use only some of the cores on each node, for example to give each task more memory, use fewer tasks per node.  For example, for 8 tasks with 2 cores each on 32 COSMA7 nodes:

```
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=2
```

### Many single-core tasks

For many independent single-core tasks, use a [job array](slurmtips.md#job-arrays) on a queue that shares nodes, such as `cosma8-serial` or `cosma5`.

To run many tasks inside one job on a whole node, see the example in `/cosma/home/sample-user/parallel_tasks/`.  Copy it to your own directory, compile the C code with `make`, and edit `slurm_batch.sh`.

### Heterogeneous jobs

Slurm can give one job several groups of nodes, each with different resources:

```
#SBATCH -A PROJECT
#SBATCH --time=72:00:00

#SBATCH -p cosma8
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

#SBATCH hetjob

#SBATCH -p cosma8
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
```

This requests one node with one task, and two more nodes with 16 tasks between them.  `mpirun` does not understand this kind of allocation, so MPI programs should be started with `srun` instead, for example:

```
salloc -A PROJECT --time=72:00:00 -p cosma8 --nodes=3
srun --nodes=1 --ntasks-per-node=1 ./server : --nodes=2 --ntasks-per-node=8 ./client
```

This starts a server task alone on the first node, and 16 client tasks on the other two nodes.  All of the tasks are in the same `MPI_COMM_WORLD`.

Another example:

```
#SBATCH -A PROJECT
#SBATCH --time=12:00:00

#SBATCH -p cosma8
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=16
#SBATCH --distribution=block:fcyclic:fcyclic,Pack

#SBATCH hetjob

#SBATCH -p cosma8
#SBATCH --ntasks=28
#SBATCH --ntasks-per-node=1
#SBATCH --distribution=cyclic

mpirun -np 64 ./swift_mpi -v 1 --pin --threads=8 --cosmology --self-gravity params.yml : \
-np 28 ./swift_mpi -v 1 --pin --threads=128 --cosmology --self-gravity params.yml
```

You may need to change `--distribution`.  This example fills each node with tasks before moving to the next one (`block` and `Pack`), then hands out tasks within a node round-robin between the sockets and cores (`fcyclic`).  The Slurm documentation lists which options must be the same for all parts of the job, and which can differ.

Open MPI supports heterogeneous jobs, but only when it is built with a process management interface (PMI) library.  If it is not, a clear error message is shown.  Intel MPI seems to work to some extent if you set `export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so`, but it may not fully support heterogeneous jobs.  For example, mixing nodes with exactly 1 task and nodes with more than 1 task can crash.  See the [Slurm heterogeneous jobs guide](https://slurm.schedmd.com/heterogeneous_jobs.html).

### Using DDT

To use the DDT debugger with Slurm, follow [these instructions](https://gitlab.cosma.dur.ac.uk/swift/swiftsim/wikis/DDT-debugger-on-Cosma).  There is also an example Slurm script in `/cosma/home/sample-user/slurm_ddt_example.qtf`, which [DDT uses to generate a batch script](issues.md#ddt).

## Priority

The order in which pending jobs start depends mainly on how much your project has used recently (fairshare), and how long the job has been waiting: see [scheduling and fairshare](slurmdetail.md), and [how jobs are prioritised](queue.md#how-jobs-are-prioritised).

To let other jobs go first, you can lower the priority of your own job:

```
scontrol update JobId=JOBID Nice=100
```

A higher value means a lower priority.  Only staff can raise a job's priority.

## Monitoring jobs

The `showq` command shows the jobs in a queue (in addition to `squeue` and `sinfo`), for example:

```
showq -q cosma7 -l -f -o
```

The `c7jobload` and `c8jobload` commands show the load (CPU demand) of a running job.  Use `-h` to see the options.  For example:

```
c8jobload -l JOBID
```

`sstat` shows the resources used by a running job, and `sacct` by a finished one.  For example, to print the memory used so far at the end of your job script:

```
sstat --jobs=${SLURM_JOB_ID}.batch --format=jobid,maxrss,ntasks
```

## GPUs

To request GPUs, see [GPU jobs](gpujobs.md), and [GPUs](gpu.md) for the hardware.  Some GPU queues are charged by GPU, not CPU: the `cosma8-draper` queue (project dp266) and the `mi300x` queue (project do018).  On these, request GPUs with `--gpus=N`, where N is the number of GPUs.

## Reservations

It is possible to request a Slurm reservation for jobs that will need around 40% or more of the cluster at the same time.  A reservation sets aside the requested number of nodes for a set period of time, for exclusive use.  This lets large jobs restart efficiently, without having to wait for many nodes to become free, which improves cluster efficiency.

A reservation needs to be authorised by the Service Management Board, and 1 month's notice should be given if possible.  The request should say how many nodes are needed (we will add a few more in case of node failures), for how long, a brief description of the science, and why the reservation is needed.

Your project will be charged for the entire reservation, not just for the time you use, so it is essential to keep a queue of jobs ready to run in it.

Once you have a reservation, use `scontrol show reservation` to view it, and submit jobs to it with `#SBATCH --reservation=RESERVATION_NAME` in your job script.

## HDF5 profiling

The [Slurm HDF5 profiling plugin](https://slurm.schedmd.com/hdf5_profile_user_guide.html) is enabled.  It can record profiling information from a job in an HDF5 file.  To use it, add `#SBATCH --profile=<all|none|energy|task|filesystem|network>` to your job script.  Results are stored in `/cosma/apps/slurm/profile_data/USERNAME`.

After the job has finished, run `sh5util -j JOBID` to combine the files from each node into a single file in the current directory.  You can then view it with the `h5ls` command, from the hdf5 module.

## Usage reports

`sreport` reports on usage.  For example, for a project's usage in October 2026, by user, in CPU hours:

```
sreport cluster AccountUtilizationByUser start=2026-10-01 end=2026-11-01 Account=dpXXX -t hours
```

Without `-t hours`, the usage is reported in CPU minutes.

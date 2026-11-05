# sbatch options

This page explains the options that you can use with `sbatch`, either in `#SBATCH` lines in a job script or on the command line.  Command line options override those in the script.  It covers the most useful ones: for the full list, run `man sbatch`.

New to Slurm?  Start with [your first job](firstjob.md).

Slurm stops reading `#SBATCH` lines at the first command in a script, and any later ones are silently ignored.  Each option has a short form, a long form, or both.

## Required on COSMA

Jobs are rejected without these.

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `-A`, `--account` | `-A dp004` | The project to charge |
| `-p`, `--partition` | `-p cosma8` | The queue: see [queues](queue.md) |
| `-t`, `--time` | `-t 12:00:00` | The time limit |

Time can be given as `MM`, `HH:MM:SS` or `D-HH:MM:SS`.  Most queues allow up to 3 days.  Request a realistic time, because shorter jobs can often start sooner.

## CPUs and tasks

A task is one copy of your program, usually an MPI rank.  A CPU is one core on most COSMA queues.

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `-n`, `--ntasks` | `--ntasks=128` | The total number of tasks |
| `-c`, `--cpus-per-task` | `-c 8` | CPUs for each task, usually for OpenMP threads |
| `-N`, `--nodes` | `-N 4` | The number of nodes |
| `--ntasks-per-node` | `--ntasks-per-node=16` | Tasks to run on each node |
| `--threads-per-core` | `--threads-per-core=1` | Hardware threads to use on each core |
| `--exclusive` | | Do not share nodes with other jobs |

Some common patterns are:

| Job | Options |
| --- | ------- |
| One program on one CPU | `--ntasks=1` |
| OpenMP on 16 CPUs | `--ntasks=1 --cpus-per-task=16` |
| MPI on 1024 CPUs | `--ntasks=1024` |
| Hybrid on 4 COSMA8 nodes | `--nodes=4 --ntasks-per-node=8 --cpus-per-task=16` |

### Threads and CPUs

On COSMA, Slurm allocates whole cores, and each core has two hardware threads.  A job with `--cpus-per-task=4` gets 4 cores but can see 8 threads, so programs that use `nproc` to choose how many threads to start will start 8.

To run one thread on each core, set the number of threads yourself:

```
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
```

`--threads-per-core=1` also limits job steps started with `srun`, but not the job script itself.  See [MPI hints](mpi.md) for pinning.

### Exclusive access

Queues differ in whether jobs share nodes:

| Queue | Sharing |
| ----- | ------- |
| `cosma7`, `cosma7-rp`, `cosma8` | Always whole nodes, so `--exclusive` is not needed |
| `cosma8-serial`, `cosma5`, the `-shm` queues | Shared.  `--exclusive` is ignored on `cosma5`: request all of the CPUs instead |

## Memory

On whole-node queues, your job gets all of the memory on its nodes.  On shared queues, please say how much you need.

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `--mem` | `--mem=32G` | Memory for each node |
| `--mem-per-cpu` | `--mem-per-cpu=4G` | Memory for each CPU |

Use one or the other.  Values can use `K`, `M`, `G` or `T`, and the default unit is megabytes.  Jobs that use more than this are killed.  The default memory per CPU depends on the queue: see [the shm queues](faq.md#what-are-the-shm-queues).

## Choosing nodes

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `-w`, `--nodelist` | `-w m8451` | Run on these nodes |
| `-x`, `--exclude` | `-x m8001` | Do not use these nodes |
| `-C`, `--constraint` | `--constraint=gpu` | Use nodes with this feature |
| `--gres` | `--gres=gpu:1` | Request generic resources: see [GPU jobs](gpujobs.md) |

COSMA8 has two types of node.  To use only one, select the `cosma8-rome` or `cosma8-milan` queue.

## Output

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `-J`, `--job-name` | `-J mysim` | The name of the job |
| `-o`, `--output` | `-o %x.%j.out` | The file for standard output |
| `-e`, `--error` | `-e %x.%j.err` | The file for errors.  Without this, errors go to the output file |
| `--open-mode` | `--open-mode=append` | Add to files instead of replacing them |
| `-D`, `--chdir` | `-D /cosma8/data/dp004/USERNAME/run1` | The directory to run in |

The default is the directory that you submit from, and an output file called `slurm-JOBID.out`.

File names can use these patterns:

| Pattern | Meaning |
| ------- | ------- |
| `%j` | Job number |
| `%x` | Job name |
| `%A` | Job number of an array |
| `%a` | Task number in an array |
| `%N` | Name of the first node |
| `%u` | User name |

## Email

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `--mail-type` | `--mail-type=END,FAIL` | When to send email.  Other values include `BEGIN`, `ALL` and `TIME_LIMIT_90` |
| `--mail-user` | `--mail-user=you@durham.ac.uk` | Where to send it |

## Controlling when a job runs

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `--begin` | `--begin=now+1hour` | Do not start before this time |
| `-d`, `--dependency` | `-d afterok:12345` | Wait for another job: see [dependencies](slurmtips.md#running-jobs-in-order) |
| `--kill-on-invalid-dep` | `--kill-on-invalid-dep=yes` | Cancel the job if its dependency can never be met |
| `-H`, `--hold` | | Hold the job until you run `scontrol release JOBID` |
| `--time-min` | `--time-min=06:00:00` | Accept a shorter time limit if this means that the job starts sooner |
| `--nice` | `--nice=100` | Lower the priority of your job, to let others go first |
| `--signal` | `--signal=B:USR1@300` | Send a signal before the time limit: see [saving work](slurmtips.md#saving-work-before-the-time-limit) |
| `--requeue` | | Allow the job to restart from the beginning after a node failure.  This is off by default on COSMA, and does not apply if your program fails |

## Other useful options

| Option | Example | Meaning |
| ------ | ------- | ------- |
| `-a`, `--array` | `--array=1-100%10` | Run many similar tasks: see [job arrays](slurmtips.md#job-arrays) |
| `--wrap` | `--wrap="python run.py"` | Run a command, without a script |
| `--test-only` | | Check the job and estimate when it would start, without submitting it |
| `--parsable` | | Print only the job number, which is useful in scripts |
| `--export` | `--export=NONE` | Choose which environment variables to pass to the job |
| `-W`, `--wait` | | Wait until the job finishes before returning |

By default, your job inherits the environment of the shell that you submit it from, including any loaded modules.  It is safest to run `module purge`, then load what you need, in your job script.

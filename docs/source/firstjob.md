# Your first job

This page takes you from logging in to a finished job.  It assumes that you already have an [account](account.md) and can [log in](ssh.md).

On COSMA you do not run large programs directly on the login node.  Instead, you describe the work in a job script, and the Slurm scheduler runs it on a compute node when one is free.

## 1. Find your project and queue

Every job needs a project and a queue.  To list the groups that you belong to, which include your projects, run:

```
groups
```

Your project is usually one of these, for example `dp004`.  The queue depends on your project:

| You are | Queue (`-p`) | Project (`-A`) | Your data space |
| ------- | ------------ | -------------- | --------------- |
| On a DiRAC project with COSMA8 time | `cosma8-serial` | Your project, e.g. `dp004` | /cosma8/data/PROJECT/USERNAME |
| On a DiRAC project with COSMA7 time | `cosma7` | Your project, e.g. `dp004` | /cosma7/data/PROJECT/USERNAME |
| A Durham user | `cosma5` | `durham` | /cosma5/data/durham/USERNAME |

The examples below use COSMA8.  If you are using another row of the table, change the directory and the `-p` and `-A` lines to match.  On `cosma7`, each job takes a whole node, so your project is charged for all 28 CPUs, even for this small job.

## 2. Make a directory

Work in your data space, not your home directory, which is small:

```
mkdir -p /cosma8/data/PROJECT/$USER/firstjob
cd /cosma8/data/PROJECT/$USER/firstjob
```

Replace `PROJECT` with your project, in this step and the next.

## 3. Write a job script

Create a file called `hello.sh` containing:

```
#!/bin/bash -l
#SBATCH -J hello
#SBATCH -o hello.%j.out
#SBATCH -e hello.%j.err
#SBATCH -p cosma8-serial
#SBATCH -A PROJECT
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH -t 00:05:00

module purge
module load python/3.12.4

echo "Running on $(hostname) as job $SLURM_JOB_ID"
python -c "import sys; print('Hello from Python', sys.version.split()[0])"
```

The `#SBATCH` lines tell Slurm what the job needs, and the rest is an ordinary shell script:

| Line | Meaning |
| ---- | ------- |
| `-J hello` | The name of the job |
| `-o hello.%j.out` | Where to write output; `%j` becomes the job number |
| `-e hello.%j.err` | Where to write errors |
| `-p cosma8-serial` | The queue |
| `-A PROJECT` | The project to charge |
| `--ntasks=1` | Run one copy of the program |
| `--cpus-per-task=1` | Give it one CPU |
| `--mem=1G` | Give it 1GB of memory |
| `-t 00:05:00` | Stop the job after 5 minutes |

The `-A`, `-p` and `-t` options are required on COSMA.  All `#SBATCH` lines must come before the first command in the script, because Slurm ignores any that come after it.

There are many more options: see [sbatch options](sbatch.md).

## 4. Submit the job

```
sbatch hello.sh
```

Slurm replies with the job number:

```
Submitted batch job 12263075
```

## 5. Check on the job

```
squeue --me
```

This lists your jobs.  The `ST` column shows the state: `PD` means pending, `R` means running, and `CG` means completing.  When the job has finished, it disappears from this list.

Short jobs often start within a few minutes, but a job can wait for much longer when the system is busy.  To see an estimate of when it will start, run `squeue --me --start`.

To cancel a job, use its number:

```
scancel 12263075
```

## 6. Look at the output

When the job has finished, there are two new files in your directory.  Look at the output with:

```
cat hello.*.out
```

You should see something like this, including a header that COSMA adds to every job:

```

====
Starting job 12263075 at Mon Nov  2 21:43:30 GMT 2026 for user USERNAME.
Running on nodes: m8525
====

Running on m8525.pri.cosma.local as job 12263075
Hello from Python 3.12.4
```

Any errors are in the `.err` file.  In this example it should be empty.

## 7. Check how the job went

```
sacct -j 12263075 -X -o JobID,JobName,State,ExitCode,Elapsed
```

A state of `COMPLETED` and an exit code of `0:0` mean that the job finished without an error:

```
JobID           JobName      State ExitCode    Elapsed
------------ ---------- ---------- -------- ----------
12263075          hello  COMPLETED      0:0   00:00:03
```

If you see anything else, see [when a job goes wrong](jobproblems.md).

## What next?

- [Useful Slurm features](slurmtips.md), such as running many similar jobs
- [Example job scripts](slurm.md#example-job-scripts), including MPI jobs
- [GPU jobs](gpujobs.md)
- [Storage](storage.md), to decide where your data should go
- [Modules](modules.md), to load compilers and libraries
- [Good citizenship](citizenship.md)

# Useful Slurm features

This page describes Slurm features that can save you time.  For the options themselves, see [sbatch options](sbatch.md).  For more detail, see the [Slurm documentation](https://slurm.schedmd.com/documentation.html), or `man sbatch`.  COSMA runs Slurm 25.11.

## Job arrays

A job array runs many similar tasks from one script, which is much better than submitting them one at a time.  Each task receives its number in `SLURM_ARRAY_TASK_ID`:

```
#!/bin/bash -l
#SBATCH -J myarray
#SBATCH -o myarray.%A_%a.out
#SBATCH -p cosma8-serial
#SBATCH -A PROJECT
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH -t 01:00:00
#SBATCH --array=1-100%10

./myprogram input_${SLURM_ARRAY_TASK_ID}.dat
```

`--array=1-100%10` runs tasks 1 to 100, with at most 10 running at once.  You can also use lists, such as `--array=1,5,9`, or steps, such as `--array=0-100:10`.  Task numbers can go up to 1000.

If your inputs do not have numbers in their names, list them in a file, and pick a line in the script:

```
FILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" inputs.txt)
./myprogram "$FILE"
```

To cancel a single task, use `scancel JOBID_TASK`, for example `scancel 12263079_3`.

## Running jobs in order

A dependency makes one job wait for another.  This is useful for a simulation followed by analysis, or for a run that is split into stages:

```
FIRST=$(sbatch --parsable simulate.sh)
sbatch --dependency=afterok:$FIRST analyse.sh
```

| Dependency | The job starts |
| ---------- | -------------- |
| `afterok:JOBID` | After the job finishes successfully |
| `afternotok:JOBID` | After the job fails |
| `afterany:JOBID` | After the job ends, however it ended |
| `after:JOBID` | After the job starts |
| `singleton` | After all of your jobs with the same name have ended |

If the first job fails, an `afterok` job can never run, and stays in the queue.  Add `--kill-on-invalid-dep=yes` to have it cancelled instead.

## Saving work before the time limit

Slurm stops your job when it reaches its time limit.  To write a checkpoint first, ask Slurm to send a signal to your script:

```
#!/bin/bash -l
#SBATCH -p cosma8-serial
#SBATCH -A PROJECT
#SBATCH --signal=B:USR1@300
#SBATCH -t 12:00:00

trap 'echo "Saving"; touch stop_now; wait; exit 0' USR1

./myprogram &
wait
```

`--signal=B:USR1@300` sends the `USR1` signal around 5 minutes before the time limit.  It can arrive up to 60 seconds earlier than requested.

The `B:` sends the signal to the batch script itself, which needs to run your program in the background with `&` followed by `wait`, otherwise it cannot handle the signal until your program ends.  What the script does next depends on your program.  This example creates a file, which your program would need to check for, then waits for your program to finish.  The `exit 0` stops Slurm from recording the job as failed.

## Changing a job after submitting it

| Task | Command |
| ---- | ------- |
| Hold a pending job | `scontrol hold JOBID` |
| Release it | `scontrol release JOBID` |
| Shorten its time limit | `scontrol update JobId=JOBID TimeLimit=01:00:00` |
| Change its name | `scontrol update JobId=JOBID JobName=newname` |
| Cancel all of your jobs | `scancel --me` |
| Cancel your jobs by name | `scancel --me --name=myjob` |

## Monitoring jobs

| Task | Command |
| ---- | ------- |
| See your jobs | `squeue --me` |
| See estimated start times | `squeue --me --start` |
| See everything about a job | `scontrol show job JOBID` |
| See memory use of a running job | `sstat -j JOBID.batch -o JobID,MaxRSS` |
| See finished jobs since a date | `sacct -S 2026-11-01 -X -o JobID,JobName,State,Elapsed` |
| See a job's priority | `sprio -j JOBID` |
| See the queues | `sinfo -s` |
| See a node's details | `scontrol show node m8451` |

`sstat` only works while a job is running.  See also [`cjobload`](system.md#cjobload) for how a running job is using its nodes.

## Variables in job scripts

Slurm sets these variables for your job:

| Variable | Meaning |
| -------- | ------- |
| `SLURM_JOB_ID` | The job number |
| `SLURM_JOB_NAME` | The job name |
| `SLURM_JOB_PARTITION` | The queue |
| `SLURM_JOB_ACCOUNT` | The project |
| `SLURM_JOB_NODELIST` | The nodes allocated to the job |
| `SLURM_JOB_NUM_NODES` | The number of nodes |
| `SLURM_NTASKS` | The number of tasks |
| `SLURM_CPUS_PER_TASK` | CPUs for each task, if you set it |
| `SLURM_CPUS_ON_NODE` | CPUs allocated on this node |
| `SLURM_SUBMIT_DIR` | The directory that you submitted the job from |
| `SLURM_ARRAY_TASK_ID` | The task number in an array |
| `SLURM_ARRAY_JOB_ID` | The job number of an array |

## Interactive jobs

To get a shell on a compute node:

```
srun -p cosma8-serial -A PROJECT -c 4 --mem=8G -t 01:00:00 --pty /bin/bash
```

Please exit as soon as you have finished.  An idle interactive job wastes resources, and your project is charged for it.  On queues that give whole nodes, your project is charged for the whole node.

## What is not available on COSMA

- `seff` is not installed.  Use `sacct` instead: see [when a job goes wrong](jobproblems.md).
- `scrontab`, for scheduled jobs, is disabled.
- Jobs are not restarted after a node failure unless you use `--requeue`.

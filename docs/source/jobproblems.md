# When a job goes wrong

This page explains how to find out why a job failed, or why it has not started.

## Find out what happened

Once a job has finished, `sacct` shows how it ended:

```
sacct -j JOBID -o JobID,JobName,State,ExitCode,Elapsed,MaxRSS,ReqMem
```

`MaxRSS` is the most memory that the job used.  It is shown on the `.batch` line, not the top line.  Add `-X` to show only the top line.

The `seff` command is not installed on COSMA.

| State | Exit code | What happened | What to do |
| ----- | --------- | ------------- | ---------- |
| `COMPLETED` | `0:0` | The script finished without an error | If the results are still wrong, read the output files |
| `FAILED` | e.g. `3:0` | The script ended with an error | Read the `.err` and `.out` files |
| `OUT_OF_MEMORY` | `0:125` | The job used more memory than it requested | Request more with `--mem` |
| `TIMEOUT` | `0:0` | The job reached its time limit | Request more time with `-t`, or save progress and restart |
| `CANCELLED` | `0:0` | The job was cancelled, for example with `scancel` | Check who cancelled it: `sacct` shows the user ID.  This also happens to a job with `--kill-on-invalid-dep=yes` if its dependency fails |
| `NODE_FAIL` | | A node failed | Resubmit the job, and contact us if it keeps happening |

The exit code has two parts, the exit code of the script and the number of the signal that stopped it.  Note that a batch script reports the exit code of its last command.  To stop at the first failure, put `set -e` near the top of your script.

## Messages in the output

If a job runs out of memory, the output contains:

```
slurm_script: line 2: 270858 Killed     python3 myprogram.py
error: Detected 1 oom_kill event in StepId=12263076.batch. Some of the step tasks have been OOM Killed.
```

Files in `/dev/shm` count towards your job's memory.

If a job reaches its time limit, the output contains:

```
error: *** JOB 12263077 ON m8525 CANCELLED AT 2026-11-02T21:44:42 DUE TO TIME LIMIT ***
```

Slurm stops the job when it reaches its time limit, with no extra time.  To save your work first, see [saving work before the time limit](slurmtips.md#saving-work-before-the-time-limit).

If you see this line, your job started in the wrong directory:

```
error: couldn't chdir to `/cosma8/data/dp004/USERNAME': No such file or directory: going to /tmp instead
```

Your job was submitted from a directory that does not exist on its compute node.  Not all file systems are available everywhere, so see [mounted file systems](storage.md#mounted-filesystems).

## Errors when submitting a job

| Message | Cause |
| ------- | ----- |
| `A valid account is required (use -A and a DiRAC project or Unix group)` | Add `-A PROJECT` |
| `You need to specify a maximum runtime (-t)` | Add a time limit with `-t` |
| `A partition is required (-p)` | Add a queue with `-p` |
| `You are not a member of the dpXXX group.` | Check the project name, using `groups` |
| `Invalid account or account/partition combination specified` | Your project cannot use this queue |
| `invalid partition specified: NAME` | Check the queue name, using `sinfo -s` |
| `Requested time limit is invalid (missing or exceeds some limit)` | The time limit is too long for the queue, which is usually 3 days |
| `Requested node configuration is not available` | No node on this queue can satisfy the request, for example too many CPUs or too much memory on one node |

You can check a job script without submitting it, using `sbatch --test-only myscript.sh`.

## Why has my job not started?

For a pending job, `squeue --me` shows the reason in brackets at the end of the line:

| Reason | Meaning |
| ------ | ------- |
| `Priority` | Other jobs have a higher priority |
| `Resources` | Your job is next, and is waiting for nodes to become free |
| `Dependency` | Your job is waiting for another job to finish |
| `DependencyNeverSatisfied` | A job that yours depends on failed, so it will never start.  Cancel it with `scancel JOBID` |
| `JobHeldUser` | Your job is on hold, so use `scontrol release JOBID` |
| `ReqNodeNotAvail` | A node that your job needs is not available, for example because it is reserved |

Useful commands are:

- `squeue --me --start` shows an estimate of when your job will start.
- `scontrol show job JOBID` shows everything about a job.
- `sprio -j JOBID` shows how its priority is calculated.

Shorter jobs can often start sooner, by using [backfill](faq.md#what-is-backfill-how-do-i-exploit-this).  Queue priorities are described in the [scheduling overview](slurmdetail.md).

## Compute nodes cannot reach the internet

Login nodes can reach the internet, but compute nodes cannot.  In a job, commands such as `pip install`, `git clone` and `wget` will hang or time out.

Download what you need on a login node before submitting your job.

## Getting help

If you need to [contact support](contact.md), please include your job number, the job script, and the output of the `sacct` command above.

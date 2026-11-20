# Interactive sessions

Most work on COSMA runs as [batch jobs](slurm.md), which wait in a queue and
run without you.  Sometimes you need to work on a compute node directly: to
test a program before submitting a large job, to debug, to compile on the type
of node the program will run on, or to run an analysis that needs more than a
login node should give.  This is an **interactive session**.

## Choosing how to work

| You want to | Use |
| ----------- | --- |
| Edit files, compile small programs, submit jobs, quick tests (a few minutes, a few cores) | A login node, directly |
| A shell on a compute node, for testing or debugging | [`srun --pty`](#a-shell-on-a-compute-node) |
| To run several commands, including MPI programs, on an allocation, from your own shell | [`salloc`](#an-allocation-with-salloc) |
| A graphical program on a compute node | [`srun --x11`](#graphical-programs) |
| Jupyter on a compute node | See [Jupyter in a batch job](jupyter.md#jupyter-in-a-batch-job) |
| A long run, or anything that does not need you watching | A [batch job](firstjob.md) |

An interactive session holds its cores and memory until you leave it, whether
or not you are using them, and your project is charged for that time.  Ask
for what you need, and **exit as soon as you have finished**.

## A shell on a compute node

```
srun -p cosma8-serial -A ACCOUNT -c 4 --mem=8G -t 01:00:00 --pty /bin/bash
```

When the job starts, the prompt changes to the compute node (for example
`m8123`), and everything you run uses that node's resources.  Type `exit` to
end the session and release the node.

- `-p` is the queue, `-A` your project's account and `-t` the time limit; all
  three are required.
- `-c 4` asks for 4 cores.  Each core has 2 hardware threads, so a program
  sees 8 CPUs.
- `--mem=8G` asks for 8GB of memory.
- If no node is free, the command waits until one is.  `Ctrl-C` cancels the
  request.

### Which queue

Use a queue that **shares nodes**, such as `cosma8-serial`, `cosma5` or
`cosma7-shm`, for anything less than a whole node.  On `cosma8` and `cosma7`,
every job is given whole nodes, and charged for them, even if you ask for one
core.  See the [queue guide](queue.md).

To test on the same CPU as your production runs, use a shared queue with the
same CPUs: `cosma8-serial` has the same nodes as `cosma8`.

## An allocation with salloc

`salloc` reserves resources and then gives you a shell **on the login node**,
from which you can run commands on the allocation.  This is useful for
running an MPI program several times, or running different commands one after
another.

```
salloc -p cosma5 -A ACCOUNT -n 4 -c 1 --mem=8G -t 01:00:00
```

When the allocation is granted, you get a new shell, still on the login node,
with `SLURM_JOB_ID` set.  Then:

```
module load gnu_comp/14.1.0 openmpi/5.0.3
mpirun -np 4 ./myprogram        # runs on the allocated node, not the login node
srun hostname                   # runs a command on the allocated node
```

`mpirun` and `srun` place the work on the allocated nodes.  Anything else you
type runs on the login node, so run heavy work through `mpirun` or `srun`.
Type `exit` to release the allocation.

For Open MPI programs, use `mpirun` rather than `srun` (see [MPI](mpi.md)).

## Graphical programs

To run a graphical program on a compute node, such as a debugger or a
visualisation tool, log in with X11 forwarding (`ssh -X`) or use
[x2go](x2go.md), then add `--x11`:

```
srun -p cosma8-serial -A ACCOUNT -c 1 --mem=4G -t 00:30:00 --x11 --pty /bin/bash
```

## Looking at a running batch job

To see what a running batch job is doing, you can start a shell, or run a
command, inside the job's allocation on its node:

```
srun --jobid=JOBID --overlap --pty /bin/bash
srun --jobid=JOBID --overlap top -b -n 1 -u $USER
```

`--overlap` lets the new command share the job's resources.  This is useful
for checking memory use, or seeing where a program is stuck (see
[debugging hangs](debugging.md#hangs)).  [`cjobload`](system.md#cjobload) also
shows how a job is using its nodes, without logging in.

## Hardware lab nodes

Some [hardware lab](hardwarelab.md) systems can be reached directly with `ssh`
from a login node during the day, and only through Slurm at night.  See each
system's page for its access times.

## Things to know

- **Your environment comes with you.**  An interactive session starts with the
  modules and environment variables of the shell you started it from.  If
  `TMPDIR` points to a folder that does not exist on the compute node, Slurm
  prints `Unable to create TMPDIR` and uses `/tmp` instead.  This is harmless.
- **No internet on compute nodes.**  Download files and install packages on a
  login node.
- **The session ends with your connection.**  If your SSH connection drops, an
  `srun --pty` session ends and its work is lost.  For anything long, use a
  batch job.
- **Time limits apply.**  The session is ended when its time limit is reached,
  with no warning beyond the limit you set.

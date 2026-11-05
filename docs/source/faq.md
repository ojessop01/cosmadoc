# Frequently Asked Questions

Here is a list of frequently asked, or otherwise useful questions. If you have
a question you'd like to see here, please let us know. For COSMA8-specific
questions, please see the [COSMA8 FAQ](cosma8.md#cosma8-faq)


## How do I best formulate my questions to the support staff?

Please direct questions to cosma-support@durham.ac.uk. Explain what you are
trying to do or would like to do, where you are trying to do it, and provide
your COSMA username.

## Who should I consult for technical problems? Which mailing list should I use?

For technical problems, please email cosma-support@durham.ac.uk. If we cannot
solve your problems, we will then try to find people who can.

## Who can get an account on cosma?

Any STFC theory community member can apply for time on the DiRAC facility
through an application to the standard call for proposals or through a
seedcorn application. See the [DiRAC facility
website](https://www.dirac.ac.uk) for more details.

Access to the Cosma5, which is part Cosma, is available to all ICC and
CEA members [(details here)](https://durhamuniversity-my.sharepoint.com/:w:/g/personal/dph0arj_durham_ac_uk/ESQiUHr4wKNCv4Y9PgPo57cBH66i03eh7oa2BR58StmN4Q).
ICC collaborators may be able to access non-DiRAC time on cosma7 and
cosma8. Contact your collaborator at Durham, cc-ing cosma-support.

## What should I do to get an account?

Follow these instructions [here](account.md).

## Can my external collaborator get an account too?

Yes, provided that they are a collaborator with the ICC.

## How do I log in to COSMA?

Follow [these instructions](ssh.md). This will work both from within and
outside Durham University.

## Can I use VNC? Where should I run the server?

VNC is not recommended for security reasons. However, [x2go](x2go.md) offers a
faster graphical interface.

## What are the main differences between cosma5, cosma7 and cosma8?

Please see [here](facilities.md).

## Why is there a cosma5, 7 and 8, but no cosma6?

COSMA6 was retired in April 2023, having reached a veritable age of 11 years,
and to make space for the COSMA8 phase-2 expansion.  COSMA5 is still in
operation because it is in a different data centre (using a different power
input), and no longer a DiRAC system.

## How do I decide which COSMA to use?

If you are working on a DiRAC project, you should use COSMA7 or COSMA8,
depending on which project you are working. You need to be a member of the
relevant Operating System Group (use the "id" command on a login node), to
submit to the corresponding COSMA.

If you are not part of a DiRAC project, you should use COSMA5. You will need
to be part of the "durham" group to do this.

## How do I copy (large) files to/from cosma?

Please see [here](data.md)

We have a [Globus Online](https://www.globus.org) endpoint, cosma#data. Please
create an account, and use this.

For intermediate sized files, you can always use scp or rsync.

## Where is my home directory?

    /cosma/home/PROJECT/USERNAME

Where PROJECT will be durham or a DiRAC project identifier.  This is usually
backed up nightly (retained for 60 days), and also snapshotted hourly
(retained for about 1 week). Just ```cd``` into the hidden directory
```.snapshot``` to view these (all directories in the home space have these).

You also have

    /cosma/apps/PROJECT/USERNAME

which is ideal for software installation, Python virtual environments, etc,
and which has daily snapshots.

You will also have data storage space, typically in one of:

    /cosma5/data/PROJECT/USERNAME
    /cosma7/data/PROJECT/USERNAME
    /cosma8/data/PROJECT/USERNAME

This is not backed up.

## Are there disk usage quotas?

Yes, these should be set. You have a quota both on total storage capacity
(typically 10TB for data and 10GB for homespace), and total number of files
used.

How do I check my quota?

On a login node, use the `quota` command. This should report all your quotas
on the different file systems (/cosma5, /cosma7, /cosma8, /cosma/home and
/cosma/apps). This is part of the cosma module, so you may need to "module
load cosma" first.

Alternatively use the `c5quota`, `c7quota`, or `c8quota` commands to see your
usage of those file systems, or the `lfsquota` command to see a report for all
lustre file systems you have access to (this should work from all login
nodes). These also need the cosma module loaded. To just see your homespace or
apps quota, use the `nfsquota` command.

Is anything backed-up?

Homespace is usually backed up every day. Data space can be archived to tape
media upon request.

Detailed usage for the data file systems can be found on [usage](system.md)
website.

## Can I print from cosma?

This is not currently possible, though if you have a Durham email, you can
email a PDF to the CIS printers using the "mail" command.

## What are these "modules"?

[Modules](modules.md) are used to setup your work environment, changing your
environment variables (e.g. PATH, etc) depending on what your requirements
are.

## Which modules should I load? Are these different on the different Cosma’s? How do I find which modules are available?

Use the "modules available" command to see available modules. These are the
same for each COSMA system, and if optimised versions exist for particular
architectures, these may be loaded automatically.

## What are the recommended modules for running Gadget? Arepo?

Please see the codes section of the site for specific code
[details](issues.md).  If you would like a specific selection adding, please
ask us (or add it yourself).

## How do I adapt the Makefile to be consistent with these modules?

Well written Makefiles should just work. However, badly written Makefiles may
need changing to make use of the environment variables created by loading
modules. The "export" command will show you the currently set environment
variables or use the "module show" command to see the variables that are
defined.

## How do I load modules automatically on login?

Put "module load MODULE" commands within your .bash_profile script (or .login
if you are an older user)

## I want to perform a large simulation: Who do I ask? Can I just run?

It is recommended to speak to cosma-support@durham.ac.uk first, so that we are
aware of your requirements. We may also be able to make recommendations.

## How do I write the submission script?

Follow these [instructions](slurm.md)

## What are the main commands to interact with a batch job?

See [here](slurm.md)

## How do I make sure my job runs on full nodes?

Nodes on the cosma7 and cosma8 queues are exclusive - you will not share nodes
with other users. However, this does mean you should make good use of all the
available cores.

The cosma5 queue is not exclusive: your job will share nodes with other jobs.
To have a node to yourself, request all 256 of its cores.  The `--exclusive`
flag is ignored on this queue.

If you are using a single core job, consider running multiple of these at the
same time, using SLURM arrays, or a parallel MPI launch. COSMA8 has a serial
queue "cosma8-serial" for smaller jobs if really needed.

## How many cores can I reasonably request?

COSMA5 has about 2000 cores

COSMA7 has ~12,500 cores.

COSMA8 has ~67,080 cores.

## What determines when my job starts? How do I know the job is running? How can I kill it?

The SLURM job submission system has a fair scheduler, based on how many jobs
you have previously submitted, how busy the queues are, and how large your job
is. If you specify a job with a shorter run-time, it is more likely to be
scheduled more quickly to fill in space. This is called backfilling.

For job control, please see [here](slurm.md)

## Where should I put the data? Is that backed-up?

You will have space in /cosma[5,7,8]/data/PROJECT/USERNAME

This data is not backed up, but operates on a maintained parallel storage
system (i.e. individual disk failures do not lead to data loss), and is
archived periodically.

Each storage location is optimally connected to that system. e.g. if you store
data in /cosma7/ please access it from the cosma7 queue.

Not every file system is available on every compute node, even if you can see
it on a login node. For example, /cosma8 is not available on the cosma5 or
cosma7 compute nodes, and /cosma7 is read-only on the cosma5 and cosma8 compute
nodes. See the [table of mounted file systems](storage.md#mounted-filesystems).

## Do I need to worry about where the initial conditions are stored?

Yes. These should be stored on the data storage connected to the compute nodes
you are using. e.g. for the cosma8 queues, use /cosma8/data/

If initial conditions are small and only used by a small number of nodes at a
time, they may be better stored in your home space, but running from the home
space is generally to be avoided.

## How do I run an embarrassingly parallel job?

Investigate using SLURM arrays or use the parallel_tasks code make a copy from
```/cosma/home/sample-user/parallel_tasks```.

## Can I log-on to a compute node? Should I?

You can either use the ```srun``` command (which will give you an empty
compute node), the ```salloc``` command (which will cause mpirun jobs to be
launched on the nodes in question), or ask to be added to the developers
group.  You can monitor CPU and memory use of a node running your job using
PCP (Performance Co-Pilot) see [here](system.md#performance-co-pilot) and some
locally developed scripts.

## How do I find how busy the system is?

SLURM commands such as squeue and sview will tell you this.

## How do I check my project's allocation?

Use `mybalance` on a login node to see how much of the current quarter's
allocation your DiRAC projects have used. `dirac-query-allocation` is the same
command under a longer name. Like `quota`, it needs the cosma module.

```
mybalance                 # all of your projects, on all systems
mybalance cosma8          # one system
mybalance -p dpXXX cosma8 # one project
mybalance -q cosma8       # every quarter, not just the current one
mybalance -h              # all options
```

The system can be `cosma7`, `cosma8`, `highram`, `dine`, `cosma8dine2` or
`cosma8mi300x`. Allocations are reported in CPU hours, except for `dine` and
`cosma8dine2` (kWh) and `cosma8mi300x` (GPU hours).

COSMA5 is not listed, because DiRAC does not award allocations on it.

## What is "backfill"? How do I exploit this?

If a large (many node) job is waiting to run, it cannot start until enough
nodes are available. This therefore means that some nodes become idle, and can
be used as "backfill" for short jobs. To use this, submit your job as usual,
and if the system deems it appropriate, it will schedule you quickly. To make
best use of this, specify a short time period for your job.

The backfill commands show which nodes are free now, and for how long a job
could run on them:

| Queue | Command | Nodes | CPUs per node | Shows partly used nodes? |
| ----- | ------- | ----- | ------------- | ------------------------ |
| cosma5 | `c5backfill` | 8 | 256 | Yes |
| cosma7 | `c7backfill` | 220 | 28 | No |
| cosma7-rp | `c7rpbackfill` | 222 | 28 | No |
| cosma8 | `c8backfill` | 527 | 128 | Yes |
| dine2 | `dine2backfill` | 8 | 64 | Yes |
| bluefield1 | `bluefield1backfill` | 18 | 32 | No |

Slurm counts each physical core as one CPU on these queues, so a cosma8 node
has 128 CPUs even though Linux tools such as `nproc` report 256.

The commands report two kinds of window:

- **Exclusive node windows** are nodes that are completely free. "No.
  hosts/slots" gives the number of nodes, then the number of CPUs on them.
- **Serial-only backfill windows** are free CPUs on nodes that are partly in
  use. Jobs can only use these on a queue that shares nodes, such as
  cosma8-serial, cosma5 or dine2.

To use a window, set your job's time limit (`-t`) to less than the runtime
shown.

## What if my job does not need a whole node?

The cosma7 and cosma8 queues give each job whole nodes, so a job that uses 1 CPU
is still charged for the whole node.  The options depend on the system:

- **COSMA8:** use the cosma8-serial queue.  It uses the same 527 nodes as cosma8,
  but only reserves the CPUs that you request, and other jobs can run on the
  same node.  Each CPU gets 8GB of memory unless you request a different amount
  with `--mem`, up to a full node of 128 CPUs and 1TB.
- **COSMA7:** there is no serial queue.  Either run several tasks inside one
  job so that you use all 28 CPUs, or use the cosma7-shm queue described below.
- **COSMA5:** the cosma5 queue already shares nodes.  Each CPU gets 4GB of memory
  by default.  You can request more with `--mem`, but Slurm may add CPUs to your
  job to match, and these count towards your usage: for example, a 1 CPU job that
  requests 24GB gets 5 CPUs.

For example, to run on 4 CPUs of a COSMA8 node with 32GB of memory:

```
#SBATCH -A dpXXX
#SBATCH -p cosma8-serial
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH -t 12:00:00
```

## What are the shm queues?

The shm queues are small queues of nodes with unusual hardware, mostly with far
more memory per CPU than the main queues.  Use them when a job needs a lot of
memory on one node, rather than many nodes.

| Queue | Node | CPUs | RAM | Default RAM per CPU | Other hardware |
| ----- | ---- | ---- | --- | ------------------- | -------------- |
| cosma7-shm | mad01 | 56 | 3TB | 13.6GB | |
| cosma7-shm | mad02 | 112 | 1.5TB | 13.6GB | |
| cosma7-shm2 | mad03 | 48 | 6TB | 46GB | |
| cosma8-shm | mad04, mad05 | 128 | 4TB | 32GB | NVIDIA A100 GPUs |
| cosma8-shm2 | ga004 | 128 | 1TB | 8GB | AMD MI100 GPU |
| cosma8-shm2 | ga006 | 64 | 1TB | 8GB | AMD MI210 GPUs |
| cosma8-shm3 | mad08, mad09 | 192 | 768GB | 4GB | |

These queues work differently from the main queues:

- They share nodes, so other jobs can run alongside yours.  Your job only
  reserves the CPUs and memory that it requests.
- Please request the memory that you need with `--mem`, because the default
  depends on the queue, as shown above.
- The maximum run time is 3 days.
- If your DiRAC project is over budget, jobs on these queues are not moved to a
  -pauper queue.

cosma7-shm2 is only available to the durham and do025 groups.  See the
[list of queues](queue.md) for more about each one.

## I want to analyse a simulation, but need a lot of memory: how do I do this?

The COSMA5 login node has 768GB. The COSMA7 login nodes login7a and login7b
have 1.5TB, and login7c has 768GB. The COSMA8 login nodes have 2TB RAM. This is
shared between other logged in users, so please check for a quiet node first.

The mad01 system has 3TB memory.

The mad02 system has 1.5TB RAM.

The mad03 system has 6TB RAM (using Apache Pass non-volatile memory, so performance is somewhat reduced).

The mad04 system has 4TB RAM.

The mad05 system has 4TB RAM.

The mad06 system has 1TB RAM.

The command `slurmnodeprop` followed by the partition name will show the
numbers of available CPU cores as well as memory.

## I want to visualise my data: what can I use?

Standard visualisation tools are available. If you need an answer to this
question, please ask us to put more details here. Several GPU servers are also
available.

## I am developing a code and need to profile and debug it

What are the debugging tools?

allinear, gdb, perf, etc are all installed.

## What are the profiling tools?

allinear, gdb, perf, etc are all installed

## My short tests take a long time to start: can I do something about this?

Specify a short time period in you batch script file so you can run using
backfill.

## Can I run interactively on a node? How do I do this?

The srun command will allow you to do this.


## Tell me about parallel compile. Can I compile on cosma5 and then run on cosma7? 

To compile in parallel, use the -j NNN argument when you type make (e.g. make
-j 4 to use 4 threads during compilation).

Heavily optimised code compiled on COSMA5 or COSMA7 may not run on COSMA8, which
does not support AVX-512. It is best to compile on the login nodes associated
with the compute cluster you intend to use. See
[the differences between systems](ssh.md#cosma8-cosma7-cosma5-differences).

Note that a full compilation environment is not installed on the compute
nodes, you are expected to compile on the logins.

## Locale errors

If you are getting locale errors when compiling or running code, check your
LANG environment variable (```echo $LANG```).  If this is not set, you can do
```export LANG=en_GB.UTF-8``` and try again.

Compilers do not always handle locales very well. If this works remember to do
this every-time you login, or add it to your ```.bash_profile```.


## Does mounting cosma via sshfs on your local machine hog any Cosma resources?

If you begin moving large files about, you may notice poor performance.

## How do I find out the disk quota I have? How can I get more?

With the cosma module loaded ("module load cosma"), use the `quota` command.

You can ask for an increase your quota by email cosma-support@durham.ac.uk but
you should make sure that this is OK with the appropriate project manager or
follows your project rules especially for larger requests. Quotas apply to
users and projects, so both can be exceeded.

## My jobs die without creating an output

Probably, you are trying to access storage not belonging to that particular
COSMA. e.g. from the cosma7 queue, you are trying to write to /cosma5. This is
not allowed (inefficient for large jobs). So, you need to make sure that all
reading/writing is done to locally attached storage.

## I am in many groups, how do I change my default one?

The "newgrp" command can be used to do this. If the "id" command shows you
being a member of several groups, you can change between them using "newgrp
GROUPNAME". This will only take effect for your current shell. However, it can
be used within batch scripts if you wish to write your data as a particular
group.  I cannot write to my data space in
/cosma*/data/PROJECT/USERNAME. Please help...

First, check that you have write permission on this directory:

ls -ld /path/to/directory

This should show something like drwxr-xr-x 1234 USERNAME GROUP ..., which
means that you have read, write and execute permission, that members of the
group have read and execute permission, and that everyone else has read and
execute permission. If the w for write permission is not present
(e.g. dr-xr-xr-x) you should add it: chmod u+w /path/to/directory

Check that the directory is owned by you, i.e. that the USERNAME returned from
the ls -ld command is your username!

If that is all okay, check that you have sufficient quota left to write data
there: "module load cosma" and then `quota`. This should be done on a login
node (login5, login6 or login7).

Finally, if you are still not able to write, check that the group you are
writing as still has quota left. To identify your group, use the "id"
command. This will show gid=XXXX(group) where XXXX is a number. You can then
use e.g. c5quota -g XXXX (or c7quota or c8quota). Also, please note that your
default group may not be that used to write your data, if your directory has a
"sticky" bit set. In this case, the "ls -ld" command will show something like
drwxr-sr-x. Note the "s". You will be writing as the specified group into this
directory, regardless of what your default group is. Then check that this
group is not over quota.

To change the group that you are writing as, if a sticky bit is set, either
remove the sticky bit (chmod g-s /path/to/directory) or re-group the directory
(chown USER:NEWGROUP /path/to/directory). If a sticky bit is not set, and your
default group is over quota, so you wish to write as a different group, you
can use the "newgrp" command: "newgrp GROUP". This will change your group to
that specified (which should be in the list given by the "id" command), for
the current terminal. Therefore, you will need to do this again if you log in
again. You will also need to put it into your Slurm batch
scripts. Alternatively, if you believe that your default group is wrong, and
wish it to be changed, please contact cosma-support.

## Using the snap file systems (/snap7, /snap8)

These file systems are typically used for rapid checkpointing, and have fast
read-write bandwidths.

Please bear in mind that this is temporary storage, is cleared
periodically, and has no redundancy - if a disk dies, you will lose
data.  So don't put anything here you can't afford to lose.

Basically, best use comes down to how you want to use the storage, and the
striping across the file system.

Assuming you have many processes which each want to write 1 file
simultaneously, then the things to bear in mind: There are 192 OSTs (disks) on
/snap8 and 160 OSTs on /snap7.  So spreading the write load across these as
best possible is a good idea.

If you are writing >96 files (80 files for /snap7), then set the
striping of the parent directory to 1 (lfs setstripe -c 1
/path/to/dir) and then all files written here will be written to a
single file.

If you want to optimise further, you can specify each file to be written to
a specific OST in advance (lfs setstripe -c 1 -i INDEX /path/to/file)
where INDEX is the
index of that specific file.  This effectively "touches" the file (creates
a 0-byte stub), which when you then write to, will be written to the
selected OST.

If you are writing fewer than 96 files (80 files on /snap7), there may
be advantages in setting the stripe count to 2 or more, depending on
file size (e.g lfs setstripe -c 2 /path/to/dir/or/file).

To check the number of OSTs, you can use e.g.:
```lfs df /snap7 | grep OST | wc -l```
Occasionally, particular OSTs are not writable (e.g. nearly full).  You can use the checkOSTs.sh script to check these (module load cosma first).  Run this command from within a directory on the file system in question, and it will print any OSTs to avoid (or just the total number of OSTs if all are writable).

## I am a PI - how do I use my time?

You may need to sign up to join your own project on SAFE (particularly if you
are a new PI and are already a member of other projects).  You also need to
specify within your Slurm batch scripts that your time should be allocated to
your project.

## As a PI, how do I manage storage allocations?

As a PI, you are responsible for managing the allocation of storage to users.
Each user assigned to your project will get a default quota (typically 10TB).
By default, we assume that if a user requires more quota, you will give
implicit approval, and therefore, their quota can be increased by emailing
COSMA support.  However, if you would like more control (some large projects
do this), then we will ask users to get approval for quota extensions from you.

The sum of the space used by users should not be greater than the total
allocation assigned to your project.

See the [Lustre](lustre.md#quotas) page for information about how to get your
current quota.

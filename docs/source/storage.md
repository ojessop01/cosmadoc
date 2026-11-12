# Storage

COSMA has several storage systems, each for a different purpose:

| Storage | Location | Typical quota | Protection | Use it for |
| ------- | -------- | ------------- | ---------- | ----------- |
| [Homespace](#homespace) | /cosma/home/PROJECT/USERNAME | 10GB | Hourly snapshots, daily backups | Scripts and settings |
| [App space](#app-space) | /cosma/apps/PROJECT/USERNAME | 100GB | Daily snapshots | Software and Python virtual environments |
| [Data space](#data-space) | /cosma5, 7 or 8/data/PROJECT/USERNAME | 10TB | Redundant disks, no backups | Simulation output and results |
| [Scratch space](#scratch-space) | /snap7 or 8/scratch/PROJECT/USERNAME | None | None | Checkpoints that can be recreated |
| [Temporary space](#temporary-space) | /tmp | None | None | Short-lived files during a job |
| [Archive space](#archive-space) | Tape | By request | Tape copy | Long-term storage |

To see your usage and quotas, use the `quota` command (see the [FAQ](faq.md#are-there-disk-usage-quotas)).

## Homespace

User homespace is found under /cosma/home and is a NFS-mounted file system.  Users typically have a 10GB quota.  This file system is snapshotted hourly, with snapshots kept for around 10 days.  It is also usually backed up daily, with backups kept for up to 60 days.

## App space

User app space is found under /cosma/apps and is a NFS-mounted file system.  Users typically have a 100GB quota.  This file system is snapshotted daily, with snapshots kept for around 10 days.

### Recovering files from snapshots

If you delete or overwrite a file in your homespace or app space, you can usually copy it back from a snapshot.  Each directory has a hidden `.snapshot` directory, which does not appear in `ls -a` but which you can list directly:

```
ls /cosma/home/PROJECT/USERNAME/.snapshot
cp /cosma/home/PROJECT/USERNAME/.snapshot/SNAPSHOT_NAME/myfile /cosma/home/PROJECT/USERNAME/
```

Snapshots are named after the time that they were taken, and are read-only.

## Data space

There are multiple data spaces, at /cosma5, /cosma7 and /cosma8.  Your space is at e.g. /cosma8/data/PROJECT/USERNAME.  Users typically have a 10TB quota.  These file systems are not backed up but have redundancy.

## Scratch space

The scratch file systems are fast Lustre file systems, designed for simulation checkpoints:

| File system | Size | Your space | Main nodes |
| ----------- | ---- | ---------- | ---------- |
| /snap7 | 440TB | /snap7/scratch/PROJECT/USERNAME | COSMA7 login nodes, cosma7 and cosma7-rp queues |
| /snap8 | 1.1PB | /snap8/scratch/PROJECT/USERNAME | COSMA8 login nodes, cosma8 queues |

Neither is available on the cosma5 queue.  See [mounted filesystems](#mounted-filesystems) for other nodes.

These file systems are not safe places to keep data:

- They have no redundancy, so if a single disk fails, data will be lost.
- They are not backed up.
- They are cleaned out every 4 months.

Therefore they should only be used for data that can be recreated.  There is no user quota, but please delete files that you no longer need.

If you use them for checkpoints, either [mirror your files](lustre.md#redundancy), or copy a set of checkpoints to /cosma7 or /cosma8 every few days.  Do not overwrite your previous copy until the new one has been checked, so that you always have one good set.

New files use a single disk by default.  To get the best speed, set the striping to suit the number of files that you write: see [using the snap file systems](faq.md#using-the-snap-file-systems-snap7-snap8).

## Temporary space

Every node has its own /tmp, which can only be seen from that node.  It works differently on login nodes and compute nodes:

| Nodes | What /tmp is | Size | Can run programs from it? | Unused files are deleted after |
| ----- | ------------ | ---- | ------------------------- | ------------------------------ |
| Login nodes, mad06 | Memory (tmpfs), shared by all users | 100GB | No | 3 days |
| Compute nodes, and other nodes for direct ssh | Local disk | 21GB to 1.4TB, see below | Yes | 10 days |
| gn002, gn003 | Part of the system disk | 800GB, shared with the operating system | Yes | 10 days |

Local disk sizes, measured on a sample of nodes in late 2026:

| Size | Nodes |
| ---- | ----- |
| 21GB to 43GB | cosma7-rp |
| 43GB | cosma7, cosma8, bluefield1, cosma7-shm |
| 88GB | cosma5, dine2, cosma8-shm, cosma8-shm2, cosma8-shm3, cosma8-ska, gn001, gn004, gn005 |
| 177GB | mad11, mad12, ga008 |
| 1.4TB | gi001 |

Nodes in the same queue can differ, so to see the size and free space on the node you are using, run `df -h /tmp`.

There is no per-user quota on /tmp, so one user can fill it for everyone on that node.  For large temporary files, use your space on /cosma* or /snap* instead.

### /tmp on login nodes

Because /tmp is held in memory on login nodes, large files take memory from other users.  Programs in /tmp cannot be run, and fail with `Permission denied`.  If a tool needs to run something from its temporary directory, point it at your app space instead:

```
mkdir -p /cosma/apps/PROJECT/USERNAME/tmp
export TMPDIR=/cosma/apps/PROJECT/USERNAME/tmp
```

### /tmp in batch jobs

Slurm does not create a private temporary directory for each job:

- /tmp is shared with any other jobs on the node.
- Files stay in /tmp when your job ends, so please delete them.
- In a multi-node job, each node has a separate /tmp.
- Your job inherits `TMPDIR` from the shell that you submit it from.  If you set it on a login node, your job will use the same directory unless you set it again in your job script.
- Do not use the `--tmp` option.  Slurm does not track space in /tmp, so jobs that use it are rejected with `Requested node configuration is not available`.

To use a private directory that is removed when your job script exits, add this to your job script:

```
export TMPDIR=$(mktemp -d /tmp/$USER.XXXXXX)
trap 'rm -rf "$TMPDIR"' EXIT
```

This also removes the directory if your job reaches its time limit.

### /dev/shm

/dev/shm is held in memory on every node, and is shared by all users.  In a batch job, files that you write there count towards your job's memory limit, so your job can be killed with an out of memory error if you do not request enough.  Files stay in /dev/shm when your job ends, so please delete them.

## Mounted filesystems

Not all login and compute nodes mount all filesystems. The following table summarizes which filesystems can be read/written from which nodes:

| Filesystem | login5* | m5*** | login7* | m7*** | login8* | m8*** |
| :--------: | :-----: | :---: | :-----: | :---: | :-----: | :---: |
| /cosma/home|   rw    |   rw  |   rw    |   rw  |    rw   |   rw  |
| /cosma/apps|   rw    |   rw  |   rw    |   rw  |    rw   |   rw  |
| /cosma5    |   rw    |   rw  |   rw    |       |    rw   |       |
| /cosma7    |   rw    |   r   |   rw    |   rw  |    rw   |   r   |
| /snap7     |         |       |   rw    |   rw  |         |       |
| /cosma8    |   rw    |       |   rw    |       |    rw   |   rw  |
| /snap8     |         |       |         |       |    rw   |   rw  |
| /cosma6    |   rw    |       |   rw    |       |    rw   |       |

In these tables, rw means read and write, r means read-only, and a blank means that the file system is not available.  /cosma/home and /cosma/apps are available everywhere, including on the nodes below.

Other nodes and queues:

| Nodes                         | /cosma5 | /cosma7 | /cosma8 | /snap7 | /snap8 |
| :---------------------------: | :-----: | :-----: | :-----: | :----: | :----: |
| mad06, gn001, gn005, gi001    |   rw    |   rw    |   rw    |        |   rw   |
| mad11, mad12, gn002           |   rw    |   rw    |   rw    |        |        |
| gn004                         |   rw    |   rw    |   rw    |   rw   |   rw   |
| ga008                         |         |   rw    |   rw    |        |        |
| cosma8-shm, cosma8-shm2, cosma8-ska | rw |  rw    |   rw    |        |   rw   |
| cosma7-shm                    |   rw    |   rw    |   rw    |   rw   |        |
| dine2                         |         |   r     |   rw    |        |   rw   |
| bluefield1, gracehopper       |   rw    |   rw    |   rw    |        |        |

To check a file system on any other node, run this on that node, using /cosma5, /cosma7, /cosma8, /snap7 or /snap8.  It prints rw or ro, followed by other mount options, or nothing if the file system is not available:

```
findmnt -n -M /cosma7 -o OPTIONS
```

## Archive space

The tape archive is a good place for long-term storage and archival of data which is not actively required, or which you wish to back up.  To archive data to tape, please contact cosma-support.

## Public space

There are multiple ways in which you can make data publicly accessible.  We have a [StorJ](storj.md) object storage system hosted on servers spread across DiRAC, which can be used for uploading data and storing with users.

It is also possible to make individual files available for download via a web link, please ask if you wish to do this.

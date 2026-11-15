# The Lustre file systems

`/cosma5`, `/cosma7`, `/cosma8`, `/snap7` and `/snap8` are **Lustre** file
systems.  Lustre is a parallel file system: it spreads data over many disks
and servers, so that many jobs can read and write at once, and a single large
file can be read or written quickly by spreading it over several disks.

To use Lustre well, it helps to know three things:

- **It is built for large files.**  Reading and writing large files is fast;
  working with very many small files is slow, and puts a load on the servers
  that everyone shares.
- **Large files should be striped**, that is, spread over several disks.  By
  default, every file goes on a single disk.
- **The `/snap` file systems are not protected** against disk failure.

See [storage](storage.md) for what each file system is for, and its quota.

## Striping

Lustre stores each file as one or more **stripes**, each on a different disk
(an "OST").  On COSMA, the default is one stripe of 1MB chunks: the whole file
is on one disk.  That is right for small files, but for large files (more
than about 100MB), striping over several disks makes reading and writing
faster, and is essential for very large files that would not fit on one disk.

### Checking a file's striping

```
lfs getstripe -c myfile.hdf5     # the number of stripes
lfs getstripe myfile.hdf5        # the full layout
lfs getstripe -d mydirectory     # the default for new files in a directory
```

### Striping new files

A file's striping is set when it is created, and new files take their
striping from the directory they are created in.  So the simplest approach is
to set striping on a directory **before** writing large files into it:

```
mkdir /cosma8/data/PROJECT/USER/bigfiles
lfs setstripe -S 4M -c 8 /cosma8/data/PROJECT/USER/bigfiles
```

Every new file in that directory is then striped over 8 disks, in 4MB chunks.
`-c` sets the number of stripes and `-S` the chunk size.

To stripe a single file, create it empty with `lfs setstripe` before writing
to it:

```
lfs setstripe -S 4M -c 8 /cosma8/data/PROJECT/USER/newfile.hdf5
```

Choosing the number of stripes:

- Use more stripes for larger files and for files read or written by many
  processes at once.  A few stripes (4 to 16) suits most large files.
- `-c -1` stripes over every disk.  This can suit a few very large files on
  `/cosma7` or `/cosma8`, but is not a good idea on `/snap8`.
- The chunk size (`-S`) must be less than 4GB; 1MB to 16MB is usual.

Lustre can also use a **progressive file layout**, in which a file gets more
stripes as it grows, so that small files stay on one disk and large files are
spread out automatically.  See the Lustre documentation for `lfs setstripe -E`
if you would like to set this up.

### Restriping existing files

Changing `lfs setstripe` on a directory does not change files already in it.
To restripe an existing file, copy it into a directory with the new striping
(and then replace the original), or use `lfs migrate`, which rewrites the file
in place:

```
lfs migrate -c 8 /cosma8/data/PROJECT/USER/bigfile.hdf5
```

Do not migrate a file while a program is using it.

### Striping in your programs

Programs can set striping themselves through Lustre's C library, but for most
codes it is easier to use a library that handles parallel I/O, such as
parallel HDF5 (the `parallel_hdf5` modules), with suitable settings, and set
striping on the output directory.

## Many small files

Every file, however small, needs work from Lustre's metadata servers, which
are shared by all users.  Millions of small files make your work slow, and slow
down the file system for everyone, including running jobs.

- Combine small files into fewer, larger ones, for example one HDF5 file with
  many datasets, or a `tar` archive for files you do not need often.
- Keep code, builds, Python environments and git repositories in your home
  directory or app space, not on Lustre.
- Avoid commands that look at every file in a large directory tree, such as
  `ls -lR` or `find` without a narrow search, more often than you need to.

## Mirroring on /snap7 and /snap8

The `/snap7` and `/snap8` file systems have no built-in protection: **if a
disk fails, the data on it is lost.**  You can protect important files by
mirroring them, so that each file is kept on two disks in different pools.

To mirror a directory, so that files created in it are mirrored:

```
lfs mirror create -N -p pool1 -N -p pool2 mirroredDirectory/
```

You can also stripe each copy, for example over 2 disks each:

```
lfs mirror create -N -p pool1 -c 2 -N -p pool2 -c 2 mirroredStripedDirectory/
```

Always give the two pools (`-p pool1` and `-p pool2`).  Without them, both
copies of a file can end up on the same disk, which gives no protection.

A mirrored file is not copied to its second disk automatically.  After writing
files, synchronise them:

```
lfs mirror resync file1
lfs mirror resync *            # several files at once
lfs mirror verify file1        # check that the copies match
```

If you keep restart or checkpoint files on `/snap7` or `/snap8`, either
mirror them, or copy a set to `/cosma7` or `/cosma8` every few days, so that a
disk failure does not lose weeks of computing.  When copying, do not overwrite
the old set until the new set has been copied and checked.

## Copying data onto Lustre

`rsync` writes files without striping them.  For files larger than about 1GB,
use the patched `rsync` in the `rsyncLustre` module, which stripes large files
automatically as it copies them:

```
module load rsyncLustre
rsync -av SOURCE /cosma8/data/PROJECT/USER/DESTINATION/
```

Alternatively, set striping on the destination directory before copying (see
[striping new files](#striping-new-files)).

## Directory sizes

`du -sh /cosma8/data/PROJECT/USER` shows the space used by a directory, but can
take a long time for directories with many files.  It reports space used on
disk, after Lustre's compression; add `--apparent-size` for the total size of
the files, as it would be on another system.

A faster way, which only asks the metadata servers, is `lfs find`:

```
lfs find /cosma8/data/PROJECT/USER --lazy --printf "%s\n" | awk '{sum+=$1;n+=1}END{print "Total: "sum" bytes, "sum/1024/1024/1024" GB, "n" files"}'
```

## Quotas

To see your own usage and quota on a Lustre file system:

```
lfs quota -u USER -h /cosma8
```

and your project's:

```
lfs quota -g GROUP -h /cosma8
```

With the `cosma` module loaded, `lfsquota` shows your quota on every Lustre
file system at once, and `lfsquota -g GROUP` your project's.

### Who is using the project's quota

The [usage pages](system.md#system-usage) show how much each user in a project
is using on each Lustre file system.  Some of this information is updated
nightly or weekly, so it may not show the last few hours.

## Sharing files

To give other people access to your files, see
[access control lists](acl.md).

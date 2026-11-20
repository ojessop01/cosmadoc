# The DAOS file system

The DAOS file system is based on 4 nodes each with 8x NVMe drives, and a total capacity of around 48TB.

It is an experimental file system, only accessible on the DINE system.

## DAOS user instructions

The DAOS file system is currently being rebuilt.  Once complete, it should be accessible from most login and compute nodes.

## A note about caching

DAOS is an object store with a POSIX overlay.  As a result, it can see some unintuitive behaviour when used on multiple nodes.  However, provided you are aware of this, it should work well.

To avoid these effects (and probably hurt performance), you can use `--disable-caching` and/or `--disable-wb-cache` arguments when mounting.  However, if you don't need to do this (depending on how you are using it), then probably best not to.  It is currently unclear what the effective differences between these are.

Without disabling caching, the following scenarios can arise.  A file written on one node, and then viewed on another node will be fine.  However, the second node will cache the file, so that further viewings will not see any updates from the first node.

If many nodes are writing to a file, it is best to disable caching.  This is not generally recommended however.  Better to use one file per node, as traditional HPC codes do.

Of key consideration here are the slurm logs which capture the print statements from the codes.  These may not have all information if caching is not disabled.

If you are using DAOS to store code, then you should note that if you do not disable caching, other nodes will not see any updates to code, re-compilations etc, unless the file system is unmounted and remounted.

## Object file operations

If you append to a file (e.g. `echo test >> file.txt`) then our current understanding is that this will create a new file, overwriting the contents of the old, rather than adding bytes onto the end of the existing.  This therefore results in poorer performance, particularly if the file is large (since it has to be fully rewritten).  Therefore, it is best to avoid appending, and rather keep a file descriptor open within your code.

## Setup instructions

1. Before you use the DAOS system: Access to the DAOS filesystem is via a DAOS pool. Pools can only be created or amended by [cosma-support](contact.md). Currently the only pool that exists is called DAOS8 and is 47TB in size, and is accessible for anyone who is part of the `durham` group. If you are part of that group then please have a go, otherwise contact [cosma-support](contact.md) and we can add you to the DAOS8 pool.

2. Create a container for your data: Think about this as a directory that you can place (mount) at different places in the file system. In this example I will mount my container in my home directory.
So we are going to create a container called “PiData”, and this container will be created in the pool named DAOS8. I am trying to give my container a name that I and anyone else who looks at in the DAOS8 pool will understand what is inside this container. The container will have a POSIX file system type, and we want to create this container with some redundancy, so I will add rf:1. This means there will always be an additional data copy erasure code (i.e. 1 disk failure).  You might wish to use rf:2 to allow for simultaneous failure of two disks.

`daos cont create DAOS8 --label PiData --type POSIX --properties rf:1`

You will be informed that the container was created.

If you have errors doing this, it may be due to environment modules that you have loaded.  Try a `module purge`, or (in the case of some Intel modules which don't unload cleanly), remove them from your `.bashrc` (or wherever), log in again, and retry.

3. Confirm container creation: If you would like to confirm this, then you can list all the containers that exist in the DAOS8 pool.

```
daos cont list DAOS8
 UUID                                 Label     
----                                 -----     
76ad9d89-1b21-4613-85bb-f23848f2db7e PiData    
6d4ce6ec-4c35-435b-90dd-0fb60a18dcb2 contTest1
```

This shows the new container PiData, and another container that was used during testing.

4. Create a local mount point: To access this container you need a place on the file system where you would like to access that data. Create a local directory and mount the container there.

```
mkdir PiData
dfuse -m ./PiData --pool DAOS8 --cont PiData [--disable-caching] [--disable-wb-cache]
```

In this case the container and the directory have the same name, however, this is not necessary.

If you ‘ls’ to see what is inside the container it should be empty as we have not used it before.

```
ls ./PiData
```

5. Using this container within your job script: Within your job script you need to mount the container on the compute node before you try to access it, and then unmount the container afterwards. This will ensure you never have any stale mounts if you use the same compute node in the future. So within your job script add the following lines:

```bash
## mount your container
mountPoint="/cosma/home/PROJECT/USER/DAOS/PiData"

dfuse -m "${mountPoint}" --pool DAOS8 --cont PiData

## Add your program here (avoid appending to large files on DAOS)
echo "$(date) -2- $(hostname)" > "${mountPoint}/PiData.log"
cat "${mountPoint}/PiData.log"

## unmount your container
fusermount3 -u "${mountPoint}"
```

6. Exemplar script: Below is a working script

```bash
#!/bin/bash -l

# 1 node, running 1 core.

#SBATCH --ntasks 1        # The number of cores you need...
#SBATCH -J Daos-PiData_01 # Give it something meaningful.
#SBATCH -o standard_output_file.%J.out
#SBATCH -e standard_error_file.%J.err
#SBATCH -p bluefield1     # Partition name
#SBATCH -A durham         # Project account, e.g. durham or dp004
#SBATCH --exclusive
#SBATCH -t 0:01:00        # Max time expected for code to run, 1 minute
#SBATCH --nodes=1         # Number of nodes to use
#SBATCH --nodelist=b101   # Specific node; for DAOS this is b101-b114
#SBATCH --mail-type=END   # notifications for job done & fail
#SBATCH --mail-user=USER@EXAMPLE.AC.UK

#module list

# mount container
mountPoint="/cosma/home/PROJECT/USER/DAOS/PiData"

dfuse -m "${mountPoint}" --pool DAOS8 --cont PiData

## Add your program here
echo "$(date) -- $(hostname)" > "${mountPoint}/PiData.log"
cat "${mountPoint}/PiData.log"

## unmount container
fusermount3 -u "${mountPoint}"
```

If you run this script then the output file will show that it ran successfully and show the date and host name. Great, it works, but if you try to view this locally mounted container you will not see the update.

7. Seeing your data: To ensure you see the updated data you need to unmount and then mount the container, if you did not previously mount it with caching disabled.

```
fusermount3 -u ./PiData
dfuse -m ./PiData --pool DAOS8 --cont PiData
```

Now any update in the container and its associated file will be visible to you.



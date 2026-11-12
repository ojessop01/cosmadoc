# Containers

COSMA supports containers through [Apptainer](https://apptainer.org/docs/user/latest/), which was previously called Singularity.  A container packages software and its dependencies into a single file.  You can run many Docker images with Apptainer, but Docker itself is not available.

Apptainer is installed on the login nodes, but only on some compute nodes:

| Queue | Apptainer |
| ----- | --------- |
| `cosma5`, `dine2`, `bluefield1`, `cosma8-ska` | Yes |
| `gracehopper` | Yes, with images built for ARM |
| `cosma8`, `cosma8-serial`, `cosma7`, `cosma7-rp`, `cosma7-shm` | No |

This list comes from testing a sample of nodes in November 2026.  To check a node, run `command -v apptainer` in a job.  The older `apptainer` module in `old-modules` could not run images when tested.

## Getting an image

Download images on a login node, because compute nodes cannot reach the internet.  Images and caches can be large, so keep them in your app or data space.  You also need to set a temporary directory, because /tmp on login nodes cannot run programs:

```
export APPTAINER_CACHEDIR=/cosma/apps/PROJECT/$USER/apptainer/cache
export APPTAINER_TMPDIR=/cosma/apps/PROJECT/$USER/apptainer/tmp
export PROOT_TMP_DIR=/cosma/apps/PROJECT/$USER/apptainer/tmp
mkdir -p $APPTAINER_CACHEDIR $APPTAINER_TMPDIR

apptainer pull alpine.sif docker://alpine:3.20
```

Without `PROOT_TMP_DIR`, the download fails with a `proot` error.

## Running a container

To run a command inside a container:

```
apptainer exec alpine.sif cat /etc/os-release
```

In a job, this works in the same way:

```
#!/bin/bash -l
#SBATCH -J container
#SBATCH -o container.%j.out
#SBATCH -p dine2
#SBATCH -A PROJECT
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH -t 00:10:00

apptainer exec /cosma/apps/PROJECT/$USER/alpine.sif cat /etc/os-release
```

Your home directory is available inside the container.  To use another directory, add it with `--bind`:

```
apptainer exec --bind /cosma/apps myimage.sif ls /cosma/apps
```

## GPUs

To use NVIDIA GPUs inside a container, add `--nv`:

```
apptainer exec --nv myimage.sif nvidia-smi
```

For AMD GPUs, use `--rocm` instead.  The GPU must also be requested as usual: see [GPU jobs](gpujobs.md).

## ARM nodes

The gn002 and gn003 nodes use ARM processors, and need images built for ARM.

# Python

Python on COSMA comes from modules.  You install the packages you need
yourself, in a virtual environment (or a conda environment) in your app
space.  This page covers choosing a Python, installing packages, running
Python in batch jobs, making it faster, and common problems.

## Python versions

| Module | Python | Notes |
| ------ | ------ | ----- |
| `python/3.12.4` | 3.12 | The default.  Use this unless you have a reason not to. |
| `python/3.13.2` | 3.13 | The **free-threaded** build of Python 3.13 (no global interpreter lock).  Some packages do not support it yet. |
| `python/3.10.1-rocky9` | 3.10 | |
| `python/3.9.19` | 3.9 | |
| `python/conda3-2025.12` and older `conda3-*`, `anaconda3-*` | Varies | Conda installations: see [using conda](#using-conda). |

Without any module, `python3` is the operating system's Python 3.9, which
has few packages.  Load a module instead.

If you need a different version, ask cosma-support.

## Installing packages in a virtual environment

The Python modules have only a few packages installed, so install what you
need in a **virtual environment**: a folder holding a copy of Python and the
packages you install into it.

1. Load the Python you want, and create the environment in your app space
   (not your home directory, which is small):

   ```
   module load python/3.12.4
   python -m venv /cosma/apps/PROJECT/USER/venvs/myenv
   ```

2. Activate it, and install packages:

   ```
   source /cosma/apps/PROJECT/USER/venvs/myenv/bin/activate
   pip install numpy scipy matplotlib h5py
   ```

3. Use it.  Each new session or job needs the `source` line to activate the
   environment (and loading `python/3.12.4` keeps `python` and library paths
   consistent; you must also load any MPI or HDF5 modules that packages such as
   `mpi4py` or `h5py` were built against).  `which python` shows which Python
   you are using: inside the environment it is `.../myenv/bin/python`.
   `deactivate` leaves it.

- **Keep a list of what you installed**: `pip freeze > requirements.txt`, then
  `pip install -r requirements.txt` makes the same environment again.
- **Keep pip's cache out of your home directory** if you install large packages:
  `export PIP_CACHE_DIR=/cosma/apps/PROJECT/USER/.cache/pip`.
- **One environment per project** avoids version clashes between projects.
- **Install on a login node**: compute nodes cannot reach the internet.
- **ARM nodes (`gn002`, `gn003`)** need their own virtual environment created on
  an ARM node; x86 virtual environments will not run there.
- **To delete an environment**, delete its folder.
- If you use csh or tcsh, source `activate.csh` instead.

For Jupyter, see [using your own Python environment](jupyter.md#using-your-own-python-environment).

## Packages with MPI: pre-built wheels

`mpi4py`, and `h5py` with parallel (MPI) support, depend on the MPI and HDF5
libraries, and are awkward to build.  Pre-built versions, matched to COSMA's
modules, are in `/cosma/local/python-wheels`:

| Python | Folder | Packages |
| ------ | ------ | -------- |
| 3.12.4 | `3.12.4/openmpi-5.0.3-hdf5-1.12.3` | `mpi4py` 3.1.6, `h5py` 3.11.0 |
| 3.13.2 (free-threaded) | `3.13.2/openmpi-5.0.3-hdf5-1.12.3` | `mpi4py` 4.1.0, `h5py` 3.14.0 |

`3.12.4/openmpi-4.1.4-hdf5-12.0` also holds a larger set of older wheels,
including `nbodykit` and its dependencies.

To use them with Python 3.12.4:

```
module load python/3.12.4 gnu_comp/14.1.0 openmpi/5.0.3 parallel_hdf5/1.12.3
source /cosma/apps/PROJECT/USER/venvs/myenv/bin/activate
W=/cosma/local/python-wheels/3.12.4/openmpi-5.0.3-hdf5-1.12.3
pip install $W/mpi4py-3.1.6-cp312-cp312-linux_x86_64.whl
pip install $W/h5py-3.11.0-cp312-cp312-linux_x86_64.whl
```

Load the same modules whenever you use these packages, and run MPI programs
with `mpirun`:

```
mpirun -np 4 python myscript.py
```

## Packages that need compiling

Some packages compile C, C++ or Fortran code when installed.  Load a compiler
module first, and any libraries the package needs:

```
module load python/3.12.4 gnu_comp/14.1.0
```

For example, to build `h5py` against COSMA's HDF5 (without MPI), rather than
using the copy of HDF5 bundled with the standard `h5py`:

```
module load python/3.12.4 gnu_comp/14.1.0 hdf5/1.14.4
source /cosma/apps/PROJECT/USER/venvs/myenv/bin/activate
pip install --no-binary=h5py h5py
```

This takes a few minutes.  `python -c "import h5py; print(h5py.version.hdf5_version)"`
confirms which HDF5 it uses.

Most packages, including `numpy`, `scipy` and the standard `h5py`, are
available as pre-built wheels from PyPI and need no compiler.

## Using conda

Virtual environments, as above, are usually simpler.  If you need conda, load a conda module, then set it up for your shell.  This module cannot be loaded at the same time as a `python` module, so unload that first:

```
module unload python
module load python/conda3-2025.12
eval "$(/cosma/local/anaconda3/202512/bin/conda shell.bash hook)"
```

Conda environments are large, so do not keep them in your home directory.  Choose a location in your app space, and do the same for its package cache:

```
export CONDA_PKGS_DIRS=/cosma/apps/PROJECT/USER/conda/pkgs
conda create -p /cosma/apps/PROJECT/USER/conda/myenv python=3.12 numpy
conda activate /cosma/apps/PROJECT/USER/conda/myenv
```

A small environment like this one, with its cache, takes around 1.5GB.  Create environments on a login node, because compute nodes cannot reach the internet.  Your job script then needs the `module load`, `eval` and `conda activate` lines.

Do not run `conda init`: it changes your `~/.bashrc` so that conda starts in
every shell, including batch jobs and other tools, which can cause confusing
problems.

## Python in batch jobs

A job script for a Python program loads the same modules and activates the
same environment you used to install the packages:

```
#!/bin/bash -l
#SBATCH -J analysis
#SBATCH -A ACCOUNT
#SBATCH -p cosma8-serial
#SBATCH -t 02:00:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o analysis.%j.out
#SBATCH -e analysis.%j.err

module purge
module load python/3.12.4
source /cosma/apps/PROJECT/USER/venvs/myenv/bin/activate

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
python analysis.py
```

- **Set the number of threads.**  NumPy and SciPy use multithreaded maths
  libraries that start as many threads as they see CPUs.  Set
  `OMP_NUM_THREADS` (and, if needed, `OPENBLAS_NUM_THREADS` or
  `MKL_NUM_THREADS`) to the cores you asked for.
- **With `multiprocessing`**, which starts several Python processes, set the
  threads per process to 1, so that the total matches your cores.
- **Many independent inputs**, such as one run per snapshot, are best as a
  [job array](sbatch.md), one task per input.
- **Print progress with `flush=True`**, or run `python -u`, so that output
  appears in the job's output file as it happens, rather than at the end.

## Finding what is slow

Use Python's own profilers; general tools such as `perf` show little useful
detail for Python code.

| Tool | Install | Shows |
| ---- | ------- | ----- |
| `cProfile` | Part of Python | Time in each function: `python -m cProfile -s cumulative myscript.py \| head -30` |
| `line_profiler` | `pip install line_profiler` | Time for each line of chosen functions |
| `py-spy` | `pip install py-spy` | Where a running program is, without changing it: `py-spy record -o profile.svg -- python myscript.py` draws a flame graph |
| `scalene` | `pip install scalene` | Time and memory use for each line |

## Making Python faster

- **Use NumPy on whole arrays** rather than Python loops over elements.  This is
  usually the largest gain.
- **Avoid copies** of large arrays, and choose the data type: `float32` arrays
  use half the memory of `float64`, if the precision is enough.
- **Numba** (`pip install numba`) compiles Python functions with loops into fast
  code, and can run them on several threads.
- **Read only the data you need** from HDF5 files, in large pieces, rather than
  whole files.
- **Use processes for parallel work**: in normal Python, threads do not run
  Python code at the same time.  `multiprocessing`, a job array, or Numba
  avoid this limit.

For more, see the Python section of
[optimising code with agents](agents-optimisation.md#python), which applies
whether or not you use an agent.

## Common problems

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `ModuleNotFoundError: No module named ...` | The environment is not activated, or the package was installed into another environment.  Check `which python`. |
| `pip install` fails with a compiler error | Load a `gnu_comp` module, and any library the package needs, then try again. |
| `Disk quota exceeded` while installing | Packages or pip's cache are filling your home directory.  Keep environments in app space; `pip cache purge` clears the cache. |
| A job is much slower than expected, or the node is overloaded | Too many threads: set `OMP_NUM_THREADS` (see [Python in batch jobs](#python-in-batch-jobs)). |
| `h5py` fails inside a Slurm job with errors about MPI | An MPI build of `h5py` tried to start MPI.  Run it with `mpirun`, or use a standard `h5py` in that environment. |
| A package does not work with `python/3.13.2` | That module is the free-threaded build.  Use `python/3.12.4`. |
| Output appears only at the end of a job | Python buffers output when writing to a file.  Use `python -u` or `print(..., flush=True)`. |

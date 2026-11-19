# Installing your own software

COSMA has a lot of software installed centrally, but you will often need
something that is not there: a newer version, a Python package, a code from
your collaborators, or a tool nobody else uses.  This page helps you choose
the best way to get it, and explains each option.

## Check first

Before installing anything, check whether it is already available:

```
module avail NAME
```

and look in the [list of modules](modulelist.md).  Some software is only
visible after loading a compiler or MPI module, or `old-modules`.

If something would be useful to other people, or is hard to build, ask
cosma-support whether it can be installed centrally.

## Choosing a method

| You want | Best method |
| -------- | ----------- |
| A Python package | A [virtual environment](#python-packages) with `pip` |
| Python with non-Python dependencies (for example, from conda-forge) | [conda](python.md#using-conda) |
| A code that builds from source with `configure` or CMake | [Build it](#building-from-source) in your app space |
| A complex package with many dependencies, or several builds of one package | [Spack](spack.md) |
| Software distributed as a container image, or needing a different Linux | A [container](containers.md) |
| A command-line tool written in Node.js (`npm`) | Install it with `npm` into your app space (see [installing agents](agents-setup.md#installing-agents) for the method) |

## Where to install

Install software in your **app space**, `/cosma/apps/PROJECT/USER`:

- your home directory is small (about 10GB), and software and its caches
  quickly fill it;
- the Lustre data file systems (`/cosma5`, `/cosma7`, `/cosma8`) are slow for
  the many small files that software consists of, and are not backed up.

A tidy layout is one folder per package and version, for example
`/cosma/apps/PROJECT/USER/software/hdf5/1.14.6`.  You can then keep several
versions, and remove one without affecting the others.

Install on a **login node**: compute nodes cannot reach the internet, so
downloads fail there.

## Python packages

Make a virtual environment in your app space, activate it, and install with
`pip`:

```
module load python/3.12.4
python -m venv /cosma/apps/PROJECT/USER/venvs/myenv
source /cosma/apps/PROJECT/USER/venvs/myenv/bin/activate
pip install numpy h5py
```

See [Python](python.md) for details, including packages that need compiling,
pre-built packages for MPI, and conda.

## Building from source

Most open-source codes are built in three steps: configure, build, install.
Load the compiler and libraries first, and install into your app space with a
**prefix**.

With `configure` (autotools):

```
module load gnu_comp/14.1.0 openmpi/5.0.3
./configure --prefix=/cosma/apps/PROJECT/USER/software/mytool/1.2
make -j8
make install
```

With CMake:

```
module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/cosma/apps/PROJECT/USER/software/mytool/1.2
cmake --build build -j 8
cmake --install build
```

- Use at most a few cores on a login node (`-j8`).  For large builds, use an
  [interactive session](interactive.md).
- Build for the CPUs you will run on (see
  [building for the right CPU](compiling.md#building-for-the-right-cpu)).
- Write the build commands into a script, so that you can repeat the build
  exactly, for example after a system upgrade.

See [compiling code](compiling.md) for compilers, libraries and common
errors.

### Using what you installed

Add the program's folders to your environment, for example in `~/.bashrc` or
your job script:

```
export PATH=/cosma/apps/PROJECT/USER/software/mytool/1.2/bin:$PATH
export LD_LIBRARY_PATH=/cosma/apps/PROJECT/USER/software/mytool/1.2/lib:$LD_LIBRARY_PATH
```

### Your own modules

If you install several packages or versions, you can write your own module
files, so that they load in the same way as COSMA's.  Create a folder for
them, with one file per version:

```
mkdir -p /cosma/apps/PROJECT/USER/modulefiles/mytool
```

and in `/cosma/apps/PROJECT/USER/modulefiles/mytool/1.2`:

```
#%Module1.0
module-whatis "My tool 1.2"
prepend-path PATH /cosma/apps/PROJECT/USER/software/mytool/1.2/bin
prepend-path LD_LIBRARY_PATH /cosma/apps/PROJECT/USER/software/mytool/1.2/lib
setenv MYTOOL_HOME /cosma/apps/PROJECT/USER/software/mytool/1.2
```

Then tell the module system about the folder, and load it as usual:

```
module use /cosma/apps/PROJECT/USER/modulefiles
module load mytool/1.2
```

Put the `module use` line in your `~/.bashrc` to make your modules always
available.  Other members of your project can use them too, if you grant group
read and execute permissions (`chmod -R g+rX /cosma/apps/PROJECT/USER/modulefiles`
and the software folder).  Note that POSIX [access control lists](acl.md) only
apply to the Lustre data file systems, not `/cosma/apps`.

## Containers

If software is hard to build, or is distributed as a Docker image, run it in a
container with Apptainer.  Note that Apptainer is installed on the login nodes
but only on some compute nodes.  See [containers](containers.md).

## Keeping track

- Note how you installed each package (the version, the modules loaded, the
  options used), for example in a `README` next to it.  You will need this
  when something breaks, or when you write the methods section of a paper.
- After a system upgrade, programs built against old system libraries may
  stop working and need rebuilding.
- Remove old versions you no longer use, to save space in your quota.

# Spack

[Spack](https://spack.readthedocs.io) is a package manager for HPC software.
It builds a package together with everything it depends on, and lets several
versions and builds of the same package live side by side.  Spack records the
location of each dependency inside the libraries it builds (using RPATH), so a
package installed by Spack does not need further modules to be loaded for its
dependencies.

```{note}
Spack on COSMA is **experimental**, and only a few packages are installed
with it.  Most software on COSMA is provided as ordinary
[modules](modules.md): look there first, in the [list of modules](modulelist.md).
Please report problems or requests to cosma-support.
```

## Using the central Spack installation

Two versions are available as modules: `spack/0.15` (the default, from 2020)
and `spack/0.22`.  Use `spack/0.22`.  Loading the module does not set Spack
up by itself; it prints the command to run:

```
module load spack/0.22
source /cosma/local/spack/0.22/spack/share/spack/setup-env.sh
```

`spack/0.15` only works with the operating system's Python (3.9).  If you
have a newer Python module loaded, its set-up fails with
`No module named 'six.moves'`.

### Environments

Packages are grouped into environments.  List them, and activate one, with:

```
spack env list
spack env activate cosma-x86-MLTest
```

Activating an environment adds its programs to your `PATH`.  `spack find`
lists what it contains, and `spack env deactivate` turns it off.  In November
2026 the environments in `spack/0.22` were:

| Environment | Contents |
| ----------- | -------- |
| `cosma-x86-MLTest` | HDF5 1.14.3 built with GCC and with Intel oneAPI, for the x86 nodes |
| `cosma-aarch64-NVHPC` | CMake, FFTW, GSL and HDF5 built with NVIDIA HPC compilers, for the ARM (Grace) node |
| `cosma-aarch64-MLTest`, `cosma-aarch64-MLTest2` | Test environments for the ARM node |
| `default` | Empty |

The message printed by the `spack/0.22` module suggests
`spack env activate cosma`, but there is no environment of that name, so that
command fails with `No such environment`.

The central installation is read-only: you can use its packages, but not
install new ones into it.

## Your own Spack

To install packages that are not available, you can run your own copy of
Spack in your app space.  This takes some disk space and build time, but gives
you full control.

1. Get Spack, in your app space rather than your home directory:

   ```
   cd /cosma/apps/PROJECT/USER
   git clone --depth=2 --branch=releases/v0.22 https://github.com/spack/spack.git
   source /cosma/apps/PROJECT/USER/spack/share/spack/setup-env.sh
   ```

2. Tell Spack about COSMA's compilers, so it does not build its own.  Load a
   compiler module, then let Spack find it:

   ```
   module load gnu_comp/14.1.0
   spack compiler find
   ```

3. Tell Spack about software that is already installed, such as `cmake` or
   `openmpi`, so it does not rebuild it: `spack external find`.

4. Install packages, building on a login node with a few cores, or in a batch
   job for large builds:

   ```
   spack install -j 8 fftw +openmp
   spack load fftw
   ```

Spack keeps downloads and build files in its own folders, which can grow to
many gigabytes.  `spack clean -a` removes them once your packages are built.
Keep your Spack in app space, not your home directory, and not on a Lustre
data file system, where building many small files is slow.

## Building for the right nodes

Spack builds for the CPU of the machine it runs on unless told otherwise, so a
package built on an AVX-512 login node may not run on COSMA8, which does not
have AVX-512.  Build on a node of the type you will run on, or set the target
explicitly, for example `spack install fftw target=zen2` for COSMA8.  See
[compiling for each system](facilities.md#compiling-for-each-system).

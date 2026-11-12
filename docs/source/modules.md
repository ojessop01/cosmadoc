# The module environment

Most software on COSMA, including compilers, MPI libraries, maths and file
libraries, Python and many applications, is installed centrally and made
available through **modules**.  Loading a module sets up your environment
(mainly `PATH` and library paths) so that you can use that software.
Unloading it takes those settings away again.  Nothing is installed or copied
when you load a module, so it is instant and safe to try.

COSMA uses Environment Modules version 4 (Tcl modules).  If you have used
Lmod on another system, most commands are the same, but there is no
`module spider`: use `module avail NAME` to search instead.

For a full list of what is installed, see the [list of modules](modulelist.md).

## Common commands

| Command | What it does |
| ------- | ------------ |
| `module avail` | List every module you can load. |
| `module avail NAME` | List the versions of one module, e.g. `module avail hdf5`.  The default version is marked `(default)`. |
| `module load NAME` | Load the default version of a module. |
| `module load NAME/VERSION` | Load a specific version, e.g. `module load gnu_comp/14.1.0`. |
| `module list` | Show the modules you have loaded. |
| `module unload NAME` | Unload one module. |
| `module purge` | Unload all modules. |
| `module show NAME` | Show what loading a module would change, without loading it. |
| `module help NAME` | Show a module's help text, if it has one. |
| `module save NAME` | Save the modules you have loaded as a named set. |
| `module restore NAME` | Load a saved set again. |
| `module savelist` | List your saved sets. |
| `module saverm NAME` | Delete a saved set. |

`module list` may print a harmless `ERROR: can't read "rows"` message on some
terminals; it can be ignored.

## Loading a compiler and libraries

Many libraries are built separately for each compiler and MPI library, so you
must choose those first.  Load modules in this order:

1. a **compiler**, such as `gnu_comp` or `intel_comp`;
2. an **MPI library**, such as `openmpi`, if your code uses MPI;
3. the **libraries** your code needs, such as `fftw`, `hdf5` or `gsl`.

For example:

```
module purge
module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5 fftw gsl
```

If you load a library before a compiler, the module refuses to load and tells
you which compilers it can be used with:

```
$ module load hdf5
A compiler must be chosen before loading the hdf5 module.
Please load one of the following compiler modules:

	gnu_comp/14.1.0
	intel_comp/2024.2.0
	...
```

Libraries such as `parmetis` need an MPI module as well as a compiler.  The
[list of modules](modulelist.md#what-to-load-first) shows, for each library,
which compiler and MPI modules it works with.

Some modules only appear after loading another one.  For example, the Intel
oneAPI modules `compiler`, `mpi`, `tbb` and `compiler-rt` appear after loading
`intel_comp`:

```
module load intel_comp/2025.3.0 compiler-rt tbb umf compiler mpi
```

### Compiler optimisation settings

The compiler modules also set two variables that you can use in makefiles:
`COSMA_OPT`, which is `-O3 -march=native`, and `COSMA_ALL_OPT`, which is
`-O3 -march=sandybridge` and works on every x86 node, at the cost of some
speed.  Code built with `-march=native` only runs on CPUs
like the one it was built on, so it may stop with `Illegal instruction` on
other nodes.  See [compiling for each system](facilities.md#compiling-for-each-system).

## Modules in job scripts

A batch job starts with the modules that were loaded when you submitted it.
To make jobs repeatable, start every job script with `module purge`, then load
exactly the modules the program was built with:

```
#!/bin/bash -l
#SBATCH ...

module purge
module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5

mpirun ./my_program
```

Use the same versions to build and to run a program.  Loading a different
compiler or MPI version at run time is a common cause of crashes and
`error while loading shared libraries` messages.

## Modules in your login files

You can load modules you always use in `~/.bashrc`, but keep it to a few: every
module loaded there is loaded in every shell, including batch jobs, scripts
and `scp`.  A `module save` set, restored when you need it, is often better:

```
module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5 fftw
module save mysim
# later, or in a job script:
module restore mysim
```

Saved sets are kept in `~/.module`.

In a shell that does not read your login files, such as a command run over
`ssh` or by some tools, the `module` command may not exist.  Run
`source /etc/profile.d/cosma-local-modules.sh` to set it up.

## Building your own software

If something you need is not available as a module, you can:

- ask cosma-support whether it can be installed centrally, especially if other
  people would use it;
- use the experimental [Spack](spack.md) installation;
- install Python packages in a [virtual environment](python.md);
- run it in a [container](containers.md);
- build it yourself in your app space (`/cosma/apps/PROJECT/USER`), using the
  compiler and library modules.

## Old modules

Modules from before COSMA moved to Rocky Linux 9 in 2024 are still available
with `module load old-modules`.  Many no longer work, because the system
libraries they were built against have changed.  The
[list of modules](modulelist.md) shows which old modules still load.

## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `A compiler must be chosen before loading ...` | Load a compiler (and MPI, if needed) first.  See [loading a compiler and libraries](#loading-a-compiler-and-libraries). |
| `ERROR: Unable to locate a modulefile for 'NAME'` | The name or version is wrong.  Search with `module avail NAME`. |
| `module: command not found` | The shell has not set up modules.  Run `source /etc/profile.d/cosma-local-modules.sh`. |
| A program worked before but now fails to start | The modules loaded now differ from those it was built with.  Check with `module list`, and load the same ones. |
| `Illegal instruction` | The program was built for a different CPU.  See [compiling for each system](facilities.md#compiling-for-each-system). |
| You are not sure which modules you need | Ask cosma-support, or see the documentation for the code you are using. |

For more about the module command, run `man module` or see the
[Environment Modules documentation](https://modules.readthedocs.io).

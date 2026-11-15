---
orphan: true
---

# Rocky 9 Cluster welcome email, 12th July 2024

For information on the cluster upgrade please see [here](clusterupgrade.md).  Below are the emails sent to users, though some of the information will now be out of date.

```
Dear all,

COSMA is now exiting maintenance mode, and returning to production.

You should be able to log in, but you will probably notice several
changes.  Please also consider the system as at-risk for the next few
weeks while we iron out any oddities.

Please note that the host keys have changed, so you will be warned about 
this when logging in for the first time.  You should be able to remove the
old entries from your system using something like:

ssh-keygen -R login8.cosma.dur.ac.uk (or other appropriate login node)

The operating system has been upgraded to the latest Rocky 9.4 OS, with a
new Linux kernel (5.14), glibc and system compilers.  Therefore existing
binaries may need recompiling.  We have left many of the old modules in
place, because some may or may not work depending on use case.  If there
is a module that you rely on which is no longer present, you can:

module load old-modules

which will then allow you to module load the required module.

The default version of compilers, Python, etc has been updated.

There is a new Intel OneAPI (compilers, etc) installation, a new GCC and a
new Python.

The old cosma Slurm partition is still down: cosma5 users should submit to
the newer cosma5 partition for now.  We hope that the old cosma partition
will be made available within a couple of months.

The old cosma5 login nodes (login.cosma.dur.ac.uk, login5a and login5b)   
are not yet available.  Please use login5c.cosma.dur.ac.uk instead.

Some of the Mad nodes (e.g. cosma*-shm* partitions) are still down,
but will be made available shortly.  The mad01 system is now
batch-queue only, and not available as a login node
(massive.cosma.dur.ac.uk).


The bluefield1 partition is also not yet available.

The cosma8-dine2 partition has been renamed to dine2.

Currently, the maximum runtime for jobs submitted to the cosma8 partitions
is limited to 2 hours, to allow for rapid testing and turn around.  This
will be reverted to 3 days next week.  The other partitions have their
normal runtimes.

The dataweb node is not yet available.

The AMD GPU nodes are not yet available - we are awaiting driver
updates (this also means that the cosma chatbot will run slower than
usual for now).

You may receive spurious email over the next few weeks while we test
things (e.g. quota alerts, etc).

Your /cosma/home/PROJECT/USER has been moved to a new file system, and we
have added a /cosma/apps/PROJECTS/USER directory.

As before, /cosma/home is backed up nightly.  However, /cosma/apps is not,
but has a significantly larger (100GB) quota.  This is therefore an ideal
place for installing software libraries, Python venvs, spack
installations, etc.  We have softlinked several of your hidden directories
to /cosma/apps (e.g. ~/.share, ~/.cache, etc).  Please note, these spaces
are not designed for running batch jobs from: use e.g. /cosma[5,7,8] for
these as appropriate.

For any x2go users, you may find windows are not refreshing.  To resolve
this, within your x2go session, go to the Applications menu, Settings ->
Settings manager.  Select the "Window Manager Tweaks" icon, and within   
this the "Compositor" tab.  Then untick "Enable display compositing".

The /madfs file system has been retired, along with /cosma7old.

Please let us know if you find anything broken, or unexpected behaviour,
and we will do our best to fix it.  However, for issues around code
compilation, module versions etc, please make an initial attempt to
resolve it.

This email is available at
https://cosma.readthedocs.io/en/latest/rocky9email.html

Unfortunately, we have lost xemacs (for now).  However, standard emacs is
still the recommended text editor of choice (though we understand vi may
be a personal choice for some users).

Best wishes,
Alastair, Mark, Peter, Paul and Richard.
```


# Update from 25th July

```
Dear all,

In case you hadn't noticed, the COSMA queue time has been restored
(for a week or so now) to the usual 3 days.

The cosma queue (old COSMA5 nodes) is still not yet available.
Likewise the DINE system (bluefield1 queue).  We hope both should be
back within the next week or so.

Please remember to acknowledge COSMA in any publications, using the
official acknowlegement at:
https://cosma.readthedocs.io/en/latest/acknowledgements.html
This changes periodically, so please check each time.

A number of Python users have been struggling with Jupyter and virtual
environments - we are regularly updating the information to help with
this at:
https://cosma.readthedocs.io/en/latest/jupyter.html

Old Python modules are unlikely to work.  We recommend using 3.12.4
(or 3.9.19 if you need something older).

Please note that when pip installing numpy, the numpy package reached
version 2.0.0 recently which has broken things for some users.
Therefore, you might wish to add a version restriction, e.g. pip
install numpy<2.0.0

Please continue to let us know if you have problems with old modules
not working - we periodically remove these into the old-modules
section.

Finally, we have had a reservation request which will be in place from
17th August for around 6 months using 164 nodes.  This leaves around
364 nodes spare - if anyone was planning on running a larger job than
that during that period, please let us know.  This is to allow a large
cosmology simulation (Colibre) to run efficiently.

Best wishes,
cosma-support!

```

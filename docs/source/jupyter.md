# Jupyter Hub

A Jupyter Hub is available on the `login5c`, `login7b` and `login8b` login nodes.  There is also a Jupyter Hub for GPU development on mad06 (A100 GPU).

## Logging in to Jupyter Hub

Please use your COSMA login/password. If you do not know your password, please email cosma-support@durham.ac.uk for a reset.

## Recommended access

Run this command in the terminal of your local machine to set up a ssh tunnel to cosma, e.g.:

    ssh -L localhost:8443:login7b:443 USER@login7b.cosma.dur.ac.uk

or

    ssh -L localhost:8443:login8b:443 USER@login8b.cosma.dur.ac.uk

or

    ssh -L localhost:8443:login5c:443 USER@login5c.cosma.dur.ac.uk

where `USER` is the username you use for SSH access. Then point your web browser to [https://localhost:8443](https://localhost:8443).  You may also wish to use the -N flag to send the prompt to the background, and/or the -i flag if you need to specify the location of your ssh key.

## Adding a venv to Jupyter

The simplest way is to use the makeJupyterVenv.sh script.  Note, this should be done on a node running Jupyter (login7b, login8b), or from within a terminal on the Jupyter Hub:

```
# Select the module you wish to use (probably 3.12.4).
module load cosma python/X.Y.Z
# cd to the directory where you want your venv.
cd /cosma/apps/PROJECT/USER/
# Run the script to create the venv.
makeJupyterVenv.sh venvname
```

See below if you wish to take a more manual approach.

Once you have created your venv and added to Jupyter, it should appear in the Jupyter dashboard after you stop and restart your server (File menu -> Hub control panel -> Stop my server).  You can then start adding packages to it, either from within Jupyter or on the command-line:

```
source venvname/bin/activate
pip install numpy
pip install whatever
```

If you are not sure whether you are in your venv or not, `which python` will show you the location of your python interpreter, which should be VENVNAME/bin/python.  You will need to source the venv whenever you start a new connection to COSMA.  If you always want this, you could add it to your .login file.

To exit a venv, use the `deactivate` command.

You can even install a package from within a Jupyter notebook, e.g.:

```
# Install a pip package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install numpy
```

For more information about virtual environments please see [here](python.md)

### Manually adding a venv to Jupyter

If you wish to have more control (rather than using the makeJupyterVenv.sh script), you can use the following recipe to add your own venv to your Jupyter session.  Note that the venv name should be lower case.

```
# cd to your apps directory - a good place for putting code/libraries/venvs
cd /cosma/apps/PROJECT/USERNAME/
# (where PROJECT is the same as used by your homespace - as seen by `realpath ~USERNAME`)

# Create a venv (you may wish to module load python/X.Y.Z before this if you want a specific Python version)
python -m venv jupytervenv

# Activate the venv
source jupytervenv/bin/activate
# (or activate.csh if using a csh or tcsh shell)

# Install ipykernel in the venv
pip install ipykernel

# Do some jupyter magic
python -m ipykernel install --name myjupytervenv --display-name myjupytervenv --prefix jupytervenv/
deactivate

# Source the venv that Jupyter Hub uses (note, this must be done on one of the Jupyter login nodes - login7b or login8b
source /opt/venv/jupyter/bin/activate
# (or activate.csh if using a csh of tcsh shell)

#This next command assumes you are in the directory from within which you created your venv (e.g. /cosma/apps/PROJECT/USER).  If not, use the full path to your venv.
jupyter kernelspec install --user jupytervenv/share/jupyter/kernels/myjupytervenv
deactivate

# And now start using your venv (either by sourcing it again, or within Jupyter)
```

It should then appear in the Jupyter dashboard after you stop and restart your server (File menu -> Hub control panel -> Stop my server).

Note, the final source must be done on a node running jupyter (login7b or login8b), or from within a terminal on the Jupyter Hub.

## Launching Jupyter Lab on a compute node

This is advisable if you will be running some long calculations, which could otherwise interfere with other users on a login node. It also gives you a machine to use for yourself, so will probably allow your computations to complete in a shorter time.

Eventually, we will have a webpage and Jupyter Lab interface to do this. But for now:

### Interactively using srun

```
srun -A DIRAC_PROJECT -p PARTITION -t TIME --pty /bin/bash
```
    (e.g. `srun -A dp004 -p cosma7 -t 1:00:00 --pty /bin/bash`)

Once you get a compute node, do:

```
    export XDG_RUNTIME_DIR=""

    # Import your environment - you'll previously have done pip install jupyterlab here.
    source /path/to/your/venv/bin/activate

    jupyter lab --no-browser --ip=`ifconfig | awk '/172.17/ {print $2}'`

    #(note, be careful with back-ticks and single quotes when copying the above command)
```

Then, on your desktop/laptop, set up a ssh tunnel, e.g.:

```
    ssh -N -L localhost:8888:NODE:8888 USER@login7.cosma.dur.ac.uk
```

where NODE is the IP address of the node (which you can get using `ifconfig | grep 172.17` when on the node)

And direct your web browser (on your desktop/laptop) to http://localhost:8888

It will ask you to input a token: This should be copied from the command line where you ran the jupyter lab command.

Once you have finished, Ctrl-C twice in the jupyter terminal will stop it, and an exit (or Ctrl-D) will then end your slurm session.

### More automatically using sbatch

Create an sbatch script with some of the following information, e.g.:

    #!/bin/bash -l
    #SBATCH --ntasks 1
    #SBATCH -J jupyter
    #SBATCH -o slurmjupyter%J.out
    #SBATCH -e slurmjupyter%J.err
    #SBATCH -p cosma5       #for example, could be cosma8, cosma7 etc
    #SBATCH -A durham       #for example, could be dp004, or other projects
    #SBATCH -t 01:00:00     #1 hour - use more if you need it
    #SBATCH --mail-type=END # notifications
    #SBATCH --mail-user=YOUR_EMAIL_ADDRESS
    module purge
    source /path/to/your/venv/bin/activate
    #Your venv will need jupyter installed (pip install jupyterlab)
    export XDG_RUNTIME_DIR=""
    #Run Jupyter
    jupyter lab --no-browser --ip=`ifconfig | awk '/172.17/ {print $2}'`


Submit this script (sbatch SCRIPTNAME)

Once the job is running (find this using `squeue -u USERNAME`), you need to `tail -f slurmjupyterJOBID.err` until a message about how to connect appears (this will take a few seconds)

Then, on your desktop/laptop, set up a ssh tunnel (to the node given by `squeue -u USERNAME`), e.g.:

    ssh -N -L localhost:8888:NODE:8888 USER@login7.cosma.dur.ac.uk

And direct your web browser (on your desktop/laptop) to http://localhost:8888

It will ask you to input a token: This should be copied from the command line where you tailed the .err file.

Once you have finished, you can use `scancel JOBID` to end the slurm session.

## FAQ

Q: When plotting, I get a "JavaScript output is disabled in JupyterLab" message.

A: Select "Help -> Launch Classic Notebook". Then navigate to your notebook file, and run it.

Q: I would like my Jupyter webpage to be secure (using https, rather than http).

A: As above, it is reasonably secure, since it is only accessible to people who already have access to COSMA (between your desktop and COSMA is protected by ssh). However, if you would like increased security, you can add a host server certificate when you start the jupyter lab. You will need to create the certificate key and public key, and then start jupyter lab with the `--certfile=mycert.pem`

Q. Using `h5py` causes it to crash and gives errors about configuring SLURM.

A. the `h5py` module has MPI support built in which it attempts to initiate when running under SLURM. The fix for this used to be doing:

    module purge
    unset SLURM_NODELIST
    module load python/3.6.5

## Alternative access methods

### Running Firefox on the COSMA login node

Run Firefox directly on a login node, either using x2go, or X11 forwarding. This is not the recommended way.

For X11 forwarding, run this command in the terminal of your local machine:

    ssh -X USER@login7b.cosma.dur.ac.uk firefox https://localhost:443

This will launch a web browser on the login node, and so will require a fast Internet connection to be usable.

### Forward COSMA traffic through a local proxy

Run this command in the terminal of your local machine:

    ssh -D 1234 USER@login7b.cosma.dur.ac.uk

where `USER` is the username you use for SSH access, and `1234` is an example value for the port forwarding; if 1234 gives an error you can pick a higher value that works, just remember to update it in your browser settings (instructions below). 

Then reconfigure your local web browser with a HTTP proxy. If you use Firefox, run:

    firefox -P

which will create a new profile. You can call it i.e. `cosma`. Then, go to Edit > Preferences > General > Network Settings, select “Manual proxy configuration” and set “SOCKS host” to localhost, port 1234 (or whatever port you specified in the `ssh` command). Then remove the localhost entry in the “No proxy for” box, and click “OK”. For the future runs, you will be able to select pre-configured `cosma` profile you have just created.

If you use Chromium, run:

    chromium-browser --proxy-server="socks5://localhost:1234" https://localhost:443

updating the `1234` if necessary.

Finally, open https://localhost:443 to login to the Jupyter Hub.

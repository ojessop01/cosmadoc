# Jupyter

There are two ways to use Jupyter notebooks on COSMA:

| | JupyterHub on a login node | Jupyter in a batch job |
| - | -------------------------- | ---------------------- |
| Best for | Editing, small analyses, plotting | Long or heavy calculations |
| Resources | Shared with everyone on that login node | Your own cores and memory on a compute node |
| Set-up | An SSH tunnel and a web browser | A job script, and an SSH tunnel to the job's node |
| Time limit | None, but it stops if the node restarts | The job's time limit |

The login nodes are shared, so anything that runs for more than a few minutes
or uses a lot of memory belongs in a batch job (see
[good citizenship](citizenship.md)).

## JupyterHub on the login nodes

JupyterHub runs on these nodes:

| Node | Use |
| ---- | --- |
| `login5c` | COSMA5 |
| `login7b` | COSMA7 |
| `login8b` | COSMA8 |
| `mad06` | GPU development, with an A100 GPU (see the [hardware lab](hardwarelab.md) for access) |

### Connecting

JupyterHub is not open to the internet, so you reach it through an SSH
tunnel.  On your own computer, run:

```
ssh -N -L 8443:localhost:443 USER@login8b.cosma.dur.ac.uk
```

(replace `login8b` with `login7b` or `login5c` for those nodes), leave it
running, and open [https://localhost:8443](https://localhost:8443) in your web
browser.  `-N` keeps the terminal free of a shell; stop the tunnel with
`Ctrl-C` when you have finished.

To avoid typing this each time, add a `LocalForward` line to your SSH
configuration (see [forwarding ports](ssh.md#forwarding-ports)):

```
Host cosma8-jupyter
    HostName login8b.cosma.dur.ac.uk
    User USER
    LocalForward 8443 localhost:443
```

and run `ssh -N cosma8-jupyter`.

Your browser will warn that the connection is not private, because
JupyterHub's certificate is issued by COSMA itself, for the login node's name
rather than `localhost`.  The connection to COSMA goes through your SSH
tunnel, so it is safe to continue.

### Logging in

Log in with your COSMA username and password.  If you have forgotten your
password, request a reset on SAFE (see
[forgotten passphrase or password](ssh.md#forgotten-passphrase-or-password)).

### Stopping your server

Your Jupyter server keeps running after you close the browser.  When you have
finished, stop it from File, Hub Control Panel, Stop My Server, so that it
does not use memory on the shared login node.

## Using your own Python environment

JupyterHub starts with a standard Python.  To use your own packages, make a
virtual environment and add it to Jupyter as a "kernel".  It then appears in
the launcher, after you stop and restart your server.

### The quick way

`makeJupyterVenv.sh` makes a virtual environment and adds it to Jupyter in one
step.  Run it on a login node that runs JupyterHub (`login5c`, `login7b` or
`login8b`), or in a terminal inside JupyterHub:

```
module load cosma python/3.12.4
cd /cosma/apps/PROJECT/USER
makeJupyterVenv.sh myenv
```

Then install the packages you need into it:

```
source /cosma/apps/PROJECT/USER/myenv/bin/activate
pip install numpy h5py matplotlib
deactivate
```

Use a short, lower-case name.  `which python` shows which Python you are
using: inside the environment it should be `.../myenv/bin/python`.  See
[Python](python.md) for more about virtual environments.

You can also install a package from inside a notebook, into the kernel that
the notebook is using:

```
import sys
!{sys.executable} -m pip install numpy
```

### Adding an environment by hand

For more control, you can do the same steps yourself:

```
cd /cosma/apps/PROJECT/USER
module load python/3.12.4              # the Python version you want
python -m venv myenv
source myenv/bin/activate
pip install ipykernel
python -m ipykernel install --name myenv --display-name myenv --prefix myenv/
deactivate

# On login5c, login7b or login8b, register the kernel with JupyterHub
source /opt/venv/jupyter/bin/activate
jupyter kernelspec install --user /cosma/apps/PROJECT/USER/myenv/share/jupyter/kernels/myenv
deactivate
```

Then stop and restart your server, and the kernel appears in the launcher.

## Jupyter in a batch job

For long or heavy work, run Jupyter on a compute node.  You then have the
node's cores and memory to yourself, and do not slow down the login node for
others.

You need JupyterLab in your own virtual environment
(`pip install jupyterlab`).

### Interactively

Ask Slurm for an interactive session.  Use a queue that shares nodes, such as
`cosma5` or `cosma8-serial`, unless you need a whole node (see the
[queue guide](queue.md)):

```
srun -A ACCOUNT -p cosma5 -t 2:00:00 -c 8 --mem=32G --pty /bin/bash
```

When you get a shell on the compute node, start Jupyter:

```
export XDG_RUNTIME_DIR=""
source /cosma/apps/PROJECT/USER/myenv/bin/activate
jupyter lab --no-browser --ip=$(ifconfig | awk '/172.17/ {print $2}')
```

Jupyter prints an address containing the node's IP address, a port (usually
8888) and a token.  On your own computer, open a tunnel to that address,
through a login node:

```
ssh -N -L 8888:NODE_IP:8888 USER@login8b.cosma.dur.ac.uk
```

and open the `http://127.0.0.1:8888/lab?token=...` address that Jupyter
printed.  When you have finished, press `Ctrl-C` twice in the Jupyter
terminal, then `exit` to end the Slurm session.

### As a batch job

To leave Jupyter running without keeping a terminal open, submit it as a
job:

```
#!/bin/bash -l
#SBATCH -J jupyter
#SBATCH -A ACCOUNT
#SBATCH -p cosma5
#SBATCH -t 04:00:00
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -o jupyter.%j.out
#SBATCH -e jupyter.%j.err

module purge
source /cosma/apps/PROJECT/USER/myenv/bin/activate
export XDG_RUNTIME_DIR=""
jupyter lab --no-browser --ip=$(ifconfig | awk '/172.17/ {print $2}')
```

Submit it with `sbatch jupyter.sh`.  When it is running (`squeue --me`),
Jupyter's address and token appear in the `.err` file within a few seconds:

```
grep -m1 "http://172" jupyter.JOBID.err
```

Open a tunnel to that address as above, and open it in your browser.  When
you have finished, end the job with `scancel JOBID`, so it does not keep using
your allocation.

## Troubleshooting

**h5py fails inside a Slurm job with errors about MPI or Slurm.**  Some
builds of `h5py` include MPI support, which tries to start MPI when it sees
it is inside a Slurm job.  Use an `h5py` without MPI in your own environment
(`pip install h5py`), or start Python with `SLURM_NODELIST` unset
(`unset SLURM_NODELIST`).

**My kernel does not appear in the launcher.**  Stop and restart your server
(File, Hub Control Panel).  Check that the kernel is registered with
`jupyter kernelspec list`, run on a JupyterHub node after
`source /opt/venv/jupyter/bin/activate`.

**The page does not load.**  Check that the SSH tunnel is still running, and
that nothing else on your computer is using the same local port (8443 or
8888).  Choose another port if it is.

**I would like an HTTPS connection to Jupyter in a batch job.**  The traffic
between your computer and COSMA is already encrypted by the SSH tunnel.  For
extra security, you can create a certificate and start Jupyter with
`--certfile=mycert.pem --keyfile=mykey.key`.

## Other ways to reach JupyterHub

### A web browser on the login node

You can run Firefox on a login node and view JupyterHub through x2go or X11
forwarding (see [graphical access](x2go.md)):

```
ssh -X USER@login8b.cosma.dur.ac.uk firefox https://localhost:443
```

This is slow unless you have a fast connection.

### A SOCKS proxy

Instead of a tunnel to one port, you can send a browser's traffic through
COSMA:

```
ssh -N -D 1234 USER@login8b.cosma.dur.ac.uk
```

Then set your browser to use a SOCKS proxy at `localhost`, port `1234` (pick a
higher number if 1234 is in use).  In Firefox, create a separate profile for
this with `firefox -P`, then set Settings, Network Settings, Manual proxy
configuration, SOCKS host `localhost`, port `1234`, and remove `localhost`
from "No proxy for".  For Chromium:

```
chromium-browser --proxy-server="socks5://localhost:1234" https://localhost:443
```

Then open [https://localhost:443](https://localhost:443).

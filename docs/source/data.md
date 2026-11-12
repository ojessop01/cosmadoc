# Data Transfer

Data transfer off-site can be done from one of the login nodes (10GBit/s connectivity or from dataweb.cosma.dur.ac.uk (20GBit/s bonded). Alternatively, a GLOBUS ONLINE account can be used (which is associated with dataweb). Various other fast copy tools are available, such as bbcp (module load bbcp).

## Using rsync and scp

For small amounts of data, use `rsync` or `scp` from your own computer.  `rsync` is usually better, because it only copies what has changed, and can carry on if it is interrupted:

```
rsync -avP myresults/ USERNAME@login8.cosma.dur.ac.uk:/cosma8/data/PROJECT/USERNAME/myresults/
```

To copy data from COSMA, swap the two locations:

```
rsync -avP USERNAME@login8.cosma.dur.ac.uk:/cosma8/data/PROJECT/USERNAME/myresults/ myresults/
```

| Option | Meaning |
| ------ | ------- |
| `-a` | Copy directories, and keep times and permissions |
| `-v` | List the files |
| `-P` | Show progress, and keep partly copied files so that you can carry on later |
| `--dry-run` | Show what would be copied, without copying anything |
| `-c` | Compare files by checksum, which is slow but thorough |

A slash at the end of the source means the contents of that directory.  Without one, `rsync` makes a directory of that name inside the destination.

`scp` is simpler, and works well for a few files:

```
scp myfile.dat USERNAME@login8.cosma.dur.ac.uk:/cosma8/data/PROJECT/USERNAME/
```

Copying many small files is slow, so use `tar` to combine them first.  To check a copy, compare the output of `sha256sum` on each side, or run `rsync -avc --dry-run`, which should list no files.

Choose the login node for the file system that you are using.  If you are copying files over 1GB onto COSMA, see [rsync on Lustre](lustre.md#rsync).

## GLOBUS Online

To use GLOBUS, you first need to visit [globus.org](https://globus.org) and sign in. Here, don't select the organisation, but use a Globus ID. If you don't have an account, create one. Then, select cosma#dataweb as an end point. From there, you will be able to transfer your files. If you do not know your COSMA password, please email cosma-support@durham.ac.uk, to have it reset.

To transfer files, it is necessary to explicitly allow access to your directory of interest. Please contact cosma-support@durham.ac.uk to allow this.

## Using bbcp

bbcp is relatively straightforward to use, once it is understood.  Instructions are at [https://www.slac.stanford.edu/~abh/bbcp/](https://www.slac.stanford.edu/~abh/bbcp/)

Some examples are provided here, known to work on the date they were tested.

To transfer data from COSMA to Tursa (September 2024, from dataweb):

```
bbcp --port 50000 -z -n -A -T "ssh  tursa bin/bbcp" /cosma8/data/dp004/flamingo/Runs/L1000N1800/HYDRO_FIDUCIAL/lightcones/lightcone1_particles/* USER@tursa-login1.dirac.ed.ac.uk:./tmp/
```

This requires a copy of bbcp in your bin/ directory on Tursa - you may need to compile this from source.

This requires a ssh tunnel to be set up (since Tursa uses MFA).  To do this, add to your .ssh/config file (change USER, PROJECT and id_TURSA to the appropriate values):

```
Host tursa
     HostName tursa.dirac.ed.ac.uk
     User USER
     IdentityFile /cosma/home/PROJECT/USER/.ssh/id_TURSA
     ControlPath ~/.ssh/controlmasters/%r@%h:%p
     ControlMaster auto
     ControlPersist yes
```

and you should then `ssh tursa` to set up the connection.  After this, the above bbcp command will work.

The flags used are:

- `--port 50000` Use port 50000 (this is known to be open on dataweb)
- `-z` Do a reverse transfer (i.e. Tursa will connect to dataweb, necessary since we don't know which ports are open on Tursa, but have port 50000 open on dataweb)
- `-n` No DNS
- `-A` Make the destination directory (tmp/) if it does not exist
- `-T` Specify the command used to run bbcp on Tursa

Other useful arguments are
- `--recursive` which allows the source to be a directory.

Performance tuning:
- `-w 64k` Set the window size.  With simple testing, 64k seemed to give the best value.  5.5 gbit/s.  Default is 128k.
- `-s 8` Set the number of streams used.  32 seems to be a good number.  Default is 4.
- `-B 64m` Sets the buffer size.  Default is the window size.  Doesn't appear to make much difference, though large sizes may help, e.g. 64m.  6.7gbit/s.


# SSH access

You connect to COSMA with SSH, to one of its 6 login nodes:

| System | Login nodes | Shared name |
| ------ | ----------- | ----------- |
| COSMA5 | login5c | login5 |
| COSMA7 | login7a, login7b, login7c | login7 |
| COSMA8 | login8a, login8b | login8 |

The full name of each is `NAME.cosma.dur.ac.uk`, for example
`login8b.cosma.dur.ac.uk`.  A shared name such as `login8` picks one of that
system's login nodes for you.

The login nodes are also the development nodes: they have the compilers, the
[modules](modules.md) and the batch system, so do your interactive work,
compiling and job submission there.  You can submit jobs to any
[batch queue](slurm.md) from any login node.  Login nodes are not the same as
the compute nodes that run your jobs, though: see
[the COSMA5 login node and compute nodes](facilities.md#the-cosma5-login-node-and-compute-nodes-are-different)
for an example, and [mounted file systems](storage.md#mounted-filesystems) for
which file systems each node can see.

## What you need

- **An SSH key pair.**  See [generating an SSH key](sshkey.md).  In short, run
  `ssh-keygen -t ed25519` on your own computer and give it a strong
  passphrase.  Upload the public part (the `.pub` file) to
  [SAFE](https://safe.epcc.ed.ac.uk/dirac).  One key works on every login
  node, and you can use the same key for other services such as GitHub.
- **Your COSMA password.**  The first one is in your welcome email.  It is
  separate from your key passphrase, and should be different from it.

## Logging in

From a terminal on your own computer:

```
ssh USER@login8b.cosma.dur.ac.uk
```

where `USER` is your COSMA username.  If your key is not in the default place,
give its path with `-i`:

```
ssh -i ~/.ssh/my_cosma_key USER@login8b.cosma.dur.ac.uk
```

SSH asks for your key passphrase, and then for your COSMA password.  To avoid
typing these every time, see
[storing your key passphrase](#storing-your-key-passphrase) and
[reusing SSH connections](#reusing-ssh-connections).

The first time you connect to each login node, SSH shows that node's
fingerprint and asks whether to trust it.  Each login node has its own
fingerprint, so you are asked once for each node.  If SSH later warns that a
fingerprint has *changed*, do not log in: contact cosma-support.

### Logging in for the first time

The first time you log in, or after a password reset, you must choose a new
password:

1. Enter the password from your email to log in.
2. Enter it again, when asked for your current password.
3. Enter your new password twice.

Use at least 16 characters, with at least three of: lower case letters, upper
case letters, digits and symbols.  Several words strung together work well.

## Saving SSH configuration

Rather than typing the full command every time, you can save your settings in
`~/.ssh/config` on your own computer (not on COSMA).  Each `Host` block gives a
short name to a login node, and `ssh NAME` then uses all the settings in that
block.  For example, with:

    Host cosma8
     User USER
     HostName login8.cosma.dur.ac.uk
     IdentityFile ~/.ssh/id_ed25519

typing

`ssh cosma8`

is the same as

`ssh -i ~/.ssh/id_ed25519 USER@login8.cosma.dur.ac.uk`

The name also works with other programs that use SSH, such as `scp`, `rsync`,
`sftp`, `sshfs`, git and the VS Code Remote-SSH extension, so `scp file.txt
cosma8:` copies a file to your home directory.

### A complete example

This example sets up every COSMA login node, with the options most people find
useful.  Replace `USER` with your COSMA username, and `~/.ssh/id_ed25519` with
the path to your private key.

```
# Short names for one login node on each system
Host cosma5
    HostName login5c.cosma.dur.ac.uk
Host cosma7
    HostName login7a.cosma.dur.ac.uk
Host cosma8
    HostName login8b.cosma.dur.ac.uk

# Every login node by its own name
Host login5c login7a login7b login7c login8a login8b
    HostName %h.cosma.dur.ac.uk

# Settings shared by all of the names above
Host cosma5 cosma7 cosma8 login5c login7a login7b login7c login8a login8b
    User USER
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    # Share one connection between all your sessions to each node
    ControlMaster auto
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlPersist 8h
    # Stop idle connections being dropped
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

Then create the directory for the shared connections:

```
mkdir -p ~/.ssh/controlmasters
chmod 700 ~/.ssh ~/.ssh/controlmasters
```

and log in with, for example, `ssh login8a` or `ssh cosma8`.

What each option does:

| Option | What it does |
| ------ | ------------ |
| `Host` | The names you type after `ssh`.  One block can cover several names, and `%h` in the block stands for the name you typed. |
| `HostName` | The real address to connect to. |
| `User` | Your COSMA username, so you can leave out `USER@`. |
| `IdentityFile` | The private key to use. |
| `IdentitiesOnly yes` | Only offer that key.  Without it, SSH also tries every key in your agent, and too many failed keys can get you refused before your password is asked for. |
| `ControlMaster`, `ControlPath`, `ControlPersist` | Reuse one connection for every session to that node.  See [Reusing SSH connections](#reusing-ssh-connections). |
| `ServerAliveInterval 30`, `ServerAliveCountMax 3` | Check every 30 seconds that the connection is still alive, and give up after 3 missed replies.  This stops home routers and firewalls closing a connection that has been idle for a while, and makes a dead connection fail after about 90 seconds rather than freezing. |
| `ForwardX11 yes` | The same as `ssh -X`: lets graphical programs show on your screen.  See [running programs with a graphical interface](#running-programs-with-a-graphical-interface). |

SSH uses the first value it finds for each option, so put the more specific
`Host` blocks above general ones such as `Host *`.  To see the settings SSH will
actually use for a name, run `ssh -G cosma8`.

To learn about more options, see the manual: `man 5 ssh_config`.

### Pick a fixed login node

The names `login5`, `login7` and `login8` pick one of several login nodes for
you.  It is better to choose a specific node, such as `login8b`, in your
config:

- Shared connections (below) only help if you land on the same node each time.
- Each login node has its own host key, so a name that moves between nodes
  can give you host key warnings.
- Programs running in `screen` or `tmux` are on one particular node, so you
  need to get back to that node to find them.

## Reusing SSH connections

Each new SSH connection to COSMA asks for your password (and second factor, if
you are asked for one).  With connection sharing, the first connection to a
node stays open, and every later `ssh`, `scp`, `rsync` or VS Code connection to
that node goes through it without logging in again.  The three options in the
example above turn this on:

- `ControlMaster auto` uses an open connection if there is one, and otherwise
  opens a new one that later connections can share.
- `ControlPath` is where SSH keeps the shared connection.  `%r@%h:%p` gives
  each user, node and port its own file.  The directory must exist.  Because
  `%h` is the real host name, `cosma8` and `login8b` in the example above share
  one connection.
- `ControlPersist 8h` keeps the shared connection open for 8 hours after you
  close your last session.  `ControlPersist yes` keeps it open until it is
  stopped, and `ControlPersist no` closes it with your first session.

Useful commands:

```
ssh -O check cosma8    # is there a shared connection?
ssh -O exit cosma8     # close it
```

If a shared connection freezes, for example after your laptop has been asleep
or changed network, `ssh -O exit NAME` closes it so that the next `ssh` logs in
again.  If that also hangs, delete the file in `~/.ssh/controlmasters`.

COSMA limits the number of sessions on a single connection to about 10.  If
you have many terminals or tools open on one node, a new one may be refused
and SSH then logs in again from scratch.  Spread your sessions over more than
one login node if you hit this.

## Reaching other nodes through a login node

Most COSMA machines can only be reached from inside COSMA.  Their internal
names end in `.pri.cosma.local` (for example `mad12.pri.cosma.local`), and only
work from a login node.  To connect to one from your own computer in a single
step, use `ProxyJump` to go through a login node:

```
Host mad12
    HostName mad12.pri.cosma.local
    User USER
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump login8b
```

`ssh mad12` then logs in to `login8b` first (reusing its shared connection if
there is one), and from there connects to `mad12`.  The same works on the
command line: `ssh -J login8b USER@mad12.pri.cosma.local`.

This is for nodes you are allowed to log in to directly, such as the
[hardware lab](hardwarelab.md) systems during their interactive hours.  The
compute nodes in the batch queues do not accept SSH logins: use
[Slurm](slurm.md) to run work on them.

## Forwarding ports

SSH can forward a port on your computer to a port on COSMA, which is how you
reach web services such as [Jupyter](jupyter.md) running on COSMA.  On the
command line this is `-L`, and in your config it is `LocalForward`.  For
example, to reach the Jupyter service on `login8b` at
[https://localhost:8443](https://localhost:8443):

```
Host cosma8-jupyter
    HostName login8b.cosma.dur.ac.uk
    User USER
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 8443 localhost:443
```

`ssh -N cosma8-jupyter` opens the tunnel without starting a shell.  Keep it
running while you use the service.

If port 8443 is already in use on your computer, pick another free port, and
change both the config and the address in your browser.  Forwarded ports are
set up when a connection is first opened, so a `LocalForward` on a host that is
already sharing a connection only takes effect after `ssh -O exit`.

## Storing your key passphrase

An SSH agent remembers your key's passphrase after you first type it, until
you log out of your computer.

- **Linux:** most desktops start an agent for you.  Add this at the bottom of
  your `~/.ssh/config` (after your specific `Host` blocks) so it applies to
  every host:

  ```
  Host *
      AddKeysToAgent yes
  ```

  The first `ssh` then asks for your passphrase once and stores the key.  You
  can also add it yourself with `ssh-add ~/.ssh/id_ed25519`, and list stored
  keys with `ssh-add -l`.
- **macOS:** add `UseKeychain yes` as well as `AddKeysToAgent yes`, and macOS
  keeps the passphrase in your keychain between restarts.
- **Windows:** start the agent once from an administrator PowerShell with
  `Get-Service ssh-agent | Set-Service -StartupType Automatic; Start-Service ssh-agent`,
  then run `ssh-add`.

If you have no agent, `keychain` can start one for you: install it, and add
`eval $(keychain --eval ~/.ssh/id_ed25519 2> /dev/null)` to the `~/.bashrc` on
your own computer.

## Running programs with a graphical interface

For a full graphical desktop on COSMA, [x2go](x2go.md) is the recommended
way: it is much more responsive than the method below.

To show single windows, such as a plot from Python, a PDF in `evince`, a
picture in `eog` or an HDF5 file in `hdfview`, log in with X11 forwarding:

```
ssh -X USER@login8b.cosma.dur.ac.uk
```

or add `ForwardX11 yes` to your config.  Then, for example, `eog picture.png`
on COSMA opens the picture on your screen.  This works on most Linux systems.
On macOS, install [XQuartz](https://www.xquartz.org) first.  On Windows 11,
WSL shows Linux windows itself.

## SSH on Windows

Windows 10 and 11 include OpenSSH, so `ssh`, `scp` and `ssh-keygen` work in
PowerShell or the command prompt (see [generating an SSH key](sshkey.md)).
Your config file is `C:\Users\YOURNAME\.ssh\config`, and uses the same format
as above.

Windows OpenSSH does not support connection sharing (`ControlMaster`), so
leave those three lines out there.  To use connection sharing, use SSH from
WSL (Windows Subsystem for Linux), which works the same way as on Linux.

## Forgotten passphrase or password

Both are fixed on [SAFE](https://safe.epcc.ed.ac.uk/dirac).  If you cannot log
in to SAFE itself, contact SAFE support at dirac-support@epcc.ed.ac.uk.

- **Forgotten key passphrase:** a passphrase cannot be recovered.
  [Generate a new key](sshkey.md), then on SAFE select "Login accounts", then
  your COSMA account, and click "Add credential" to upload the new public key.
  Wait for cosma-support to accept it.
- **Forgotten COSMA password:** on the same SAFE page, click "Request Password
  Reset".  A new password is emailed to you once cosma-support has processed
  the request.  Log in with it and choose a new password, as in
  [logging in for the first time](#logging-in-for-the-first-time).

## Cannot get access?

If you get `Permission denied`, check these in turn:

1. **Wrong key.**  Make sure SSH is using the key you uploaded to SAFE: use
   `ssh -i /path/to/key`, or `IdentityFile` in your config.
   `ssh -v USER@login8b.cosma.dur.ac.uk` shows which keys are tried.
2. **Key not yet accepted.**  A new key uploaded to SAFE has to be accepted by
   cosma-support before it works.
3. **Key file permissions.**  SSH ignores a private key that other users can
   read.  Run `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/id_ed25519`.
4. **Old key type.**  Some old key types are no longer accepted.
   [Generate an ed25519 key](sshkey.md) and upload it to SAFE.
5. **First login.**  Follow [logging in for the first time](#logging-in-for-the-first-time)
   carefully: you need to enter the emailed password twice.
6. **Forgotten passphrase or password.**  See
   [above](#forgotten-passphrase-or-password).
7. **Too many failed attempts.**  After several wrong passwords, your address is
   blocked, usually for about 15 minutes.  Wait, or try another login node.
   After many failed attempts the block can be longer: contact cosma-support
   to have it removed.

For anything else, contact cosma-support.

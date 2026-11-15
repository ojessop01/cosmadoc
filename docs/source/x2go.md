# Graphical access

Most work on COSMA is done at the command line, but sometimes you need a
graphical program: a plot viewer, a debugger such as DDT, a visualisation
tool such as ParaView, or a file browser.  There are three ways to do this:

| Method | Best for | Set-up |
| ------ | -------- | ------ |
| [x2go](#x2go) | A full desktop on COSMA, or using graphical programs for a long time | Install the x2go client once |
| [X11 forwarding](ssh.md#running-programs-with-a-graphical-interface) | Opening the odd window, such as a quick plot | Log in with `ssh -X` |
| [VNC](#vnc) | Only if x2go does not work for you | More complicated |

x2go is the recommended way.  It is much more responsive than X11 forwarding
over a slow connection, and if your connection drops, the desktop keeps
running and you can reconnect to it.

## x2go

x2go gives you a graphical desktop (Xfce) running on a COSMA login node, in a
window on your own computer.  The x2go server is installed on every login
node.

### Installing the client

Install the x2go client on your own computer:

- **Linux:** from your distribution's packages, usually called `x2goclient`.
- **macOS and Windows:** download it from the
  [x2go website](https://wiki.x2go.org/doku.php/download:start).  On macOS you
  also need [XQuartz](https://www.xquartz.org).

### Setting up a session

Start the x2go client and create a new session with these settings:

| Setting | Value |
| ------- | ----- |
| Session name | Anything you like, such as `cosma8` |
| Host | A specific login node, such as `login8b.cosma.dur.ac.uk` or `login5c.cosma.dur.ac.uk` |
| Login | Your COSMA username |
| SSH port | 22 |
| Use RSA/DSA key for ssh connection | The private SSH key you uploaded to SAFE, such as `~/.ssh/id_ed25519` |
| Session type | `XFCE` |

Use a specific login node, not `login8` or `login7`, so that you return to the
same node, and the same desktop, each time.

![x2go session settings](./images/x2gosetup.png)

You may need to untick **Try auto login (via SSH Agent or default SSH key)**.
If logging in works with it ticked, leave it ticked.

Save the session, then click it to connect.  You will be asked for your key
passphrase and your COSMA password, and then the desktop opens.  The first
connection can take a little while.

### Disconnecting and reconnecting

- **Suspend** the session (the pause button in the x2go client, or closing the
  window and choosing to suspend) to leave your programs running.  Connect
  again later to carry on where you left off.
- **Log out** from the desktop's menu when you have finished, so that your
  programs do not keep running on the shared login node.

Like everything on a login node, a suspended session is lost if that login node
is restarted, for example during the scheduled downtimes listed on the
[front page](index.rst).

### If x2go does not work

- **The login fails or the desktop never appears.**  An error in your
  `~/.bashrc`, such as loading a module that does not exist or a command that
  waits for input, can stop the desktop starting.  Try commenting out recent
  changes to `~/.bashrc`, and make sure it prints nothing in non-interactive
  shells.
- **Windows are not redrawn properly when moved.**  Turn off compositing: run
  `xfwm4-tweaks-settings` (or open Applications, Settings, Window Manager
  Tweaks), go to the Compositor tab, and untick compositing.
- **The screen locks and asks for a password.**  Turn off the screen lock in
  Applications, Settings, Xfce Screensaver, Lock Screen.
- **It is slow.**  In the session settings, under Connection, choose a lower
  connection speed or a different compression method.

## X11 forwarding

For opening a single window, such as a plot or a PDF, log in with
`ssh -X` and start the program from the command line.  See
[running programs with a graphical interface](ssh.md#running-programs-with-a-graphical-interface).

## VNC

```{note}
On Rocky Linux 9, `vncserver` is an older command kept for compatibility: it
prints a warning that it "has been replaced by a systemd unit and is now
considered deprecated".  The steps below may not work.  Use x2go if you can,
and contact cosma-support if you need VNC.
```

VNC also gives a remote desktop.  The usual steps are:

1. On a login node, set a VNC password with `vncpasswd`, then start a server
   with a display number `N` (try 1, and a higher number if it is in use):

   ```
   vncserver :N
   ```

2. On your own computer, forward VNC's port (5900 plus `N`) through SSH, and
   connect a VNC viewer to it.  For example, for display 2 on login7a:

   ```
   ssh -N -L 5900:localhost:5902 USER@login7a.cosma.dur.ac.uk
   vncviewer localhost:5900
   ```

3. When you have finished, stop the server on the login node with
   `vncserver -kill :N`, so that it does not keep running.

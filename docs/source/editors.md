# Editing code on COSMA

You can edit files on COSMA in two ways:

- **In a terminal on COSMA**, with an editor such as nano, Vim or Emacs.  This
  works from any computer with SSH, needs nothing installed, and is quick for
  small changes.
- **In an editor on your own computer** that works on COSMA's files over SSH,
  such as [VS Code](vscode.md).  This gives you a familiar graphical editor,
  with the files and the terminal on COSMA.

There is no single right choice.  Many people use both: VS Code for writing
code, and a terminal editor for quick changes to job scripts and settings.

## Terminal editors

All of these are installed on every login node.

| Editor | Command | Good for | Learning curve |
| ------ | ------- | -------- | -------------- |
| [nano](nano.md) | `nano FILE` | Quick edits, if you are new to terminal editors | Gentle: the main commands are shown at the bottom of the screen |
| [Vim](vi.md) | `vim FILE` | Fast editing once learned; available on almost every Unix system | Steep at first |
| [Emacs](emacs.md) | `emacs -nw FILE` | A complete, highly customisable environment, with modes for most languages | Moderate |
| [ed](ed.md) | `ed FILE` | Editing by commands, line by line, in scripts | Only for the curious |

If you are not sure, start with nano.  If you will spend a lot of time on
COSMA, it is worth learning Vim or Emacs.

### Setting your default editor

Some programs, such as `git commit` and `crontab -e`, open an editor for you.
Choose which one by adding a line to your `~/.bashrc`:

```
export EDITOR=nano       # or vim, or "emacs -nw"
```

## Editors on your own computer

- **[VS Code](vscode.md)** with the Remote-SSH extension opens folders on COSMA
  as if they were local, with a terminal on COSMA built in.
- **Other editors**, such as JetBrains IDEs or Sublime Text, have similar
  remote features or plugins.
- **Mounting COSMA's files** on your computer with `sshfs` lets any local
  editor open them, but every file access goes over the network, so it can be
  slow with large folders.

Whichever you use, the programs you run still run on COSMA, so the
[good citizenship](citizenship.md) rules for login nodes apply.

## Graphical editors on COSMA

Graphical editors such as `gedit`, and the graphical version of Emacs, also
run on COSMA, and show on your screen through [x2go](x2go.md) or X11
forwarding.  Over a slow connection this is much less responsive than a
terminal editor or VS Code.

## Keeping your session

[tmux](tmux.md) lets you keep terminal sessions running on COSMA after you
disconnect, and split one terminal into several, for example an editor in one
pane and a shell in another.

## Tips

- Many terminal editors can have several files open at once (buffers), so you
  do not need a new terminal for each file.
- Most editors can show line numbers, which helps when an error message refers
  to a line: in Vim `:set number`, in nano `Alt-#` (or start it with
  `nano -l`), and in Emacs `M-x display-line-numbers-mode`.
- Keep your own configuration files (`~/.vimrc`, `~/.emacs.d/`, `~/.nanorc`)
  small, as they live in your home directory.

```{toctree}
:hidden:

nano
vi
emacs
ed
tmux
```

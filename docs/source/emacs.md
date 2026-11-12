# Emacs

Emacs is a powerful, highly customisable editor with modes for almost every
programming language.  Version 27 is installed on the login nodes.

To edit a file in the terminal:

```
emacs -nw myscript.sh
```

`-nw` ("no window") runs Emacs in the terminal.  Without it, Emacs opens a
graphical window if it can (through [x2go](x2go.md) or X11 forwarding), which
is slower over a network.

## The commands to know first

In Emacs's notation, `C-` means the Ctrl key and `M-` means the Alt (Meta)
key.  `C-x C-s` means Ctrl-X followed by Ctrl-S.

| Keys | What it does |
| ---- | ------------ |
| `C-x C-s` | Save |
| `C-x C-c` | Quit |
| `C-x C-f` | Open a file |
| `C-x b` | Switch to another open file (buffer) |
| `C-g` | Cancel the current command |
| `C-/` | Undo |
| `C-s` | Search forward |
| `M-%` | Search and replace |
| `C-k` | Cut to the end of the line |
| `C-y` | Paste |
| `M-g g` | Go to a line number |
| `C-x 2`, `C-x 3`, `C-x 1` | Split the window, side by side, or back to one |

If you get stuck in a command, press `C-g` until it stops.

## Learning more

Press `C-h t` in Emacs for the built-in tutorial.  The
[Emacs reference card](https://www.gnu.org/software/emacs/refcards/pdf/refcard.pdf)
lists the common commands.  Your settings go in `~/.emacs.d/init.el`.

# nano

nano is a simple terminal editor, and the easiest one to start with.  Its main
commands are always shown at the bottom of the screen.

To edit a file:

```
nano myscript.sh
```

In nano's help, `^` means the Ctrl key and `M-` means the Alt key, so `^O`
means Ctrl-O.

| Keys | What it does |
| ---- | ------------ |
| `Ctrl-O`, then Enter | Save the file |
| `Ctrl-X` | Exit (it asks whether to save any changes) |
| `Ctrl-W` | Search |
| `Ctrl-\` | Search and replace |
| `Ctrl-K` | Cut the current line |
| `Ctrl-U` | Paste |
| `Ctrl-_`, then a number | Go to a line number |
| `Alt-U` | Undo |
| `Alt-#` | Show or hide line numbers |
| `Ctrl-G` | Help |

Start nano with `nano -l FILE` to show line numbers from the start.  Settings
such as this can be kept in `~/.nanorc`, for example `set linenumbers`.

nano is fine for job scripts and small changes.  For larger programs, a more
powerful editor such as [Vim](vi.md), [Emacs](emacs.md) or [VS Code](vscode.md)
is worth learning.

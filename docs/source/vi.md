# Vim (vi)

Vim is a powerful terminal editor, and an improved version of `vi`, which is
found on almost every Unix system.  It is fast once learned, but works
differently from most editors, which confuses many new users at first.

To edit a file:

```
vim myscript.sh
```

## Modes

Vim has modes.  When it starts, it is in **normal mode**, where keys are
commands, not text.

- Press `i` to go into **insert mode** and type text.
- Press `Esc` to go back to normal mode.
- In normal mode, type `:` followed by a command and Enter, for commands such
  as saving.

If Vim seems to do strange things when you type, press `Esc` and start again
from normal mode.

## The commands to know first

| Keys (in normal mode) | What it does |
| --------------------- | ------------ |
| `i` | Start typing (insert mode); `Esc` to stop |
| `:w` | Save |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Quit without saving |
| `u` | Undo |
| `Ctrl-R` | Redo |
| `dd` | Cut the current line |
| `yy` | Copy the current line |
| `p` | Paste after the cursor |
| `/text` | Search for `text`; `n` for the next match |
| `:%s/old/new/g` | Replace every `old` with `new` |
| `:42` | Go to line 42 |
| `:set number` | Show line numbers |

## Learning more

Run `vimtutor` on COSMA for a 30-minute interactive lesson, which is the best
way to learn the basics.  Settings, such as always showing line numbers
(`set number`), go in `~/.vimrc`.

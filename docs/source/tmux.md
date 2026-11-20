# tmux (terminal multiplexer)

`tmux` is a terminal multiplexer.  It lets you keep sessions running on COSMA
after you disconnect, and split one terminal into several panes or windows.

## Managing sessions

```
tmux new -s work          # start a named session
tmux ls                   # list running sessions
tmux attach -t work       # reattach after reconnecting
tmux kill-session -t work # end a session
```

## Keybindings inside tmux

All `tmux` commands start with the prefix key **`Ctrl-b`**, followed by a second key:

| Keys | Action |
| ---- | ------ |
| `Ctrl-b d` | Detach from the session (leaves it running) |
| `Ctrl-b %` | Split pane vertically (left/right) |
| `Ctrl-b "` | Split pane horizontally (top/bottom) |
| `Ctrl-b` + arrow key | Move between panes |
| `Ctrl-b c` | Create a new window |
| `Ctrl-b n` / `Ctrl-b p` | Next / previous window |
| `Ctrl-b [` | Enter scroll/copy mode (use arrow keys or `PgUp`/`PgDn`; press `q` to leave) |

## Notes for COSMA

- Sessions live on the specific login node where you started them.  Log in to a
  [fixed login node](ssh.md#pick-a-fixed-login-node) (such as `login8b` rather
  than `login8`) and check `hostname` before reattaching.
- Login nodes are rebooted periodically, which stops `tmux` sessions.
- Do not leave heavy computation running inside `tmux` on a login node: submit
  a [Slurm job](slurm.md) instead (see [good citizenship](citizenship.md)).

See the [tmux cheat sheet](https://tmuxcheatsheet.com) for more shortcuts.

# AI coding agents

AI coding agents are programs that read your files, run commands and edit
code for you, using a large language model.  Examples are Claude Code, OpenAI
Codex, Gemini CLI, GitHub Copilot, Cursor and Google Antigravity.  They can
save a lot of time on COSMA, but they act with *your* account: every file they
delete, every job they submit and every login they attempt is done as you.

This section explains how to set them up and use them on COSMA well, without
causing problems for yourself or for other users.  Most of the problems it
describes have happened to COSMA users.

```{important}
**You are responsible for everything an agent does with your account**, in
exactly the same way as if you had typed the commands yourself.  COSMA's
[good citizenship guide](citizenship.md) and [policies](policies.md) apply in
full.  If you are unsure whether an agent should do something, stop it and ask
cosma-support.
```

This section of the documentation has several pages:

| Page | What it covers |
| ---- | -------------- |
| [Setting up agents](agents-setup.md) | Where agents can run, installing them in app space, their folders and accounts, instructions files, and your shell setup. |
| [What agents are good for](agents-uses.md) | The kinds of work where agents save the most time on COSMA, with examples. |
| [Writing code with agents](agents-coding.md) | Bash scripts, Python, job scripts, tests, documentation, porting code to another language, and code that breaks on COSMA. |
| [Optimising code with agents](agents-optimisation.md) | Timing fairly, profiling tools on COSMA, compiled code, OpenMP, MPI, GPUs, Python and file I/O. |
| [Writing good requests](agents-prompts.md) | General guidelines for asking an agent for work: what to include, how to break up tasks, reviews, follow-ups, and common mistakes. |
| [Using agents safely](agents-safe.md) | Temporary files, fair use of login nodes and file systems, Slurm, SSH, data, approvals, checking the agent's work, and troubleshooting. |

## The COSMA rules for agents

COSMA staff have written a set of rules for AI agents, in
`/etc/claude-code/AGENTS.md` on every login node.  **Read it before using an
agent, and make sure your agent reads it too** (see
[giving the agent the rules](agents-setup.md#giving-the-agent-the-rules)).  Its main points
are:

- Never get around a limit, block, permission, quota or queue.  If something
  is blocked, the agent should stop and tell you.
- Never turn off an agent's sandbox or approval prompts, for example with
  `--dangerously-bypass-approvals-and-sandbox` or a similar option.
- Never delete, move or overwrite files without asking you first.
- Never use `sudo`, and never change permissions with `chmod`, `chown` or
  `setfacl` unless you asked for exactly that.
- Never submit or cancel Slurm jobs unless you asked for that specific job, in
  your own words, and agreed to the exact `sbatch` command.  Read-only
  commands such as `squeue --me` and `sacct -j JOBID` are fine.
- Only search inside your own directories.  No `find`, `grep -r` or `du` over a
  whole shared file system.
- Keep login node use small: no more than about 30 cores on a COSMA8 login
  node, or 14 cores on a COSMA5 or COSMA7 login node, and no more than about
  300GB of memory per login node.
- No repeated SSH attempts or retry loops, because failed logins can get your
  address blocked.
- Limit the size of error output from long commands, for example with
  `2>&1 | tail -n 200`.  An uncapped error file once grew to 851GB.
- Keep large temporary files (over 1GB), job output and logs out of `/tmp` on
  the login nodes and out of your home directory.
- Do not create, remove or change conda environments, and never run
  `conda clean` or `conda init`.
- Never read, print or copy keys, tokens or passwords.

The rest of this page explains how to set things up so that following these
rules is easy, and what goes wrong when they are not followed.

## Quick start

1. Read the COSMA rules above, and `/etc/claude-code/AGENTS.md` itself.
2. Install the agent in your app space, not your home directory (see [installing agents](agents-setup.md#installing-agents)).
3. Move the agent's own folder to app space (see [moving the agents' folders](agents-setup.md#move-the-agents-own-folders-out-of-your-home-directory)).
4. Set `TMPDIR` to a folder in your app space (see [temporary files](agents-safe.md#temporary-files)).
5. Give the agent the rules and the COSMA facts in its instructions file (see [the starting template](agents-setup.md#a-starting-template)).
6. Start the agent in your project folder, keep its approval prompts on, and check its work (see [using agents safely](agents-safe.md)).

# AI coding agents

AI coding agents are programs that read your files, run commands and edit
code for you, using a large language model.  Examples are Claude Code, OpenAI
Codex, Gemini CLI, GitHub Copilot, Cursor and Google Antigravity.  They can
save a lot of time on COSMA, but they act with *your* account: every file they
delete, every job they submit and every login they attempt is done as you.

This page explains how to set them up and use them on COSMA without causing
problems for yourself or for other users.  Most of the problems described
here have happened to COSMA users.

```{important}
**You are responsible for everything an agent does with your account**, in
exactly the same way as if you had typed the commands yourself.  COSMA's
[good citizenship guide](citizenship.md) and [policies](policies.md) apply in
full.  If you are unsure whether an agent should do something, stop it and ask
cosma-support.
```

## The COSMA rules for agents

COSMA staff have written a set of rules for AI agents, in
`/etc/claude-code/AGENTS.md` on every login node.  **Read it before using an
agent, and make sure your agent reads it too** (see
[giving the agent the rules](#giving-the-agent-the-rules)).  Its main points
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

## Where agents can run

### On a login node

Command-line agents (Claude Code, Codex, Gemini CLI and others) run well on
the login nodes.  The login nodes can reach the internet, which the agent
needs to talk to its model.

The login nodes are shared by everyone, and there is no automatic limit on how
much CPU or memory one person can use on them.  Keep within the limits in the
rules above, and see [using the login nodes fairly](#using-the-login-nodes-fairly).

### Not in batch jobs

The compute nodes cannot reach the internet, so an agent that uses an online
model cannot run inside a batch job.  Instead, the agent prepares a job
script, and you submit it (see [Slurm and agents](#slurm-and-agents)).

### From your own computer

Editor-based agents, such as VS Code with Copilot or another agent extension,
Cursor and Antigravity, run on your own computer and work on COSMA over SSH,
in the same way as [VS Code](vscode.md).  For these:

- Set up [connection sharing](ssh.md#reusing-ssh-connections), so the editor
  and agent reuse one login instead of asking for your password each time.
- Connect to a fixed login node, such as `login8b`, rather than `login8`.
- The rules on this page still apply, because the commands the agent runs
  still run on COSMA as you.

### On the hardware lab nodes

Some [hardware lab](hardwarelab.md) systems can be reached by SSH only at
certain times of day, and are used through Slurm at other times.  Check the
access times before pointing an agent at one, and make sure it does not keep
trying to log in when access is closed.

## Installing agents

### Install in /cosma/apps, not your home directory

Install agents, and everything they download, in your
[app space](storage.md#app-space) (`/cosma/apps/PROJECT/USER`), not in your
home directory (`/cosma/home/PROJECT/USER`).

Your home directory has a quota of about 10GB, and agents are larger than
they look.  Installing Claude Code, Codex and Gemini CLI together takes about
1.2GB: 862MB for the programs, plus 366MB of download cache.  Each agent then
also keeps settings, logs and conversation histories, which grow with use.
App space has a 100GB quota and is meant for software like this.

### Command-line agents that use Node.js

Claude Code, Codex and Gemini CLI are installed with `npm`, which comes with
Node.js.  Load the Node.js module first: it is available on every login node,
whereas the system copy of Node.js is not.

1. Set up `npm` to install into your app space.  You only need to do this
   once:

   ```
   module load nodejs/24.18.1
   mkdir -p /cosma/apps/PROJECT/USER/npm /cosma/apps/PROJECT/USER/npm-cache
   npm config set prefix /cosma/apps/PROJECT/USER/npm
   npm config set cache /cosma/apps/PROJECT/USER/npm-cache
   ```

   These settings are saved in `~/.npmrc`, so later `npm` commands use them.

2. Add the programs to your `PATH`, by adding these lines to `~/.bashrc`:

   ```
   module load nodejs/24.18.1
   export PATH=/cosma/apps/PROJECT/USER/npm/bin:$PATH
   ```

3. Install the agents you want:

   ```
   npm install -g @anthropic-ai/claude-code    # Claude Code: the claude command
   npm install -g @openai/codex                # Codex: the codex command
   npm install -g @google/gemini-cli           # Gemini CLI: the gemini command
   ```

4. Check that they work, for example with `claude --version`.

To update an agent later, run the same `npm install -g` command again.

### Agents that use Python

For agents installed with `pip`, make a Python virtual environment in your
app space, as described on the [Python](python.md) page, and install the agent
into it.  Do not install agents into a conda environment that a project
depends on.

### When an install or update goes wrong

App space is an NFS file system, and an install that is interrupted part way
through (a dropped connection, a full quota, or two updates at once) can leave
the agent broken.  Typical signs are a `command not found` or
`Cannot find module` error for an agent that used to work, empty package
folders under `npm/lib/node_modules`, a half-downloaded folder with a name
such as `.codex-XXXXXXXX`, and `.nfs` files that cannot be deleted.

The `.nfs` files are files that were deleted while a program still had them
open.  They disappear when that program stops.  They are usually held by old
copies of the agent, or of its plugins, that are still running in the
background.  To repair the install:

1. Close all your sessions of that agent, on every login node you use.
2. Look for copies still running, and stop them by process ID (PID):

   ```
   ps -u $USER -o pid,lstart,cmd | grep -i codex
   kill PID
   ```

3. Check what is in the broken folder, then delete it yourself, for example
   `/cosma/apps/PROJECT/USER/npm/lib/node_modules/@openai/codex`.
4. Install the agent again with `npm install -g`.

Some agents update themselves automatically when they start.  If you run
several sessions at once, they can try to update at the same time and break
each other.  If this happens, turn automatic updates off in the agent's
settings and update by hand when no sessions are running.

### Move the agents' own folders out of your home directory

Agents keep their settings, logs and histories in hidden folders in your home
directory.  On COSMA, `~/.cache` and `~/.config` already point to your app
space, but these do not:

| Folder | Used by |
| ------ | ------- |
| `~/.claude` | Claude Code |
| `~/.codex` | Codex |
| `~/.gemini` | Gemini CLI and Antigravity |
| `~/.npm` | npm: its logs, and its cache if you did not set `cache` above |
| `~/.vscode-server`, `~/.cursor-server` | VS Code and Cursor over SSH |

Most agents create their folder the first time you run them, even just to ask
for `--version`.  Move each one to your app space and leave a link in its
place.  Do this while the agent is not running.  For example, for Claude
Code:

```
mkdir -p /cosma/apps/PROJECT/USER/dotfiles
mv ~/.claude /cosma/apps/PROJECT/USER/dotfiles/claude
ln -s /cosma/apps/PROJECT/USER/dotfiles/claude ~/.claude
```

If the folder does not exist yet, make the empty folder in app space and
create the link before you first run the agent.

To see what is using your home quota, run `du -sh ~/.[!.]* | sort -h`.

### One folder for each account

Each agent folder holds the account you are logged in with.  If you use two
accounts with the same agent (for example a personal and a group
subscription), do not let them share one folder: logging in with one
overwrites the other's login.  Give each account its own folder, and choose
which one to use when you start the agent.  Claude Code reads the folder from
the `CLAUDE_CONFIG_DIR` variable, and Codex from `CODEX_HOME`:

```
CLAUDE_CONFIG_DIR=/cosma/apps/PROJECT/USER/dotfiles/claude-group claude
```

## Temporary files

Agents create a lot of temporary files, and often do not delete them.
Claude Code, for example, keeps a folder of temporary files for each session
(command output, scripts it writes, diffs) and leaves it behind when the
session ends.  One user's folder of these grew to 206MB, in over 100
sub-folders, half of them more than a week old, and there was another 80MB in
`/tmp` on one login node.  Plugins and other tools add more.  Some agents
also keep temporary files inside their own folder in your home directory:
Codex, for example, uses `~/.codex/tmp`, which is another reason to
[move that folder](#move-the-agents-own-folders-out-of-your-home-directory).

This matters most for `/tmp` on the login nodes:

- **It is shared.**  Everyone on that login node uses the same `/tmp`, and
  there is no per-user quota, so one person can fill it for everyone.
- **It is stored in memory.**  `/tmp` on the login nodes is a `tmpfs`, so
  every file in it uses the node's RAM until it is deleted.
- **It cannot run programs** (it is mounted `noexec`), so tools that unpack
  and run code there fail.

`/dev/shm` is also stored in memory and shared.  Programs that use shared
memory, such as some Python analysis packages and Jupyter kernels, can leave
large files there when they crash or are killed: in one case 82GB, which
stayed in the node's memory until it was found and deleted.

See [temporary space](storage.md#temporary-space) for more on `/tmp` and
`/dev/shm`.

### Send temporary files to your own space

Most agents, like most programs, put temporary files wherever the `TMPDIR`
variable points.  Set it to a folder in your app space, in `~/.bashrc`:

```
mkdir -p /cosma/apps/PROJECT/USER/tmp
export TMPDIR=/cosma/apps/PROJECT/USER/tmp
```

`TMPDIR` is also passed on to batch jobs, where it can cause problems (see
[code that breaks on COSMA](#code-that-breaks-on-cosma)).  In a job, `/tmp` on
the compute node is usually the better place for temporary files, so put
`export TMPDIR=/tmp` at the top of your job scripts.

### Do not keep anything important in temporary folders

Agents, and the tools they use, may clear their own temporary folders without
warning, for example when a session ends or after a few days.  If an agent
writes a script, a result or a note that you want to keep, ask it to save it
in your project folder instead.

### Clean up regularly

Check what you have left in `/tmp` and `/dev/shm` on the login node you are
on:

```
find /tmp /dev/shm -maxdepth 2 -user $USER 2>/dev/null
du -sh /tmp/*$USER* /tmp/claude-$(id -u) 2>/dev/null
```

and in your own temporary folder:

```
du -sh /cosma/apps/PROJECT/USER/tmp/*
find /cosma/apps/PROJECT/USER/tmp -maxdepth 1 -mtime +7
```

Delete what you no longer need **yourself**, after checking what it is.  Do
not ask the agent to "clean up" in general: the rules above forbid agents from
deleting files without your agreement, for good reason.  Remember that `/tmp`
and `/dev/shm` on each node are separate, so check each node you use.

## Giving the agent the rules

Each agent reads an instructions file at the start of every session.  Use
this file to give it the COSMA rules and the facts it needs about COSMA, so
that it does not have to guess.

| Agent | Instructions file for all your projects | For one project |
| ----- | --------------------------------------- | --------------- |
| Claude Code | `~/.claude/CLAUDE.md` | `CLAUDE.md` in the project folder |
| Codex | `~/.codex/AGENTS.md` | `AGENTS.md` in the project folder |
| Gemini CLI | `~/.gemini/GEMINI.md` | `GEMINI.md` in the project folder |

Claude Code also reads `/etc/claude-code/CLAUDE.md` automatically, which COSMA
uses for a few short rules.  **No agent reads `/etc/claude-code/AGENTS.md`
automatically**, so include it yourself.  In `CLAUDE.md` or `GEMINI.md`, a
line containing just `@/etc/claude-code/AGENTS.md` pulls in the whole file.
For Codex, or if your agent does not support `@` lines, copy the file's
contents into your instructions file, and check it again from time to time for
updates.

### A starting template

Copy this into your instructions file and fill in the parts in capitals.  Each
line answers a question that agents otherwise get wrong on COSMA.

```
@/etc/claude-code/AGENTS.md

# COSMA facts
- Username: USER.  Project: PROJECT.  Slurm account: ACCOUNT.
- My directories: /cosma/home/PROJECT/USER (small, 10GB),
  /cosma/apps/PROJECT/USER (software, 100GB),
  /cosmaN/data/PROJECT/USER (data, large).  Work only inside these.
- Temporary files go in /cosma/apps/PROJECT/USER/tmp, never /tmp.
- Use absolute paths.  The working directory can change between commands.
- Modules are Environment Modules (Tmod 4), not Lmod: there is no
  "module spider", use "module avail NAME".  If "module" is missing, run
  "source /etc/profile.d/cosma-local-modules.sh" first.
- Libraries need a compiler loaded first, e.g.
  "module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5".
- Never pipe "module load" or "source": it runs in a subshell and is lost.
- Slurm jobs need -A, -p and -t.  Use mpirun, not srun, for Open MPI.
  Never submit or cancel jobs: give me the exact command instead.
- Login nodes are shared: at most 8 threads for builds and tests here
  (e.g. make -j8), and no long or memory-heavy runs.
- Put a time limit on any command that might hang: "timeout 600 CMD".
- Never search /cosma5, /cosma7, /cosma8, /snap7 or /snap8 as a whole.
- The compute nodes have no internet access.
- Use "ssh -o BatchMode=yes".  If ssh fails, stop and tell me; never retry.
- Do not compile with -march=native unless I say which nodes it will run on.
- Show me the command and its output for every claim that something works.
```

Keep the file short and factual.  Agents follow a short list of clear rules
far better than a long essay, and the whole file is read into the agent's
limited working memory in every session.  If your instructions file grows
past a page or two, trim it: one user halved theirs and found the agent
followed it more reliably.

## Your shell setup

Agents run commands in your shell, so problems in your shell start-up files
show up as strange agent behaviour.  Most of these also affect `scp`, `rsync`,
VS Code and batch jobs.

### Modules in agent shells

Agents usually run commands in a plain, non-login `bash` shell, which does not
read your login files.  In such a shell, the `module` command may not exist:

```
$ bash -c 'module avail gcc'
bash: line 1: module: command not found
```

There are two ways to fix this:

- Run commands in a login shell, `bash -l -c '...'`, which sets up modules as
  normal.
- Or, at the start of the command, run:

  ```
  source /etc/profile.d/cosma-local-modules.sh
  ```

Use `cosma-local-modules.sh`, not `/etc/profile.d/modules.sh`.  In a plain
shell, `modules.sh` sets up the operating system's own module setup, which
cannot see any of COSMA's modules, so `module avail` then lists almost
nothing.

### .bashrc and .bash_profile

- **Modules or settings in `~/.bash_profile` are missing in many places.**
  `~/.bash_profile` is only read by login shells.  A command run with
  `ssh NODE 'command'`, or by an agent, reads only `~/.bashrc`.  So a compiler
  or library you load in `~/.bash_profile` is not there, and builds fail with
  errors such as `nvcc: command not found` or a missing FFTW.  Load what your
  agent needs in the command itself, or in `~/.bashrc`.
- **Do not change directory in `~/.bashrc`.**  If `~/.bashrc` runs `cd`, every
  agent command, and every job script that starts with `#!/bin/bash -l`, starts
  in that directory instead of the one you expect.  Files then end up in the
  wrong place.
- **Keep `~/.bashrc` fast.**  Every agent command starts a new shell, so a
  `~/.bashrc` that takes seconds (loading many modules, or listing a large
  Lustre directory) slows everything down, and can make tools time out.
- **Do not print anything from `~/.bashrc` in non-interactive shells.**  Extra
  output confuses `scp`, `rsync` and agents that read command output.  Put any
  messages inside `if [[ $- == *i* ]]; then ... fi`.
- **Avoid shell functions and aliases with the names of real commands.**  A
  function called `stat`, for example, hides the real `stat`, and an agent
  gets output it does not understand.  If you have one, tell the agent, and
  use `command stat` in scripts.  Never keep aliases that delete things under
  innocent names.

### Pipes lose environment changes

A very common agent mistake is to pipe a command that changes the shell's
environment:

```
module load gnu_comp/14.1.0 | tail -n 5     # the module is NOT loaded afterwards
source setup.sh | tail -n 5                 # nothing in setup.sh is kept
```

Each part of a pipe runs in its own subshell, so the change is lost as soon as
that part finishes.  Run such commands on their own line, and send their
output to a file if it is too long.

### If your login shell is not bash

If your login shell is zsh or another shell, the agent's commands may run in
it.  Shells differ in small but important ways: zsh does not split a variable
into words (`for f in $LIST` loops once over the whole list), and treats `==`
and unquoted `'` differently.  Tell the agent which shell you use, or ask it
to run scripts with `bash -c '...'`.

If something works in your own terminal but not for the agent, compare `env`
in both.

## Using the login nodes fairly

Agents often start parallel builds, test suites and searches without being
asked, and run them over and over.  On a shared login node this can make the
node slow for everyone.

- Tell the agent how many threads to use (see the template above), and keep
  well within the limits in the COSMA rules: about 30 cores on a COSMA8 login
  node, 14 on a COSMA5 or COSMA7 login node.
- Anything that needs real computing time belongs in a [batch job](slurm.md),
  not on a login node.
- Do not leave an agent repeatedly checking something (a job, a file, a web
  page) every few seconds.  Ask it to check once, or at long intervals.
- Agents can start helper agents of their own.  Each one runs its own
  commands, so several at once multiply the load on the node.  Limit how many
  run at the same time.
- Never run two timing tests or benchmarks on the same node at once, and only
  compare timings measured on the same node.

### Leftover and stuck processes

When an agent is interrupted, or a command times out, the programs it started
often keep running.  Test runners, compilers, MPI programs, Jupyter kernels and
file watchers are common culprits.  In one case, dozens of leftover processes
from interrupted test runs were found on a single node, still using CPU.

- Check for your processes on each node you have used:

  ```
  ps -u $USER -o pid,etime,pcpu,rss,cmd --sort=-pcpu | head -20
  ```

- Stop the ones you no longer need by process ID: `kill PID`, and
  `kill -9 PID` only if that does not work.
- **Never use `pkill -u $USER` or `killall`** to clean up.  They also stop
  your agent, your editor's connection and your login session.
- A command that sits at 0% CPU for a long time is usually stuck, for example
  a test waiting for something that will never happen, or an MPI program where
  the ranks are out of step.  Agents wait for such commands for a long time.
  Ask the agent to run commands that might hang with a time limit:
  `timeout 600 COMMAND`.

## File systems

The `/cosma5`, `/cosma7`, `/cosma8`, `/snap7` and `/snap8` file systems are
[Lustre](lustre.md) file systems shared by every user.  Searching them as a
whole, with commands such as `find /cosma8`, `grep -r` or `du` at the top
level, puts a heavy load on the servers that hold the list of files, and slows
down everyone's work, including running jobs.

- Start the agent in your project folder, and tell it to work only there.
- For the size of a large folder on Lustre, `lfs find` is gentler than `du`
  (see [directory sizes](lustre.md#directory-sizes)).
- COSMA works best with a small number of large files.  If an agent's script
  writes millions of small files, ask it to combine them.

### Lustre is slow for small files

Lustre is built for large files.  Work that reads and writes many small files
(building code, running test suites, generating code, installing Python
packages) can be several times slower on Lustre than on app space.  In one
case, a code-generation step took 26 minutes on Lustre instead of 8.

- Keep source code, build folders and virtual environments in app space or
  your home directory, and keep the data file systems for data.
- In batch jobs, build and test in `/tmp` on the compute node, which is local
  to that node.

### pip and other caches on Lustre

`pip` writes its download cache carefully, forcing each file to disk.  On
Lustre this can make `pip install` hang for a long time, which looks to the
agent like a stuck command.  Keep the pip cache off Lustre: your `~/.cache`
already points to app space, so this only happens if something moves the
cache onto a data file system.  For automated installs, such as test
pipelines, setting `PIP_NO_CACHE_DIR=1` avoids the cache entirely.

### Quotas

A full quota makes agents fail in confusing ways: half-written files, broken
installs, or errors about something else entirely.

- Check your quotas before an agent writes a lot of data: see
  [quotas](lustre.md#quotas) for the data file systems, and the
  [storage](storage.md) page for home and app space.
- App space can fill up too, for example with test data, build folders or
  conversation histories.  Keep large outputs on a data file system.
- Data file system quotas are often shared by everyone in a project, so an
  agent that fills the project quota stops other people's jobs too.

## Slurm and agents

Under the COSMA rules, agents must not submit or cancel jobs by themselves.  A
good way to work:

1. Ask the agent to write the job script.
2. Ask it to check the script with `sbatch --test-only script.sh`, which
   checks the request without submitting it.
3. Read the script, then submit it yourself with `sbatch`, or tell the agent
   to submit that one script after it has shown you the exact command and
   resources.
4. If the job fails, do not let the agent resubmit it automatically: look at
   the error first.

Things to watch for in scripts that agents write:

- `-A ACCOUNT`, `-p PARTITION` and `-t TIME` are all required on COSMA.
- Some queues give you a whole node, and charge for it, even if you ask for
  one core.  For small jobs, use a queue that shares nodes (see the
  [queue guide](queue.md)).
- Separate `--output` and `--error` files make problems easier to find.
- Use a [job array](sbatch.md) instead of a loop of `sbatch` commands.
  Hundreds of separate submissions slow the scheduler for everyone.
- Never let an agent edit a script that a queued or running job will use:
  `bash` reads scripts as it goes, so the edit can break the running job.
- `sbatch --test-only` does not show everything.  On some queues, asking for
  more memory per CPU than the queue allows makes Slurm give the job extra
  CPUs, and charge for them, but `--test-only` does not show this.  After
  submitting, check what was actually allocated with
  `scontrol show job JOBID`.

See [your first job](firstjob.md) and the [Slurm pages](slurm.md) for more.

## Code that breaks on COSMA

Agents write code that works on a typical laptop or cloud server.  Some
common choices break on COSMA:

- **`-march=native`.**  This builds code for the CPU of the machine you
  compile on.  Built on an AVX-512 login node, the program stops with
  `Illegal instruction` on nodes without AVX-512, such as COSMA8.  See
  [compiling for each system](facilities.md#compiling-for-each-system).
- **`srun` with Open MPI.**  On COSMA, start Open MPI programs with `mpirun`.
  `srun` does not start them correctly.
- **`TMPDIR` on a network file system.**  If `TMPDIR` points to app space or
  home in a job (it is passed on from your login), Open MPI warns that its
  shared-memory files are on a network file system, and can run slowly.  Set
  `export TMPDIR=/tmp` in the job script.
- **Binding with Intel MPI.**  Wrapping `numactl` around `mpirun` does not
  confine Intel MPI ranks, because Intel MPI sets its own binding.  Put
  `numactl` after `mpirun` instead, so that it applies to each rank, and check
  where the ranks really run.
- **Writing output with `>` in automated jobs.**  `command > file` empties the
  file before the command starts.  If the command then fails, the file is left
  empty, and a scheduled job may publish or commit the empty file.  Write to a
  temporary file and rename it only when the command succeeded.

## SSH, passwords and logins

- **Never give an agent your SSH key passphrase or your COSMA password**, and
  never put them in a file it can read.
- **Agents cannot answer password or second-factor prompts.**  An agent or
  script that keeps retrying a login that needs one causes a run of failed
  logins, and COSMA then blocks your address.  The block may only apply to
  one login node, but do not try the others in turn: stop, and log in
  yourself.
- **Ask agents to use `ssh -o BatchMode=yes`.**  This makes SSH fail at once
  instead of asking for a password.  Without it, SSH can wait forever for an
  answer, or open a password window on your screen if you are using X11
  forwarding.
- **Share your connection.**  If an agent needs to reach COSMA from your own
  computer, log in once yourself with
  [connection sharing](ssh.md#reusing-ssh-connections) turned on, so its
  connections reuse yours instead of logging in again.
- **About 10 sessions per connection.**  COSMA refuses more than about 10
  sessions on one shared connection.  When an agent opens many at once (for
  example several terminals, file transfers and an editor), the extra ones are
  refused, and SSH starts a fresh login that asks for a password.  To the
  agent this looks like a hang.  Spread the work over more than one login
  node, or reduce the number of parallel connections.
- **SSH between COSMA nodes uses your Kerberos ticket**, not your SSH key.  You
  get the ticket when you log in with your password, and it expires after
  about 24 hours.  After that, an agent's `ssh mad12` or `ssh login7a` from a
  login node fails.  Check with `klist`, and get a new ticket with `kinit`.
- **Shared connections started on COSMA need `%L`.**  Your home directory is
  the same on every login node.  If an agent sets up connection sharing from a
  login node to another machine, a `ControlPath` such as
  `~/.ssh/cm-%r@%h:%p` is shared by every login node, so a connection closing
  on one node removes it for the others.  Add `%L` (the name of the local
  machine): `~/.ssh/cm-%L-%r@%h:%p`.
- Do not let agents change your `~/.ssh` files, set up tunnels or forward
  ports.  The COSMA rules forbid it.

## Data, privacy and accounts

```{note}
This section describes general good practice.  Your project, funder or
institution may have its own rules on using AI tools, and those take
priority.  Ask cosma-support or your PI if you are unsure.
```

- **What you show the agent is sent to its company.**  Online agents send
  the files they read, the command output they see and your messages to the
  company that runs the model.  Before using one on unpublished results,
  data covered by a data-sharing agreement, personal data, or code you are not
  allowed to share, check that this is allowed.  Many agents have settings to
  keep certain files or folders out of reach.
- **Keep API keys and login tokens private.**  Agents store these in their
  own folders (see [above](#move-the-agents-own-folders-out-of-your-home-directory)).
  Make sure only you can read them (`chmod 700` on the folder), and never put
  keys in shared project folders or commit them to git.
- **If a key is shown, treat it as leaked.**  If a key or token appears in an
  agent's output, a log file, a shared folder or a git commit, cancel it and
  make a new one straight away.  Deleting the text afterwards is not enough.
- **Give tokens only the access they need.**  A GitHub token, for example,
  usually only needs access to the repositories the agent works on, not your
  whole account.
- **Do not share agent accounts or keys** with other COSMA users.
- **Check before an agent sends anything outside COSMA**, such as emails,
  issue comments, pull requests or uploads.  These are public or hard to take
  back.

## Approvals and permissions

Most agents ask before running commands or editing files, and let you decide
which actions they may take without asking.  Use this.

- **Never turn off the approval prompts or the sandbox**, for example with
  `--dangerously-skip-permissions`, `--yolo` or
  `--dangerously-bypass-approvals-and-sandbox`, or by setting the agent to skip
  approvals by default in its settings file.  It is tempting, because the
  prompts slow you down, but the COSMA rules forbid it, and it removes the
  last check before a mistake.
- Instead, allow specific safe commands without asking.  It is reasonable to
  allow read-only commands (`ls`, `cat`, `git status`, `git diff`,
  `squeue --me`).
- Always read before approving anything that deletes, moves or overwrites
  files (`rm`, `mv`, `>`), changes git history (`git push --force`,
  `git reset --hard`), submits jobs, or touches shared data.
- If an agent's safety check blocks a command, do not ask it to find another
  way to do the same thing.  Look at why it was blocked.
- An approval you gave in one session does not carry over to the next.

### Protect your work

- Keep code in git, and commit before letting an agent make large changes,
  so you can see exactly what it changed (`git diff`) and undo it.
- Never let an agent work directly on raw simulation output or other data
  that cannot be regenerated.  Write results to a separate folder.
- If an agent deletes something from your home or app space, it can usually
  be recovered from a [snapshot](storage.md#recovering-files-from-snapshots).
  The data file systems are **not** backed up.

## Long sessions and several agents

### Agents forget

An agent can only hold a limited amount of a conversation in its working
memory.  In a long session, it summarises older parts to make room, and
details are lost: rules you gave earlier, which files it changed, what it has
already tested.  After that, it may repeat work, undo a fix, or state
something from the earlier part wrongly.

- Ask the agent to keep notes of decisions and results in a file in the
  project, not only in the conversation.
- Put rules you need it to follow every time in its instructions file, not in
  a message.
- Start a new session for a new task.

### Usage limits

Most agent subscriptions limit how much you can use them in a few hours or a
week.  When the limit is reached, the agent stops part way through a task.
Commit often, so that work is never left half-done when it stops.

### Several agents at once

- Give each agent its own copy of the code: a separate clone, or a
  `git worktree`.  Two agents editing the same files at once overwrite each
  other's changes.
- Agents that create branches and worktrees often leave them behind.  Check
  with `git worktree list` and `git branch`, and remove the ones you no longer
  need with `git worktree remove` once their work is merged.
- Do not let several agents run benchmarks on the same node at once.

## Checking the agent's work

Agents can be wrong while sounding certain.  They may say a script works when
it was never run, report a number they did not measure, record a task as done
before checking it, or say something is missing from a file without having
read all of it.

- Ask the agent to show the command and its output for each claim, rather
  than a summary.
- **Test in the same conditions as the real use.**  A script that works when
  the agent runs it may fail when run by a scheduled job, in a batch job or on
  another node, because the environment is different.  In one case, a script
  worked in the agent's shell but, run from a scheduled job, found only 6 of
  almost 300 modules, because the scheduled job's environment was set up
  differently.  Ask the agent to test with the same shell, environment and
  node that will be used for real.
- Read the changes (`git diff`) before committing them.
- For anything you will publish or send to someone else, check the numbers
  yourself from the original output.
- Timing tests on a shared login node are unreliable, because other people's
  work affects them.  Run benchmarks in a batch job.

## At the end of a session

1. Check that no jobs are left that you did not mean to run: `squeue --me`.
2. Check for leftover processes on each node you used:
   `ps -u $USER`.
3. Check for temporary files in `/tmp`, `/dev/shm` and your own temporary
   folder (see [clean up regularly](#clean-up-regularly)).
4. Commit or discard the agent's changes in git, and remove worktrees you no
   longer need.
5. Make sure the agent's notes and results are saved in your project, not
   only in its temporary folder.

## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `module: command not found` | The agent's shell does not set up modules.  See [modules in agent shells](#modules-in-agent-shells). |
| `module avail` shows almost nothing | `/etc/profile.d/modules.sh` was used instead of `/etc/profile.d/cosma-local-modules.sh`. |
| A module seems loaded but is not | `module load` was piped into another command.  See [pipes lose environment changes](#pipes-lose-environment-changes). |
| A compiler or library is missing over `ssh NODE command` | It is loaded in `~/.bash_profile`, which that command does not read.  See [.bashrc and .bash_profile](#bashrc-and-bash-profile). |
| `node: command not found`, or `npm` installs to a system folder | Load `nodejs/24.18.1`, and set the `npm` prefix to your app space. |
| An agent that worked now fails to start, or `.nfs` files cannot be deleted | An interrupted install or update.  See [when an install or update goes wrong](#when-an-install-or-update-goes-wrong). |
| Logging in to one account logs the other out | Two accounts share one agent folder.  See [one folder for each account](#one-folder-for-each-account). |
| `Disk quota exceeded` in your home directory | Agent folders or caches are in `~`.  Move them to app space (see [above](#move-the-agents-own-folders-out-of-your-home-directory)). |
| The agent stops at a password or second-factor prompt, or SSH hangs | Agents cannot answer these.  Log in yourself with connection sharing turned on.  If a shared connection is frozen, run `ssh -O exit HOST`. |
| SSH to another COSMA node stopped working after a day | Your Kerberos ticket has expired.  Check with `klist`, renew with `kinit`. |
| New SSH sessions suddenly ask for a password | More than about 10 sessions on one shared connection.  Use fewer at once, or another login node. |
| `pip install` hangs | The pip cache is on Lustre.  See [pip and other caches on Lustre](#pip-and-other-caches-on-lustre). |
| Builds or tests are much slower than on your laptop | The code is on Lustre.  See [Lustre is slow for small files](#lustre-is-slow-for-small-files). |
| `Illegal instruction` | The code was built with `-march=native` for a different CPU.  See [compiling for each system](facilities.md#compiling-for-each-system). |
| `Permission denied` running a program the agent unpacked in `/tmp` | `/tmp` on the login nodes cannot run programs.  Set `TMPDIR` to your app space. |
| The agent's connection to its model fails inside a batch job | Compute nodes cannot reach the internet.  Run the agent on a login node. |
| The node is slow, or your memory use is high after a session | Leftover processes or files in `/dev/shm`.  See [leftover and stuck processes](#leftover-and-stuck-processes). |

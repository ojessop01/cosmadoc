# Setting up AI coding agents

This page explains where agents can run on COSMA, how to install them, and how to set up your account so that they work well.  Start with the [overview](agents.md) and the COSMA rules for agents.

## Where agents can run

### On a login node

Command-line agents (Claude Code, Codex, Gemini CLI and others) run well on
the login nodes.  The login nodes can reach the internet, which the agent
needs to talk to its model.

The login nodes are shared by everyone, and there is no automatic limit on how
much CPU or memory one person can use on them.  Keep within the limits in the
rules above, and see [using the login nodes fairly](agents-safe.md#using-the-login-nodes-fairly).

### Not in batch jobs

The compute nodes cannot reach the internet, so an agent that uses an online
model cannot run inside a batch job.  Instead, the agent prepares a job
script, and you submit it (see [Slurm and agents](agents-safe.md#slurm-and-agents)).

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

Copy this into your instructions file for all projects (for example
`~/.claude/CLAUDE.md`), and replace the parts in capitals with your own
details.  Delete any line that does not apply to you.  Each line answers a
question that agents otherwise get wrong on COSMA.

```
@/etc/claude-code/AGENTS.md

# About me
- COSMA username: USER.  Project: PROJECT.  Default Slurm account: ACCOUNT.
- I work mainly on: SHORT DESCRIPTION, e.g. "SWIFT simulations and Python
  analysis of their snapshots".
- Ask me when something is unclear, rather than guessing.

# My directories (work only inside these)
- Home: /cosma/home/PROJECT/USER.  Small (about 10GB) and backed up: only
  settings and small scripts.
- App space: /cosma/apps/PROJECT/USER.  About 100GB: code, builds, virtual
  environments, installed software.
- Data: /cosma8/data/PROJECT/USER.  Large, on Lustre, not backed up: data
  and job output.  Never put code, builds or venvs here.
- Temporary files: /cosma/apps/PROJECT/USER/tmp.  Never /tmp or my home.
- Use absolute paths in every command.  The working directory may change
  between commands.

# Safety
- Never delete, move or overwrite files, or change permissions, without
  asking me first.  Before overwriting a file, look at what is in it.
- Never submit, cancel or change Slurm jobs.  Write the job script, check it
  with "sbatch --test-only", and give me the exact command to run.
- Never turn off approvals or the sandbox.  If something is blocked, say
  exactly what and stop.
- Never read, print or copy keys, passwords or tokens.
- Treat simulation outputs and other raw data as read-only.  Write results to
  a separate folder.
- Commit to git before large changes, and show me "git diff" before
  committing.  Never "git push --force" or "git reset --hard".

# Using the login nodes
- Login nodes are shared.  Use at most 8 threads for builds and tests
  (e.g. "make -j8", "pytest -n 8"), and nothing long or memory-heavy.
- Anything that needs real computing goes in a batch job.
- Put a time limit on any command that might hang: "timeout 600 CMD".
- Limit long output: "CMD 2>&1 | tail -n 200".
- Do not leave processes running.  Check with "ps -u $USER" before finishing.

# Modules and software
- Modules are Environment Modules (Tmod 4), not Lmod: no "module spider",
  use "module avail NAME".
- If "module" is missing, run "source /etc/profile.d/cosma-local-modules.sh".
- Load a compiler first, then MPI, then libraries, e.g.
  "module load gnu_comp/14.1.0 openmpi/5.0.3 hdf5".
- Never pipe "module load" or "source": the change is lost in a subshell.
- My usual modules: MODULES.
- Python: use my virtual environment VENV_PATH.  Never create, change or
  remove conda environments.

# Slurm
- Every job needs -A, -p and -t.  Maximum time is 3 days.
- cosma8 and cosma7 give whole nodes, charged in full.  For less than a node
  use cosma8-serial, cosma7-shm or cosma5, which share nodes.
- Start job scripts with "module purge" and load every module needed.
- Use mpirun, not srun, for Open MPI programs.
- Set "export TMPDIR=/tmp" in job scripts.
- Use job arrays rather than loops of sbatch.
- Never edit a script that a queued or running job uses.

# Building code
- CPUs differ between systems.  Do not use -march=native unless I say which
  nodes the program will run on: AVX-512 builds fail on cosma8.
- Build and test on the node type the code will run on.

# Files and the network
- Never search /cosma5, /cosma7, /cosma8, /snap7 or /snap8 as a whole.
  Search only inside my directories.
- Lustre is slow for many small files.  Prefer fewer, larger files.
- Check space before writing a lot of data: "quota" shows home, app space
  and every Lustre file system.
- Compute nodes have no internet access.
- Use "ssh -o BatchMode=yes".  If ssh fails, stop and tell me.  Never retry.

# How to report
- Start with one line saying whether it worked.
- Show the command and its actual output for every claim that something
  works.  For every number, say where it came from (command, job ID, node).
- Say what you did not check, and mark guesses as guesses.
```

#### What to change, and what to leave

- **Fill in** the capitals: your username, project and account, your data
  folder (change `/cosma8` to `/cosma5` or `/cosma7` if your data is there),
  your usual modules, and your virtual environment.
- **Remove** sections that do not apply.  For example, if you never build
  code, drop "Building code".
- **Keep** the safety section.  It matches the COSMA rules, and is the part
  that prevents the most damage.
- **Add** facts about your own work that the agent keeps getting wrong: units
  and definitions in your field, the name of your main code, how your
  simulation outputs are laid out.

#### A template for one project

For a particular project, add a short file in the project's folder
(`CLAUDE.md`, `AGENTS.md` or `GEMINI.md`, depending on the agent) with
the facts that only apply there:

```
# This project
- What it is: ONE OR TWO SENTENCES.
- Code: /cosma/apps/PROJECT/USER/CODE (git repository, main branch: main).
- Data: /cosma8/data/PROJECT/USER/DATA.  Read-only.
- Results go in: /cosma8/data/PROJECT/USER/RESULTS.

# Building and testing
- Build: BUILD COMMAND, after "module load MODULES".
- Test: TEST COMMAND.  Run it after every change.
- Quick test input: SMALL INPUT FILE.

# Conventions
- Units: e.g. "lengths in comoving Mpc, masses in 1e10 Msun".
- Style: follow the existing code; no unrelated changes.

# Jobs
- Usual queue and resources: e.g. "cosma8, 1 node, 128 ranks, 12 hours".
- Job scripts live in: /cosma/apps/PROJECT/USER/CODE/jobs.
```

#### Keep it short

Agents follow a short list of clear rules far better than a long essay, and
the whole file is read into the agent's limited working memory in every
session.  Aim for a page or two.  If your file grows longer, trim it: one user
halved theirs and found the agent followed it more reliably.  Review it now
and then, and remove rules that no longer matter.

For Codex, which does not read `@` lines, copy the contents of
`/etc/claude-code/AGENTS.md` into the file in place of the first line.

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

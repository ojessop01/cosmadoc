# AI coding agents

AI coding agents are programs that read your files, run commands and edit
code for you, using a large language model.  Examples are Claude Code, OpenAI
Codex, Gemini CLI, GitHub Copilot, Cursor and Google Antigravity.  They can
save a lot of time on COSMA, but they act with *your* account: every file they
delete, every job they submit and every login they attempt is done as you.

This page explains how to set them up and use them on COSMA without causing
problems for yourself or for other users.

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
rules is easy.

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

### Keeping an agent running

If your connection drops, a command-line agent running in it stops.  To keep
it running, start it inside [tmux](tmux.md):

```
tmux new -s agent
```

Detach with `Ctrl-b d`, and reattach later with `tmux attach -t agent`.  tmux
sessions only exist on the login node where you started them, so note which
node that was (`hostname`), and log in to the same one to get back to it.

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

Move each one to your app space and leave a link in its place.  Do this while
the agent is not running.  For example, for Claude Code:

```
mkdir -p /cosma/apps/PROJECT/USER/dotfiles
mv ~/.claude /cosma/apps/PROJECT/USER/dotfiles/claude
ln -s /cosma/apps/PROJECT/USER/dotfiles/claude ~/.claude
```

If the folder does not exist yet, make the empty folder in app space and
create the link before you first run the agent.

To see what is using your home quota, run `du -sh ~/.[!.]* | sort -h`.

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

See [temporary space](storage.md#temporary-space) for more on `/tmp`.

### Send temporary files to your own space

Most agents, like most programs, put temporary files wherever the `TMPDIR`
variable points.  Set it to a folder in your app space, in `~/.bashrc`:

```
mkdir -p /cosma/apps/PROJECT/USER/tmp
export TMPDIR=/cosma/apps/PROJECT/USER/tmp
```

`TMPDIR` is also passed on to batch jobs.  In a job, `/tmp` on the compute
node is usually the better place for temporary files, so set
`export TMPDIR=/tmp` at the top of your job scripts if you want that.

### Clean up regularly

Check what you have left in `/tmp` on the login node you are on:

```
find /tmp -maxdepth 2 -user $USER 2>/dev/null
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
on each login node is separate, so check each node you use.

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
- Slurm jobs need -A, -p and -t.  Use mpirun, not srun, for Open MPI.
  Never submit or cancel jobs: give me the exact command instead.
- Login nodes are shared: at most 8 threads for builds and tests here
  (e.g. make -j8), and no long or memory-heavy runs.
- Never search /cosma5, /cosma7, /cosma8, /snap7 or /snap8 as a whole.
- The compute nodes have no internet access.
```

Keep the file short and factual.  Agents follow a short list of clear rules
far better than a long essay, and every line costs part of the agent's
working memory in every session.

## Modules in agent shells

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

Some agents also do not read `~/.bashrc`, so settings made there, such as
`PATH` or `TMPDIR`, may be missing too.  If something works in your own
terminal but not for the agent, compare `env` in both.

## Using the login nodes fairly

Agents often start parallel builds, test suites and searches without being
asked, and run them over and over.  On a shared login node this can make the
node slow for everyone.

- Tell the agent how many threads to use (see the template above), and keep
  well within the limits in the COSMA rules: about 30 cores on a COSMA8 login
  node, 14 on a COSMA5 or COSMA7 login node.
- Anything that needs real computing time belongs in a [batch job](slurm.md),
  not on a login node.
- Agents can leave processes running in the background after a session.
  Check with `ps -u $USER -o pid,etime,pcpu,rss,cmd --sort=-pcpu | head` on
  each login node you have used, and stop any you no longer need with
  `kill PID`.
- Do not leave an agent repeatedly checking something (a job, a file, a web
  page) every few seconds.  Ask it to check once, or at long intervals.

## File systems

The `/cosma5`, `/cosma7`, `/cosma8`, `/snap7` and `/snap8` file systems are
[Lustre](lustre.md) file systems shared by every user.  Searching them as a
whole, with commands such as `find /cosma8`, `grep -r` or `du` at the top
level, puts a heavy load on the servers that hold the list of files, and slows
down everyone's work, including running jobs.

- Start the agent in your project folder, and tell it to work only there.
- Keep code, which the agent searches often, in your home or app space, and
  big data on the data file systems.
- For the size of a large folder on Lustre, `lfs find` is gentler than `du`
  (see [directory sizes](lustre.md#directory-sizes)).
- Cosma works best with a small number of large files.  If an agent's script
  writes millions of small files, ask it to combine them.

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

See [your first job](firstjob.md) and the [Slurm pages](slurm.md) for more.

## SSH, passwords and logins

- **Never give an agent your SSH key passphrase or your COSMA password**, and
  never put them in a file it can read.
- Agents cannot answer password or second-factor prompts.  An agent or script
  that keeps retrying a login that needs one causes a run of failed logins,
  and COSMA then blocks your address.  If an agent's SSH command fails, stop it
  and log in yourself.
- If you want an agent to reach another login node or a node such as `mad12`,
  log in once yourself with [connection sharing](ssh.md#reusing-ssh-connections)
  turned on, so its connections reuse yours instead of logging in again.
- Do not let agents change your `~/.ssh` files, set up tunnels or forward
  ports.

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
- **Do not share agent accounts or keys** with other COSMA users.

## Approvals and permissions

Most agents ask before running commands or editing files, and let you decide
which actions they may take without asking.  Use this.

- **Never turn off the approval prompts or the sandbox**, for example with
  `--dangerously-skip-permissions`, `--yolo` or
  `--dangerously-bypass-approvals-and-sandbox`.  The COSMA rules forbid it.
- It is reasonable to allow read-only commands (`ls`, `cat`, `git status`,
  `squeue --me`) without asking.
- Always read before approving anything that deletes, moves or overwrites
  files (`rm`, `mv`, `>`), changes git history (`git push --force`,
  `git reset --hard`), submits jobs, or touches shared data.
- An approval you gave in one session does not carry over to the next.

### Protect your work

- Keep code in git, and commit before letting an agent make large changes,
  so you can see exactly what it changed (`git diff`) and undo it.
- Never let an agent work directly on raw simulation output or other data
  that cannot be regenerated.  Write results to a separate folder.
- If an agent deletes something from your home or app space, it can usually
  be recovered from a [snapshot](storage.md#recovering-files-from-snapshots).
  The data file systems are **not** backed up.

## Checking the agent's work

Agents can be wrong while sounding certain.  They may say a script works when
it was never run, report a number they did not measure, or say something is
missing from a file without having read all of it.

- Ask the agent to show the command and its output for each claim, rather
  than a summary.
- Read the changes (`git diff`) before committing them.
- For anything you will publish or send to someone else, check the numbers
  yourself from the original output.
- Timing tests on a shared login node are unreliable, because other people's
  work affects them.  Run benchmarks in a batch job.

## At the end of a session

1. Check that no jobs are left that you did not mean to run: `squeue --me`.
2. Check for leftover processes: `ps -u $USER`.
3. Check for temporary files in `/tmp` and your own temporary folder (see
   [clean up regularly](#clean-up-regularly)).
4. Commit or discard the agent's changes in git.
5. Close `tmux` sessions you no longer need: `tmux kill-session -t agent`.

## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `module: command not found` | The agent's shell does not set up modules.  See [modules in agent shells](#modules-in-agent-shells). |
| `module avail` shows almost nothing | `/etc/profile.d/modules.sh` was used instead of `/etc/profile.d/cosma-local-modules.sh`. |
| `node: command not found`, or `npm` installs to a system folder | Load `nodejs/24.18.1`, and set the `npm` prefix to your app space. |
| `Disk quota exceeded` in your home directory | Agent folders or caches are in `~`.  Move them to app space (see [above](#move-the-agents-own-folders-out-of-your-home-directory)). |
| The agent stops at a password or second-factor prompt, or SSH hangs | Agents cannot answer these.  Log in yourself with connection sharing turned on.  If a shared connection is frozen, run `ssh -O exit HOST`. |
| `Permission denied` running a program the agent unpacked in `/tmp` | `/tmp` on the login nodes cannot run programs.  Set `TMPDIR` to your app space. |
| The agent's connection to its model fails inside a batch job | Compute nodes cannot reach the internet.  Run the agent on a login node. |
| The agent stopped when your connection dropped | Run it inside `tmux`, and reattach on the same login node. |

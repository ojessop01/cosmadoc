# Using AI coding agents safely

This page covers the things that most often go wrong when agents are used on a shared system, and how to avoid them.  Read it together with the COSMA rules on the [overview](agents.md) page.

## Temporary files

Agents create a lot of temporary files, and often do not delete them.
Claude Code, for example, keeps a folder of temporary files for each session
(command output, scripts it writes, diffs) and leaves it behind when the
session ends.  One user's folder of these grew to 206MB, in over 100
sub-folders, half of them more than a week old, and there was another 80MB in
`/tmp` on one login node.  Plugins and other tools add more.  Some agents
also keep temporary files inside their own folder in your home directory:
Codex, for example, uses `~/.codex/tmp`, which is another reason to
[move that folder](agents-setup.md#move-the-agents-own-folders-out-of-your-home-directory).

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
[code that breaks on COSMA](agents-coding.md#code-that-breaks-on-cosma)).  In a job, `/tmp` on
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
  own folders (see [above](agents-setup.md#move-the-agents-own-folders-out-of-your-home-directory)).
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
| `module: command not found` | The agent's shell does not set up modules.  See [modules in agent shells](agents-setup.md#modules-in-agent-shells). |
| `module avail` shows almost nothing | `/etc/profile.d/modules.sh` was used instead of `/etc/profile.d/cosma-local-modules.sh`. |
| A module seems loaded but is not | `module load` was piped into another command.  See [pipes lose environment changes](agents-setup.md#pipes-lose-environment-changes). |
| A compiler or library is missing over `ssh NODE command` | It is loaded in `~/.bash_profile`, which that command does not read.  See [.bashrc and .bash_profile](agents-setup.md#bashrc-and-bash-profile). |
| `node: command not found`, or `npm` installs to a system folder | Load `nodejs/24.18.1`, and set the `npm` prefix to your app space. |
| An agent that worked now fails to start, or `.nfs` files cannot be deleted | An interrupted install or update.  See [when an install or update goes wrong](agents-setup.md#when-an-install-or-update-goes-wrong). |
| Logging in to one account logs the other out | Two accounts share one agent folder.  See [one folder for each account](agents-setup.md#one-folder-for-each-account). |
| `Disk quota exceeded` in your home directory | Agent folders or caches are in `~`.  Move them to app space (see [above](agents-setup.md#move-the-agents-own-folders-out-of-your-home-directory)). |
| The agent stops at a password or second-factor prompt, or SSH hangs | Agents cannot answer these.  Log in yourself with connection sharing turned on.  If a shared connection is frozen, run `ssh -O exit HOST`. |
| SSH to another COSMA node stopped working after a day | Your Kerberos ticket has expired.  Check with `klist`, renew with `kinit`. |
| New SSH sessions suddenly ask for a password | More than about 10 sessions on one shared connection.  Use fewer at once, or another login node. |
| `pip install` hangs | The pip cache is on Lustre.  See [pip and other caches on Lustre](#pip-and-other-caches-on-lustre). |
| Builds or tests are much slower than on your laptop | The code is on Lustre.  See [Lustre is slow for small files](#lustre-is-slow-for-small-files). |
| `Illegal instruction` | The code was built with `-march=native` for a different CPU.  See [compiling for each system](facilities.md#compiling-for-each-system). |
| `Permission denied` running a program the agent unpacked in `/tmp` | `/tmp` on the login nodes cannot run programs.  Set `TMPDIR` to your app space. |
| The agent's connection to its model fails inside a batch job | Compute nodes cannot reach the internet.  Run the agent on a login node. |
| The node is slow, or your memory use is high after a session | Leftover processes or files in `/dev/shm`.  See [leftover and stuck processes](#leftover-and-stuck-processes). |

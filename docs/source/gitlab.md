# GitLab

COSMA has its own GitLab server, the ICC GitLab, at
[gitlab.cosma.dur.ac.uk](https://gitlab.cosma.dur.ac.uk), for hosting code
repositories, sharing code within a group, and reviewing changes.  It is
useful for code that should stay within COSMA's community rather than on a
public site such as GitHub.

## Getting an account

Accounts are set up by COSMA staff.  Email cosma-support@durham.ac.uk to ask
for one, saying which group or project you will work with.

## Using GitLab with SSH

To push and pull over SSH, add an SSH public key to your GitLab profile
(your avatar, Edit profile, SSH Keys).  You can use the key you use to log in
to COSMA (see [generating an SSH key](sshkey.md)), or a separate key.  If you
will clone repositories while logged in to COSMA, the key must be on COSMA
too, or forwarded with your SSH agent.

Clone a repository with its SSH address, shown under the **Code** button on
the repository's page:

```
git clone git@gitlab.cosma.dur.ac.uk:GROUP/REPOSITORY.git
```

To check that your key works:

```
ssh -T git@gitlab.cosma.dur.ac.uk
```

which prints a welcome message with your GitLab username when it works, and
`Permission denied (publickey)` if GitLab does not know your key.

## Where to keep your clones on COSMA

Keep repositories in your app space (`/cosma/apps/PROJECT/USER`) or home
directory, not on the Lustre data file systems, where git's many small files
are slow.  Large data files do not belong in git: keep them on the data file
systems, and keep only code and small inputs in the repository.

## Things to know

- **No large files.**  The COSMA GitLab does not have much storage.  Please
  do not store large binary files, simulation outputs or datasets in it.
- **Learning git and GitLab.**  The [GitLab documentation](https://docs.gitlab.com)
  covers merge requests, issues, CI and everything else, and the
  [Pro Git book](https://git-scm.com/book) is a good introduction to git
  itself.

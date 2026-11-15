# Getting an account

COSMA accounts are requested through
[SAFE](https://safe.epcc.ed.ac.uk/dirac/), the website used to manage
accounts on all DiRAC systems.  Getting an account takes four steps:

1. **Get ready**: make an SSH key, and find out your project code.
2. **Create a SAFE account**, if you do not already have one.
3. **Request a COSMA login account** on SAFE, for your project.
4. **Wait for approval**, first by your project's PI or manager, then by COSMA
   staff, who create the account and email you.

Then you can [log in](ssh.md) and [run your first job](firstjob.md).

## 1. Before you start

You need two things:

- **An SSH key pair.**  Make one on the computer you will log in from, with a
  strong passphrase.  See [generating an SSH key](sshkey.md).  You will upload
  the public part, the file ending `.pub`.
- **A project code.**  Every account belongs to a project.  Ask your
  supervisor or PI which one to join:

  | You are | Project code |
  | ------- | ------------ |
  | Part of a DiRAC project | `dpXXX` (a three-digit number), from your project's PI |
  | Using the HPC Hardware Lab | One of the hardware lab codes, such as `do016` for NVIDIA GPUs |
  | A Durham user (or collaborator) of COSMA5 | `hpcicc` |

  See [project codes](project.md) for the full list.

## 2. Create a SAFE account

If you already have a SAFE account, for example from another DiRAC system,
log in and go to [step 3](#request-a-cosma-login-account).

1. Go to [SAFE](https://safe.epcc.ed.ac.uk/dirac/) and click
   **Create an account**.

   ![The SAFE login page, with the "Create an account" link](images/DiRACSAFEscreen.png)

2. Fill in the registration form.  Use your **institutional email address**,
   not a personal one.  You can upload your SSH public key here as your
   default key, but it is not added to COSMA until you request a login
   account (step 3).

   ![The empty SAFE registration form](images/account2.png)

   ![The registration form filled in, with an SSH public key chosen](images/account3.png)

3. Read and accept the terms and conditions of access.

   ![The User Access Agreement page](images/account4.png)

4. Set a password for SAFE.  This is your **SAFE password**, used only for
   the SAFE website.  It is different from your COSMA password, which you get
   later.

   ![Setting the SAFE password](images/account5.png)

5. You are now logged in to SAFE.  Click **Continue**.

   ![The SAFE welcome page](images/account6.png)

## 3. Request a COSMA login account

1. SAFE shows that you are a new user, with a restricted view until you join a
   project.  Open the **Login accounts** menu and choose to request a new login
   account.

   ![The SAFE home page for a new user, pointing to the Login accounts menu](images/account7.png)

2. Enter your **project code**, such as `hpcicc` or `dp004`, and click
   **Next**.

   ![Entering the project code](images/account8.png)

3. Select **cosma: The Durham COSMA machine**, not COSMOS or another DiRAC
   system, and click **Next**.  The policies listed should all have ticks; a
   cross means something, such as a missing SSH key, must be fixed first.

   ![Choosing the COSMA machine](images/account9.png)

4. Check your username, and upload your SSH **public** key (the `.pub` file),
   unless you already gave a default key.  Click **Request**.

   ![The username and SSH public key](images/account10.png)

5. SAFE confirms the request.

   ![The request confirmation](images/account11.png)

## 4. Wait for approval

Two things happen before you can log in:

1. Your project's **PI or a project manager** approves your request.  Make sure
   they know who you are and expect your request, especially for DiRAC
   projects.
2. **COSMA staff** create your account and add your SSH key.  This is done by
   hand, so it can take a little while, depending on how busy they are.

You then receive a **welcome email** with your username and a first
password.

## Your first login

Log in as described in [SSH access](ssh.md), for example:

```
ssh USER@login8b.cosma.dur.ac.uk
```

You will be asked for your SSH key passphrase, then your COSMA password.  The
first time, you must change the password straight away: enter the password
from the email twice (once to log in, once as your current password), then
your new password twice.  See
[logging in for the first time](ssh.md#logging-in-for-the-first-time).

## What next

- **New to COSMA?**  Read [your first job](firstjob.md), which goes from logging in
  to running a job, and [good citizenship](citizenship.md).
- **Avoid typing passwords repeatedly**: set up
  [connection sharing](ssh.md#reusing-ssh-connections) and an
  [SSH agent](ssh.md#storing-your-key-passphrase).
- **Find out where to keep your files**: see [storage](storage.md).
- **Find the software you need**: see [modules](modules.md).

## Managing your account later

Use the same SAFE login to:

- **reset your COSMA password** or **add a new SSH key**: Login accounts, then
  your COSMA account (see
  [forgotten passphrase or password](ssh.md#forgotten-passphrase-or-password));
- **join another project**: COSMA allows only one account per person, so
  select your existing COSMA account in the Login accounts menu and request
  access to the other project from there;
- **see your project's usage and allocation**.

If you cannot log in to SAFE itself, contact SAFE support at
dirac-support@epcc.ed.ac.uk.  For problems with your COSMA account, contact
cosma-support@durham.ac.uk.

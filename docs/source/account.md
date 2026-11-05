# Getting an account

To get a new COSMA account, you need to apply via the [DiRAC SAFE
system](https://safe.epcc.ed.ac.uk/dirac/)

When creating your account, it is essential that you upload an ssh
key. You should also select the project to which you will belong. This
will either be a DiRAC project, a [HPC Hardware Lab testbed project](project.md) or if you are a local Durham user (for COSMA5), please select project hpcicc.

Once this form has been submitted and authorised by the project PI,
you will then have to wait for COSMA staff to create your account. You
will be notified by email.

Detailed instructions are available below.

You will need a [ssh key](sshkey.md).

Once you can log in, see [your first job](firstjob.md).


## Accessing Cosma

First, you need a SAFE account,

- (Service Administration From EPCC)
- Used for all DiRAC facilities.
- In summary: 
 - [https://safe.epcc.ed.ac.uk/dirac/](https://safe.epcc.ed.ac.uk/dirac/)
 - Create an account (institutional email, not personal email)
 - Upload an ssh key
  - Select your project e.g. hpcicc or dpXXX (ask your supervisor)
  - Select COSMA (not COSMOS)
  - Wait...

![Creating an Account](images/DiRACSAFEscreen.png)

![Creating an Account](images/account2.png)

![Creating an Account](images/account3.png)

![Creating an Account](images/account4.png)

![Creating an Account](images/account5.png)

![Creating an Account](images/account6.png)

![Creating an Account](images/account7.png)

![Creating an Account](images/account8.png)

![Creating an Account](images/account9.png)

![Creating an Account](images/account10.png)

  - While the account is first authorised...
  - And then created...
  - Finally, you will receive an email!

![Creating an Account](images/account11.png)

cosma-support will then add your key to the system (so it might take a
few minutes, depending how busy we are).

To avoid having to enter your passphase every time you ssh to COSMA,
you can use an ssh-agent. e.g. in your local .bashrc file, you can put
something like: `eval $(keychain --eval /path/to/id_rsa 2> /dev/null`)

Note, you can use the same public key on other systems,
e.g. mira.dur.ac.uk, hamilton.dur.ac.uk, github, etc, provided the
private part remains on your system.  Take great care with the private
part.

You will also require a password (in addition to the ssh key passphrase) to log in to COSMA.  This will be provided in your welcome email, and you will be asked to reset it the first time you ssh in.  Note, this means that you will need to enter the temporary password twice (once to log in, and once to being the password reset process), and then enter a new password of your choice twice.  It needs to be at least 16 characters long and contain 2 character classes (lower case, upper case, numeric, special).

If you don't like to enter your password too many times, you can [set up a ssh control tunnel](ssh.md#reusing-ssh-connections).

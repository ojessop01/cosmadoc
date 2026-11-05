# Using VS Code with COSMA

Although we would recommend Emacs, many users prefer VS Code.  The following guidance is under review, and if you spot anything that could be changed, please let us know or put in a pull request.

## Install VS Code

Install Visual Studio Code on your local computer.

You’ll also want the Remote-SSH extension from Microsoft. It allows VS Code to connect directly to the HPC login node over SSH.  Avoid the "Remote Tunnels" feature.

## Make sure SSH works

First, test the HPC connection from a normal terminal:

```
ssh -i /path/to/ssh/key username@loginX.cosma.dur.ac.uk
```

Replace the hostname and username with those relevant for you.  You will be asked for your ssh key passphrase, then your COSMA password.

## Add COSMA to your SSH config

VS Code uses your normal SSH settings, so add an entry for COSMA.  On your local computer, create the folder for shared connections:

```
mkdir -p ~/.ssh/controlmasters
```

Then add this to `~/.ssh/config`, changing USERNAME, the key and the login node to suit you:

```
Host cosma8
    HostName login8.cosma.dur.ac.uk
    User USERNAME
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 8h
```

Test it from a normal terminal with `ssh cosma8`.  The ControlMaster lines share [one connection](ssh.md#reusing-ssh-connections) between your terminals and VS Code, so that you only need to authenticate once per session.  They are not supported by the SSH client included with Windows, so leave them out if you are using Windows, and expect to enter your password more often.  Take care, because too many failed logins will get you banned.

`login8` picks one of the two COSMA8 login nodes.  To always use the same one, use `login8a` or `login8b` for the HostName.

## Configure VS Code

In VS Code:

- Install Remote-SSH.
- Open the Command Palette with Ctrl+Shift+P (Cmd+Shift+P on macOS).
- Select Remote-SSH: Connect to Host...
- Select `cosma8`, the host that you added to your SSH config

VS Code will establish an SSH connection and install its remote components on the HPC system.  Using your /cosma/apps space is good for this.

A new VS Code window will open. The bottom-left corner should indicate that you are connected to the remote machine.

You will need to enter your passphrase and password.  If you do not see a prompt for them, turn on `remote.SSH.showLoginTerminal` in your local VS Code settings, so that the login appears in a terminal.

If you get your VS Code setup wrong, it will repeatedly try to access COSMA, fail, and you will quickly be banned after a few failed attempts.  This ban is initially temporary (10-15 minutes), but if you are repeatedly banned, you will then automatically be placed under a permanent ban.  If this is the case, fix your setup, and then contact cosma-support to get yourself unbanned.

## Open your project

Once connected, use:

File → Open Folder

and select your project directory on the HPC filesystem, for example:

/cosma/home/project/your_username/my_project

You can now edit files as though they were local files, but the files actually reside on the HPC system.

## Use the integrated terminal

Open:

Terminal → New Terminal

The terminal is running on the HPC system, so commands such as:

```
pwd
ls
module avail
```

are executed remotely.

Modules also work:

```
module load python
python my_script.py
```

## Set up Python

Without any setup, Python on COSMA is the system version (3.9), which has few packages.  Instead, use a [virtual environment](python.md#installing-python-libraries) and tell VS Code about it.

1. In the VS Code terminal, create a virtual environment in your app space:

    ```
    module load python/3.12.4
    python -m venv /cosma/apps/PROJECT/USERNAME/venvs/myenv
    source /cosma/apps/PROJECT/USERNAME/venvs/myenv/bin/activate
    pip install numpy
    ```

    Replace `numpy` with the packages that you need.  Add `ipykernel` if you want to use notebooks.

2. In the Extensions panel, install the Python extension, using the button that installs it on the remote host.
3. Open the Command Palette and select Python: Select Interpreter.
4. Select Enter interpreter path, and enter `/cosma/apps/PROJECT/USERNAME/venvs/myenv/bin/python`.

To check that it worked, open a new terminal and run `which python`.  It should print the path to your virtual environment.  If it does not, run the `source` command above.

You do not need to load the Python module again to use the environment.  You may still need other modules, such as MPI or HDF5, if your packages were compiled against them.

The gn002 and gn003 nodes use ARM processors, so they need their own virtual environment.

### Notebooks

To use notebooks, also install the Jupyter extension on the remote host and `ipykernel` in your virtual environment.  Open a notebook, click Select Kernel, and select your virtual environment.

Anything that you run with the Run button or in a notebook runs on the login node, so please keep it short and small.  For anything larger, submit a [Slurm job](slurm.md), or [launch Jupyter on a compute node](jupyter.md#launching-jupyter-lab-on-a-compute-node).

## Don't normally run heavy jobs on the login node

This is one of the most important HPC rules.

The login node is generally intended for lightweight tasks such as:

- editing files
- compiling small programs
- inspecting files
- submitting jobs
- managing environments

Don't run a long-running or computationally intensive program directly from the VS Code terminal.

Instead, submit your work to the [Slurm batch scheduler](slurm.md).

## Running interactive jobs

For development, debugging, or testing, an interactive compute session is often more convenient.

For example:

```
srun -p PARTITION -A ACCOUNT --pty --cpus-per-task=4 --mem=8G --time=01:00:00 bash
```

Once the job starts, your VS Code shell is running on a compute node rather than the login node.

You can then run your program:

python my_script.py

This is particularly useful when you need access to GPUs or other compute-node resources.

## Using VS Code for debugging

VS Code can be especially useful for debugging Python or other languages remotely.

A typical workflow is:

Local computer -> SSH -> Login node -> Job submission -> Compute node -> Your job

For straightforward development, you can edit the code through VS Code and use the terminal to submit jobs.

For more advanced workflows, VS Code can also attach to an interactive compute node, allowing you to use features such as the debugger, Python interpreter, Jupyter notebooks, and language servers on the compute node.

## Prevent VS Code from scanning large HPC filesystems

Avoid opening VS Code directly on large directories as a workspace root.  It will typically scan all files within your workspace, which can cause problems.  Open the specific project subdirectory instead.

You should avoid allowing VS Code to index or search entire filesystems such as /snap*, /cosma*,  since recursive scanning can generate a large amount of filesystem traffic and may negatively affect both your session and the system.

VS Code provides settings that let you exclude directories from file watching, searching, and Explorer operations.

For example, add the following to your VS Code settings.json:

```
{
    "files.watcherExclude": {
        "**/.git/**": true,
        "**/cosma/**": true,
        "**/cosma8/**": true,
        "**/cosma7/**": true,
        "**/cosma7/**": true,
        "**/cosma6/**": true,
        "**/cosma5/**": true,
        "**/snap8/**": true,
        "**/snap7/**": true,
    },

    "search.exclude": {
        "**/.git/**": true,
        "**/cosma/**": true,
        "**/cosma8/**": true,
        "**/cosma7/**": true,
        "**/cosma7/**": true,
        "**/cosma6/**": true,
        "**/cosma5/**": true,
        "**/snap8/**": true,
        "**/snap7/**": true,
    },

    "files.exclude": {
        "**/.git/**": true,
        "**/cosma/**": true,
        "**/cosma8/**": true,
        "**/cosma7/**": true,
        "**/cosma7/**": true,
        "**/cosma6/**": true,
        "**/cosma5/**": true,
        "**/snap8/**": true,
        "**/snap7/**": true,
    }
}
```

You can also add your own directories, for example if you have a large data directory, you can exclude that.

### Excluding HPC-wide filesystems

Be particularly careful if you have opened a high-level directory such as:

```
/cosma/home/PROJECT/your_username
```

If these contain many projects, datasets, or millions of files, don't open the whole directory in VS Code. Instead, open the specific project:

```
/cosma/home/PROJECT/your_username/project_a
```

This is usually preferable to trying to exclude everything else after opening a huge filesystem hierarchy.

### Git repositories

For large repositories, .git directories should normally be excluded from file watching and searching:

```
{
    "files.watcherExclude": {
        "**/.git/**": true
    }
}
```

VS Code and Git can otherwise generate substantial filesystem activity in large repositories.

### Extensions can also scan files

The VS Code core isn't the only source of filesystem activity. Extensions such as Python, C/C++, language servers, linters, Git tools, and notebook extensions may scan files independently.  Please consider:

- installing only extensions you actually need;
- excluding large data/output directories;
- avoiding opening your entire home or project hierarchy;
- keeping datasets and generated output outside the source tree where practical;
- checking extension-specific settings if an extension is still scanning files.
- Be cautious with extensions which run local language servers, linters or formatters when saving for large code bases as these can cause high login node load and run continuously in the background.
- If VS Code starts running slowly, disable extensions.

## A good HPC principle

Only open the smallest directory that contains the code you are currently working on.

For example, prefer:

/cosma/home/project/username/src/my_project

over:

/cosma/home/project/username

This reduces unnecessary filesystem operations and makes VS Code considerably more responsive.

Also, don't assume that files.watcherExclude prevents every form of scanning. It primarily controls file watching; search, language servers, Git, and individual extensions can have separate mechanisms and settings.

# Understanding VS Code connections

You cannot SSH directly to a compute node.  VS Code connects to a login node, and therefore anything that VS Code itself runs (e.g. extensions, linters, kernels) also run on the login node, which is a shared resource.  You should therefore try to keep the VS Code footprint to a minimum.

Use VS Code for editing and file work.  Testing of code, debugging and full jobs should be submitted to Slurm.

The VS Code Remote-SSH button is a single click which makes it tempting to use by default for everything.  Every connection starts a persistent server process on the login node.  Therefore you should use it when:
- You need to debug interactively as you edit
- You're working with files that are impractical to copy locally

You should edit locally (e.g. on your laptop) not using Remote-SSH when:
- You're just writing or editing source files
- You want full local VS Code performance and don't need a live connection to COSMA
- You're making small, occasional edits and don't need a server process sitting on the login node for the whole session.

In this case, edit the files locally in a non-remote VS Code window and use rsync, or better, git, to transfer them to COSMA to run something.

# File system and quota awareness

The Remote-SSH extension installs a server into ~/.vscode-server on first connection to each login node. This can be troublesome, mostly because the home directory is usually reserved for code, may have a limited storage quota, and the remote server can take up a lot of space.

## Selecting vscode-server installation path

COSMA already provides a specific storage space more appropriate for this kinds of applications in the Apps space. To achieve this, you can change the default installation path of the vscode-server to a more appropriate location.

For this one needs to change the local VS Code setting `remote.SSH.serverInstallPath` to decide where the server is installed. To open the **local user** settings:

- Open the Command Palette (CTRL + Shift + P on Windows/Linux or CMD + Shift + P on Mac)
- Type *">open settings"* (you must include the '>' at the beginning)
- Open User Settings (JSON)

In the VS Code user settings (`settings.json`), you can add the following configuration:

```
"remote.SSH.serverInstallPath": {
    "remote_host_name": "/desired/location",
}
```

- Replace `remote_host_name` with the name of the remote host you are connecting to (as defined in your SSH config file).
- Replace `/desired/location` with the path where you want the vscode-server to be installed, in this case the path to your Apps space provided by COSMA.

This should reduce the footprint of the vscode-server installation in your home directory and make better use of the available storage space on the remote server. Once you have made this change, the next time you connect to the remote server, VS Code will install the vscode-server in the specified location instead of the default home directory and you can safely remove the previous installation from your home directory if needed.

## AI assistants

AI coding assistants (Copilot, the ChatGPT extension, and similar) are
worth singling out because several are known to run continuously in
the background - polling, sending telemetry, or maintaining a
connection - rather than only acting when you invoke them.

Check the extension's own settings for anything related to auto-completion, background suggestions, or telemetry, and turn it off if you only want it available on demand. For the ChatGPT extension specifically, look for and disable auto-triggered/inline suggestion settings and any "keep session alive" style options - leave it as invoke-on-request only.

Many extensions don't actually need to run on the remote host at all - VS Code lets you force an extension to run only in the local UI process (your laptop) instead of on the remote server, via remote.extensionKind in your local settings.json:

```
 {  "remote.extensionKind": {    "publisher.chatgpt-extension-id": ["ui"]  }}
```

- Replace with the actual extension ID - check the extension's page or right-click it in the Extensions view for its ID). This stops it from spinning up a background process on the shared login node entirely, while still being usable from the same window.
- If an assistant extension needs deep workspace/file access to be useful (rather than just chat), forcing it to the local UI may limit some features — check its docs. But for anything you're using mainly as a chat sidebar rather than something reading your remote files directly, the local UI is usually sufficient and avoids adding background load to the login node.

# Tips with Extensions

## Recommended extensions

Every extension adds some load, so please only install what you need:

| Extension | Install on | Use it for |
| --------- | ---------- | ----------- |
| Remote - SSH | Your local computer | Connecting to COSMA |
| Python | COSMA | Choosing an interpreter, and debugging |
| Jupyter | COSMA | Notebooks |
| C/C++ or clangd | COSMA | Writing C and C++ |

When connected to COSMA, the Extensions panel shows which extensions are installed locally and which are installed on COSMA.

## C/C++

The C/C++ extension (`ms-vscode.cpptools`) or `clangd` will index your codebase on open. On large repositories - especially ones with big third-party header trees - this is one of the heaviest things VS Code can do on a login node, both in CPU and in filesystem metadata traffic.

- Generate a compile_commands.json (e.g. via CMake with CMAKE_EXPORT_COMPILE_COMMANDS=ON) so the language server indexes only what your build actually uses, rather than guessing include paths broadly.

`cpptools` specifically has been observed generating a lot of background activity on remote connections - continuous parsing, logging, and re-scanning even when you're not actively editing. In your remote workspace settings (.vscode/settings.json in the folder you open on the remote host), the following cut this down significantly:

```
 {  "C_Cpp.intelliSenseEngine": "disabled",  "C_Cpp.autocomplete": "disabled",  "C_Cpp.loggingLevel": "None",  "C_Cpp.workspaceParsingPriority": "low",  "C_Cpp.intelliSense.maxCachedProcesses": 1,  "C_Cpp.maxConcurrentThreads": 1}
 ```
 
Setting intelliSenseEngine and autocomplete to disabled assumes you're using clangd instead for actual code intelligence — clangd tends to be lighter and gives more direct control over indexing via its own arguments, e.g.:

```
{  "clangd.arguments": ["--background-index=false", "-j=1"]}
```

## Python

Point the Python extension to the correct Python interpreter, as described in [Set up Python](#set-up-python).

The `pylance` extension indexes your workspace, so exclude this behaviour similarly to the C/C++ section.

## Fortran

The `fortls` language server should be configured with the correct module and include directories so that it does not scan unnecessarily.

# Security

Running untrusted VS Code extensions can lead to security issues.

- Make sure you keep your SSH keys pass-phrase protected incase these get exfiltrated by an extension, and do not syncronise them to unencrpyted cloud storage.  Explicitly exclude your `~/.ssh` folder from sync.
- Avoid SSH agent forwarding (ForwardAgent yes) to login/compute nodes, as this exposes your agent socket on the remote host, allowing others to potentially authenticate elsewhere as you.
- Keep your VS Code and OS up to date.
- Be selective with extensions.
- Use the VS Code Workspace Trust feature when opening directories you do not fully control.


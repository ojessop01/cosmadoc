# Project codes

Every COSMA account belongs to a project, identified by a project code.  You
give the code when you [request your account](account.md) on SAFE, and use it
as the Slurm account (`-A`) when you submit jobs.  The project's PI or manager
must approve your request, so make sure they know who you are.

| You are | Project code |
| ------- | ------------ |
| Part of a DiRAC project awarded time by the Resource Allocation Committee (RAC) | `dpXXX`, a three-digit number: ask your project's PI |
| Using the HPC Hardware Lab | One of the codes below |
| A Durham user, or a collaborator, using COSMA5 | `hpcicc` |
| Wanting FLAMINGO data | `do012` (see [project data](projectdata.md)) |

## HPC Hardware Lab projects

For the [HPC Hardware Lab](hardwarelab.md), use one of these codes (others may
also exist; ask cosma-support if none fits):

| Code | For |
| ---- | --- |
| `do009` | DINE and training |
| `do015` | The DINE2 queue, including A30 and V100 GPUs |
| `do016` | NVIDIA GPUs, including Grace Hopper, Hopper and Blackwell, and the `cosma8-shm` queue (A100) |
| `do017` | Intel GPUs |
| `do018` | AMD GPUs (MI100, MI210, MI300A and MI300X) |
| `do023` | The Tenstorrent RISC-V system |
| `dr004` | DiRAC training |

## Which account to use for jobs

If you belong to more than one project, choose the one to charge each job to
with `-A`, for example `#SBATCH -A dp004`.  `mybalance` lists your DiRAC
projects, with each one's allocation this quarter and how much has been used
(see the [FAQ](faq.md#how-do-i-check-my-project-s-allocation)).

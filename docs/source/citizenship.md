# Good citizenship guide

- Please remember that login nodes are a shared resource
  - Interactive jobs
  - Testing
  - Compilation
  - Post-analysis

- Please do not run interactive jobs on batch queues unless essential
  - in which case please do not let them remain idle
    - Idle jobs in queues waste precious compute time

- Please do not run long non-interactive jobs on login nodes
  - for more than a few seconds
  - These are better submitted to the queues

- Please do not run jobs that will hog memory on login nodes

- Do not share your account details with anyone else
  - They should apply for their own account

- Follow common sense
  - Do not use COSMA as a VPN
  - Do not attempt to use sudo
  - Do not install dodgy or malicious software
  - Do not try to circumvent any software licences
  - Do not run unlicenced or illegal software
  - Only use COSMA for your authorised scientific workloads

- If you see problems, please let us know

There are some [policies](policies.md) which should be adhered to.

```{note}
Large numbers of queued jobs and frequent submissions can slow down the
scheduler for everyone. Use job arrays for similar runs, and consider grouping
very short tasks into fewer jobs. Avoid submitting jobs in a tight loop.

Job-count limits can differ between users and accounts. Check your own limits
before a large campaign; another user's limit may not apply to you. Contact
COSMA support if you need to discuss a large submission.
```

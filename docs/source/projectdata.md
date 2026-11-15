# Project data

Some projects make the data they produce on COSMA available to other
researchers.  For data available on the web, see [data links](links.md).

## FLAMINGO

To work with data from the [FLAMINGO](https://flamingo.strw.leidenuniv.nl/)
simulations on COSMA:

1. Create a [SAFE](https://safe.epcc.ed.ac.uk/dirac/) account, if you do not
   have one (see [getting an account](account.md)).
2. Request a COSMA login account for project **do012**.

Once your account is set up, you can log in to COSMA and read the data from
the login nodes, and run analysis jobs through Slurm.

```{note}
In November 2026 no Slurm queue accepted jobs from the `do012` account, and
the `flamingo` queue named in earlier versions of this page no longer exists.
Contact cosma-support to find out which queue and account to use for
analysis jobs.
```

For anything more than a quick look, use a [batch job](slurm.md) rather than
an interactive session: an interactive session holds its resources even while
you are not using them.

If you need the data without a COSMA account, an S3-compatible share can be
made available, which lets you mount the data on your own system.  Contact
cosma-support if this would be useful.  For reading FLAMINGO data remotely,
see also the FLAMINGO HDF5 streaming service on the
[data links](links.md) page.

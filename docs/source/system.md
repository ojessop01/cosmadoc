# System Usage

This page explains how to see what the system, and your jobs, are using.  For
the Slurm commands to check a job, see [monitoring jobs](slurmtips.md#monitoring-jobs).

## Nightly batch and disk use

Each night the batch queues and filesystems are processed to produce summary
information about the usage of the various SLURM clusters and main storage
file systems up to that time.

All this can be viewed in the usage web pages found at:

* [https://virgodb.cosma.dur.ac.uk/usage/index.php](https://virgodb.cosma.dur.ac.uk/usage/index.php)

This is where you can find out if your DiRAC project has gone over budget for
the current quarter (when this happens your submissions will be automatically
demoted to the pauper queue) or how your usage is progressing, as well as who
is using the project storage (you can only view your own quotas and those of
groups you belong to using the command-line tools). To access this you will
need your COSMA username and password.

For simplicity some of this information can be viewed from the command line
once logged in using the commands:

    $ diracusage

and

    $ diskusage

note you will need the cosma module loaded (this happens by default, unless
you have changed this in your login scripts). They have many options, use the
`--help` flag to see these.  `diracusage` is the same command as `mybalance`:
see [how do I check my project's allocation?](faq.md#how-do-i-check-my-project-s-allocation)

## Seeing the resources used by a running job

To analyse usage of a node running a current job, you can use Performance Co-Pilot or the cjobload command.  The example output on this page comes from older jobs, so the numbers will differ from yours.

## cjobload

Running: `cjobload -n 2 JOBID` will show the CPU load and RAM for the job given, every 2 seconds, for each node used by the job.
There are also `c8jobload`, `c7jobload`, `c7rpjobload` and `c5jobload` variants that show value for all the currently running jobs
on these partitions. See the `--help` of `cjobload` for additional options.


## Performance Co-Pilot

Performance Co-Pilot (PCP) is a system for monitoring the status of computers,
and is installed on the compute nodes of COSMA. Some of the information that
it monitors (so called metrics) is available for remote access, so you can use
it to check things like the load and memory use of any node, without any need
for special privilege (logging into compute nodes is not allowed, unless you
are a member of the developers group).

There are a lot of commands that PCP offers, somewhat overwhelming at first
glance (and documentation is usually focused on system configuration), so we
have a couple of scripts that should show things that are useful when
determining if a job is using the compute resources as expected. So they show
the activity of the CPUs and memory use:

    $ pcpslurmnode
    $ pcpslurmjobs

See the `--help` output for more options, but for instance if you know the
node `m8001` is running your job you can do:

    $ pcpslurmnode m8001
    #-  Node: m8001, Cpus: 256, Tasks: 3326 total, 129 running, 51 sleeping
    #-  Memory: 1006.92 total, 360.25 free,  Load averages: 128.67,128.58,128.49
    # JobID              CPUs   NodeCPU%        Mem   NodeMem%
    # -----              ----   --------        ---   --------
      9175206          128.32      50.13     625.37      62.11

Interesting numbers here, other the obvious use of CPUs and memory are the
number of processes and the 1, 5 and 15 minute load averages, these are all
suggesting that the correct numbers are being used, i.e. 128. Higher loads
usually indicate that too many processes or threads are being used.

You can also give a range of nodes or more node names, but to see all the
nodes for a job use:

    $ pcpslurmjobs 9175206
    # Node usage by jobs (for detailed usage use pcpslurmnode):
    # Node       JobID            CPUs        MEM
    # ----       -----            ----        ---
      m8146      9175206        127.40    625.123
      m8075      9175206        127.31    625.477
      m8266      9175206        127.38    623.506
      m8152      9175206        127.27    625.148
      m8145      9175206        127.37    625.218
      m8156      9175206        127.38    623.514
      m8279      9175206        127.35    625.228
      m8330      9175206        127.37    623.851
      m8252      9175206        127.38    623.873
      m8001      9175206        127.36    625.381
      m8086      9175206        127.44    625.404
      m8155      9175206        127.32    624.141
      m8288      9175206        127.37    624.376
      m8044      9175206        127.40    625.231
      m8267      9175206        127.40    624.737
      m8278      9175206        127.33    624.779
      m8251      9175206        127.36    622.996
      m8167      9175206        127.33    623.896
      m8277      9175206        127.43    624.720
      m8265      9175206        127.38    623.966
      m8111      9175206        127.40    625.391
      m8280      9175206        127.42    623.801
      m8161      9175206        127.35    623.892
      m8154      9175206        127.37    624.156
      m8169      9175206        127.40    624.374

    # Summary of job usage:
    # JobID            CPUs   CPUsNode  CPUsEffic     MemTotal     MemNode   MemEffic   NumNodes
    # -----            ----   --------  ---------     --------     -------   --------   --------
      9175206       3184.26     127.37      99.51     15612.18      624.49      62.08         25

So you can see this job is probably using an MPI rank per core and has a high
memory use.

The following descriptions offer a somewhat arbitrary number of other,
hopefully, useful commands.

### Machine Overview

To get a more detailed overview of memory and cpu usage on a compute node, use
the command pmstat with the -h option to query:

    $ pmstat -h m7014
    loadavg                         memory      swap       io    system         cpu
        1 min   swpd   free   buff  cache   pi   po   bi   bo   in   cs  us  sy  id
        27.00      0   478g 177040  2249m    0    0    0    0  29K 2924  47   1  52
        27.00      0   478g 177040  2249m    0    0    0    0  28K 1831  47   1  52

This is updated every 5 seconds until interrupted. You can change the update
interval to get a faster or slower rate using the -t flag:

    $ pmstat -h m7014 -t 1min
    $ pmstat -h m7014 -t .5sec

You can also query more than one node at a time:

    $ pmstat -h m7014 -h m7250
    node    loadavg               memory      swap        io    system         cpu
              1 min   swpd   buff  cache   pi   po   bi   bo   in   cs  us  sy  id
    m7014.p   27.00      0   478g  2249m    0    0    0    0  28K  742  47   1  52
    m7250.p   28.00      0   442g 20604m    0    0    0    0  29K 1262  49   1  50
    m7014.p   27.00      0   478g  2249m    0    0    0   11  29K 3774  47   1  52
    m7250.p   28.00      0   442g 20604m    0    0    0   25  29K 1250  49   1  50
    m7014.p   27.00      0   478g  2249m    0    0    0    0  28K 1793  47   1  52
    m7250.p   28.00      0   442g 20604m    0    0    0   20  29K 1146  49   1  50

In this output, the column headed buff shows the free memory.

The pmstat man page describes the various fields, but loadavg is probably the
first thing to look at, it is roughly the number of runnable processes (not
quite, for more details see the uptime man page). In general this should not
exceed the number of physical cores on the machine, so an optimal load for
COSMA7 is 28 and for COSMA8 128. If your code uses hyper-threads then these
numbers may double. In this case we can see a job using fewer cores, this may
be necessary to achieve the memory use per core. Hybrid codes will also not in
general show loads equal to the numbers of cores as they will not be
continually runnable (it would be nice if they were, however don't be fooled
into thinking that is bad, most MPI codes that use a single rank per core are
also not continually busy, they are usually just spinning the CPU waiting for
communication).

You can get the 1min, 5min and 15min loads using the pcp dstat sub-commands:

    $ pcp -h m7001 dstat -l
    ---load-avg---
    1m   5m  15m
    27.9 27.8 27.7
    27.9 27.8 27.7
    27.9 27.8 27.7
    27.9 27.8 27.7

dstat also has options to report cpu and memory use as well. See the pcp-dstat
man page.

### Detailed Memory Use

The memory profile of the whole machine is important when understanding if
your code is making optimal use of the memory. There are various commands that
report memory use, but a good one is:

    $ pmrep -h m7420 :sar-r
                kbmemfree kbmemavai kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
    17:44:30    337693080 386612632 190087944     36.02    128736  49919624 127783768     23.84 146485992  29643324       188
    17:44:31    337693080 386612632 190087944     36.02    128736  49919624 127783768     23.84 146485992  29643324       188
    17:44:32    337693080 386612632 190087944     36.02    128736  49919624 127783768     23.84 146485992  29643324       188
    17:44:33    337685304 386610904 190095720     36.02    128736  49926392 127783768     23.84 146488008  29647356     10716

This is a clone of the output from the sar -r command, and reports much of the
node memory information from the /proc/meminfo file. The pmrep command, like
pcp dstat has a large number of possible reports, these defined in the file
/etc/pcp/pmrep/pmrep.conf

### NUMA Balance

A well behaved batch job will distribute itself over the all the cores and
sockets of the machine. A classic issue is sharing a single core with more
than one pinned thread, so checking that both the CPUs and cores are loaded as
expected can be a good idea. The socket balance can be seen using:

    $ pmrep -h m7400 :numa-per-node-cpu
                NUMA n      %usr     %nice      %sys   %iowait    %steal      %irq     %soft    %guest    %gnice     %idle
    17:47:09     node0     49.97      0.00      0.04      0.00      0.00      0.00      0.00      0.00      0.00     50.01
    17:47:09     node1     50.05      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00     50.01
    17:47:10     node0     50.00      0.00      0.07      0.00      0.00      0.00      0.00      0.00      0.00     49.92
    17:47:10     node1     49.92      0.00      0.14      0.00      0.00      0.00      0.00      0.00      0.00     50.00

This report may show N/A for every value, because some metrics cannot be read
remotely.  If so, use the per-core report below instead.

In this case the balance is good, each NUMA node has the same work and all the
cores are in use as 50% equals all the physical cores -- the other 50% would
be used if hyper-threading was required. Note that nodes in this case are a
equivalent to a socket holding a CPU, some architectures allow CPUs to be
split into more NUMA regions (COSMA8 has 4 per socket), usually depending on
how the memory is accessed.

The activity per core can be seen using:

    $ pmrep -h m7400 :mpstat-P-ALL

the output can be very long (256 lines for COSMA8), but looking closely you
can see which CPUs are active. If you have pinning enabled these should remain
fixed.

### Infiniband Use

The only IO of interest on a typical node is how much traffic is being
generated on the infiniband fabric, there are potentially a lot of metrics
that can be reported about this, but the command:

    $ pmrep -h m7400 infiniband.port.total.bytes -t 3s -b MB

will report the total megabytes per second averaged over 3 seconds.

### Visualization

The metrics that can be reported from a node can be seen using the command:

    $ pminfo -h m7400

each of these can be queried using the pmval or pmrep commands, they can also
be visualized in a graph using the pmchart command. This is very flexible and
can be used to see the metrics of more than one node at a time, as in:

    $ pmchart -h m7001 m7002 m7003

you can then select the metrics of interest from the nodes for comparison and
can also capture the information. There is fuller help at
[here](https://pcp.io/docs/lab.pmchart.html)

The CPU value defines a view which are some predefined plots. Other useful
views are Memory and Overview, but if using Overview increase the vertical
size to 1000. On COSMA the infiniband read and write rates are also available
in the IB view.

### Final Words

As was noted at the beginning, and if you have looked at the output of pminfo,
PCP will allow you to monitor a lot of details of the compute nodes, but there
are some limitations. The metrics that make reports at the process level
require privilege that is not available using remote access, so if you try
them they will fail (a shame as pcp atop, would be very nice, like a remote
top command). All metrics are available locally, just leave the -h part out.

It is also not possible to see any archival material, so you need to check
things when your job is running.

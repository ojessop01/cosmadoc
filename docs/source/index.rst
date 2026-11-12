Welcome to the COSMA support documentation!
===========================================

.. image:: images/logocosma.jpg

The Compute Optimised System for Modelling and Analysis (COSMA)
includes:

* The DiRAC Memory Intensive Service

  * Two generations of the COSmology MAchine (COSMA7 and COSMA8)

* The Institute for Computational Cosmology internal HPC service

  * COSMA5

* The HPC Hardware Lab national facility

COSMA can also refer to the :doc:`Carbon Optimising System <environmental>` for
Modelling and Analysis.
 
For an overview of the system, see :doc:`cosma` and :doc:`facilities`.

New to COSMA?
-------------

Follow these pages in order to go from no account to running jobs:

1. :doc:`account`: apply for an account through SAFE, with an SSH key and a
   project code (see :doc:`project`).
2. :doc:`ssh`: log in for the first time, and set up SSH so you do not have to
   type passwords repeatedly.
3. :doc:`firstjob`: run your first batch job, step by step.
4. :doc:`storage`: where to keep your files, and how much space you have.
5. :doc:`modules`: find and load compilers, libraries and other software.
6. :doc:`citizenship`: how to use the shared login nodes and queues fairly.

When something goes wrong, see :doc:`jobproblems`, the :doc:`faq`, or
:doc:`contact`.

.. note::

   COSMA is in an :doc:`draperperiod`.

.. note::

   Downtimes: COSMA has 3 periods of scheduled downtime per year, lasting up to a week, though typically the affected period is shorter. These are during the first full weeks of February, June and October (every 4 months). Current scheduled periods are:

   - 1-5th February 2027
   - 31st May - 4th June 2027
   - 4-8th October 2027
   
.. note::

   These pages are under active development.  If you see any
   out-of-date or incorrect information, please let us know!

Contents
--------

.. toctree::
   :maxdepth: 1
   :caption: ABOUT

   cosma
   facilities
   dirac
   essentials
   centreofexcellence
   excalibur
   cosma8

.. toctree::
   :maxdepth: 2
   :caption: GETTING STARTED

   account
   project
   sshkey
   ssh
   firstjob
   citizenship
	     
.. toctree::
   :maxdepth: 3
   :caption: SOFTWARE

   modules
   spack
   modulelist
   gitlab
   python
   containers
   jupyter
   mpi
   lustre
   acl
   x2go
   editors
   
.. toctree::
   :maxdepth: 4
   :caption: RUNNING JOBS

   slurm
   sbatch
   slurmtips
   queue
   slurmdetail
   system
   jobproblems

.. toctree::
   :maxdepth: 3
   :caption: AI CODING AGENTS

   agents
   agents-setup
   agents-uses
   agents-coding
   agents-optimisation
   agents-prompts
   agents-safe

.. toctree::
   :maxdepth: 4
   :caption: HARDWARE LAB

   hardwarelab
   hardwarelab-hybridnodes
   gpu
   gpujobs
   rockportlab
   dine
   dine2
   cpucomputelab
   amdgpu
   nvidiagpu
   composable
   quantum
   storagelab

   
.. toctree::
   :maxdepth: 4
   :caption: STORAGE AND DATA
	  
   storage
   data
   archive
   datacuration
   projectdata

.. toctree::
   :maxdepth: 4
   :caption: AZIMUTH CLOUD PORTAL
	  
   azimuth/index

.. toctree::
   :maxdepth: 5
   :caption: GETTING HELP

   codeperformance
   clusterupgrade
   faq
   rockport
   virgo
   issues
   presentations
   policies

.. toctree::
   :maxdepth: 6
   :caption: ADDITIONAL RESOURCES

   news
   technotes
   environmental
   links
   usefullinks
   movies
   industry
   acknowledgements
   contact

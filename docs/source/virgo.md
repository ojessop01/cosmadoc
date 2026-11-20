# VIRGO Disk Usage

Virgo disk quotas

## 1. Current projects

1.1 All users will have a disk quota of 5TB on COSMA-7 and 10TB on COSMA-8. These quotas may be revised in future depending on circumstances.

1.2 A temporary quota extension can be requested but will need a detailed justification. These temporary extensions are for a fixed time only (to be specified in the request) and are intended for users running big projects and processing files before they are either stored on tape or allocated to a project-specific account, as described in Section 2. At the end of a run the quota will be reduced back to normal. Requests should be made by email to a.r.jenkins@durham.ac.uk and c.s.frenk@durham.ac.uk, cc'ing cosma-support@durham.ac.uk.

1.3 Data that are part of a large Virgo project (EAGLE, FLAMINGO, FLARES, MTNG, etc.) should be "re-owned" to the project account, as explained in Section 2 below.

1.4 Once the quota is reached, the user will no longer be able to generate new data without freeing up space. They can do this by either:

a) transferring the data to tape and then deleting files

b) re-owning some files to a large project account as explained in Section 2 below

1.5 At the moment, transferring data to tape requires the user to ask cosma-support to do it. We are hoping to change this so that individual users can access the data storage directly. (We are waiting for the company that supplied the storage to fix a bug in their software.)

1.6 Data of people who have left Virgo will be stored in tape and deleted from disk, unless the person makes the case for some space, capped at 2TB. PhD student advisors are responsible for the data of their (former) students and, if no action is taken, the student's data will be counted against the supervisor's allocation. This policy will also come into effect on September 15th 2022.

## 2. Large projects and legacy datasets

These are datasets generated in projects that have either finished or are well advanced. These should be stored in a project-specific account overseen by a named person who is responsible for keeping a record of the files it contains, storing on tape data that are not frequently used and deleting files. As a project proceeds, individual users may own large files (see Section 1) but once a project is well advanced or completed, the files should be "re-owned" by the project account, as described below.

The list of current projects of this kind and the name of the person that I would like to nominate to be responsible are (if you would rather someone else was nominated just let me know):

- APOSTLE (Azi Fattahi)

- AURIGA (Francesca Fragkoudi)

- BAHAMAS (Ian McCarthy)

- COCO (Sownak Bose)

- COLIBRE (Matthieu Schaller)

- DOVE (Till Sawala)

- EAGLE (Matthieu Schaller)

- FLAMINGO (Matthieu Schaller)

- FLARES (Chris Lovell)

- HYDRANGEA/C-EAGLE (Yannick Bahe & Scott Kay)

- MACSIS (Scott Kay)

- MILLENNIUM* (Adrian Jenkins)

- P-MILLENNIUM (Carlton Baugh)

- MTNG (Volker Springel)

- SIBELIUS (Till Sawala)

* includes Millennium run, Millennium-II, Millgas and MXXL

2.1 The person responsible should ensure that all the relevant files are re-owned to these projects, by contacting the relevant people and asking [cosma-support](contact.md) to change the ownership. For example, they could ask sysadmin to execute a command such as `mv /cosma7/data/dp004/USER/somedir /cosma7/data/dp004/flares/ ; chown -R flares /cosma7/data/dp004/flares/somedir`.

All files associated with a project should be in the same location, as in this example. If you own a legacy file you should tell the person responsible immediately. If this person does not react reasonably swiftly, feel free to contact sysadmin and request the transfer to tape and then delete the file.

2.2 The person responsible should store on tape files that have not been used recently (by requesting this to cosma-support; make sure you keep a log of the files that have been stored on tape). The deadline is also SEPTEMBER 15th 2022.

2.3 As soon as the data are transferred to tape, the person responsible should delete the files from disk. Note that cosma-support keep two copies of all files on tape, one as backup in case of tape failure, or erasure code the data, ensuring that it can be retrieved in the event of a single tape failure.  However, this does not prevent data loss if two tapes fail.

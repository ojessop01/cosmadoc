# Rockport lab

The Rockport cluster is a 222-node production partition (`cosma7-rp`) equipped with a 100G 6D torus low-latency Ethernet fabric.  This is a "switchless" fabric as there is no central packet switching facility.  Rather, routes are determined on the fly, the best route is used, and packets pass through multiple cards on their way from source to destination.

[Usage instructions](rockport.md) are available.

## History

A 16-node prototype Rockport fabric was installed in 2021.  The success of this system led to the need to test at scale, and in 2022 half of the COSMA7 system was converted to Rockport, allowing a direct performance comparison between Rockport and COSMA7's InfiniBand fabric.

## Funding

This system is funded by ExCALIBUR and DiRAC.

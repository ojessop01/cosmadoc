# Tenstorrent QuietBox RISC-V Blackhole node

We have a single [Tenstorrent QuietBox](https://tenstorrent.com/hardware/tt-quietbox) node with 4x [p150 Blackhole cards](https://tenstorrent.com/en/hardware/cards).

The host system is a single AMD 8124P 16-core processor with 512GB RAM.

It is a highly capable system for AI inferencing, with further information in the [Tenstorrent documentation](https://docs.tenstorrent.com/).

## Accessing the Tenstorrent system

To access this system you need to join the do023 project, and then `ssh tenstorrent` from a login node.

## Usage of the Tenstorrent system

Most tenstorrent commands start with tt.  To access many of these, you will need to `source /opt/venv/tenstorrent/bin/activate` which makes commands like `tt-smi` available.

To install an updated software stack as a user, you may be able to follow the instructions here (though this may require root access):
[https://docs.tenstorrent.com/getting-started/README.html](https://docs.tenstorrent.com/getting-started/README.html)

### Resource sharing

From our testing so far, tenstorrent cards appear to prefer jobs to be run serially.
If a card is running an inference server, for example, it cannot also be used to run a tt-metalium
program.

We have not yet tested running multiple tt-metalium programs in parallel.

### tt-metalium

The tt-metalium library for C++ is installed on the machine; this is the low-level SDK for Tenstorrent devices.

Include the relevant headers like so:
```
#include <tt-metalium/host_api.hpp>
#include <tt-metalium/device.hpp>
#include <tt-metalium/...>
```

Note: tt-metalium requires that your compiler use at least the C++20 standard.
Example programs can be found [here](https://github.com/tenstorrent/tt-metal/tree/main/tt_metal/programming_examples).

When planning the structure of your program, it can be helpful to know the architecture of the device.

The p150 has:
- 120 Tensix cores (each containing 3 compute cores connected to a compute engine, 2 data-mover cores, and dedicated SRAM)
- 32GB of whole-device DRAM 
- 16 full RISC-V cores

In the previous generation of TT devices (wormhole), orchestration and memory movement was handled by the host CPU.  The introduction of 16 RISC-V cores on the card itself allows orchestration to be done on-device, reducing the reliance on PCIe transfers.
Most of the existing documentation for tt-metal assumes a wormhole device is being used, and therefore does not make use of the RISC-V cores.

Please try using the tools and give any feedback.

## Tutorials

There are a number of tutorials, podcasts and lectures on [GitHub](https://github.com/RISCVtestbed/tt-tutorial).

## Usergroup

If you would like to join a UK Tenstorrent research mailing list, please [contact cosma-support](contact.md).  Primarily for discussion between users.


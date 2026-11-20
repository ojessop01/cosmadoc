# Detailed GPU specification table

The initial version of this table was AI generated, and we are tidying up as time allows.

| Vendor / GPU | Architecture | FP64 Vector | FP64 Matrix / Tensor | FP32 Vector | FP16 Vector | FP16 Matrix / Tensor | FP8 Matrix / Tensor | Memory | Memory Bandwidth | Power | Interconnect / I/O |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| NVIDIA B200 | Blackwell | ~40 TFLOPS | Tensor accelerated | — | Not separately specified | ~2.25 PFLOPS | ~4.5 PFLOPS | 180 GB HBM3e | ~8 TB/s | ~1,000 W | NVLink 5 |
| NVIDIA H200 SXM | Hopper | ~34 TFLOPS | ~67 TFLOPS | ~67 TFLOPS | Not separately specified | ~989 TFLOPS | ~1,979 TFLOPS | 141 GB HBM3e | ~4.8 TB/s | ~700 W | NVLink 4 |
| NVIDIA H100 SXM | Hopper | ~34 TFLOPS | ~67 TFLOPS | ~67 TFLOPS | Not separately specified | ~989 TFLOPS | ~1,979 TFLOPS | 80 GB HBM3 | ~3.35 TB/s | ~700 W | NVLink 4, 900 GB/s |
| NVIDIA A100 80 GB SXM | Ampere | 9.7 TFLOPS | 19.5 TFLOPS | 19.5 TFLOPS | Not separately specified | 312 TFLOPS | — | 80 GB HBM2e | ~2.04 TB/s | 400 W | NVLink 3, 600 GB/s |
| NVIDIA A100 80 GB PCIe | Ampere | 9.7 TFLOPS | 19.5 TFLOPS | 19.5 TFLOPS | Not separately specified | 312 TFLOPS | — | 80 GB HBM2e | ~1.94 TB/s | 300 W | PCIe 4 / NVLink bridge |
| NVIDIA RTX PRO 6000 Blackwell | Blackwell | Not HPC-focused | — | 125 TFLOPS | Not separately specified | Tensor accelerated | FP8 supported | 96 GB GDDR7 ECC | ~1.6 TB/s | 600 W server | PCIe 5 |
| NVIDIA RTX PRO 4500 Blackwell | Blackwell | Not HPC-focused | — | — | Not separately specified | Tensor accelerated | FP8 supported | 32 GB GDDR7 ECC | >896 GB/s* | 165 W server | PCIe 5 |
| NVIDIA L40S | Ada Lovelace | Not HPC-focused | — | ~91.6 TFLOPS | Not separately specified | ~362 TFLOPS | FP8 supported | 48 GB GDDR6 ECC | ~864 GB/s | 350 W | PCIe 4 |
| AMD Instinct MI325X | CDNA 3 | 81.7 TFLOPS | 163.4 TFLOPS | 163.4 TFLOPS | Not separately specified | 1,307 TFLOPS | 2,615 TFLOPS | 256 GB HBM3e | 6 TB/s | 1,000 W | PCIe 5 + Infinity Fabric |
| AMD Instinct MI300X | CDNA 3 | 81.7 TFLOPS | 163.4 TFLOPS | 163.4 TFLOPS | Not separately specified | 1,307 TFLOPS | 2,615 TFLOPS | 192 GB HBM3 | 5.3 TB/s | 750 W | PCIe 5 + Infinity Fabric |
| AMD Instinct MI250X | CDNA 2 | ~47.9 TFLOPS | Matrix accelerated | ~47.9 TFLOPS | Not separately specified | ~383 TFLOPS | — | 128 GB HBM2e | ~3.2 TB/s | ~560 W | Infinity Fabric |
| Intel Data Center GPU Max 1550 | Xe-HPC | ~52.4 TFLOPS | XMX accelerated | ~52.4 TFLOPS | ~52.4 TFLOPS | ~839 TFLOPS XMX | — | 128 GB HBM2e | ~3.28 TB/s | 600 W | PCIe 5 + Xe Link |
| Intel Crescent Island / GPU D-Series | Xe3P | 10 TFLOPS | XMX accelerated | 20 TFLOPS | 41 TFLOPS | XMX accelerated; peak TBD | 1300 TFLOPS | 160 GB LPDDR5X reference | 1.5 TB/s | 350 W | PCIe |

## Notes
- All performance figures are theoretical peak values and should not be interpreted as application benchmark results.
- "Vector" distinguishes conventional GPU arithmetic from specialised matrix/Tensor/XMX operations.
- Matrix/Tensor values refer to dense performance where a dense figure is available. Sparse performance can be substantially higher.
- FP16 Matrix / Tensor and FP8 Matrix / Tensor values are not directly comparable with FP16 Vector performance.
- "Not separately specified" means a suitable vector FP16 figure was not clearly specified in the source data; matrix/Tensor throughput has deliberately not been substituted.
- NVIDIA A100 supports 9.7 TFLOPS conventional FP64 and 19.5 TFLOPS FP64 Tensor Core performance.
- AMD MI300X and MI325X provide 81.7 TFLOPS FP64 vector and 163.4 TFLOPS FP64 matrix performance.
- Intel Data Center GPU Max 1550 has approximately 52.4 TFLOPS FP16 vector performance, distinct from its much higher XMX matrix throughput.
- *The >896 GB/s RTX PRO 4500 figure is from the workstation specification, whereas the 165 W power figure is for the Server Edition; they should not be assumed to describe exactly the same board configuration.
- "-" indicates unsupported, unavailable, or not sufficiently established for a like-for-like comparison.

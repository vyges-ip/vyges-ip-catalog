# Vyges IP Catalog — Metadata Quality Scores

- **Aggregate:** 88/100
- **IPs scored:** 135
- **Good (≥80):** 121
- **Medium (60–79):** 6
- **High-risk (<60):** 8
- **Scorer:** [vyges/metadata-scorer-action@v1](https://github.com/vyges/metadata-scorer-action/tree/v1)

## Needs work (bottom 20)

| IP | Score | Tier | Top gap |
|---|---:|---|---|
| `caliptra-libs` | 40 | High-risk | interfaces: interfaces (none declared) |
| `caliptra-uart` | 40 | High-risk | interfaces: interfaces (none declared) |
| `coralnpu-i2c-master` | 40 | High-risk | interfaces: interfaces (none declared) |
| `coralnpu-rvv-backend` | 40 | High-risk | interfaces: interfaces (none declared) |
| `coralnpu-rvv-common-lib` | 40 | High-risk | interfaces: interfaces (none declared) |
| `coralnpu-tlul-pkg` | 40 | High-risk | interfaces: interfaces (none declared) |
| `coralnpu-tlul2axi` | 40 | High-risk | interfaces: interfaces (none declared) |
| `opentitan-flash-ctrl` | 40 | High-risk | interfaces: interfaces (none declared) |
| `hardfloat` | 60 | Medium | interfaces: interfaces (none declared) |
| `opentitan-racl-ctrl` | 60 | Medium | interfaces: interfaces (none declared) |
| `tech_cells_generic` | 65 | Medium | interfaces: interfaces (none declared) |
| `cf-sram` | 70 | Medium | interfaces: interfaces[].type=reset |
| `vyges-pinmux-lite` | 71 | Medium | implementation: asic{} or fpga{} |
| `opentitan-prim-xilinx` | 75 | Medium | interfaces: interfaces[].type=clock |
| `sky130-bandgap-reference` | 80 | Good | interfaces: interfaces[].type=clock |
| `sky130-opamp` | 80 | Good | interfaces: interfaces[].type=clock |
| `tlul-apb-adapter` | 80 | Good | interfaces: interfaces[].type=clock |
| `caliptra-ahb-lite-bus` | 83 | Good | interfaces: interfaces[].type=clock |
| `caliptra-datavault` | 83 | Good | interfaces: interfaces[].type=clock |
| `caliptra-edn` | 83 | Good | interfaces: interfaces[].type=clock |

## Top 20 (highest scores)

| IP | Score |
|---|---:|
| `fast-fourier-transform-ip` | 100 |
| `ibex` | 100 |
| `openfasoc-temp-sensor` | 100 |
| `opentitan-rv-core-ibex` | 100 |
| `opentitan-uart` | 100 |
| `vyges-rv-plic-lite` | 100 |
| `vyges-spi-host-lite` | 100 |
| `32bit-risc-core` | 98 |
| `adams-bridge` | 98 |
| `caliptra-aes` | 98 |
| `caliptra-csrng` | 98 |
| `caliptra-ecc` | 98 |
| `caliptra-entropy-src` | 98 |
| `caliptra-hmac` | 98 |
| `caliptra-prim` | 98 |
| `caliptra-sha256` | 98 |
| `caliptra-sha512` | 98 |
| `coralnpu-axi2tlul` | 98 |
| `coralnpu-core` | 98 |
| `coralnpu-spi2tlul` | 98 |

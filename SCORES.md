# Vyges IP Catalog — Metadata Quality Scores

- **Aggregate:** 88/100
- **IPs scored:** 146
- **Good (≥80):** 126
- **Medium (60–79):** 13
- **High-risk (<60):** 7
- **Scorer:** [vyges/metadata-scorer-action@v1](https://github.com/vyges/metadata-scorer-action/tree/v1)

## Needs work (bottom 20)

| IP | Score | Tier | Top gap |
|---|---:|---|---|
| `caliptra-libs` | 40 | High-risk | interfaces: interfaces (none declared) |
| `caliptra-uart` | 40 | High-risk | interfaces: interfaces (none declared) |
| `opentitan-flash-ctrl` | 40 | High-risk | interfaces: interfaces (none declared) |
| `cf-gpio-config` | 45 | High-risk | interfaces: interfaces[].type=clock |
| `sky130-ef-adc3v-12bit` | 50 | High-risk | interfaces: interfaces[].type=reset |
| `secworks-aes` | 55 | High-risk | interfaces: interfaces[].type=bus |
| `usb-cdc` | 55 | High-risk | interfaces: interfaces[].type=bus |
| `hardfloat` | 60 | Medium | interfaces: interfaces (none declared) |
| `opentitan-racl-ctrl` | 60 | Medium | interfaces: interfaces (none declared) |
| `cf-i2c` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `cf-i2s` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `cf-spi` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `cf-tmr32` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `ef-wdt32-1` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `wrapped-wb-hyperram` | 63 | Medium | interfaces: interfaces[].bus.signals |
| `tech_cells_generic` | 65 | Medium | interfaces: interfaces (none declared) |
| `cf-sram-1024x32` | 70 | Medium | interfaces: interfaces[].type=reset |
| `vyges-pinmux-lite` | 71 | Medium | implementation: asic{} or fpga{} |
| `cf-uart` | 73 | Medium | interfaces: interfaces[].bus.signals |
| `opentitan-prim-xilinx` | 75 | Medium | interfaces: interfaces[].type=clock |

## Top 20 (highest scores)

| IP | Score |
|---|---:|
| `fast-fourier-transform-ip` | 100 |
| `ibex` | 100 |
| `openfasoc-temp-sensor` | 100 |
| `opentitan-rv-core-ibex` | 100 |
| `opentitan-uart` | 100 |
| `picorv32` | 100 |
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
| `coralnpu-core` | 98 |
| `coralnpu-i2c-master` | 98 |

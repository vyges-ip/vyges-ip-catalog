# Metadata schema drift report

- **Generated:** 2026-06-09T15:39:34+00:00
- **Schema:** bundled Vyges metadata schema (vendored at `schema/vyges-metadata.schema.json`)
- **Total IP metadata files:** 148
- **Failing schema validation:** 37/148
- **Passing:** 111/148

> Report-only. This check never fails the build; it is a periodic drift signal.

## Error counts by category

| Category | Count |
| --- | ---: |
| enum_violation | 36 |
| pattern_violation | 17 |
| missing_required | 10 |
| type_violation | 8 |
| additional_property | 7 |
| unknown_top_level_property | 5 |

## Failing IPs

| IP metadata file | Error count |
| --- | ---: |
| `vyges-pinmux-lite.json` | 11 |
| `opentitan-prim-xilinx.json` | 7 |
| `vexriscv.json` | 7 |
| `opentitan-aes.json` | 5 |
| `usb-cdc.json` | 4 |
| `wrapped-wb-hyperram.json` | 4 |
| `cf-sram-1024x32.json` | 3 |
| `riscduino-pwm.json` | 3 |
| `vyges-rv-dbg-tlul.json` | 3 |
| `coralnpu-core.json` | 2 |
| `fast-fourier-transform-ip.json` | 2 |
| `opentitan-edn.json` | 2 |
| `opentitan-pattgen.json` | 2 |
| `pulp-riscv-dbg.json` | 2 |
| `pwm-controller.json` | 2 |
| `tech_cells_generic.json` | 2 |
| `tlul-apb-adapter.json` | 2 |
| `adams-bridge.json` | 1 |
| `caliptra-csrng.json` | 1 |
| `caliptra-doe.json` | 1 |
| `cf-ip-util.json` | 1 |
| `cf-uart.json` | 1 |
| `cva6.json` | 1 |
| `i3c-core.json` | 1 |
| `ibex.json` | 1 |
| `mlow-codec.json` | 1 |
| `openfasoc-temp-sensor.json` | 1 |
| `opentitan-otp-macro.json` | 1 |
| `opentitan-spi-device.json` | 1 |
| `sky130-bandgap-reference.json` | 1 |
| `sky130-delta-sigma-adc.json` | 1 |
| `sky130-opamp.json` | 1 |
| `sky130-potentiometric-dac.json` | 1 |
| `sky130-sar-adc.json` | 1 |
| `uart-controller.json` | 1 |
| `vyges-rv-plic-lite.json` | 1 |
| `vyges-spi-host-lite.json` | 1 |

<details><summary>Per-IP error detail</summary>

### `vyges-pinmux-lite.json` (11)

- [<root>] 'category', 'owner', 'rtl_files', 'top_module' do not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [branding] 'provider' is a required property
- [interfaces/2/signals/0/type] 'tl_h2d_t' is not one of ['data', 'control', 'clock', 'reset', 'interrupt', 'status', 'address', 'bus']
- [interfaces/2/signals/1/type] 'tl_d2h_t' is not one of ['data', 'control', 'clock', 'reset', 'interrupt', 'status', 'address', 'bus']
- [registers/0] Additional properties are not allowed ('width' was unexpected)
- [registers/1] Additional properties are not allowed ('width' was unexpected)
- [registers/2] Additional properties are not allowed ('width' was unexpected)
- [registers/3] Additional properties are not allowed ('width' was unexpected)
- [registers/4] Additional properties are not allowed ('width' was unexpected)
- [registers/5] Additional properties are not allowed ('width' was unexpected)
- [registers/6] Additional properties are not allowed ('width' was unexpected)

### `opentitan-prim-xilinx.json` (7)

- [interfaces/0/type] 'inout' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/1/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/2/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/3/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/4/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/5/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/6/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `vexriscv.json` (7)

- [parameters/0/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [parameters/1/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [parameters/2/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [parameters/3/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [parameters/4/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [parameters/5/type] 'plugin' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']
- [test] 'status' is a required property

### `opentitan-aes.json` (5)

- [interfaces/5/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/6/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/7/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/8/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/9/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `usb-cdc.json` (4)

- [<root>] 'notes', 'platforms' do not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [categories/0] 'communication' is not of type 'object'
- [categories/1] 'usb' is not of type 'object'
- [interfaces/2/type] 'interface' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `wrapped-wb-hyperram.json` (4)

- [<root>] 'notes', 'platforms' do not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [categories/0] 'memory-controller' is not of type 'object'
- [categories/1] 'external-interface' is not of type 'object'
- [interfaces/3/type] 'interface' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `cf-sram-1024x32.json` (3)

- [<root>] 'hardened_files', 'rtl_files', 'soc_integration' do not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [categories/0/main_category] 'Memory' is not one of ['Analog & Mixed-Signal', 'Arithmetic Units', 'Base Libraries', 'Chiplet Integration', 'Control Logic', 'Converters', 'Interface Controllers', 'Memory Subsystems', 'Miscellaneous', 'Processing Cores', 'Security IP', 'Signal Processing', 'Timing & Clocking', 'Verification & Testing']
- [source/type] 'bundle' is not one of ['git', 'archive']

### `riscduino-pwm.json` (3)

- [parameters/0] 'name' is a required property
- [parameters/0] 'type' is a required property
- [test] 'status' is a required property

### `vyges-rv-dbg-tlul.json` (3)

- [<root>] 'debug_spec', 'firmware_integration', 'memory_regions', 'rtl_files', 'schema_integration', 'soc_integration' do not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [branding] 'provider' is a required property
- [parameters/3/type] 'logic [31:0]' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']

### `coralnpu-core.json` (2)

- [performance/area] '1.5mm^2' is not of type 'object'
- [performance/power] '1.2W' is not of type 'object'

### `fast-fourier-transform-ip.json` (2)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [branding] 'provider' is a required property

### `opentitan-edn.json` (2)

- [interfaces/4/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/5/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `opentitan-pattgen.json` (2)

- [interfaces/4/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/5/type] 'input' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `pulp-riscv-dbg.json` (2)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [parameters/3/type] 'logic [NrHarts-1:0]' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']

### `pwm-controller.json` (2)

- [interfaces/10/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']
- [interfaces/11/type] 'output' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `tech_cells_generic.json` (2)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [categories/0/main_category] 'Building Blocks' is not one of ['Analog & Mixed-Signal', 'Arithmetic Units', 'Base Libraries', 'Chiplet Integration', 'Control Logic', 'Converters', 'Interface Controllers', 'Memory Subsystems', 'Miscellaneous', 'Processing Cores', 'Security IP', 'Signal Processing', 'Timing & Clocking', 'Verification & Testing']

### `tlul-apb-adapter.json` (2)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'
- [branding] 'provider' is a required property

### `adams-bridge.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `caliptra-csrng.json` (1)

- [interfaces/2/type] 'application' is not one of ['bus', 'clock', 'reset', 'interrupt', 'custom', 'control', 'signal', 'data', 'io', 'status', 'analog', 'gpio', 'digital', 'serial', 'audio', 'debug', 'packet', 'jtag', 'tieoff', 'entropy', 'keyvault', 'power', 'alert', 'sideload', 'register', 'trace', 'ground', 'chiplet', 'lifecycle', 'rng', 'pcr_vault']

### `caliptra-doe.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `cf-ip-util.json` (1)

- [<root>] 'modules' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `cf-uart.json` (1)

- [dependencies/0] 'cf-ip-util' is not of type 'object'

### `cva6.json` (1)

- [performance/area] '0.5mm^2' is not of type 'object'

### `i3c-core.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `ibex.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `mlow-codec.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `openfasoc-temp-sensor.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `opentitan-otp-macro.json` (1)

- [parameters/2/type] 'top_racl_pkg::racl_policy_sel_t' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']

### `opentitan-spi-device.json` (1)

- [parameters/2/type] 'array' is not one of ['int', 'bool', 'string', 'real', 'bit', 'enum', 'float', 'int unsigned', 'logic']

### `sky130-bandgap-reference.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `sky130-delta-sigma-adc.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `sky130-opamp.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `sky130-potentiometric-dac.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `sky130-sar-adc.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `uart-controller.json` (1)

- [<root>] 'rtl_files' does not match any of the regexes: '^(architecture|artifacts|trust)$', '^\\$schema$', '^_', '^upstream$'

### `vyges-rv-plic-lite.json` (1)

- [branding] 'provider' is a required property

### `vyges-spi-host-lite.json` (1)

- [branding] 'provider' is a required property

</details>


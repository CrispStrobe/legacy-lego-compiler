# Third-Party Notices & Attribution

`legacy-lego-compiler` is distributed under the **MIT** license (see [`LICENSE`](LICENSE)),
which covers **only CrispStrobe's original wrapper code** — the FastAPI REST
service, the `*_transpile_*.js` helpers, and the build/deploy scripts.

The repository also ships **pre-compiled third-party compiler/assembler binaries
and headers**, which are *not* CrispStrobe's work and retain their own upstream
licenses:

| Vendored artifact | Upstream project | Author(s) | License |
|---|---|---|---|
| `bin/nbc-linux`, `bin/nbc_includes/*.h` (`NBCCommon.h`, `NXCDefs.h`, `NXTDefs.h`) | NBC / NXC compiler (BricxCC) | John Hansen | **MPL 1.1** (Mozilla Public License) |
| `bin/nqc-linux` | [`jverne/nqc`](https://github.com/jverne/nqc) at commit [`21c24ec1e520c736ce78e33e4c0dafca887fc2b7`](https://github.com/jverne/nqc/tree/21c24ec1e520c736ce78e33e4c0dafca887fc2b7), built unmodified by `.github/workflows/build-nqc.yml` | Dave Baum, John Hansen | **MPL 2.0** — source available at the linked commit |
| `bin/lmsasm-linux` | [`ev3dev/lmsasm`](https://github.com/ev3dev/lmsasm) | the ev3dev project | per upstream — see the ev3dev/lmsasm repository |

The MIT license applies to CrispStrobe's wrapper code only. The vendored NBC
binary and headers remain under the **Mozilla Public License 1.1**; the NQC
binary remains under the **Mozilla Public License 2.0**, and its Source Code Form
is the upstream commit linked above; the `lmsasm`
binary remains under its upstream **ev3dev/lmsasm** license. Those terms govern
redistribution of the respective artifacts.

LEGO® is a trademark of the LEGO Group, which does not sponsor or endorse this software.

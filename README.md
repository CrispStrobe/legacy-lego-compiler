# LEGO Bytecode Compiler API (NXT and EV3)

A serverless REST API that compiles **NXC (Not eXactly C)** to LEGO NXT `.rxe`
files and **lmsasm** (LMS Assembly) to LEGO EV3 bytecode.

It cross-compiles the 15-year-old Pascal NBC compiler and the more modern Go
[`ev3dev/lmsasm`](https://github.com/ev3dev/lmsasm) assembler into x86_64 Linux
binaries, then wraps them in FastAPI behind Vercel's serverless functions.

**Live API:** <https://lego-compiler.vercel.app/>

## Who calls this

This API is the compile-side of the "transpile to brick bytecode" extensions in
[`CrispStrobe/turbowarp-lego`](https://github.com/CrispStrobe/turbowarp-lego)
and [`CrispStrobe/extensions`](https://github.com/CrispStrobe/extensions/tree/main/extensions/CrispStrobe):

- `legonxt_transpile_universal.js` — Scratch → NXC → `.rxe` for NXT
- `ev3_lms_transpile.js` — Scratch → lmsasm → EV3 bytecode

The browser POSTs the source it generated to `/compile`; the API returns the
binary as base64; the extension hands it to the brick.

---

## Architecture

Pre-built binaries shipped alongside a thin FastAPI wrapper, so each Vercel
function invocation can `exec()` the compiler against a writable `/tmp`
workspace.

1. **NBC/NXC compiler** — built from Pascal (FPC) inside a Debian container
   targeting `x86_64-linux`.
2. **lmsasm assembler** — `go build` cross-compiled to `x86_64-linux`.
3. **FastAPI wrapper** — copies request body to `/tmp/<uuid>/`, runs the
   binary, base64-encodes the output, and returns it.

---

## Deployment / build steps

### 1. Compile NBC for Linux

Since Vercel runs Linux x86_64, build NBC via Docker (macOS host shown):
```bash
docker run --rm --platform linux/amd64 -v $(pwd):/sources debian:stable-slim \
  sh -c "apt-get update && apt-get install -y fpc && cd /sources && \
  fpc -Sd -FuNXT -onext_mkdata_linux NXT/mkdata.dpr && \
  ./NXT/next_mkdata_linux NXT/NBCCommon.h NBCCommonData_linux.pas nbc_common_data && \
  ./NXT/next_mkdata_linux NXT/NXTDefs.h NXTDefsData_linux.pas nxt_defs_data && \
  ./NXT/next_mkdata_linux NXT/NXCDefs.h NXCDefsData_linux.pas nxc_defs_data && \
  echo \"const DEFAULT_INCLUDE_DIR = '/var/task/bin/nbc_includes';\" > nbc_preproc_linux.inc && \
  fpc -Sd -O2 -dNEXT -FiNXT -FuNXT -Fibricktools -Fu. -onbc-linux NXT/nbc.dpr"

```

### 2. Compile lmsasm for Linux

Inside an [`ev3dev/lmsasm`](https://github.com/ev3dev/lmsasm) checkout:

```bash
GOOS=linux GOARCH=amd64 go build -o lmsasm-linux ./lmsasm
```

### 3. Assemble the deployment package

Layout Vercel needs:

```text
.
├── app.py             # FastAPI logic
├── vercel.json        # Deployment config
├── requirements.txt   # FastAPI, Uvicorn, Pydantic
└── bin/
    ├── nbc-linux      # Compiled in Step 1
    ├── lmsasm-linux   # Compiled in Step 2
    └── nbc_includes/  # Header files (.h) from NBC/NXT source
```

### 4. Deploy to Vercel

```bash
vercel --prod
```

---

## API

### Endpoint

`POST https://lego-compiler.vercel.app/compile`

Request:

```json
{
  "compiler": "nxc" | "lmsasm",
  "code": "<source>"
}
```

Response (success):

```json
{
  "success": true,
  "base64": "<base64-encoded .rxe or EV3 bytecode>",
  "log": "<compiler stdout/stderr>"
}
```

Response (failure):

```json
{
  "success": false,
  "log": "<compiler error output>"
}
```

### cURL

```bash
curl -X POST https://lego-compiler.vercel.app/compile \
  -H "Content-Type: application/json" \
  -d '{
    "compiler": "nxc",
    "code": "task main() { OnFwd(OUT_A, 75); Wait(1000); Off(OUT_A); }"
  }'
```

### Python

```python
import requests, base64

def compile_nxc(code, out="program.rxe"):
    res = requests.post(
        "https://lego-compiler.vercel.app/compile",
        json={"compiler": "nxc", "code": code},
    ).json()
    if not res.get("success"):
        raise RuntimeError(res.get("log", "compile failed"))
    with open(out, "wb") as f:
        f.write(base64.b64decode(res["base64"]))
```

### JavaScript (browser / TurboWarp extension)

```javascript
async function compileNXC(nxcCode) {
  const res = await fetch('https://lego-compiler.vercel.app/compile', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ compiler: 'nxc', code: nxcCode }),
  });
  const data = await res.json();
  if (!data.success) throw new Error(data.log);
  return data.base64; // hand to brick
}
```

---

## Licensing

- **NBC (Next Byte Codes)** — [MPL](https://www.mozilla.org/en-US/MPL/).
- **lmsasm** — © 2009 The Go Authors & 2016 David Lechner. [BSD-3-Clause](https://github.com/ev3dev/lmsasm/blob/master/LICENSE.txt).
- **This API wrapper** — MIT. Provided as-is for educational use.

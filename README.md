
# 🤖 LEGO Bytecode Compiler API (NXT & EV3)

A high-performance, serverless REST API that compiles **NXC (Not eXactly C)** for LEGO NXT bricks and **LMS Assembly** for LEGO EV3 bricks. 

This project integrates the cross-compiled 15-year-old Pascal source code of NBC and the more modern ev3dev Go source of LMSASM into Linux-compatible binaries, hosting them via FastAPI on Vercel.

---

## 🏗 System Architecture

The project uses a **Pre-built Binary + Serverless Function** architecture to bypass the limitations of cloud environments.

1.  **NBC Compiler**: Compiled from Pascal source using Docker (Target: x86_64-linux).
2.  **LMSASM Assembler**: Compiled from Go source (Target: x86_64-linux).
3.  **FastAPI Wrapper**: A Python interface that manages a writable `/tmp` execution environment for the compilers.



---

## 🚀 Deployment & Build Steps

### 1. Compile NBC for Linux (The Pascal Hurdles)
Since Vercel runs on Linux x86_64, we used Docker on macOS to produce a compatible binary:
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

### 2. Compile LMSASM for Linux (The Go Way)

Inside the `ev3dev/lmsasm` repository:

```bash
GOOS=linux GOARCH=amd64 go build -o lmsasm-linux ./lmsasm

```

### 3. Assemble the Deployment Package

We structure the files as follows for Vercel compatibility:

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
# Clean up build artifacts to stay under 250MB limit
rm *.o *.ppu *.rsj
vercel --prod

```

---

## 📡 API Usage Examples

### 1. cURL (NXT/NXC)

```bash
curl -X POST [https://your-app.vercel.app/compile](https://your-app.vercel.app/compile) \
  -H "Content-Type: application/json" \
  -d '{
    "compiler": "nxc",
    "code": "task main() { OnFwd(OUT_A, 75); Wait(1000); Off(OUT_A); }"
  }'

```

### 2. Python

```python
import requests
import base64

def get_rxe(code):
    url = "[https://your-app.vercel.app/compile](https://your-app.vercel.app/compile)"
    payload = {"compiler": "nxc", "code": code}
    res = requests.post(url, json=payload).json()
    if res["success"]:
        with open("program.rxe", "wb") as f:
            f.write(base64.b64decode(res["base64"]))

```

### 3. JavaScript (TurboWarp/Browser)

```javascript
const compileCode = async (nxcCode) => {
    const response = await fetch('[https://your-app.vercel.app/compile](https://your-app.vercel.app/compile)', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ compiler: 'nxc', code: nxcCode })
    });
    const data = await response.json();
    return data.base64; // Ready for download/upload to brick
};

```

---

## ⚖️ Licensing

* **NBC (Next Byte Codes)**: Released under the [Mozilla Public License (MPL)](https://www.mozilla.org/en-US/MPL/).
* **LMSASM**: Copyright (c) 2009 The Go Authors & 2016 David Lechner. Released under the [BSD-3-Clause License](https://www.google.com/search?q=https://github.com/ev3dev/lmsasm/blob/master/LICENSE.txt).
* **This API Wrapper**: MIT, provided as-is for educational use.

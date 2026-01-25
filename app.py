from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os
import base64
import stat
import shutil

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# These are the SOURCE paths in the read-only deployment
SRC_BIN_DIR = os.path.join(BASE_DIR, "bin")
SRC_LMS = os.path.join(SRC_BIN_DIR, "lmsasm-linux")
SRC_NBC = os.path.join(SRC_BIN_DIR, "nbc-linux")
INC_DIR = os.path.join(SRC_BIN_DIR, "nbc_includes")

# These will be the EXECUTION paths in the writable /tmp
TMP_BIN_DIR = "/tmp/bin"
LMS_PATH = os.path.join(TMP_BIN_DIR, "lmsasm-linux")
NBC_PATH = os.path.join(TMP_BIN_DIR, "nbc-linux")

def setup_binaries():
    """Copy binaries to /tmp and make them executable."""
    if not os.path.exists(TMP_BIN_DIR):
        os.makedirs(TMP_BIN_DIR, exist_ok=True)
    
    for src, dest in [(SRC_LMS, LMS_PATH), (SRC_NBC, NBC_PATH)]:
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copy2(src, dest)
            st = os.stat(dest)
            os.chmod(dest, st.st_mode | stat.S_IEXEC)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CompileReq(BaseModel):
    code: str
    compiler: str = "lms"

@app.get("/")
async def health():
    setup_binaries() # Ensure binaries are ready
    return {
        "status": "online",
        "binaries_ready": os.path.exists(NBC_PATH),
        "src_exists": os.path.exists(SRC_NBC)
    }

@app.post("/compile")
async def api_compile(req: CompileReq):
    setup_binaries()
    try:
        if req.compiler.lower() == "nxc":
            return {"success": True, "base64": compile_nxc(req.code), "type": "rxe"}
        return {"success": True, "base64": compile_lms(req.code), "type": "rbf"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def compile_lms(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lms', delete=False) as f:
        f.write(code)
        src = f.name
    out = src.replace('.lms', '.rbf')
    try:
        res = subprocess.run([LMS_PATH, '-output', out, src], capture_output=True, text=True, timeout=10)
        if res.returncode != 0: raise RuntimeError(f"LMS Error: {res.stderr or res.stdout}")
        with open(out, 'rb') as f: return base64.b64encode(f.read()).decode('utf-8')
    finally:
        for p in [src, out]:
            if os.path.exists(p): os.unlink(p)

def compile_nxc(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.nxc', delete=False) as f:
        f.write(code)
        src = f.name
    out = src.replace('.nxc', '.rxe')
    try:
        # Note: We still point to INC_DIR in /var/task because headers don't need +x permissions
        res = subprocess.run([NBC_PATH, f"-I={INC_DIR}", f"-O={out}", src], capture_output=True, text=True, timeout=15)
        if res.returncode != 0: raise RuntimeError(f"NBC Error: {res.stdout or res.stderr}")
        with open(out, 'rb') as f: return base64.b64encode(f.read()).decode('utf-8')
    finally:
        for p in [src, out]:
            if os.path.exists(p): os.unlink(p)

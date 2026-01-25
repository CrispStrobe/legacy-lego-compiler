import gradio as gr
import subprocess
import tempfile
import os
import base64
import stat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ==========================================
# 1. PATH CONFIGURATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# On Vercel, the app is in /var/task. Binaries are in /var/task/bin
BIN_DIR = os.path.join(BASE_DIR, "bin")

LMS_PATH = os.path.join(BIN_DIR, "lmsasm-linux")
NBC_PATH = os.path.join(BIN_DIR, "nbc-linux")
INC_DIR = os.path.join(BIN_DIR, "nbc_includes")

def setup_env():
    """Vercel resets permissions on deploy; we must force +x bit."""
    for path in [LMS_PATH, NBC_PATH]:
        if os.path.exists(path):
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)

setup_env()

# ==========================================
# 2. CORE LOGIC
# ==========================================
def compile_lms(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lms', delete=False) as f:
        f.write(code)
        src_path = f.name
    out_path = src_path.replace('.lms', '.rbf')
    try:
        res = subprocess.run([LMS_PATH, '-output', out_path, src_path], 
                             capture_output=True, text=True, timeout=10)
        if res.returncode != 0: raise RuntimeError(res.stderr or res.stdout)
        with open(out_path, 'rb') as f: data = f.read()
        return base64.b64encode(data).decode('utf-8'), len(data)
    finally:
        for p in [src_path, out_path]:
            if os.path.exists(p): os.unlink(p)

def compile_nxc(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.nxc', delete=False) as f:
        f.write(code)
        src_path = f.name
    out_path = src_path.replace('.nxc', '.rxe')
    try:
        # Pass the Absolute Include Path
        res = subprocess.run([NBC_PATH, f"-I={INC_DIR}", f"-O={out_path}", src_path], 
                             capture_output=True, text=True, timeout=15)
        if res.returncode != 0: raise RuntimeError(res.stdout or res.stderr)
        with open(out_path, 'rb') as f: data = f.read()
        return base64.b64encode(data).decode('utf-8'), len(data)
    finally:
        for p in [src_path, out_path]:
            if os.path.exists(p): os.unlink(p)

# ==========================================
# 3. API & GRADIO
# ==========================================
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CompileReq(BaseModel):
    code: str
    compiler: str = "lms"

@app.post("/compile")
async def api_compile(req: CompileReq):
    try:
        if req.compiler.lower() == "nxc":
            b64, size = compile_nxc(req.code)
            return {"success": True, "base64": b64, "type": "rxe"}
        b64, size = compile_lms(req.code)
        return {"success": True, "base64": b64, "type": "rbf"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Gradio Interface (Mounted at root)
with gr.Blocks() as demo:
    gr.Markdown("# LEGO Compiler API")
    with gr.Tab("NXT (NXC)"):
        input_nxc = gr.Textbox(lines=10, label="NXC Code")
        btn_nxc = gr.Button("Compile")
        output_nxc = gr.Textbox(label="Base64 Result")
        btn_nxc.click(fn=lambda x: compile_nxc(x)[0], inputs=input_nxc, outputs=output_nxc)

app = gr.mount_gradio_app(app, demo, path="/")


if __name__ == "__main__":
    import uvicorn
    # Vercel doesn't use this, but your Mac terminal will!
    uvicorn.run(app, host="0.0.0.0", port=7860)

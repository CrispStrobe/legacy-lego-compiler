from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import tempfile
import os
import base64
import stat
import shutil

# --- Configuration & Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_BIN_DIR = os.path.join(BASE_DIR, "bin")
INC_DIR = os.path.join(SRC_BIN_DIR, "nbc_includes")
TMP_BIN_DIR = "/tmp/bin"
LMS_PATH = os.path.join(TMP_BIN_DIR, "lmsasm-linux")
NBC_PATH = os.path.join(TMP_BIN_DIR, "nbc-linux")

def setup_binaries():
    if not os.path.exists(TMP_BIN_DIR):
        os.makedirs(TMP_BIN_DIR, exist_ok=True)
    for src, dest in [(os.path.join(SRC_BIN_DIR, "lmsasm-linux"), LMS_PATH), 
                      (os.path.join(SRC_BIN_DIR, "nbc-linux"), NBC_PATH)]:
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copy2(src, dest)
            os.chmod(dest, os.stat(dest).st_mode | stat.S_IEXEC)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CompileReq(BaseModel):
    code: str
    compiler: str = "nxc"

@app.post("/compile")
async def api_compile(req: CompileReq):
    setup_binaries()
    is_nxc = req.compiler.lower() == 'nxc'
    suffix, ext = ('.nxc', '.rxe') if is_nxc else ('.lms', '.rbf')
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(req.code)
        src = f.name
    out = src.replace(suffix, ext)
    
    try:
        cmd = [NBC_PATH, f"-I={INC_DIR}", f"-O={out}", src] if is_nxc else [LMS_PATH, '-output', out, src]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode != 0: raise RuntimeError(res.stdout or res.stderr)
        with open(out, 'rb') as f:
            return {"success": True, "base64": base64.b64encode(f.read()).decode('utf-8'), "filename": f"program{ext}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        for p in [src, out]:
            if os.path.exists(p): os.unlink(p)

@app.get("/", response_class=HTMLResponse)
async def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LEGO Cloud Compiler</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.36.1/min/vs/loader.min.js"></script>
        <style>
            body { margin: 0; font-family: -apple-system, system-ui, sans-serif; background: #1e1e1e; color: white; display: flex; flex-direction: column; height: 100vh; }
            header { padding: 12px 20px; background: #252526; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; }
            #container { flex: 1; }
            .controls { display: flex; gap: 10px; align-items: center; }
            button { background: #007acc; color: white; border: none; padding: 8px 16px; cursor: pointer; border-radius: 4px; font-weight: 600; transition: 0.2s; }
            button:hover { background: #0062a3; }
            button.secondary { background: #3a3d41; }
            button.secondary:hover { background: #4a4d51; }
            select { background: #3c3c3c; color: white; border: 1px solid #555; padding: 7px; border-radius: 4px; outline: none; }
            #console { height: 120px; background: #000; color: #aaa; padding: 10px; font-family: 'SFMono-Regular', Consolas, monospace; overflow-y: auto; border-top: 1px solid #333; white-space: pre-wrap; font-size: 12px; }
            
            /* Modal Logic */
            #modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center; }
            #modal-content { background: #252526; padding: 30px; border-radius: 8px; max-width: 600px; border: 1px solid #444; line-height: 1.6; }
            #modal-content h2 { margin-top: 0; color: #007acc; }
            #modal-content a { color: #4fc1ff; text-decoration: none; }
            #modal-content a:hover { text-decoration: underline; }
            .close-btn { float: right; cursor: pointer; font-size: 20px; color: #888; }
        </style>
    </head>
    <body>
        <div id="modal">
            <div id="modal-content">
                <span class="close-btn" onclick="toggleModal()">×</span>
                <h2>Project Information</h2>
                <p>A cloud-based toolchain for compiling LEGO Mindstorms bytecode for legacy bricks.</p>
                <ul>
                    <li><b>NXT (NXC) Source:</b> <a href="https://bricxcc.sourceforge.net/nbc/" target="_blank">NBC/NXC Compiler</a></li>
                    <li><b>EV3 (LMS) Assembler:</b> <a href="https://github.com/ev3dev/lmsasm" target="_blank">Lmsasm Go Rewrite</a></li>
                    <li><b>EV3 Docs:</b> <a href="https://analyticphysics.com/Diversions/Assembly%20Language%20Programming%20for%20LEGO%20Mindstorms%20EV3.htm" target="_blank">LMS Programming Guide</a></li>
                </ul>
                <hr style="border:0; border-top:1px solid #444; margin: 20px 0;">
                <p style="font-size: 0.85rem; color: #888;">This tool cross-compiles Pascal and Go sources for serverless execution on Vercel.</p>
            </div>
        </div>

        <header>
            <div style="font-size: 1.1rem; font-weight: bold; letter-spacing: 0.5px;">🤖 LEGO CLOUD COMPILER</div>
            <div class="controls">
                <button class="secondary" onclick="toggleModal()">ⓘ Info</button>
                <select id="compiler" onchange="updateExample()">
                    <option value="nxc">NXT (NXC)</option>
                    <option value="lms">EV3 (LMS)</option>
                </select>
                <button onclick="compile()">🔧 Compile & Download</button>
            </div>
        </header>
        <div id="container"></div>
        <div id="console">Ready to compile. Select a target and write your code.</div>

        <script>
            let editor;
            const examples = {
                nxc: 'task main() {\\n    // NXT: Drive forward and play a tone\\n    OnFwd(OUT_BC, 75);\\n    PlayTone(440, 500);\\n    Wait(2000);\\n    Off(OUT_BC);\\n    TextOut(0, LCD_LINE3, "Build Success!");\\n}',
                lms: 'vmthread MAIN {\\n    // EV3: Set motor speed on Port A\\n    OUTPUT_SPEED(0, 1, 50)\\n    OUTPUT_START(0, 1)\\n    \\n    // Wait 2 seconds (2000ms)\\n    TIMER_WAIT(2000, 0)\\n    \\n    OUTPUT_STOP(0, 1, 0)\\n}'
            };

            require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.36.1/min/vs' } });
            require(['vs/editor/editor.main'], function () {
                editor = monaco.editor.create(document.getElementById('container'), {
                    value: examples.nxc,
                    language: 'cpp',
                    theme: 'vs-dark',
                    automaticLayout: true,
                    fontSize: 14
                });
            });

            function updateExample() {
                const type = document.getElementById('compiler').value;
                editor.setValue(examples[type]);
            }

            function toggleModal() {
                const m = document.getElementById('modal');
                m.style.display = (m.style.display === 'flex') ? 'none' : 'flex';
            }

            async function compile() {
                const log = (msg, err=false) => { 
                    const c = document.getElementById('console');
                    c.innerHTML = `<span style="color: ${err ? '#ff5f5f' : '#4ec9b0'}">${msg}</span>`;
                };
                log("Processing compilation...");
                try {
                    const res = await fetch('/compile', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            compiler: document.getElementById('compiler').value, 
                            code: editor.getValue() 
                        })
                    });
                    const data = await res.json();
                    if (!data.success) throw new Error(data.error);
                    
                    const blob = await (await fetch(`data:application/octet-stream;base64,${data.base64}`)).blob();
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = data.filename;
                    link.click();
                    log("✅ Build Complete. Downloaded " + data.filename);
                } catch (e) { log("❌ Build Failed:\\n" + e.message, true); }
            }
        </script>
    </body>
    </html>
    """
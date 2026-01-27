
# TurboWarp Extensions (mostly for LEGO Hubs)

For some of these, if you use them on Desktop (Windows, MacOS), you need the LEGO ScratchLink software as a bridge. Alternatively, some of these extensions support a custom (Websocket) bridge.

For most of these, you must disable Sandbox Mode in TurboWarp.

For iOS, you might try them in Scrub App which provides a ScratchLink-like functionality (https://github.com/bricklife/Scrub) (this is untested yet).

## 📁 Quick File Reference

| Category | Files |
|----------|-------|
| **LEGO Spike Prime** | [`legospikeprime_btc_scratchlink.js`](./legospikeprime_btc_scratchlink.js), [`legospikeprime_ble.js`](./legospikeprime_ble.js), [`legospike_ble.js`](./legospike_ble.js), [`legospike_bridge.js`](./legospike_bridge.js) |
| **LEGO Boost** | [`legoboost_scratchlink.js`](./legoboost_scratchlink.js), [`legoboost_ble.js`](./legoboost_ble.js), [`legoboost_turbowarp.js`](./legoboost_turbowarp.js) |
| **LEGO EV3** | [`ev3_btc.js`](./ev3_btc.js), [`ev3_lms_transpile.js`](./ev3_lms_transpile.js), [`ev3_transpile.js`](./ev3_transpile.js) |
| **LEGO NXT** | [`legonxt_transpile_scratchlink.js`](./legonxt_transpile_scratchlink.js), [`legonxt_transpile_direct.js`](./legonxt_transpile_direct.js), [`legonxt_transpile_bridge.js`](./legonxt_transpile_bridge.js), [`legonxt-direct.js`](./legonxt-direct.js), [`legonxt_turbowarp.js`](./legonxt_turbowarp.js) |
| **Math/Utilities** | [`csp.js`](./csp.js), [`planetemaths.js`](./planetemaths.js), [`arrays.js`](./arrays.js), [`gamepad.js`](./gamepad.js) |
| **Python Bridges** | [`nxt_bridge.py`](./nxt_bridge.py), [`ev3_ondevice_bridge.py`](./ev3_ondevice_bridge.py), [`lego_bridge.py`](./lego_bridge.py) |

---

## LEGO Spike Prime = Robot Inventor Hub

### Bluetooth Classic (BTC)

**Extension:** [`legospikeprime_btc_scratchlink.js`](./legospikeprime_btc_scratchlink.js)

Note for this you need the older 2.x firmware which works with Bluetooth Classic (BTC).

You can switch firmwares by running upgrade from Spike Prime app, or [downgrade](https://spikelegacy.legoeducation.com/hubdowngrade/#step-1) or use dfu-util/pybricksdev (backup/restore).

### Bluetooth Low Energy (BLE)

This is work in progress and I could not yet test it:
- **Extension:** [`legospike_ble.js`](./legospike_ble.js)
- **Alternative:** [`legospikeprime_ble.js`](./legospikeprime_ble.js)

For this you need the newer firmware (you can upgrade from Spike Prime app).

---

## LEGO Boost (BLE)

**Extension:** [`legoboost_scratchlink.js`](./legoboost_scratchlink.js) (requires ScratchLink installed)

**Alternatives:**
- [`legoboost_ble.js`](./legoboost_ble.js) - Direct BLE connection
- [`legoboost_turbowarp.js`](./legoboost_turbowarp.js) - Bridge-based connection

---

## LEGO EV3

### Original Firmware

**[`ev3_lms_transpile.js`](./ev3_lms_transpile.js)** - Allows streaming mode (direct command execution) and transpiling to lmsasm, which can then be compiled to bytecode that should run on the EV3 Brick. Compilation needs internet connectivity as it uses a REST API which wraps [NBC](https://bricxcc.sourceforge.net/nbc/) and [lmsasm](https://github.com/ev3dev/lmsasm) at https://lego-compiler.vercel.app/ ([source](https://github.com/CrispStrobe/legacy-lego-compiler)). **Use with caution!**

**[`ev3_btc.js`](./ev3_btc.js)** - Connects to the original firmware with streaming mode only.

### EV3DEV Firmware

With ev3dev, you have Linux on the device and can do lots of cool things.

**Python Bridge:** [`ev3_ondevice_bridge.py`](./ev3_ondevice_bridge.py) - Supports both streaming mode (direct command execution) and transpiling code blocks to Python scripts with on-device execution.

**Extension:** [`ev3_transpile.js`](./ev3_transpile.js) - Required for transpilation features.

⚠️ This is all work in progress.

---

## LEGO NXT

### Transpilation Extensions (Scratch → NXC → RXE)

**[`legonxt_transpile_scratchlink.js`](./legonxt_transpile_scratchlink.js)** ⭐ **RECOMMENDED** - Works with ScratchLink and gives you the option to transpile code blocks to NXC and then compile them to RXE files which the NXT Brick can run directly.

**Alternatives:**
- [`legonxt_transpile_direct.js`](./legonxt_transpile_direct.js) - Direct connection (incomplete)
- [`legonxt_transpile_bridge.js`](./legonxt_transpile_bridge.js) - Bridge-based (incomplete)

Compilation needs internet connectivity, using REST API at https://lego-compiler.vercel.app/ ([source](https://github.com/CrispStrobe/legacy-lego-compiler)).

### Direct Control Extensions

**[`legonxt-direct.js`](./legonxt-direct.js)** - Direct Bluetooth control (pair NXT via device Bluetooth settings first)

**[`legonxt_turbowarp.js`](./legonxt_turbowarp.js)** - Uses WebSocket bridge

**Python Bridge:** [`nxt_bridge.py`](./nxt_bridge.py) - Main WebSocket bridge (keep running)

**Legacy/Debug Files:**
- [`lego_bridge.py`](./lego_bridge.py) - Older bridge attempt
- [`nxt-diag.py`](./nxt-diag.py) - Connection diagnostics
- [`nxt-pybluez-bridge.py`](./nxt-pybluez-bridge.py) - Experimental alternative bridge
- [`reset_nxt.sh`](./reset_nxt.sh) - Reset pairing on macOS
- [`test_bt.py`](./test_bt.py) - Bluetooth discovery test

---

## Non-LEGO Extensions

### Math

- **[`csp.js`](./csp.js)** - Simple Constraint-Satisfaction-Problem solver
- **[`planetemaths.js`](./planetemaths.js)** - Additional math operations (rewritten from CodePM extension)
- **[`arrays.js`](./arrays.js)** - Array/vector/tensor handling

### Gamepad

**[`gamepad.js`](./gamepad.js)** - Gamepad support (untested)

---

# LEGO NXT Bluetooth Control for TurboWarp

Control LEGO Mindstorms NXT robots directly from TurboWarp using Bluetooth. This project provides both a WebSocket bridge for remote access and a direct Web Serial API extension for local connections.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 🎯 Features

### Motor Control
- Continuous motor power control (-100% to 100%)
- Precise angle-based movement (degrees/rotations)
- Position tracking and reset
- Brake and coast modes

### Sensor Support
- **Touch Sensor**: Boolean press detection
- **Light Sensor**: Brightness readings (0-1023) with LED control
- **Sound Sensor**: Loudness measurement in dB/dBA mode
- **Ultrasonic Sensor**: Distance measurement (0-255 cm) via I2C

### Display Graphics
- Clear screen and update display
- Draw text with 5×7 bitmap font (A-Z, 0-9, symbols)
- Draw pixels, lines, rectangles (filled/outline)
- Built-in patterns (checkerboard, stripes, grid, dots, border)
- Screen capture (returns base64 BMP image)

### Sound
- Play tones (200-14000 Hz)
- Musical notes (C4-B5)

### Status
- Battery voltage monitoring (mV)
- Connection status

## 📋 Requirements

### Hardware
- LEGO Mindstorms NXT brick (NXT 1.0 or 2.0)
- Bluetooth connection (built-in NXT Bluetooth)
- **macOS, Windows, or Linux** computer

### Software
- **Python 3.8+** (for WebSocket bridge)
- **Chrome/Edge 89+** (for Web Serial API)
- **Python packages**: `websockets`, `pyserial`

```bash
pip install websockets pyserial
```

## 🚀 Quick Start

### Method 1: WebSocket Bridge (Recommended)

1. **Pair NXT via Bluetooth** (see [macOS Setup](#macos-bluetooth-setup) below)

2. **Run the bridge**:
```bash
python nxt_bridge.py
```

3. **Load extension in TurboWarp**:
   - Load [`legonxt_turbowarp.js`](./legonxt_turbowarp.js) as a custom extension
   - Use the "connect to [URL]" block with `localhost:8080`

### Method 2: Direct Web Serial (Experimental)

1. **Pair NXT via Bluetooth**
2. **Load extension** [`legonxt-direct.js`](./legonxt-direct.js) in TurboWarp Desktop
3. **Connect** and select `/dev/cu.NXT` (macOS) or appropriate COM port

## 🔧 Setup

### macOS Bluetooth Setup

**Critical Steps** (Bluetooth connection drops frequently on macOS):

1. **Forget existing pairing** (if any):
```bash
blueutil --disconnect 00-16-53-XX-XX-XX
blueutil --unpair 00-16-53-XX-XX-XX
```

2. **Turn NXT off and back on**

3. **Re-pair with PIN 1234**:
```bash
blueutil --pair 00-16-53-XX-XX-XX
# Enter PIN: 1234
```

4. **Verify connection**:
```bash
python nxt-diag.py
```

You should hear a beep and see battery data!

**⚠️ Important**: The Bluetooth connection may drop after inactivity. If commands stop working, **repeat the pairing process** using the [`reset_nxt.sh`](./reset_nxt.sh) script:

```bash
chmod +x reset_nxt.sh
./reset_nxt.sh
```

### Windows Setup

1. Pair NXT via Bluetooth settings
   You probably must first enable "Advanced" Discovery in Windows 11:
   - Open Settings (Win + I)
   - Go to Bluetooth & devices > Devices
   - Scroll down to Device settings
   - Change Bluetooth devices discovery from "Default" to "Advanced"
   - Enter the NXT Bluetooth PIN: default = 1234

   Note you might also do this in Windows Terminal:
```cmd
btpair -u
```

2. Note the COM port
3. Run the bridge

### Linux Setup

You can inspect the COM port at `/dev/rfcomm0`

## 📁 File Descriptions

### JavaScript Extensions

| File | Description |
|------|-------------|
| [`legonxt_turbowarp.js`](./legonxt_turbowarp.js) | Lego NXT over local Python Bridge (Full feature set) ⭐ |
| [`legonxt-direct.js`](./legonxt-direct.js) | Lego NXT Direct Bluetooth Connection (Development version) |
| [`legonxt_transpile_scratchlink.js`](./legonxt_transpile_scratchlink.js) | NXT Transpilation via ScratchLink (Scratch → NXC → RXE) ⭐ |
| [`legonxt_transpile_direct.js`](./legonxt_transpile_direct.js) | NXT Transpilation Direct (Incomplete) |
| [`legonxt_transpile_bridge.js`](./legonxt_transpile_bridge.js) | NXT Transpilation Bridge (Incomplete) |

### Python Bridges

| File | Description |
|------|-------------|
| [`nxt_bridge.py`](./nxt_bridge.py) | **WebSocket bridge** - Polling-based for reliable communication ⭐ |
| [`nxt-diag.py`](./nxt-diag.py) | **Diagnostic tool** - Test Bluetooth connection |
| [`nxt-pybluez-bridge.py`](./nxt-pybluez-bridge.py) | PyBluez alternative bridge (experimental) |
| [`reset_nxt.sh`](./reset_nxt.sh) | Quick reset script for macOS pairing |
| [`test_bt.py`](./test_bt.py) | Bluetooth discovery test |

## 💻 Usage Examples

### Basic Motor Control

```scratch
when flag clicked
connect to [localhost:8080]
wait until <connected?>
motor [A] power [75] %
wait (2) seconds
motor [A] [brake]
```

### Sensor Reading

```scratch
setup ultrasonic [S4]
forever
  say (join [Distance: ] (ultrasonic [S4] distance (cm)))
end
```

### Display Graphics

```scratch
clear screen
draw text [HELLO NXT] at x:[10] y:[10]
draw line from x:[0] y:[0] to x:[99] y:[63]
🖥️ update display
wait (3) seconds  // Display update takes 1-3 seconds
```

### Transpilation (NXC Compilation)

1. Load [`legonxt_transpile_scratchlink.js`](./legonxt_transpile_scratchlink.js)
2. Build your program with Scratch blocks
3. Use "transpile project to NXC" block
4. Use "compile NXC to .rxe" block (requires internet)
5. Use "upload program to NXT" block

### Pattern Drawing

```scratch
draw pattern [checkerboard]
wait (2) seconds
draw pattern [smile]
```

## 🐛 Troubleshooting

### Problem: No beep, no data received

**Cause**: Bluetooth connection not established

**Solution**:
1. Run `blueutil --unpair <MAC-address>`
2. Turn NXT off/on
3. Re-pair with PIN 1234
4. Test with `python nxt-diag.py`

### Problem: Commands sent but nothing happens

**Cause**: Bluetooth RFCOMM channel dropped

**Solution**:
- Run [`./reset_nxt.sh`](./reset_nxt.sh) to reset connection
- Wait 10 seconds after pairing before testing

### Problem: Display patterns work, but text/drawings don't

**Cause**: Missing `updateDisplay()` method

**Solution**: 
- Ensure you're using [`legonxt_turbowarp.js`](./legonxt_turbowarp.js) (latest version)
- Call "🖥️ update display" block after drawing operations
- Wait 2-3 seconds for display update to complete

### Problem: `ModuleNotFoundError: No module named 'serial'`

**Cause**: Must install python package `pyserial`

**Solution**:
```bash
pip install pyserial
```

### Problem: "Port not found" error

**macOS**: Use `/dev/cu.NXT` (NOT e.g. `/dev/cu.Bluetooth-Incoming-Port`)

**Windows**: Check Device Manager for COM port number

**Linux**: Try `/dev/rfcomm0` or create with `rfcomm bind`

## ⚡ Performance Notes

### Display Operations
- **Update time**: 1-3 seconds per display update
- **Strategy**: Batch all drawing operations, call `updateDisplay()` once
- **Buffer size**: 800 bytes (100×64 pixels ÷ 8 bits)

```javascript
// Good pattern (faster)
clearScreen();
drawText('Line 1', 0, 0);
drawText('Line 2', 0, 10);
drawRect(0, 0, 100, 64, false);
updateDisplay();  // Single 1-3s operation

// Bad pattern (slower)
drawText('Line 1', 0, 0);
updateDisplay();  // 1-3s wait
drawText('Line 2', 0, 10);
updateDisplay();  // Another 1-3s wait
```

## 🔬 Protocol Details

### NXT Telegram Structure
```
[2-byte length (LE)] [command type] [opcode] [payload...]
```

**Command Types**:
- `0x00`: Direct command (with reply)
- `0x80`: Direct command (no reply)
- `0x01`: System command (with reply)
- `0x02`: Reply telegram

**Key Opcodes**:
- `0x03`: PLAY_TONE
- `0x04`: SET_OUT_STATE (motors)
- `0x05`: SET_IN_MODE (sensors)
- `0x07`: GET_IN_VALS (read sensor)
- `0x0B`: GET_BATT_LVL (battery)
- `0x0F`/`0x10`: LS_WRITE/LS_READ (I2C)
- `0x94`/`0x95`: READ_IO_MAP/WRITE_IO_MAP (display)

### Display Memory Layout
- **Resolution**: 100×64 pixels (monochrome)
- **Module ID**: `0xA0001` (little-endian)
- **Offset**: 119
- **Format**: 800 bytes, 8 vertical pixels per byte
- **Bit order**: LSB = top pixel, MSB = bottom pixel

## 📜 License

This project is licensed under the GNU General Public License v3.0.

**Happy building! 🤖**

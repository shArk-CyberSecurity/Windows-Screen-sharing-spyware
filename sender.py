import subprocess
import sys
import os
import time
import json
from pathlib import Path
import ctypes
import psutil

"""
RTMP Screen Streamer + Auto-Startup Installer
Identical startup mechanism to your working MSS code
Streams to Restream.io 24/7 - Auto-restarts on crash
"""

# ============================================================================
# RTMP STREAMER FUNCTIONS (KEEP ALL ORIGINAL)
# ============================================================================

def save_config(url, key):
    with open("sender.json", "w") as f:
        json.dump({"url": url, "key": key}, f)

def get_config():
    config = Path("sender.json")
    if config.exists():
        try:
            with open(config) as f:
                d = json.load(f)
            return d["url"], d["key"]
        except:
            pass
    url = "rtmp://live.restream.io/live"
    key = "re_11107479_event5118ef0032d04e13a6990c43867b8a79"
    save_config(url, key)
    return url, key

def production_cmd(url, key):
    return [
        "ffmpeg", "-f", "gdigrab", "-framerate", "30", "-offset_x", "0",
        "-offset_y", "0", "-video_size", "1920x1080", "-draw_mouse", "1",
        "-i", "desktop", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "veryfast", "-profile:v", "high", "-level:v", "4.0",
        "-b:v", "2500k", "-maxrate", "2500k", "-bufsize", "5000k",
        "-r", "30", "-g", "60", "-keyint_min", "60", "-sc_threshold", "0",
        "-f", "flv", f"{url}/{key}"
    ]

def kill_existing_ffmpeg():
    for p in psutil.process_iter(['name']):
        try:
            if p.info['name'].lower() == 'ffmpeg.exe':
                p.kill()
        except:
            pass
    time.sleep(3)

def ffmpeg_running():
    for p in psutil.process_iter(['name']):
        try:
            if p.info['name'].lower() == 'ffmpeg.exe':
                return True
        except:
            pass
    return False

def run_rtmp_sender():
    """Main RTMP sender - IDENTICAL TO YOUR MSS infinite loop"""
    print("🎬 RTMP Sender Active - Streaming 24/7")
    print("-" * 50)
    
    url, key = get_config()
    
    while True:  # INFINITE RESTART LOOP (like your MSS)
        try:
            kill_existing_ffmpeg()
            cmd = production_cmd(url, key)
            
            proc = subprocess.Popen(
                cmd,
                stdout=open(os.devnull, 'w'),
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW | 0x08000000
            )
            
            print("✅ Streaming live...")
            
            # Wait for FFmpeg to finish (crash/restart)
            proc.wait()
            print("🔄 FFmpeg stopped - Restarting in 2s...")
            time.sleep(2)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e} - Restarting...")
            time.sleep(2)

# ============================================================================
# STARTUP INSTALLER (EXACT COPY OF YOUR WORKING MSS METHOD)
# ============================================================================

def create_silent_launcher():
    """Create VBS launcher EXACTLY like your MSS code"""
    script_path = os.path.abspath(__file__)
    python_exe = sys.executable
    
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{python_exe}" & Chr(34) & " " & chr(34) & "{script_path}" & Chr(34) & " --sender", 0
Set WshShell = Nothing
'''
    
    startup_folder = os.path.join(
        os.environ['APPDATA'],
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    
    vbs_path = os.path.join(startup_folder, 'RTMPSender.vbs')
    
    try:
        with open(vbs_path, 'w') as f:
            f.write(vbs_content)
        return vbs_path
    except:
        return None

def install_to_startup():
    """EXACT installer from your MSS code"""
    print("=" * 70)
    print(" " * 20 + "RTMP SCREEN STREAMER INSTALLER")
    print("=" * 70)
    print("\nInstalls 24/7 RTMP streaming to Restream.io")
    print("Auto-starts on Windows boot - completely silent")
    
    input("\nPress Enter to install (Ctrl+C to cancel)...")
    
    print("\n[1/2] Installing to startup...")
    vbs_path = create_silent_launcher()
    
    if vbs_path:
        print(f"✓ Installed: {vbs_path}")
    else:
        print("✗ Installation failed")
        return
    
    print("\n[2/2] Launching streamer...")
    try:
        subprocess.Popen([sys.executable, __file__, "--sender"])
        print("✓ Streamer launched in background!")
    except:
        subprocess.Popen(['wscript', vbs_path])
    
    print("\n" + "=" * 70)
    print("✅ INSTALLATION COMPLETE!")
    print("🎥 Streaming to Restream.io 24/7")
    print("\nTo STOP: Delete", os.path.basename(vbs_path))
    print("To REINSTALL: Delete sender.json + run again")
    input("\nPress Enter to exit installer...")

# ============================================================================
# MAIN ENTRY POINT (IDENTICAL TO YOUR MSS)
# ============================================================================

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--sender':
        run_rtmp_sender()  # SILENT MODE (startup)
    else:
        install_to_startup()  # INTERACTIVE MODE (first run)

if __name__ == "__main__":
    main()
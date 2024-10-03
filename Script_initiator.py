import logging
import os
import subprocess
import platform
import sys
import argparse
from datetime import datetime
import configparser

# Read configuration from config file
config = configparser.ConfigParser()
config.read('config.ini')

log_file = config['logging']['log_file']
log_level = config['logging']['log_level']
log_format = config['logging']['log_format']

# Get the current year and month
current_time = datetime.now()
log_filename = f'{log_file}-{current_time.strftime("%Y-%m")}.log'

# Configure logging
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level.upper()))

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_filename, mode='a')  # Append mode

# Create formatters and add them to handlers
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def is_script_running(script_path):
    current_pid = os.getpid()
    script_name = os.path.basename(script_path)
    if platform.system() == "Windows":
        escaped_script_path = script_path.replace("\\", "\\\\")
        cmd = (
            '$currentPID = $PID; '
            'Get-WmiObject Win32_Process | '
            'Where-Object { $_.CommandLine -ne $null } | '
            f'Where-Object {{ $_.CommandLine -match "python.*{escaped_script_path}" }} | '
            f'Where-Object {{ $_.CommandLine -notmatch "{script_name}" }} | '
            'Where-Object { $_.ProcessId -ne $currentPID } | '
            'Select-Object ProcessId, CommandLine'
        )
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        processes = [
            line for line in result.stdout.splitlines()
            if script_path in line and str(current_pid) not in line
        ]
    else:
        cmd = f'ps -ef | grep "[/]{script_path}" | grep -v grep | grep -v {current_pid} | grep -v {script_name}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        processes = result.stdout.splitlines()
    
    return len(processes) > 0

def start_script(script_path):
    if platform.system() == "Windows":
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["python3", script_path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check and run a script if not already running.")
parser.add_argument("script_path", help="The full path to the script to check and run.")
args = parser.parse_args()

script_path = args.script_path

if is_script_running(script_path):
    logger.info(f"{script_path} is already running.")
else:
    logger.info(f"{script_path} is not running. Starting it now...")
    start_script(script_path)
    sys.exit()
import logging
import os
import subprocess
import platform
import sys
import argparse
from datetime import datetime
import configparser

# Read configuration from config file
config = configparser.ConfigParser()
config.read('config.ini')

log_file = config['logging']['log_file']
log_level = config['logging']['log_level']
log_format = config['logging']['log_format']

# Get the current year and month
current_time = datetime.now()
log_filename = f'{log_file}-{current_time.strftime("%Y-%m")}.log'

# Configure logging
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level.upper()))

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_filename, mode='a')  # Append mode

# Create formatters and add them to handlers
formatter = logging.Formatter(log_format)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def is_script_running(script_path):
    current_pid = os.getpid()
    script_name = os.path.basename(script_path)
    if platform.system() == "Windows":
        escaped_script_path = script_path.replace("\\", "\\\\")
        cmd = (
            '$currentPID = $PID; '
            'Get-WmiObject Win32_Process | '
            'Where-Object { $_.CommandLine -ne $null } | '
            f'Where-Object {{ $_.CommandLine -match "python.*{escaped_script_path}" }} | '
            f'Where-Object {{ $_.CommandLine -notmatch "{script_name}" }} | '
            'Where-Object { $_.ProcessId -ne $currentPID } | '
            'Select-Object ProcessId, CommandLine'
        )
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        processes = [
            line for line in result.stdout.splitlines()
            if script_path in line and str(current_pid) not in line
        ]
    else:
        cmd = f'ps -ef | grep "{script_path}" | grep -v grep | grep -v {current_pid} | grep -v {script_name}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        processes = result.stdout.splitlines()
    
    return len(processes) > 0

def start_script(script_path):
    if platform.system() == "Windows":
        subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["python3", script_path], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Check and run a script if not already running.")
parser.add_argument("script_path", help="The full path to the script to check and run.")
args = parser.parse_args()

script_path = args.script_path

if is_script_running(script_path):
    logger.info(f"{script_path} is already running.")
else:
    logger.info(f"{script_path} is not running. Starting it now...")
    start_script(script_path)
    sys.exit()

import sys
import pytz
import socket
import psutil 
import datetime
import platform
import subprocess
from tzlocal import get_localzone
from importlib.metadata import version

def get_cpu_model():
    if platform.system() == 'Windows':
        try:
            command = 'wmic cpu get name /value'
            output = subprocess.check_output(command, shell=True, 
                                             universal_newlines=True)
            cpu_model = output.strip().split('=')[1]
            return cpu_model
        except subprocess.CalledProcessError:
            return "Unknown"
    elif platform.system() == 'Linux':
        try:
            command = "cat /proc/cpuinfo | grep 'model name' | uniq"
            output = subprocess.check_output(command, shell=True, 
                                             universal_newlines=True)
            cpu_model = output.strip().split(':')[1].strip()
            return cpu_model
        except subprocess.CalledProcessError:
            return "Unknown"
    else:
        return "Unknown"
    
def get_machine_info():
    gb = 1024.0 ** 3
    machine_info = dict(
        machine_name = socket.gethostname(),
        machine_timezone = str(get_localzone()),
        operating_system = platform.system(),
        os_version = platform.release(),
        cpu_model = get_cpu_model(),
        cpu_architecture = platform.machine(),
        cpu_cores = psutil.cpu_count(), # includes hyperthreads
        total_memory = round(psutil.virtual_memory().total / gb, 2)
        )
    return machine_info

def get_resource_usage(tz = 'America/New_York'):
    
    utc_now = datetime.datetime.utcnow()
    tz = pytz.timezone(tz)
    dttm = utc_now.astimezone(tz)
    dttm =  dttm.strftime("%Y-%m-%d %H:%M:%S.%f %Z")
    cpu_used = psutil.cpu_percent()
    memory_used = psutil.virtual_memory().percent 
    usage = dict(
        cpu_used = str(cpu_used) + '%',
        memory_used = str(memory_used)  + '%',
        datetime = dttm
        )
    return usage

def get_env_info(pkgs = None):
    py_ver = ".".join(str(component) for component in sys.version_info[:3])
    
    pkg_ver = dict()
    pkgs = [pkgs] if type(pkgs) == str else pkgs
    pkgs = pkgs if pkgs else list()
    for pkg in pkgs:
        pkg_ver[pkg] = version(pkg)
        
    env_info = dict(python_version = py_ver,
                    python_path = sys.executable,
                    package_versions = pkg_ver)
    
    return env_info
        
def sys_info(pkgs = None, tz = 'America/New_York'):
    machine_info = get_machine_info()
    usage = get_resource_usage(tz)
    env_info = get_env_info(pkgs)
    out = dict(
        system_name = machine_info['machine_name'],
        system_timezone = machine_info['machine_timezone'],
        datetime = usage['datetime'],
        operating_system = machine_info['operating_system'],
        os_version = machine_info['os_version'],
        cpu_model = machine_info['cpu_model'], 
        cpu_architecture = machine_info['cpu_architecture'],
        cpu_cores = machine_info['cpu_cores'],
        cpu_used = usage['cpu_used'],
        total_memory = machine_info['total_memory'],
        memory_used = usage['memory_used']
        )
    out = {**out, **env_info}
    return out
    

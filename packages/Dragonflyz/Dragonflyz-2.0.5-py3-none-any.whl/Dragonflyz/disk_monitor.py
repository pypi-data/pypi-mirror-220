import inspect
import subprocess

from pathlib import Path
from typing import TypeAlias

Standardized_Bytes: TypeAlias = [str, float]

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def run(command: str):
    return subprocess.run(command, capture_output=True).stdout.decode().strip()

def standardize_disk(str_value: str, option: str = 'G') -> Standardized_Bytes:
    val, size = float(str_value[:-1]), str_value[-1]
    
    match size:
        case 'K':
            val *= 10 ** 3
        case 'M':
            val *= 10 ** 6
        case 'G':
            val *= 10 ** 9
        case _:
            pass
            
    match option:
        case 'G':
            return [f'{val / 10 ** 9}G', val]
        case _:
            raise Exception(f'Not supporting {option} right now!') 
       
# WARNING: Spaces in names screws this up 
# Standardizes to gigabytes for now
def check_disks():
    disks = {}
    
    # First line is header: Filesystem\tSize\Used\Avail\tUse%\tMounted On
    ## Return bytes with K, M and G
    for line in run(['df', '-h']).split('\n')[1:]:
        try:
            name, size, used, avail, used, mounted, *args = [item.strip() for item in line.strip().split()]
            
            disks[name] = {}
            
            for item in (size, used, avail):
                item_name = retrieve_name(item)[0]
                
                disks[name][item_name] = {}
                disks[name][item_name]['str'], disks[name][item_name]['value'] = standardize_disk(item)
                
            disks[name]['used'] = used
            disks[name]['mounted'] = mounted
            disks[name]['disk'] = True
        except:
            print(f'The following line failed: {line}')
        
    return disks
    
def get_database_size(path: Path, option: str = 'G') -> Standardized_Bytes:
    val = path.stat().st_size
    
    match option:
        case 'G':
            return [f'{val / 10 ** 9}G', val]
        case _:
            raise Exception(f'Not supporting {option} right now!')

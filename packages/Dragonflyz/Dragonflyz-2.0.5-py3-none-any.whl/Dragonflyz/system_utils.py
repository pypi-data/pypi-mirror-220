import re

from typing import Any, TypeAlias
from pathlib import Path
from abc import ABC, abstractmethod

File_Contents: TypeAlias = str

# Get the general idea of what the memory/cpu environment is... asynchroneous ops
class ProcHandler(ABC):    
    
    @classmethod
    def read_file(cls, path_of_interest: Path) -> File_Contents:        
        with open(str(path_of_interest)) as reader:
            return reader.read().strip()
                
    
    def __init__(self):
        self.data = None
        
    @abstractmethod    
    def pull_info(self):
        pass
        
    def __str__(self):
        return "\n".join([line.strip() for line in self.data.split('\n')])
        
    def __repr__(self):
        return self.__str__() 
        
    def __enter__(self):
        self.pull_info()
        
        return self
        
    def __exit__(self, exc_type, exc, tb):
        pass  
        
class MemoryHandler(ProcHandler):
    mem_info: Path = Path('/proc/meminfo')
    
    def pull_info(self):
        self.data = self.read_file(self.mem_info)
        
    def get_json(self):
        result_json = {}
        
        for line in self.data.split('\n'):
            name, value = line.strip().split(':')
            value = value.strip()
            result_json[name] = value
        
        return result_json
        
    def basic_memory_info(self):
        memory_data = self.get_json()
        
        return {'Total Memory': memory_data['MemTotal'], 'Free Memory': memory_data['MemFree'], 'Available Memory': memory_data['MemAvailable']}
    
class CpuHandler(ProcHandler):
    cpu_info: Path = Path('/proc/cpuinfo')
    
    def pull_info(self):
        self.data = self.read_file(self.cpu_info)
        
    def get_json(self):
        result_json = {}
        # processor_section_matches 
        p = [m for m in re.finditer(f'^processor.*:', self.data, re.MULTILINE)]
        
        processor_section_ranges = [(p[i].start(), p[i + 1].start()) for i in range(len(p) - 1)] + [(p[-1].start(), -1)]
        processor_sections = [self.data[r[0]:r[1]] for r in processor_section_ranges][0]
        #print(processor_sections.split('\n'))
        for line in processor_sections.split('\n'):
            try:
                name, value = line.split(':')
                if not value:
                    raise Exception(f'{name} has a bad value!')
                
                name = name.strip()
                value = value.strip()
                result_json[name] = value
            except:
                pass

        return result_json 
        
    # Doesn't work on devices displaying only one processor
    def basic_cpu_info(self, all_capabilities: bool = True):
        for cpu_core, values in sorted(self.get_json().items(), key = lambda x: int(x[0].split()[-1])):
            model_name = values['model name']
            if all_capabilities:
                capabilities = values['flags']
            else:
                capabilities = [item for item in values['flags'].split() if item in ['fpu', 'sse3', 'sse4a', 'avx', 'avx2']]
            print(f"Cpu core {cpu_core}\n\tModel Name:\t{model_name}\n\tCapabilities:\t{capabilities}")
            
        
if __name__ == "__main__":
    # Memory section
    with MemoryHandler() as memory:
        print(memory.basic_memory_info())
        
    # Cpu section
    with CpuHandler() as cpu:
        print(cpu.get_json())
        # print(cpu.basic_cpu_info(all_capabilities=False))


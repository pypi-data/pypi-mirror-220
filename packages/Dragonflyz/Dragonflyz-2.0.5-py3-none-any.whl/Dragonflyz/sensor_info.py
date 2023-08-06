import subprocess

# Assumes positive Celsius
def sensor_info(with_adapter: bool = True, tolerance: float = 50):
    devices = {}
    
    name = None
    adapter = None
    
    for line in subprocess.run(['sensors'], capture_output=True).stdout.decode().strip().split('\n'):
        line = line.strip().split(':')
        length = len(line)
        
        match length:
            case 1:
                if '(' not in line[0] and line[0] != '':
                    # Shouldnt be repeats

                    name = line[0]
                    devices[name] = {}
            case 2:
                if '+' in line[1]:
                    # Get rid of colon
                    identifier = line[0].strip()
                    # Get rid of leading +
                    temperature = float(line[1].split()[0].strip()[1:-2])
                    extras = {'temperature': temperature}
                    
                    try:
                        extremes = line[1].split('(')[1].split(',')
                        
                        for extreme in extremes:
                            key, val = extreme.split('=')
                            key = key.strip()
                            val = val.strip()
                            if ')' in val:
                                val = val[:-1]
                                
                            # Disgard low for now
                            if key in ('high', 'crit'):
                                extras[key] = float(val.strip()[1:-2])
                            
                        if 'high' not in extras.keys() and 'crit' in extras.keys():
                            extras['high'] = extras['crit']
                        elif 'high' in extras.keys() and 'crit' not in extras.keys():
                            extras['crit'] = extras['high']
                            
                        goodness_val = extras['temperature'] + tolerance
                        
                        if  goodness_val < extras['high']:
                            extras['goodness'] = 'Good'
                        elif extras['temperature'] < extras['crit']:
                            extras['goodness'] = 'Ok'
                        else:
                            extras['goodness'] = 'Bad'
                    
                    except Exception as e:
                        print(f'Error {e}; for the following line: {line}')
                        extras['goodness'] = 'Ok'
                    
                    if with_adapter:
                        devices[name][adapter][identifier] = extras
                    else:
                        devices[name][identifier] = extras
                else:
                    if with_adapter:
                        adapter = line[1].strip()
                        devices[name][adapter] = {}
            case _:
                # blank line
                pass
            
    return devices  

def print_devices(devices: dict, with_adapter: bool = True):
    for key, values in devices.items():
        print(f'Device: {key}')
        if with_adapter:
            for adapter, sensors in values.items():
                print(f'\tAdapter: {adapter}')
                for sensor, extras in sensors.items():
                    try:
                        print(f"\t\t{sensor} Sensor:\n\t\t\tTemperature:\t{extras['temperature']}\
                            \n\t\t\tHigh Temperature:\t{extras['high']}\n\t\t\tCritical Temperature:\t{extras['crit']}")
                    except:
                        print(f'\t\t{sensor} Sensor:\n\t\tTemperature:\t{extras["temperature"]}')
        else:
            for sensor, extras in values.items():
                try:
                    print(f"\t{sensor} Sensor:\n\t\tTemperature:\t{extras['temperature']}\
                        \n\ttHigh Temperature:\t{extras['high']}\n\t\tCritical Temperature:\t{extras['crit']}")
                except:
                    print(f'\t{sensor} Sensor:\n\t\tTemperature:\t{extras["temperature"]}')
                    
if __name__ == "__main__":
    print_devices(sensor_info(with_adapter=False), with_adapter=False)
    print(sensor_info(with_adapter=False))

import os
import time
import functools
# from PenguinServices import verifyFolder, openFile
import panel as pn

def verifyFoler(path):
    return path if path[-1] == '/' else path + '/'
    
def openFile(path, splitLines: bool = True):
    with open(path) as reader:
        data = reader.read().strip()
        
    return data if not splitLines else data.split('\n')
    
class EnergyTracer:
    def __init__(self, intervalSecs = 0.5):
        self.vals = {} # first ones in lists are baseline
        self.intervalSecs = intervalSecs
        
        self.setup()

    def convertVal(self, val: str):
        return float(val) / 10 ** 6

    def setup(self):
        baseDir = "/sys/class/powercap/intel-rapl/"
        self.locations = {}

        for each in os.listdir(baseDir):
            if each.count(":") == 1:
                self.locations[each] = verifyFolder(os.path.join(baseDir, each)) + "energy_uj"
                self.vals[each] = [self.convertVal(openFile(self.locations[each], splitLines = False))]
        
    def getStates(self):
        return {key: [vals[idx] - vals[0] for idx in range(1, len(vals))] for key, vals in self.vals.items()}

    def addState(self):
        for key, val in self.locations.items():
            self.vals[key].append(self.convertVal(openFile(val, splitLines = False)))

class EnergyDeco(EnergyTracer):
    def __init__(self, fxn, panel, bounds):
        super().__init__()
        self.fxn = fxn
        self.panel = panel
        self.bounds = bounds

    def __call__(self, *args, **kwargs):
        result = self.fxn(*args, **kwargs)
        self.addState()
        
        if self.panel:
            template = pn.template.MaterialTemplate(title = '', header_background = '#b9d5f0', main=[pn.Row(pn.indicators.Gauge(name = "Energy Consumption", value = int(sum([val[0] for val in self.getStates().values()])), bounds = self.bounds, format = '{value} Joule', colors = [(0.2, 'green'), (0.8, 'gold'), (1, 'red')]))])
            template.show()
        else:
            return self.getStates()

def EnergyConsumed(panel = False, bounds = (0, 100)):
    def _EnergyDeco(function):
        return EnergyDeco(function, panel, bounds)
    return _EnergyDeco

def totalEnergy(energyConsumedJson):
    return f"{sum([sum(deviceVals) for deviceVals in energyConsumedJson.values()])} Joules used during this execution!"

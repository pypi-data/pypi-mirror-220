import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Date:
    day: int
    month: int
    year: int

    def __str__(self):
        return f"{self.day}-{self.month}-{self.year}"

    def __int__(self):
        return self.day + (self.month + 1) * 100 + (self.year + 1) * 1000

    def pad(self, integer, padding = 2):
        string = str(integer)
        while len(string) < padding:
            string = "0" + string
        return string

    def datetime_format(self):
        year = self.pad(self.year, padding = 4)
        month = self.pad(self.month)
        day = self.pad(self.day)
        return f"{year}-{month}-{day}"

class Date_Range_Generator:
    days = [32, 29, 32, 31, 32, 31, 32, 32, 31, 32, 31, 32]
    months = {0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul", 7: "Aug", 8: "Sept", 9: "Oct", 10: "Nov", 11: "Dec"}

    def __init__(self, day, month, year, count = 10):
        month -= 1
        if month > 11 or month < 0:
            raise Exception("There are only twelve months")
        if day > self.days[month] or day < 1:
            raise Exception(f"The maximum days for {self.months[month]} are {self.days[month]}")
        self.day = day
        self.month = month
        self.year = year
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        if self.count > 0:
            day = int(self.day)
            month = int(self.month)
            year = int(self.year)
            date = Date(day, month, year)
            self.day, self.month, self.year = self.generate_next_day(day, month, year)
            self.count -= 1
            return date
        else:
            raise StopIteration()

    def pad(self, integer):
        res = str(integer)
        
        while len(res) < 2:
            res = "0" + res

        return res
    
    def generate_next_day(self, day, month, year):
        if (day + 1) > self.days[month]:
            month = (month + 1) % 12
            if month == 0:
                year += 1
                month = 1
            day = 1
        else:
            day += 1

        day = self.pad(day)
        month = self.pad(month)
        year = self.pad(year)
        return day, month, year

def project_gantt(tasks, project_name = "", filename = "gantt_project.png", destination = "./"):
    names = tasks["people"].keys()
    jobIds = tasks["jobIds"]

    fig, ax = plt.subplots(figsize=(12,4))
    ax.margins(0.15, 0.15) 
    title = "Software Penetration Testing"
    if project_name:
        title += f"\nProject: {project_name}"

    ax.set_title(title, fontsize = "large", loc = "center", fontweight = "bold", family = "Ariel")
    
    ax.legend(handles = [mpatches.Patch(color = val[1], label = val[0]) for key, val in jobIds.items()], bbox_to_anchor = (0.9, 1.0))

    for name in names:
        for key, val in (tasks['people'][name]).items():
            for date in val:
                ax.barh(name, width=1.0, left=mdates.date2num(datetime.fromisoformat(date)), height=1.0, color=jobIds[key][1], align='center')
    for i in range(len(names)+1):
        ax.axhline(i-0.5, color='black')

    ax.xaxis_date()
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    ax.autoscale(enable=True, axis='y', tight=True)
    #plt.show()
    plt.savefig(f'{destination}{filename}')

# length of project is in mins
def sprint_gantt(tasks, project_length = 180, project_name = "", filename = "gantt_project.png", destination = "./"):
    jobs = ['tab:orange', 'tab:red', 'tab:blue', 'tab:green', 'tab:purple', 'tab:pink', 'tab:olive']

    fig, gnt = plt.subplots()
    
    title = "Software Kill Chain Analysis"
    if project_name:
        title += f"\nProject: {project_name}"

    gnt.set_title(title, fontsize = "large", loc = "center", fontweight = "bold", family = "Ariel")
    
    gnt.legend(handles = [mpatches.Patch(color = x[0].split(":")[1], label = x[1]) for x in zip(jobs, ["Code Analysis", "Modification", "Access", "Execute", "State Analysis", "Networking", "Your Move"])])

    names = list(tasks.keys())
    num_people = len(tasks)
    num_jobs = max([len(person) for person in tasks])
    
    if num_jobs > 7:
        raise Exception("Only 7 phases in the software kill chain")
    
    ylim = num_people * 15 + 100
    
    gnt.set_ylim(0, ylim)
    gnt.set_xlim(0, project_length)
 
    gnt.set_xlabel('Minutes On Project')
    gnt.set_ylabel('White Hats/Sw Engineers')
 
    gnt.set_yticks([x for x in range(15, num_people * 15 + 15, 15)])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(names)
 
    # Setting graph attribute
    gnt.grid(True)

    for idx, name in enumerate(names):
        gnt.broken_barh(tasks[name]['jobs'], ((idx + 1) * 15 - 5, 9), facecolors = [jobs[x] for x in range(len(tasks[name]['jobs']))])
 
    plt.savefig(f'{destination}{filename}')

def map_job_ids(tasks, people):
    for name, val in people.items():
        tasks['people'][name] = {}
        for jobId, dateObj in val.items():
            for date in dateObj:
                if jobId in tasks['people'][name]:
                    tasks['people'][name][jobId].append(date.datetime_format())
                else:
                    tasks['people'][name][jobId] = [date.datetime_format()]
    return tasks

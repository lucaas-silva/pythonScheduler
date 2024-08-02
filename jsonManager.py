import json
from task import Task

class JsonManager:
    def __init__(self):
        with open("file.json", "r") as file:
            file_contents = json.load(file)

        self.simulation_time = file_contents["simulation_time"]
        self.scheduler_name = file_contents["scheduler_name"].lower()
        self.task_number = file_contents["tasks_number"]
        self.tasks = self.create_task_list(file_contents["tasks"])
        self.timeCpuUsed = 0

    def create_task_list(self, tasks):
        taskList = []
        for task in tasks:
            offset = task["offset"]
            computation_time = task["computation_time"]
            period_time = task["period_time"]
            quantum = task["quantum"]
            deadline = task["deadline"]
            n = 0 
            id = 0 

            taskTemp = Task(offset, computation_time, period_time, quantum, deadline, n, id)
            taskList.append(taskTemp)
        return taskList
            
    
    def __str__(self):
        return f"simulation_time: {self.simulation_time}\nscheduler_name: {self.scheduler_name}\ntask_number: {self.task_number}\ntasks: {self.tasks}\n" + ("..." * 21)

from logs import Logs 
from task import Task

class Scheduler:
    def __init__(self, schedulerInfos):
        self.info = schedulerInfos
        self.tasks = schedulerInfos.tasks
        self.cpu = [None]
        self.readyQueue = []
        self.finishedQueue = []
        self.log = Logs()

        for n, task in enumerate(self.tasks):
            task.id = n + 1


    def fcfs(self):
        for i in range(0, self.info.simulation_time + 1):
            self.addToReadyQueue(i)

            if self.cpu[0] is not None:
                self.compute(i)
            if self.cpu[0] is None and len(self.readyQueue) > 0:
                self.removeFromReadyQueue()
            self.printLogs(i)
        self.log.printLogs(self.info, self.finishedQueue, 0)

    def roundRobin(self):
        for i in range(0, self.info.simulation_time + 1):
            self.addToReadyQueue(i)

            if self.cpu[0] is not None:
                self.compute(i)
            if self.cpu[0] is None and len(self.readyQueue) > 0:
                self.removeFromReadyQueue()
            self.printLogs(i)
        self.log.printLogs(self.info, self.finishedQueue, 0)

    def rateMonotonic(self):
        utilizationSum = sum([task.computation_time / task.period_time for task in self.tasks]) 

        if utilizationSum > 1:
            print("Warning: the set is not scalable")
            return

        for i in range(self.info.simulation_time + 1):
            self.addToReadyQueue(i)
            if self.cpu[0] is not None:
                self.compute(i)
            if self.cpu[0] is None and len(self.readyQueue) > 0:
                self.removeFromReadyQueue()

            self.checkMissedDeadLine(i)
            self.printLogs(i)
        self.finalizeSimulation(utilizationSum)

    def earliestDeadlineFirst(self):
        utilizationSum = sum([task.computation_time / task.period_time for task in self.tasks]) 

        if utilizationSum > 1:
            print("Warning: the set is not scalable")
            return

        for i in range(self.info.simulation_time + 1):
            self.addToReadyQueue(i)

            self.readyQueue.sort(key=lambda task: task.deadline)

            if self.cpu[0] is not None:
                self.compute(i)
            if self.cpu[0] is None and len(self.readyQueue) > 0:
                self.removeFromReadyQueue()

            self.checkMissedDeadLine(i)
            self.printLogs(i)
        self.finalizeSimulation(utilizationSum)


    def compute(self, i):
        if self.cpu[0] is not None:
            self.cpu[0].computation_time -= 1

            if self.cpu[0].quantum != 0:
                self.cpu[0].quantum -= 1

            self.info.timeCpuUsed += 1
            
            for task in self.readyQueue:
                if task.offset != i and (i - task.offset) % task.period_time != 0:
                    task.waiting_time += 1
            if self.cpu[0].computation_time == 0:
                self.cpu[0].computation_time = self.cpu[0].initial_computation_time
                self.finishedQueue.append(self.cpu[0])
                self.cpu[0] = None
            else:
                match self.info.scheduler_name:
                    case "fcfs":
                        pass
                    case "rr":
                        if self.cpu[0].quantum == 0:
                            self.cpu[0].quantum = self.cpu[0].initial_quantum
                            self.readyQueue.append(self.cpu[0])
                            self.cpu[0] = None
                    case "rm":
                        for task in self.readyQueue:
                            if self.cpu[0].deadline > task.period_time:
                                self.readyQueue.append(self.cpu[0])
                                self.cpu[0] = task
                                self.readyQueue.remove(task)
                    case "edf":
                        for task in self.readyQueue:
                            if self.cpu[0].deadline > task.deadline:
                                self.readyQueue.append(self.cpu[0])
                                self.cpu[0] = task
                                self.readyQueue.remove(task)

    def addToReadyQueue(self, i):
        for task in self.tasks:
            if task.offset == i or (i - task.offset) % task.period_time == 0:
                task.initial_computation_time = task.computation_time
                task.initial_quantum = task.quantum
                task.n += 1

                periodicTask = Task(i, task.computation_time, task.period_time, task.quantum, task.deadline * task.n, task.n, task.id)
                self.readyQueue.append(periodicTask)

    def removeFromReadyQueue(self):
        self.cpu[0] = self.readyQueue.pop(0)

    def checkMissedDeadLine(self, i):
        for task in self.readyQueue:
            if task.deadline == i:
                task.countMissedDeadLines += 1
                print(f"MISSED DEADLINE OF TASK {task.id} AT TIME {i}")

    def printLogs(self, i):
        print(f"@ CURRENT TIME: {i}")
        print(f"@ CPU: {self.cpu[0]}")
        print(f"@ READY QUEUE: {self.readyQueue}")
        print(f"@ finishedQueue: {self.finishedQueue}")
        print("..."*21) 

    def finalizeSimulation(self, utilizationSum=0):
        if self.cpu[0] is not None:
            self.finishedQueue.append(self.cpu[0])
            self.cpu[0] = None

        self.log.printLogs(self.info, self.finishedQueue, utilizationSum)

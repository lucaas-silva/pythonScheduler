import math
class Logs:

    def printLogs(self, info, queue, utilizationSum):
        for task in queue:
            print(f"Task {task.id}: Waiting time: {task.waiting_time} | Turnaround time: {task.computation_time + task.waiting_time}")

            if task.countMissedDeadLines != 0:
                print(f"\nLost deadline for task {task.id}")
                print(f"Frequency of lost deadlines = {(task.n - 1)/task.countMissedDeadLines}")
            if task.waiting_time + task.initial_computation_time > info.simulation_time:
                print(f"\nStarvation of task {task.id}")

        biggestWaitingTime = max(queue, key=lambda task: task.waiting_time)
        smallestWaitingTime = min(queue, key=lambda task: task.waiting_time)
        biggestTurnAroundTime = max(queue, key=lambda task: task.computation_time + task.waiting_time)
        smallestTurnAroundTime = min(queue, key=lambda task: task.computation_time + task.waiting_time)

        print(f"\nUtilization Time: {info.timeCpuUsed/info.simulation_time}")
        print(f"Productivity: {len(queue)/info.simulation_time}")
        print(f"\nBiggest and Smallest waiting time: \n{biggestWaitingTime} ({biggestWaitingTime.waiting_time}) | {smallestWaitingTime} ({smallestWaitingTime.waiting_time})")
        print(f"Biggest and Smallest turnaround time: \n{biggestTurnAroundTime} ({biggestTurnAroundTime.waiting_time + biggestTurnAroundTime.computation_time}) | {smallestTurnAroundTime} ({smallestTurnAroundTime.waiting_time + smallestTurnAroundTime.computation_time})")

        print("\nScalability Test: ")
        match info.scheduler_name:
            case "fcfs", "rr":
                print("Test is not necessary")
            case "rm":
                print(f"u = {utilizationSum} <= {info.task_number * (math.pow(2,1/info.task_number)-1)}")
            case "edf":
                print(f"u = {utilizationSum} <= {1}")

        print("\nAvarage waiting time and turnaround time of each task (multiple executions): ")

        for i in range(1, info.task_number + 1):
            appearances = 1 
            waitingTimeSum = 0
            lifeTimeSum = 0

            # for task in queue:
            #     if(task.id == i):
            #         waitingTimeSum += task.waiting_time
            #         lifeTimeSum += task.computation_time + task.waiting_time
            #         appearances = task.n
            waitingTimeSum += sum([task.waiting_time for task in queue if task.id == i])
            lifeTimeSum += sum([task.computation_time + task.waiting_time for task in queue if task.id == i])
            appearances = max([task.n for task in queue if task.id == i], default=1) 
                    
            print(f"Task {i}: (appearances = {appearances}): WT avg = {waitingTimeSum/appearances}| TT avg = {lifeTimeSum/appearances}")

        waitingTimeSum, lifeTimeSum = 0, 0 

        for i in range(1, info.task_number + 1):
            n = max([task.n for task in queue if task.id==i], default=1)
            waitingTimeSum += sum([task.waiting_time/n for task in queue if task.id==i])
            lifeTimeSum += sum([(task.computation_time + task.waiting_time)/n for task in queue if task.id==i])
        print(f"Waiting time (avg sys): {waitingTimeSum / info.task_number}")
        print(f"Turnaround time (avg sys): {lifeTimeSum / info.task_number}")

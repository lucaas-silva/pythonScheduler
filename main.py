from jsonManager import JsonManager
from scheduler import Scheduler

if __name__ == "__main__":
    schedulerInfos = JsonManager()
    scheduler = Scheduler(schedulerInfos)
    print(schedulerInfos)

    match schedulerInfos.scheduler_name:
        case "fcfs":
            scheduler.fcfs()
        case "rr":
            scheduler.roundRobin()
        case "rm":
            scheduler.rateMonotonic()
        case "edf":
            scheduler.earliestDeadlineFirst()


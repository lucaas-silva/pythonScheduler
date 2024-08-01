class Task:
    def __init__(self, offset, computation_time, period_time, quantum, deadline, n, id=0):
        self.offset = offset
        self.computation_time = computation_time
        self.period_time = period_time
        self.quantum = quantum
        self.deadline = deadline
        self.id = id
        self.n = n
        self.waiting_time = 0
        self.initial_computation_time = computation_time
        self.initial_quantum = quantum
        self.countMissedDeadLines = 0

    def __str__(self):
        return f"Task {self.id}"

    def __repr__(self):
        return self.__str__()

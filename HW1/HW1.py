import math
class Task:
    def __init__(self, task_id, priority, transmission_time, period):
        self.task_id = task_id
        self.priority = priority
        self.transmission_time = transmission_time
        self.period = period
        self.worst_response_time = 0
        
def CAN_schedule(n, tau, tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x.priority)
        
    for i in range(n):
        task = sorted_tasks[i]
        B = max((t.transmission_time for t in sorted_tasks[i: ]), default=0)
        Q = B
        RHS = 0
        while True:
            Q_plus_tau = Q + tau
            RHS = B
            for j in range(i):
                RHS += math.ceil(Q_plus_tau / sorted_tasks[j].period) * sorted_tasks[j].transmission_time
                
            if Q == RHS:
                break
            
            Q = RHS
        
        task.worst_response_time = round(task.transmission_time + Q, 5)
        
        if task.worst_response_time > task.period:
            return False
    
    tasks = sorted(sorted_tasks, key=lambda x: x.task_id)
    return True
    
    

if __name__ == '__main__':
    with open('./input.dat', 'r') as file:
        lines = file.readlines()
        n = int(lines[0])
        tau = float(lines[1])
        tasks = [Task(i, int(P), float(C), int(T)) for i, (P, C, T) in enumerate(line.split() for line in lines[2:])]
        
    if not CAN_schedule(n, tau, tasks):
        print("No feasible schedule")
        exit()
        
    for task in tasks:
        print(f"Task {task.task_id:02d}'s worst response time: {task.worst_response_time:.5f}")
    total_worst_response_time = sum(task.worst_response_time for task in tasks)
    print(f"Total worst response time: {total_worst_response_time:.5f}")
        
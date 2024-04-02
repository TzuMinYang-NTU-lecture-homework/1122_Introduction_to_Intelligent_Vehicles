import math
import random
import copy

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

def cost(n, tau, S): # sum Task.worst_response_time, will set worst_response_time
    if not CAN_schedule(n, tau, S):
        return 1e10
    else:
        return sum(task.worst_response_time for task in S)

def neighbor(S): # Randomly choose two tasks, and swap their priorities
    i, j = random.sample(range(n), 2)
    S[i].priority, S[j].priority = S[j].priority, S[i].priority

def Simulated_Annealing(n, tau, tasks):
        
    T = 10000
    T0 = 0.001
    r = 0.995
    
    S = copy.deepcopy(tasks)
    
    best_S = copy.deepcopy(S)
    best_total_worst_response_time = cost(n, tau, best_S)
    
    while T > T0:
        cost_S = cost(n, tau, S) 
        S_prime = copy.deepcopy(S)
        neighbor(S_prime)
        cost_S_prime = cost(n, tau, S_prime)
        delta_C = cost_S_prime - cost_S
        P = min(1, math.exp(-1 * delta_C / T))
        S = S_prime if random.random() < P else S
        
        cost_S = cost(n, tau, S)
        if cost_S < best_total_worst_response_time:
            best_S, best_total_worst_response_time = copy.deepcopy(S), cost_S
        
        T *= r
        
    return best_S, best_total_worst_response_time

if __name__ == '__main__':
    with open('./input.dat', 'r') as file:
        lines = file.readlines()
        n = int(lines[0])
        tau = float(lines[1])
        tasks = [Task(i, int(P), float(C), int(T)) for i, (P, C, T) in enumerate(line.split() for line in lines[2:])]
        
    tasks, best_total_worst_response_time = Simulated_Annealing(n, tau, tasks)
    for task in tasks:
        print(task.priority)
    print(f"{best_total_worst_response_time:.5f}")
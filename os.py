#Producer consumer problem
import threading
import time
CAPACITY = 10
buffer = [-1 for i in range(CAPACITY)]
in_index = 0
out_index = 0

mutex = threading.Semaphore()
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)

class Producer(threading.Thread):
    def run(self):
        global CAPACITY,buffer,in_index,out_index
        global mutex,empty,full
        item_produced = 0
        counter = 0
        while item_produced < 20:
            empty.acquire()
            mutex.acquire()
            counter += 1
            buffer[in_index] = counter
            in_index = (in_index+1)%CAPACITY
            print("producer produced:",counter)
            mutex.release()
            full.release()
            time.sleep(1)
            item_produced += 1
class Consumer(threading.Thread):
    def run(self):
        global CAPACITY,buffer,in_index,out_index,counter
        global mutex,empty,full
        item_consumed = 0
        while item_consumed < 20:
            full.acquire()
            mutex.acquire()
            item = buffer[out_index]
            out_index = (out_index+1)%CAPACITY
            print("consumer consumed item:",item)
            mutex.release()
            empty.release()
            time.sleep(2.5)
            item_consumed += 1
producer = Producer()
consumer = Consumer()
producer.start()
consumer.start()
producer.join()
consumer.join()



#Reader Writer problem
#Aim: Write a program to give solution for reader-writer problem.
import time
from threading import Thread,Lock,Semaphore

class SharedResource:
    MAX_READERS = 10
    
    def __init__(self):
        self.rsemaphore = Semaphore(SharedResource.MAX_READERS)
        self.wlock = Lock()
    
class Reader:
    def __init__(self,name,resource):
        self.name = name
        self.resource = resource
    
    def read(self):
        while self.resource.wlock.locked():
            continue
        self.resource.rsemaphore.acquire()
        
        print(f"Reader{self.name} reading data")
        time.sleep(1)
        print(f"Reader {self.name} reading done")
        self.resource.rsemaphore.release()
    
class Writer:
    def __init__(self,name,resource):
        self.name = name
        self.resource = resource
        
    def write(self):
        while self.resource.rsemaphore._value != SharedResource.MAX_READERS: 
            continue
        self.resource.wlock.acquire()
        print(f"Writer {self.name} writing data")
        time.sleep(2)
        print(f"Writer {self.name} writing done")
        self.resource.wlock.release()
        
if __name__=='__main__':
    sr = SharedResource()
    reader1 = Reader("reader1", sr)
    reader2 = Reader("reader2", sr)
    reader3 = Reader("reader3", sr)
    writer1 = Writer("writer1", sr)
    writer2 = Writer("writer1", sr)
        
    Thread(target=reader1.read).start()
    Thread(target=writer1.write).start()
    time.sleep(10)
    Thread(target=reader2.read).start()
    Thread(target=writer2.write).start()
    Thread(target=reader3.read).start()
    
        
    
    
#fcfs
print("FIRST COME FIRST SERVE SCHEDULING")
n = int(input("Enter Number Of Processes: "))
d = dict()
# Input arrival and burst times for each process
for i in range(n):
    key = "p" + str(i+1)
    a = int(input("Enter Arrival Time Of Process " + str(i+1) + ": "))
    b = int(input("Enter Burst Time Of Process " + str(i+1) + ": "))
    l = []
    l.append(a)
    l.append(b)
    d[key] = l
    
    
# Sort processes by arrival time
d = sorted(d.items(), key=lambda item: item[1][0])
# Calculate Exit Time (ET), Turn Around Time (TAT), and Waiting Time (WT)
ET = []
TAT = []
WT = []
total_wt = 0
for i in range(len(d)):
    if i == 0:
        ET.append(d[i][1][0] + d[i][1][1])
    else:
        ET.append(ET[i-1] + d[i][1][1])
    
    TAT.append(ET[i] - d[i][1][0])
    WT.append(TAT[i] - d[i][1][1])
    total_wt += WT[i]


avg_WT = total_wt / n


# Display the scheduling results
print("Process | Arrival | Burst | Exit | Turn Around | Wait |")
for i in range(n):
    print("   ", d[i][0], "   |  ", d[i][1][0], "   ", d[i][1][1], "   ", ET[i], "   |  ", TAT[i], "   |  ", WT[i], "  |  ")

print("Average Waiting Time: ", avg_WT)





#FiFO
from collections import deque
def fifo_page_replacement(page_reference_string, num_frames):
    page_frames = deque(maxlen = num_frames)
    page_set = set()
    page_faults = 0
    for page in page_reference_string:
        if page not in page_set:
            if len(page_frames) == num_frames:
                oldest_page = page_frames.popleft()
                page_set.remove(oldest_page)
            page_frames.append(page)
            page_set.add(page)
            page_faults += 1
        print(f"Current Page Frames: {list(page_frames)}")
    return page_faults
page_reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
num_frames = 3
page_faults = fifo_page_replacement(page_reference_string, num_frames)
print(f"Total Page Faults: {page_faults}")


#Bounded Buffer problem
import threading
#Buffer size
N = 1
#Buffer init
buff = [0]*N

fill_count=threading.Semaphore(0)
empty_count = threading.Semaphore(N)
stop_event=threading.Event()

def produce():
    print("One item produced!")
    return 1

def producer():
    front=0
    while not stop_event.is_set():
        x=produce()
        empty_count.acquire()
        buff[front] = x
        print(f"Produced: {x} at position{front}")
        fill_count.release()
        front = (front + 1) % N

def consume(y):
    print("One itm consumed!")
    

def consumer():
    rear = 0
    while not stop_event.is_set():
        fill_count.acquire()
        y = buff[rear]
        print(f"Consumed: {y} from position {rear}")
        empty_count.release()
        consume(y)
        rear = (rear + 1) % N

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()
stop_event.set()

producer_thread.join()
consumer_thread.join()
print("Production and consumption stopped")


#RR alogorithm
if __name__ == "__main__":
    print("Enter total process number:")
    total_p_no = int(input())
    total_time = 0
    total_time_consumed = 0
    proc = []
    wait_time = 0
    turnaround_time = 0
    for _ in range(total_p_no):
        print("Enter process arrival time and burst time:")
        input_info = list(map(int, input().split(" ")))
        arrival, burst, remaining_time = input_info[0], input_info[1], input_info[1]
        proc.append([arrival, burst, remaining_time, 0])
        total_time += burst
    print("Enter time quantum:")
    time_quantum = int(input())
    while total_time != 0:
        for i in range(len(proc)):
            if proc[i][2] <= time_quantum and proc[i][2] >= 0:
                total_time_consumed += proc[i][2]
                total_time -= proc[i][2]
                proc[i][2] = 0
            elif proc[i][2] > 0:
                proc[i][2] -= time_quantum
                total_time -= time_quantum
                total_time_consumed += time_quantum
            if proc[i][2] == 0 and proc[i][3] != 1:
                wait_time += total_time_consumed - proc[i][0] - proc[i][1]
                turnaround_time += total_time_consumed - proc[i][0]
                proc[i][3] = 1
    print("Avg Waiting time is ", (wait_time * 1) / total_p_no)
    print("Avg turnaround time is ", (turnaround_time * 1) / total_p_no)



#Banker algorithm
import numpy as np
class BankersAlgorithm:
    def __init__(self, max_resources, allocation, maximum):
        self.max_resources = np.array(max_resources)
        self.allocation = np.array(allocation)
        self.maximum = np.array(maximum)
        self.n_processes = len(allocation)
        self.n_resources = len(max_resources)
        self.need = self.maximum - self.allocation
    def is_safe(self):
        work = self.max_resources - self.allocation.sum(axis=0)
        finish = [False] * self.n_processes
        safe_sequence = []
        while len(safe_sequence) < self.n_processes:
            progress_made = False
            for i in range(self.n_processes):
                if not finish[i] and all(self.need[i] <= work):
                    work += self.allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    progress_made = True
                    break
            if not progress_made:
                return False, []
        return True, safe_sequence
    def request_resources(self, process_id, request):
        if any(request > self.need[process_id]):
            raise ValueError("Request exceeds maximum claim.")       
        if any(request > self.max_resources - self.allocation.sum(axis=0)):
            raise ValueError("Request exceeds available resources.")
        self.allocation[process_id] += request
        self.need[process_id] -= request
        safe, _ = self.is_safe()
        if not safe:
            self.allocation[process_id] -= request
            self.need[process_id] += request
            raise ValueError("Request cannot be granted as it leads to an unsafe state.")
        return True
if __name__ == "__main__":
    max_resources = [10, 5, 7]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    bankers = BankersAlgorithm(max_resources, allocation, maximum)
    safe, sequence = bankers.is_safe()
    if safe:
        print("The system is in a safe state.")
        print("Safe sequence is:", sequence)
    else:
        print("The system is not in a safe state.")     
    process_id = 1
    request = [1, 0, 2]
    try:
        bankers.request_resources(process_id, request)
        print(f"Request for process {process_id} has been granted.")
    except ValueError as e:
        print(f"Request for process {process_id} cannot be granted: {e}")



#NONpreemtion
def priority(process_list):
    gantt = []
    t = 0
    completed = {}
    while process_list != []:
        available = []
        for p in process_list:
            arrival_time = p[3]
            if arrival_time <= t:
                available.append(p)
        if available == {}:
            gantt.apend("Idle")
            t += 1
            continue
        else:
            available.sort()
            process = available[0]
            process_list.remove(process)
            pid = process[1]
            gantt.append(pid)
            burst_time = process[2]
            t += burst_time
            ct = t
            arrival_time = process[3]
            tt = ct - arrival_time
            wt = tt - burst_time
            completed[pid] = [ct, tt, wt]
    print(gantt)
    print(completed)
if __name__ == "__main__":
    process_list = [[5,"p1",6,2],[4,"p2",2,5],[1,"p3",8,1],[2,"p4",3,0],[3,"p5",4,4]]
    priority(process_list)

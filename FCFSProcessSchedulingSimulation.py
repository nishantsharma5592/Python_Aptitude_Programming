# The problem is so defined. Several processes come at different arrival times 
# to a server. Each process has an associated arrival time and an associated 
# burst time (service time). We are asked to calculate the average waiting 
# time of a process and the average turnaround time. A server only serves one 
# process at a time with some scheduling paradigm. We consider the First Come 
# First Served paradigm here

# Consider the following process chart
# Process name    Arrival time    Burst time
#   P0              1               6
#   P1              1               8
#   P2              2               7
#   P3              3               3

# We create the process class:

class Process:
    def __init__(self, _name, _arrival_time, _burst_time):
        self.name = _name
        self.arrival_time = _arrival_time
        self.burst_time = _burst_time
        self.remaining_execution_time = _burst_time # This time can be 
        # decremented per loop iteration
        self.waiting_time = 0.0
        self.turnaround_time = 0.0
        self.checkpoint_time = 0.0 # in case of interruption
        self.finished = False # when the process has finished execution
        self.in_progress = False # Is the process currently in progress?
    def getName(self):
        return self.name
    def getArrivalTime(self):
        return self.arrival_time
    def getBurstTime(self):
        return self.burst_time
    def getRemainingExecutionTime(self):
        return self.remaining_execution_time
    def updateRemainingExecutionTime(self):
        self.remaining_execution_time = self.remaining_execution_time - 1 # 
        # Decremented by 1 always
    def getWaitingTime(self):
        return self.waiting_time
    def updateWaitingTime(self, wt):
        self.waiting_time = self.waiting_time + wt
    def getTurnaroundTime(self):
        return self.turnaround_time
    def setTurnaroundTime(self, tt):
        self.turnaround_time = self.turnaround_time + tt
    def getCheckpointTime(self):
        return self.checkpoint_time
    def updateCheckpointTime(self, ct):
        self.checkpoint_time = self.checkpoint_time + ct
    def getFinishedStatus(self):
        return self.finished
    def setFinishedStatus(self, status):
        self.finished = status
    def getInProgressStatus(self):
        return self.in_progress
    def updateInProgressStatus(self, status):
        self.in_progress = status

# We need to know when all processes have finished executing for the simulation 
# to stop
def have_all_processes_finished(process_list):
    for process in process_list:
        if process.getFinishedStatus() == False:
            return False
    return True

# We also need to know if any process is in progress at a particular time
# [so that we do not start a new process until the current executing process
# has finished executing]
def is_any_process_in_progress(process_list):
    for process in process_list:
        if process.getInProgressStatus() == True:
            return True
    return False

# For FCFS we need to know that process whose arrival time is minimum. If two 
# processes clash in arrival time, we pick the one with the minimum burst time

def choose_new_process_to_start(process_list, current_time):
    possible_processes_to_schedule = [process for process in process_list\
            if (process.getArrivalTime() <= current_time) and \
            (process.getFinishedStatus() != True)]
     
    """ 
    print ("Possible processes to schedule at time:", current_time, "is (are):"\
            , [process.getName() for process in \
            possible_processes_to_schedule])
    """

    # If there is no possible process to schedule:
    if possible_processes_to_schedule == []:
        return None
    
    # Among all possible processes to schedule we wish to choose those
    # that have the minimum arrival time

    min_arrival_time = 99999
    # First, we just find what is the minimum arrival time
    for process in possible_processes_to_schedule:
        if process.getArrivalTime()<min_arrival_time:
            min_arrival_time = process.getArrivalTime()

    # Then we extract processes with the minimum arrival time
    processes_with_minimum_arrival_time = [process for process in \
            possible_processes_to_schedule \
            if process.getArrivalTime()==min_arrival_time] 

    # If there is only one such process [with minimum arrival time]:
    if len(processes_with_minimum_arrival_time) == 1:
        return processes_with_minimum_arrival_time[0]
    # If there are more than one of those with minimum arrival time, 
    # then we select the one that has the minimum burst time
    elif len(processes_with_minimum_arrival_time)>1:
        min_burst_time = 99999
        choice = None
        for process in processes_with_minimum_arrival_time:
            if process.getBurstTime() < min_burst_time:
                min_burst_time = process.getBurstTime()
                choice = process
        return choice
    else: # The control will never reach here! 
        return None
        
def fcfs(process_list):
    timer = 1
    while(True):
        
        if have_all_processes_finished(process_list):
            break
        
        if is_any_process_in_progress(process_list)==False:
            # See if there is any new process that may be started:
            process_to_start = choose_new_process_to_start(process_list, timer)
            if process_to_start != None:
                print("At time:", timer, "process",\
                        process_to_start.getName(), "was started!")
                # Set the process in progress status to true
                process_to_start.updateInProgressStatus(True)
                process_to_start.updateWaitingTime(timer -\
                        process_to_start.getArrivalTime())
        
        current_executing_process = [process for process in process_list \
                if process.getInProgressStatus() == True][0]
        
        """ 
        print("Current executing process at time", timer, "is:", \
                current_executing_process.getName())
        """    

        current_executing_process.updateRemainingExecutionTime() 
        
        """ 
        print("The remaining execution time of:", \
                current_executing_process.getName(), "is:",\
                current_executing_process.getRemainingExecutionTime())
        """

        # Has this process finished?
        if (current_executing_process.getRemainingExecutionTime() == 0):
            current_executing_process.updateInProgressStatus(False)
            current_executing_process.setFinishedStatus(True)
            current_executing_process.setTurnaroundTime\
                    (timer - current_executing_process.getArrivalTime() + 1)
        # Update timer 
        timer = timer + 1
     
if __name__ == "__main__":
    
    p0 = Process("P0", 1, 6)
    p1 = Process("P1", 1, 8)
    p2 = Process("P2", 2, 7)
    p3 = Process("P3", 3, 3)
    
    # print(p3.getArrivalTime())
    
    process_list = [p0, p1, p2, p3]
    
    fcfs(process_list)
    
    print("First Come First Served Statistics (FCFS):")
    
    # Let us print the waiting time for each process (FCFS)
    print("Waiting time of processes (FCFS):")
    for process in process_list:
        print("Process", process.getName(),"was recorded to have", \
                "waiting time:", process.getWaitingTime())
    
    # Average waiting time (FCFS):
    avg_waiting_time_process = sum([process.getWaitingTime() for process in\
            process_list])/len(process_list)
    
    print("Average waiting time of a process (FCFS):",\
            avg_waiting_time_process)

    # Let us print the turnaround time for each process (FCFS)
    print("Turnaround time of processes (FCFS):")
    for process in process_list:
        print("Process", process.getName(),"was recorded to have", \
                "turnaround time:", process.getTurnaroundTime())
    
    # Average turnaround time (FCFS):

    avg_turnaround_time_process = sum([process.getTurnaroundTime() for process in\
            process_list])/len(process_list)
    
    print("Average turnaround time of a process (FCFS):",\
            avg_turnaround_time_process)



        

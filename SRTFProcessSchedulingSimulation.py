# The problem is so defined. Several processes come at different arrival times 
# to a server. Each process has an associated arrival time and an associated 
# burst time (service time). We are asked to calculate the average waiting 
# time of a process and the average turnaround time. A server only serves one 
# process at a time with some scheduling paradigm. We consider the Shortest 
# Remaining Time First paradigm here

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
        self.turnaround_time = tt
    def getCheckpointTime(self):
        return self.checkpoint_time
    def updateCheckpointTime(self, ct):
        self.checkpoint_time = ct
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

# The SRTF scheduling works as follows: If a new process arrives, the remaining
# execution time of all processes that have arrived so far is compared.
# The process with the shortest remaining execution time is selected to be started
# Any currently executing process may be paused (interrupted)

def has_any_process_arrived_in_current_time(process_list, current_time):
    for process in process_list:
        if process.getArrivalTime() == current_time:
            return True
    return False

def choose_process_with_minimum_execution_time_remaining_among_all_executing_processes\
        (process_list, current_time):
            # Let us first find what is the minimum execution time remaining
            # among processes
            minimum_execution_time_remaining = 99999
            for process in process_list:
                if (process.getFinishedStatus() != True) and \
                        (process.getArrivalTime() <= current_time)\
                        and process.getRemainingExecutionTime() > 0\
                        and process.getRemainingExecutionTime() < \
                        minimum_execution_time_remaining:
                        minimum_execution_time_remaining =\
                                process.getRemainingExecutionTime()

            # Then we extract the process with the minimum execution time
            # remaining
            for process in process_list:
                if (process.getFinishedStatus()!= True) and\
                        (process.getRemainingExecutionTime() ==\
                        minimum_execution_time_remaining) and \
                        (process.getArrivalTime() <= current_time):
                            return process
            return None
            
def srtf(process_list):
    timer = 1
    current_executing_process = None
    while(True):

        # Among all processes that have arrived till the current time [in
        # interruption] we select the one that has the minimum remaining 
        # execution time
        if has_any_process_arrived_in_current_time(process_list, timer):
            process_to_start =\
                    choose_process_with_minimum_execution_time_remaining_among_all_executing_processes(process_list, timer)
            
            # If there is no currently executing process:
            # set process to start = the currently executing process
            if current_executing_process == None:
                current_executing_process = process_to_start
                print("At time:", timer, "process",\
                        process_to_start.getName(), "was started!")
            
                # The waiting time of this process is 0.0
            
            # If the currently executing process is selected during the 
            # current time as well:
            elif current_executing_process == process_to_start:
                print("At time:", timer, "process",\
                        process_to_start.getName(), "continued!") 
                pass

            # If there is a currently executing process and it has not been
            # selected during the current time; then update its internal
            # variables
            else:
                current_executing_process.updateCheckpointTime(timer)
                print(current_executing_process.getName(), "was recorded"\
                        " to have checkpoint:", \
                        current_executing_process.getCheckpointTime())
                current_executing_process.updateInProgressStatus(False)
                # Update the currently executing process
                current_executing_process = process_to_start
                print("At time:", timer, "process",\
                        process_to_start.getName(), "was started!")
                if (current_executing_process.getCheckpointTime() == 0):
                    current_executing_process.updateWaitingTime(timer - \
                        current_executing_process.getArrivalTime())
                else:
                    current_executing_process.updateWaitingTime(
                        timer + 1  -\
                        current_executing_process.getCheckpointTime())
            
                current_executing_process.updateInProgressStatus(True)
                
        current_executing_process.updateRemainingExecutionTime() 
         
        print("The remaining execution time of:", \
                current_executing_process.getName(), "is:",\
                current_executing_process.getRemainingExecutionTime())

        # Has this process finished?
        if (current_executing_process.getRemainingExecutionTime() == 0):
            current_executing_process.updateInProgressStatus(False)
            current_executing_process.setFinishedStatus(True)
            current_executing_process.setTurnaroundTime\
                    (timer - current_executing_process.getArrivalTime() + 1)
            
            # Check if all processes have now finished
            if have_all_processes_finished(process_list):
                break

            # If not, we must schedule another process
            current_executing_process = choose_process_with_minimum_execution_time_remaining_among_all_executing_processes(process_list, timer + 1)
            
            print("At time:", timer + 1, "process",\
                        current_executing_process.getName(), "was started!")
            
            if (current_executing_process.getCheckpointTime() == 0):
                current_executing_process.updateWaitingTime(timer + 1 - \
                        current_executing_process.getArrivalTime())
            else:
               current_executing_process.updateWaitingTime(
                       timer + 1  -
                        current_executing_process.getCheckpointTime())
            
        # Update timer 
        timer = timer + 1
     
if __name__ == "__main__":
    
    p0 = Process("P0", 1, 6)
    p1 = Process("P1", 1, 8)
    p2 = Process("P2", 2, 7)
    p3 = Process("P3", 3, 3)
    
    # print(p3.getArrivalTime())
    
    process_list = [p0, p1, p2, p3]
    
    srtf(process_list)
    
    print("Shortest Remaining Time First (SRTF) Statistics:")
    
    # Let us print the waiting time for each process (SRTF)
    print("Waiting time of processes (SRTF):")
    for process in process_list:
        print("Process", process.getName(),"was recorded to have", \
                "waiting time:", process.getWaitingTime())
    
    # Average waiting time (SRTF):
    avg_waiting_time_process = sum([process.getWaitingTime() for process in\
            process_list])/len(process_list)
    
    print("Average waiting time of a process (SRTF):",\
            avg_waiting_time_process)

    # Let us print the turnaround time for each process (SRTF)
    print("Turnaround time of processes (SRTF):")
    for process in process_list:
        print("Process", process.getName(),"was recorded to have", \
                "turnaround time:", process.getTurnaroundTime())
    
    # Average turnaround time (SRTF):

    avg_turnaround_time_process = sum([process.getTurnaroundTime() for process in\
            process_list])/len(process_list)
    
    print("Average turnaround time of a process (SRTF):",\
            avg_turnaround_time_process)     

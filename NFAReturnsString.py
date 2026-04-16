# If the given Non-deterministic Finite State Automaton NFA 
# accepts any string, return one such string; 
# Otherwise, return None

# This exercise assumes an understanding of NFAs [which
# succeed Deterministic Finite State Automaton (DFA)]: 

# A brief:
# In a Non-deterministic Finite State Automaton (NFA):
# -> On taking an input alphabet, we can
# transition from an input state to more than one next states;
# -> Unlike Deterministic Finite State Automaton (DFA), 
# we do not need to specify transitions on
# all input symbols
# -> If there is a path to any of the final_states
# [staring at the start_state: here 1] then we consider
# the input_string to be accepted

# This problem is tricky!
# Instead of using a complicated recursion; i propose
# to use the augmented vertex strategy; and
# finding simple paths

# A Bellman Ford algorithm with constant weight 1 can help us
# in finding simple paths from a start_state to all states in NFA

class Vertex():
    def __init__(self, _name):
        self.name = _name
        self.distance_from_source =  99999
        self.predecessor = None
    
    def getName(self):
        return self.name
    
    def getDistanceFromSource(self):
        return self.distance_from_source

    def setDistanceFromSource(self, d):
        self.distance_from_source = d

    def getPredecessor(self):
        return self.predecessor

    def setPredecessor(self, _pi):
        self.predecessor = _pi


# The function to relax an edge [in Bellman Ford algorithm]:
def relax(edge):
    # Weight is 1 (a fixed constant)
    sv = edge[0]
    dv = edge[2]
    ew = 1 # weight

    if (dv.getDistanceFromSource() > sv.getDistanceFromSource() + ew):
        dv.setDistanceFromSource(sv.getDistanceFromSource() + ew)
        dv.setPredecessor(sv)
        return True # This is a return on relax
    return False

# Bellman ford algorithm:
# We get the number of vertices as a separate input, to keep things simple

def bellmanFord(graph, no_of_vertices):
    for i in range(1, no_of_vertices): # one less than the number of vertices
        for edge in graph:
            relax(edge)

    # Evaluate if the algorithm succeeded
    for edge in graph:
        sv = edge[0]
        dv = edge[2]
        ew = 1 # weight
        if (dv.getDistanceFromSource() > sv.getDistanceFromSource() + ew):
            return False
    return True


def nfaReturnsString(nfa, start_state, final_states):
    # We first apply the Bellman Ford algorithm to
    # generate simple paths from the start_state to all_states
    bellmanFord(nfa, 5)
    
    """
    for each in vertices:
        if each.getPredecessor() != None:
            print(each.getName(), each.getDistanceFromSource(),\
                each.getPredecessor().getName())
        else:
            print(each.getName(), each.getDistanceFromSource(),\
                "None")
    """

    # We are interested in establishing if there is a simple path from
    # final_states back to start_state

    # For this particular example, let us say that we look at only one final_state
    final_state = final_states[0]
    
    # This is the method that establishes a simple path from the start_state
    # to a final_state if one exists
    def predecessorList(start_state, final_state, p_list): 
        if final_state == start_state:
            p_list = [start_state] + p_list
            return p_list
        
        prev_state = final_state.getPredecessor()
        new_p_list = [final_state] + p_list
        return predecessorList(start_state, prev_state, new_p_list) 
    
    if final_state.getPredecessor() != None:
        # Then we construct the predecessor list
        pred_list_final_state = predecessorList(start_state, final_state, [])
    
        # Here, we construct the return string
        ret_str = ""
        for i in range(len(pred_list_final_state)-1):
            j = i+1
            source = pred_list_final_state[i]
            destination = pred_list_final_state[j] 
            desired_edge = [edge for edge in nfa if edge[0] == source \
                        and edge[2] == destination][0]
            label = desired_edge[1]
            ret_str = ret_str + label
        return ret_str
    else:
        # Otherwise, return None
        return None

if __name__ == "__main__":
    
    # There are maximum five vertices in both of our examples 
    one = Vertex("1")
    two = Vertex("2")
    three = Vertex("3")
    four = Vertex("4")
    five = Vertex("5")
   
    # This is the first example. The accepted string printed is abc
    
    """
    nfa = [[one, "a", two], [one, "a", three], [two, "a", two],\
            [three, "b", four], [three, "b", two], [four, "c", five]]
    
    # You can draw this nfa in your notebook
    # -> Vertex one has a directed edge to vertex two with egde label "a"
    # -> Vertex one also has a directed edge to vertex three with edge label "a"
    # -> and so on
    
    start_state = one
    one.setDistanceFromSource(0)
    final_states = [five] # accepting could have been more than one states
    print(nfaReturnsString(nfa, start_state, final_states))
    """
    
    # This is the second example. It accepts None
    """ 
    nfa = [[one, "a", one], [two, "a", two]]
    start_state = one
    one.setDistanceFromSource(0)
    final_states = [two]
    print(nfaReturnsString(nfa, start_state, final_states))
    """

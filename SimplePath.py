
# A simple path between two nodes [source and destination] in a graph is a 
# path where no vertex is repeated; there are no cycles, etc.

# All we need for that is an augmented definition for a vertex 
# [its name, its distance from source, its predecessor on the shortest path
# from source to destination]

# We consider a directed graph

# Thus, we can use Bellman Ford algorithm to populate the predecessor field 

class Vertex():
    def __init__(self, _name):
        self.name = _name
        self.d = 99999
        self.pi = "nil"
    def getName(self):
        return self.name
    def getDistanceFromSource(self):
        return self.d
    def setDistanceFromSource(self, _d):
        self.d = _d
    def getPi(self):
        return self.pi
    def setPi(self, predecessor):
        self.pi = predecessor

def BellmanFord (graph, V):
    weight = 1 # a constant
    # Bellman ford runs for V-1 times
    for i in range(V-1):
        # We must relax each edge V-1 times
        for each in graph:
            # Here we implement the relax procedure
            source = each[0]
            destination = each[1]
            if destination.getDistanceFromSource() > \
                    source.getDistanceFromSource() + weight:
                destination.setDistanceFromSource\
                        (source.getDistanceFromSource() + weight)
                destination.setPi(source)
    # This is the check cycle [Vth cycle]
    for each in graph:
        if destination.getDistanceFromSource() > \
                source.getDistanceFromSource() + weight:
               return False
    return True
               
def simplePath(graph, source, destination, collect):
    if destination == source:
        collect = [source.getName()] + collect
        return collect
    else:
        pred = destination.getPi()
        collect = [destination.getName()] + collect
        return simplePath(graph, source, pred, collect)

if __name__ == "__main__": 
    s = Vertex("s")
    a = Vertex("a")
    b = Vertex("b")
    c = Vertex("c")
    d = Vertex("d")
    t = Vertex("t")

    # We consider a directed graph 
    graph = [[s, a], [s, b], [b, a], [a, c], [c, b], [b, d], [d, c],\
            [d, t], [c, t]]
    
    s.setDistanceFromSource(0)
    
    BellmanFord(graph, 6)

    # print(t.getDistanceFromSource())
    
    # simple_path_list = simplePath(graph, s, c, [])
    simple_path_list = simplePath(graph, s, t, [])

    print(simple_path_list)
    



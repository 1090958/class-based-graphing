class node:
    def __init__(self, name):
        self.name = name
        self.edges=[]
        self.adjacent=set()
        
    def __str__(self):
        return str(self.name)

class edge:
    def __init__(self,A,B, value):
        self.nodes=(A,B)
        A.adjacent.add(B)
        B.adjacent.add(A)
        self.value = value
        
    def __str__(self):
        return f'({str(self.nodes[0])}, {str(self.nodes[1])})'
    def __getitem__(self, index) ->node:
        return self.nodes[index]
class graph:
    def __init__(self):
        self.nodes=[]
        self.edges = []
    def __str__(self):
        out=''
        for edge_ in self.edges:
            out+=str(edge_)+'\n'
        return out
    def __getitem__(self, item):
        if type(item) == tuple:
            for edge_ in self.edges:
                if edge_.nodes[0].name == item[0] and edge_.nodes[1].name == item[1]:
                    return edge_
                if edge_.nodes[0].name == item[1] and edge_.nodes[1].name == item[0]:
                    return edge_
        else:
            
            for node_ in self.nodes:
                if node_.name == item:
                    return node_
    
    def add_node(self, name):
        
        for node_ in self.nodes:
            if node_.name == name:
                return
        self.nodes.append(node(name))
    
    def add_edge(self,A,B, value = 0):
        #if A == B: return
        self.add_node(A)
        self.add_node(B)
        for edge_ in self.edges:
            if edge_.nodes == (self[A],self[B]) or edge_.nodes == (self[B],self[A]):
                return
        self.edges.append(edge(self[A],self[B], value))
        
    def remove_node(self, node_ : node):
        for node__ in node_.adjacent:
            node__.adjacent.remove(node_)
            
        self.nodes.remove(node_)
        
    def remove_edge(self,edge_):
        
        edge_[0].adjacent.remove(edge_[1])
        edge_[1].adjacent.remove(edge_[0])
        
        self.edges.remove(edge_)
        

    def connect_all_nodes(self):
        nodes1 = [i.name for i in self.nodes]
        for node1 in nodes1:
            nodes2 = [i.name for i in self.nodes if i.name != node1]
            for node2 in nodes2:
                
                #print([i.name for i in graph.nodes])
                self.add_edge(node1, node2, value=bias(node1,node2))
    def paths_between_edges(self, A, B):
        paths = []
        visited = set()
        
        def backtrack(node, path):
            if node == B:
                paths.append(path + [B])
                return

            if node in visited:
                return

            visited.add(node)

            for neighbor in node.adjacent:
                backtrack(neighbor, path + [node])

        backtrack(A, [A])
        return paths
    def is_tree(self):
        count = 0
        for node in self.nodes:
            if node.adjacent == []:
                return self
            if len(node.adjacent) > 2:
                count += 1
        if count > 1:
            return False
        
        for edge in self.edges:
            A=edge.nodes[0]
            B=edge.nodes[1]
            if len(self.paths_between_edges(A, B)) > 1:
                return False
            

        return True

    def is_connected(self):
        return True if len(max(self.nodes, key = lambda node: len(node.adjacent)).adjacent) == 0 else False
    def minimise(self):
        visited = set()
        
        def smallest_unvisited_edge(edges):
            min = float('inf')
            out = None
            for edge_ in edges:
                # will be a cause of problems
                if edge_.value <= min and edge_[0] not in visited or edge_[1] not in visited:
                    min = edge_.value
                    out = edge_
            return out
        newgraph = graph()
        while len(newgraph.nodes) != len(self.nodes):
            newedge = smallest_unvisited_edge(self.edges)
            visited.add(newedge[0])
            visited.add(newedge[1])
            newgraph.add_edge(newedge[0].name,newedge[1].name, value = newedge.value)
        
        self = newgraph 
        # ^ ^ ^ ^ ^ ^ ^
        # | | | | | | |
        # does not work but 
        # will still keep it 
        # here in case I find 
        # a workaround
        return(self)
    
bias = lambda A, B: 1

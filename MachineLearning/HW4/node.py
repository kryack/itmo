'''
This is a class that implements a node in a Bayesian network. 
The distribution field is a dictionary containing the conditional probability distribution of the node given its parents.
The keys to the dictionary are tuples containing the names of the possible states of the node and the evidence of the parents
for each line in the CPD table. If a node has no parents, the distribution will store the marginal distribution.
This is my implementation for a node. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor. 
'''

# node py

class Node:
    def __init__(self, name, node_type, n_states, states, the_property):
        self.name =  name
        self.node_type = node_type
        self.n_states = n_states
        self.states = states
        self.parents = []
        self.children = []
        self.information = []
        self.dist = None
        self.the_property = the_property
        self.marginal = None
    
    def add_children(self, children):
        for a in children:
            self.children.append(a)

    def add_parent(self, parents):
        for a in parents:
            self.parents.append(a)
    
    def is_root(self):
        return self.num_parents() == 0
        
    def is_leaf(self):
        return self.n_hildren() == 0
    
    def get_name(self):
        return self.name
    
    def num_children(self):
        return len(self.children)
    
    def get_states(self):
        return self.states

    def num_states(self):
        return self.n_states
    
    def num_parents(self):
        return len(self.parents)

    def get_parents(self):
        return self.parents

    def get_children(self):
        return self.children
    
    def set_dist(self, distribution):
        self.dist = distribution
        if self.is_root():
            self.marginal = {}
            for key, value in distribution.items():
                i=0
                while i < len(value):
                    self.marginal[(key[i],)] = value[i]
                    i += 1
    
    def get_dist(self):
        return self.dist

    def receive_marginal(self, message, factor):
        if not self.information:
            self.information = [0]*(self.num_children()+(not self.is_root()))
        if factor.get_index(self.get_name()) == 0:
            self.information[0] = message
        else:
            child_name = factor.get_fields()[0].get_name()
            i=0
            while i<len(self.children):
                if child_name == self.children[i].get_name():
                    break
                i+=1
            self.information[i+(not self.is_root())] = message

    def update_marginal(self):
        if not self.is_root():
            the_sum = 0
            vals = {(state,): 1 for state in self.states}
            for a in self.information:
                for ev in a.keys():
                    vals[ev] = vals[ev]*a[ev]

            for val in vals.values():
                the_sum += val

            for key in vals.keys():
                if the_sum != 0:
                    vals[key] = vals[key] /the_sum
            self.marginal = vals

    def get_marginal(self):
        return self.marginal

    def send_marginal(self, target_factor):
        index = -1
        cache_query = target_factor.get_fields()[0].get_name()
        if self.is_root():
            return self.marginal

        if cache_query == self.name:
            index = 0
        else:
            j = 0
            while j < len(self.children):
                if cache_query == self.get_children()[j].get_name():
                    index = j + (not self.is_root())
                j+=1
        _sum=0
        vals = {(state,): 1 for state in self.states}
        i=0
        while i<len(self.information):
            if (i != index):
                for ev in self.information[i].keys():
                    vals[ev] = vals[ev]*self.information[i][ev]
            i += 1
        for val in vals.values():
            _sum += val

        for key in vals.keys():
            vals[key] = vals[key]/_sum
        return vals


    def printNode(self):
        print(self.get_name())
        print("Parents: ")
        for b in self.parents:
            print(c.get_name())
        print("CPD: ")
        print(self.get_dist())
        print("Children: ")
        for c in a.children:
            print(c.get_name())
        print("")
import copy


class Factor:
    def __init__(self, table, nodes):
        self.fields = nodes
        self.states = list(table.keys())[0][0]
        self.potential = {}
        self.information = {}
        for key, value in table.items():
            i = 0
            while i < len(value):
                new_key = [key[0][i]]
                new_key.extend(list(key[1]))
                new_key = tuple(new_key)
                self.potential[new_key] = value[i]
                i += 1

    def receive_belief(self, message, node):
        self.information[node.get_name()] = message

    def get_index(self, node_name):
        i = 0
        while i < len(self.get_fields()):
            if self.fields[i].get_name() == node_name:
                return i
            i += 1

    def get_fields(self):
        return self.fields

    def get_potential(self):
        return self.potential

    def send_belief(self, node):
        i = self.get_index(node.get_name())
        j = len(self.fields)-1
        sum_over = copy.deepcopy(self.potential)
        while j >= 0: 
            if i != j:
                temp_node = self.get_fields()[j]
                key = temp_node.get_name()
                info = copy.deepcopy(self.information[key])
                tuple_keys = sum_over.keys()
                temp_dict = {}
                for tups in tuple_keys:
                    temp_dict[tups[:j] + tups[j+1:]] = 0
                for tups in tuple_keys:
                    temp_dict[tups[:j] + tups[(j+1):]] = temp_dict[tups[:j] + tups[(j+1):]] + sum_over[tups]*info[(tups[j],)]
                sum_over = copy.deepcopy(temp_dict)
            j -= 1
        return sum_over

    def print_factor(self):
        print("Fields: ")
        for a in self.fields:
            print(a.get_name())
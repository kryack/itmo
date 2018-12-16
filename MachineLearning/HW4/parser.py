from node import Node
import re


class Parser:
    def __init__(self, file_name):
        self.file_name = file_name

        with open(self.file_name, 'r+') as bif_file:
            self.row_lines = bif_file.readlines()

    def parse_file(self):

        cleared_lines = list()

        for line in self.row_lines:

            if line != "\n":
                cleared_line = re.sub('([,])', r'\1 ', line)

                cleared_lines.append(cleared_line.strip())

        i = 0
        num_lines = len(cleared_lines)
        nodes = []

        while i < num_lines:
            line_lst = cleared_lines[i].split()

            if line_lst[0] == 'variable':
                name = line_lst[1]
                i += 1
                while cleared_lines[i] != '}':
                    line_lst = cleared_lines[i].split()

                    if line_lst[0] == 'type':
                        type = line_lst[1]
                        num_states = int(line_lst[3])
                        line_lst[6:6 + num_states] = [x.strip(",") for x in line_lst[6:6 + num_states]]
                        states = tuple(line_lst[6:6 + num_states])
                        t_property = ''

                    elif line_lst[0] == 'property':
                        t_property = ''.join(line_lst[1:])

                    i += 1
                nodes.append(Node(name, type, num_states, states, t_property))
            elif line_lst[0] == 'probability':

                cleared_lines[i] = re.sub('([()])', r' \1 ', cleared_lines[i])

                line_lst = cleared_lines[i].split()

                for theNode in nodes:
                    if theNode.get_name() == line_lst[2]:
                        temp = theNode
                        break

                if line_lst[3] == '|':
                    j = 4
                    while line_lst[j] != ')':
                        for parent in nodes:
                            if parent.get_name() == line_lst[j].strip(","):
                                temp.add_parent([parent])
                                parent.add_children([temp])
                                break
                        j += 1
                i += 1
                the_cpd = {}

                while cleared_lines[i] != '}':
                    line_lst = cleared_lines[i].split()

                    if line_lst[0] == 'table':
                        del line_lst[0]
                        table = str.maketrans(dict.fromkeys(',;'))
                        prob = [x.translate(table) for x in line_lst]

                        the_cpd[temp.get_states()] = tuple([float(h) for h in prob])

                    elif line_lst[0][0] == "(":
                        table = str.maketrans(dict.fromkeys('(,;)'))
                        line_lst = [states.translate(table) for states in line_lst]

                        the_cpd[(temp.get_states(), tuple(line_lst[:temp.num_parents()]))] = \
                            tuple([float(h) for h in line_lst[temp.num_parents():]])
                    i += 1
                temp.set_dist(the_cpd)
            else:
                i += 1
        return nodes
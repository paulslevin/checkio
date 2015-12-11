class Graph(object):

    def __init__(self, d):
        self.graph_dict = d
        self.vertices = set(d.keys())
        self.edges = d.values()

    def __repr__(self):
        return str(self.graph_dict)

    def get_edges(self, vertex):
        return self.graph_dict[vertex]

    def dfs(self, start_vertex, visited=None):
        if visited is None:
            visited = set()
        visited.add(start_vertex)
        for next_vertex in self.get_edges(start_vertex) - visited:
            self.dfs(next_vertex, visited)
        return visited

    def get_components(self, components=None):
        if components is None:
            components = []
        seen = set.union(*components) if components else set()
        remaining_vertices = self.vertices - seen
        if not remaining_vertices:
            return components
        vertex = iter(remaining_vertices).next()
        components.append(self.dfs(vertex))
        return self.get_components(components)


class ColouredGraph(Graph):

    def __init__(self, d, c=4):
        Graph.__init__(self, d)
        self.possible_colours = {}
        self.number_of_colours = c
        self.all_colours = range(1, c + 1)
        for v in self.vertices:
            self.possible_colours[v] = range(1, self.number_of_colours + 1)
            self.colours[v] = None

    def get_colour(self, vertex):
        return self.colours[vertex]

    def get_colour_list(self):
        colour_list = [0 for _ in self.vertices]
        for index, colour in self.colours.items():
            colour_list[index] = colour
        return colour_list

    def set_colour(self, vertex, colour):
        self.colours[vertex] = colour
        if colour is None:
            self.possible_colours[vertex] = range(1, self.number_of_colours + 1)
        else:
            self.possible_colours[vertex].remove(colour)

    def is_colouring_locally_valid(self, vertex):
        for edge in self.get_edges(vertex):
            if self.get_colour(vertex) == self.get_colour(edge):
                return False
        return True

    def is_coloured(self):
        if None in self.colours.values():
            return False
        return True

    def is_colouring_valid(self):
        if not self.is_coloured():
            return False
        for v in self.vertices:
            if not self.is_colouring_locally_valid(v):
                return False
        return True

    def get_colouring(self):
        vertex_tuple = tuple(self.vertices)
        index = 0
        while not self.is_colouring_valid():
            current_vertex = vertex_tuple[index]
            current_colour = self.possible_colours[current_vertex][0]
            self.set_colour(current_vertex, current_colour)
            if self.possible_colours[current_vertex] and not \
                    self.is_colouring_locally_valid(current_vertex):
                continue
            elif self.is_colouring_locally_valid(current_vertex):
                index += 1
            else:
                index -= 1
                self.set_colour(current_vertex, None)
        return self.get_colour_list()

"""
Executive function: color_map
Input: tuple of tuples of numbers representing countries.
Output: a 4-coloring of the map
Example: ((0, 0, 0), (0, 1, 1), (0, 0, 2)) --> [1, 2, 3]
Link: http://www.checkio.org/mission/color-map/
"""
from itertools import izip, product


class Graph(object):

    def __init__(self, d):
        self.graph_dict = d
        self.vertices = set(d.keys())
        self.edges = d.values()

    def __repr__(self):
        return str(self.graph_dict)

    def get_edges(self, vertex):
        return self.graph_dict[vertex]


class ColouredGraph(Graph):

    def __init__(self, d, c=4):
        Graph.__init__(self, d)
        self.possible_colours = {}
        self.colours = {}
        self.number_of_colours = c
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


class Map(object):

    def __init__(self, data):
        self.map = data
        self.height = len(data)
        self.width = len(data[0])
        self.product = tuple(product(range(self.height), range(self.width)))
        self.countries = set(self.map[i][j] for i, j in self.product)

    def get_4_neighbours(self, row, col):
        neighbours = []
        for i, j in izip((0, 0, -1, 1), (1, -1, 0, 0)):
            if (row + i, col + j) in self.product:
                neighbours.append(self.map[row + i][col + j])
        return neighbours

    def bordering_countries(self, country):
        bordering = set()
        for row, col in self.product:
            if self.map[row][col] == country:
                bordering.update(self.get_4_neighbours(row, col))
        if country in bordering:
            bordering.remove(country)
        return bordering

    def get_country_graph(self):
        graph_dict = dict((country, self.bordering_countries(country)) for
                          country in self.countries)
        return ColouredGraph(graph_dict)


def color_map(data):
    m = Map(data)
    return m.get_country_graph().get_colouring()

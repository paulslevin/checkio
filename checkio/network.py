"""
Executive function: capture
Input: matrix containing details of a computer network
Output: the time until the whole network is infected
Example: [[0, 1, 0, 1, 0, 1],
          [1, 8, 1, 0, 0, 0],
          [0, 1, 2, 0, 0, 1],
          [1, 0, 0, 1, 1, 0],
          [0, 0, 0, 1, 3, 1],
          [1, 0, 1, 0, 1, 2]] --> 8
Link: http://www.checkio.org/mission/network-attack/
"""


class Network(object):

    def __init__(self, matrix):
        self.network = matrix
        self.computers = set(range(len(matrix)))
        self.infection_times = {0: 0}

    def security_level(self, computer):
        return self.network[computer][computer]

    def infected(self):
        return set(self.infection_times.keys())

    def get_infection_time(self, computer, other_computer):
        return self.infection_times[computer] + self.security_level(
            other_computer)

    def uninfected_adjacents(self, computer):
        return set(
            other_computer for other_computer in self.computers - {computer}
            if self.network[computer][other_computer] and other_computer not
            in self.infection_times.keys())

    def captured(self):
        while len(self.infection_times) != len(self.network):
            candidates = set()
            for computer in self.infected():
                for other_computer in self.uninfected_adjacents(computer):
                    candidates.add((other_computer,
                                    self.get_infection_time(computer,
                                                            other_computer)))
            infected = min(candidates, key=lambda t: t[1])
            self.infection_times[infected[0]] = infected[1]
        return max(self.infection_times.values())


def capture(matrix):
    return Network(matrix).captured()

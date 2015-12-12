"""
Executive function: mind_switcher
Input: tuple of 2-element sets containing bodies who have undergone a mind swap
Output: the sequence of mind swaps required to get everyone back to their
original bodies
Example: ({"scout", "super"},) --> ({"super", "nikola"}, {"sophia", "scout"},
                                    {"nikola", "scout"}, {"sophia", "super"},
                                    {"nikola", "sophia"})
Link: http://www.checkio.org/mission/mind-switcher/
"""


class Futurama(object):

    def __init__(self, bodies):
        self.body_dict = {body: body for body in bodies}

    def perform_swap(self, swap):
        iterswap = iter(swap)
        body1 = iterswap.next()
        body2 = iterswap.next()
        mind1 = self.body_dict[body1]
        mind2 = self.body_dict[body2]
        self.body_dict[body1] = mind2
        self.body_dict[body2] = mind1


def mind_switcher(journal):
    bodies = journal_to_bodies(journal)
    futurama = Futurama(bodies)
    for swap in journal:
        futurama.perform_swap(swap)
    all_cycles = generate_all_cycles(futurama.body_dict)
    cycles = [cycle for cycle in all_cycles if len(cycle) != 1]
    swaps = map(lambda x: solve(x, ["nikola", "sophia"]), cycles)
    if len(swaps) % 2:
        swaps.append([{"nikola", "sophia"}, ])
    return sum(swaps, [])


def journal_to_bodies(journal):
    return list(set.union(*journal))


def generate_cycle(k, d):
    c = dict(d)
    cycle = (k,)
    current_key = k
    while current_key in c.keys():
        if d[current_key] != cycle[0]:
            cycle += (d[current_key],)
        del c[current_key]
        current_key = cycle[-1]
    return cycle


def generate_all_cycles(d):
    cycles = set()
    for k in d:
        cycle = generate_cycle(k, d)
        if set(cycle) not in (set(x) for x in cycles):
            cycles.add(generate_cycle(k, d))
    return cycles


def solve(cycle, robots):
    if len(cycle) == 1:
        return []
    swaps = [{cycle[len(cycle) - 1], robots[0]}]
    for i, _ in enumerate(cycle):
        swaps.append({cycle[i], robots[1]})
    swaps.append({cycle[0], robots[0]})
    return swaps

"""
Executive function: checkio
Input: a labyrinth map as a list of lists with 1 and 0 (12x12) where 1
represents an obstacle; the map is always bordered by 1's and we start at
square (1, 1) and want to reach square (10, 10)
Output: a string of compass directions to escape the labyrinth
Example: [[1,1,1,1,1,1,1,1,1,1,1,1],
          [1,0,0,0,0,0,0,0,0,0,0,1],
          [1,0,1,1,1,1,1,1,0,1,1,1],
          [1,0,1,0,0,0,0,0,0,0,0,1],
          [1,0,1,0,1,1,1,1,1,1,0,1],
          [1,0,1,0,1,0,0,0,0,0,0,1],
          [1,0,0,0,1,1,0,1,1,1,0,1],
          [1,0,1,0,0,0,0,1,0,1,1,1],
          [1,0,1,1,0,1,0,0,0,0,0,1],
          [1,0,1,0,0,1,1,1,1,1,0,1],
          [1,0,0,0,1,1,0,0,0,0,0,1],
          [1,1,1,1,1,1,1,1,1,1,1,1],] --> "EEEEEEESSEESSWWWWSSSEEEESS"
Link: http://www.checkio.org/mission/open-labyrinth/
"""
COMPASS = {(1, 0): "S", (-1, 0): "N", (0, 1): "E", (0, -1): "W"}


def checkio(maze_map):

    poss_directions = {}
    for i in range(1, 11):
        for j in range(1, 11):
            poss_directions[(i, j)] = set()
            if maze_map[i - 1][j] == 0:
                poss_directions[(i, j)].add((i - 1, j))
            if maze_map[i + 1][j] == 0:
                poss_directions[(i, j)].add((i + 1, j))
            if maze_map[i][j - 1] == 0:
                poss_directions[(i, j)].add((i, j - 1))
            if maze_map[i][j + 1] == 0:
                poss_directions[(i, j)].add((i, j + 1))

    pos = (1, 1)
    route = [pos]
    direction_string = ""

    while not pos == (10, 10):
        if poss_directions[pos]:
            new_direction = poss_directions[pos].pop()
            route.append(new_direction)
            poss_directions[new_direction].remove(pos)
            pos = new_direction
        else:
            for i in range(len(route), -1, -1):
                if poss_directions[route[i - 1]]:
                    route = route[:i]
                    pos = route[-1]
                    break

    for i in range(1, len(route)):
        compass_direction = (route[i][0] - route[i - 1][0],
                             route[i][1] - route[i - 1][1])
        direction_string += COMPASS[compass_direction]

    return direction_string

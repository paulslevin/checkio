from fractions import Fraction

start_of_words = ["g", "t", "i", "c"]
end_of_words = ["dl", "ni", "no", "re"]


def checkio(alloys):
    matrix, vector = alloys_to_pair(alloys)
    inverse = invert(matrix)
    return sum(inverse[0][i] * vector[i] for i in range(4))


def invert(matrix):
    """ Invert the given matrix.
    :param matrix:
    """
    copy = [list(row) + [0, 0, 0, 0] for row in matrix]
    for i in range(4):
        copy[i][i + 4] = Fraction(1, 1)
    gaussed = gauss(copy)
    return [row[4:] for row in gaussed]


def alloys_to_pair(alloys):
    """
    Turn the alloys into a matrix m and vector v
    such that m * [g, i, t, c]^T = v^T.
    :param alloys:
    """
    m, v, d = [], [], almost_matrix(alloys)
    for row in d:
        m.append(list(row))
        v.append(d[row])
    m.append([Fraction(1, 1) for _ in range(4)])
    v.append(Fraction(1, 1))
    for i in range(3):
        if m[i][0] == 1:
            m[0], m[i], v[0], v[i] = m[i], m[0], v[i], v[0]
            break
    return m, v


def almost_matrix(alloys):
    """
    Give the three rows of the matrix corresponding
    to the three alloys.
    :param alloys:
    """
    return {create_row(alloy): alloys[alloy] for alloy in alloys}


def create_row(alloy):
    row = [0, 0, 0, 0]
    row[start_of_words.index(alloy[0])] = Fraction(1, 1)
    row[end_of_words.index(alloy[:-3:-1])] = Fraction(1, 1)
    return tuple(row)


def gauss(matrix):
    """Get the inverse using the Gauss-Jordan algorithm.
    :param matrix:
    """
    i, j, height, width = 0, 0, len(matrix), len(matrix[0])
    while i < height and j < width:
        if matrix[i][j] == 0:
            for k in range(i, height):
                if matrix[k][j]:
                    matrix[i], matrix[k] = matrix[k], matrix[i]
                    break
        matrix[i] = [x / matrix[i][j] for x in matrix[i]]
        for k, _ in enumerate(matrix):
            if k != j:
                matrix[k] = [matrix[k][p] - (matrix[k][j] / matrix[i][j]) *
                             matrix[i][p] for p, __ in enumerate(matrix[0])]
        i, j = i + 1, j + 1
    return matrix

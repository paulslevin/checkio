# models the distributive law I discovered
# see http://www.emis.ams.org/journals/TAC/volumes/30/32/30-32.pdf, p.1092


class Dist(object):
    def __init__(self, y):
        self.dist = []
        for i, x in enumerate(y):
            for z in x:
                self.dist.append([z] + [p[0] for p in y[i + 1:]])


class Comonad(object):
    def __init__(self, y):
        self.coprod = []
        for i, x in enumerate(y):
            self.coprod.append(y[i:])
        self.counit = y[0]

import re
BINARY_LENGTHS = {0: 2, 1: 4, 2: 3, 3: 4, 4: 3, 5: 4}


class MorseClock(object):

    def __init__(self, time_string):
        time_string = re.sub(":[0-9]:",
                             lambda m: ":0" + m.group()[1:], time_string)
        time_string = re.sub("\A[0-9]:|:[0-9]\Z",
                             lambda m: "0" + m.group(), time_string)
        self.time = list(time_string.replace(":", ""))
        self.binaries = [bin(int(n))[2:] for n in self.time]
        for i, b in enumerate(self.binaries):
            self.binaries[i] = "0" * (BINARY_LENGTHS[i] - len(b)) + b

    def get_binary_time(self):
        time = ""
        self.morsify()
        for i, b in enumerate(self.binaries):
            if i in {0, 2, 4}:
                time += b + " "
            elif i in {1, 3}:
                time += b + " : "
            else:
                time += b
        return time

    def morsify(self):
        for i, b in enumerate(self.binaries):
            self.binaries[i] = ""
            for char in b:
                if char == "0":
                    self.binaries[i] += "."
                else:
                    self.binaries[i] += "-"


def checkio(time_string):
    return MorseClock(time_string).get_binary_time()

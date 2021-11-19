# The Call class represents a single call, including all the values
# assigned to it in the CSV file, for the first value (since it is
# constant). Additionally, a direction parameter is computed according
# the source and destination floors.

class Call:
    def __init__(self, callList):
        self.time = float(callList[1])
        self.source = int(callList[2])
        self.destination = int(callList[3])
        if self.source < self.destination:
            self.direction = True
        elif self.source > self.destination:
            self.direction = False
        self.assignment = callList[5] # Should always be -1 initially.

    # Returns a list representing the call, in the format expected for
    # the output file.
    def toList(self):
        return ['Elevator call', self.time, self.source,
                self.destination, 0, self.assignment]

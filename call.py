class Call:
    def __init__(self, callList):
        self.time = float(callList[1])
        self.source = int(lcallList[2])
        self.destination = int(callList[3])
        if self.source < self.destination:
            self.direction = True
        elif self.source > self.destination:
            self.direction = False
        self.assignment = callList[5]

    def toList(self):
        return ['Elevator call', self.time, self.source,
                self.destination, 0, self.assignment]

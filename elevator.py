# The Elevator class represents a single elevator in the building,
# including all the parameters supplied for elevators in the JSON
# building description except for the ID since it isn't used.

class Elevator:
    def __init__(self, speed, minFloor, maxFloor, closeTime,
                 openTime, startTime, stopTime):
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime

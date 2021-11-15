# The Elevator class represents a single elevator in the building,
# including all the parameters supplied for elevators in the JSON
# building description except for the ID (it is used as the key in the
# dictionary containing the elevators).
# The floor parameter is updated according the floor the elevator will
# stop at next.

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

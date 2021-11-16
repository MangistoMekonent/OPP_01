import sys
import json
import csv

from elevator import Elevator # Our Elevator object.
from call import Call

def main(buildingFile, callsFile, outputFile):
    # Read the building description.
    with open(buildingFile) as b:
        buildingData = json.load(b)

    # Assign values gathered from the JSON building description.
    maxFloor = buildingData['_maxFloor']
    minFloor = buildingData['_minFloor']

    # Each Elevator is added to the dictionary with its parameters
    # gathered from the JSON description, with the ID as the key.
    elevators = {elevator['_id']: Elevator(elevator['_speed'],
                                           elevator['_minFloor'],
                                           elevator['_maxFloor'],
                                           elevator['_closeTime'],
                                           elevator['_openTime'],
                                           elevator['_startTime'],
                                           elevator['_stopTime'])
                 for elevator in buildingData['_elevators']}

    # Read the calls from the input file.
    with open(callsFile) as c:
        callsReader = csv.reader(c)
        calls = [Call(call) for call in callsReader]

    outputCalls = []
    for id, elevator in elevators.items():
        floor = 0 # Destination floor of the last call assigned.
        finishTime = 0 # Finish time of the last path.

        for firstCall in calls:
            # If the first call is received before the last call of
            # the previous path, skip this call.
            if firstCall.time < finishTime:
                continue

            # The direction of the current path is dictated by its
            # first call.
            direction = firstCall.direction
            # The finish time is dictated by the first call (we try to
            # assign other calls to this elevator "in the middle" of
            # this path).
            finishTime = callFinishTime(elevator, firstCall, floor)
            floor = firstCall.destination
            # Remove this call from the input list and add it to the
            # output list with an assignment.
            calls.remove(firstCall)
            firstCall.assignment = id
            outputCalls.append(firstCall)
            for call in calls:
                # Only assign this call to this elevator if its
                # direction is the same as the path direction, it's
                # received before the path is finished, and if it's
                # source/destination are somewhere along the current path.
                if call.time < finishTime and call.direction == direction:
                    if direction == True and (call.source < floor or
                                              call.destination >
                                              firstCall.destination):
                        pass
                    elif direction == False and (call.source > floor or
                                                 call.destination <
                                                 firstCall.destination):
                        pass
                    else:
                        floor = call.destination
                        calls.remove(call)
                        call.assignment = id
                        outputCalls.append(call)
        
    # Sort the output calls chronologically.
    outputCalls.sort(key=lambda c: c.time)
    with open(outputFile, 'w') as o:
        outputWriter = csv.writer(o)
        for call in outputCalls:
            outputWriter.writerow(call.toList())

# Returns the time at which an elevator will finish servicing a call
# if it started at a specific floor.
def callFinishTime(elevator, call, floor):
    return (call.time + elevator.startTime +
            (elevator.speed * abs(floor - call.source)) +
            elevator.stopTime + elevator.openTime + elevator.closeTime +
            elevator.startTime +
            (elevator.speed * abs(call.source - call.destination)) +
            elevator.stopTime + elevator.openTime + elevator.closeTime)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

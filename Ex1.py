import sys
import json
import csv

from elevator import Elevator # Our Elevator object.
from call import Call # Our Call object.

def main(buildingFile, callsFile, outputFile):
    # Read the building description.
    with open(buildingFile) as b:
        buildingData = json.load(b)

    # Assign values gathered from the JSON building description.
    maxFloor = buildingData['_maxFloor']
    minFloor = buildingData['_minFloor']

    # Each Elevator is added to the dictionary with its parameters
    # gathered from the JSON description, with the ID as the key.
    elevators = [Elevator(elevator['_speed'],
                          elevator['_minFloor'],
                          elevator['_maxFloor'],
                          elevator['_closeTime'],
                          elevator['_openTime'],
                          elevator['_startTime'],
                          elevator['_stopTime'])
                 for elevator in buildingData['_elevators']]

    # Read the calls from the input file.
    calls = []
    with open(callsFile) as c:
        callsReader = csv.reader(c)
        for callRaw in callsReader:
            call = Call(callRaw)
            # Ensure the call makes sense in the current building.
            if (call.source < minFloor or call.source > maxFloor or
                call.destination < minFloor or call.destination > maxFloor):
                print("The specified building can't handle these calls.")
                quit(1)
            calls.append(call)

    outputCalls = []
    while (calls != []):
        for i in range(len(elevators)):
            elevator = elevators[i]
            floor = 0 # Destination floor of the last call assigned.
            finishTime = 0 # Finish time of the last path.
            
            for firstCall in calls:
                # If the first call is received before the last call of
                # the previous path, or the elevator can't reach the one
                # of the call's floors, try the next call instead.
                # All other calls in this should be within the same
                # boundaries of floors, so this check is only necessary
                # for the first call.
                if (firstCall.time < finishTime or firstCall.source >
                    elevator.maxFloor or firstCall.source < elevator.minFloor
                    or firstCall.destination > elevator.maxFloor or
                    firstCall.destination < elevator.minFloor):
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
                firstCall.assignment = i
                outputCalls.append(firstCall)
                for call in calls:
                    # Only assign this call to this elevator if its
                    # direction is the same as the path direction, it's
                    # received before the path is finished, and if it's
                    # source/destination are somewhere along the current
                    # path.
                    if call.time < finishTime and call.direction == direction:
                        # These 'if' statements have been split to make
                        # the more readable.
                        if direction == True and (call.source < floor or
                                                  call.destination >
                                                  firstCall.destination):
                            continue
                        elif direction == False and (call.source > floor or
                                                     call.destination <
                                                     firstCall.destination):
                            continue
                        else:
                            floor = call.destination
                            calls.remove(call)
                            call.assignment = i
                            outputCalls.append(call)
                    # Since input calls are sorted chronologically, we
                    # know that if we've reached a call which doesn't
                    # fall within the finish time, the rest won't either.
                    elif call.time >= finishTime:
                        break
        
    # Sort the output calls chronologically.
    outputCalls.sort(key=lambda c: c.time)

    # Write the assigned calls to the output file.
    with open(outputFile, 'w') as o:
        outputWriter = csv.writer(o)
        for call in outputCalls:
            outputWriter.writerow(call.toList())

# Returns the time at which an elevator will finish servicing a call
# if it started at a specific floor.
def callFinishTime(elevator, call, floor):
    # The elevator starts movement twice - at its source floor and the
    # call's source floor.
    if floor == call.source:
        startTimes = elevator.startTime
    else:
        startTimes = 2 * elevator.startTime

    # The elevator stops movement twice - at the call's source and
    # destination floors
    if floor == call.source:
        stopTimes = elevator.stopTime
    else:
        stopTimes = 2 * elevator.stopTime

    # The elevator closes doors twice - at the call's source and
    # destination floors (after dropping off passengers).
    closeTimes = 2 * elevator.closeTime

    # The elevator opens doors twice - at the call's source and
    # destination floors.
    openTimes = 2 * elevator.openTime

    # The elevator moves between its source floor and the call's
    # source, and then between the call's source and the call's
    # destination.
    moveTimes = (abs(floor - call.source)/elevator.speed +
                 abs(call.source - call.destination)/elevator.speed)

    # Return the sum of all "times".
    return (call.time + startTimes + stopTimes
            + closeTimes + openTimes + moveTimes)
            
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

import sys
import json
import csv

from elevator import Elevator # Our Elevator object.

def main(buildingFile, callsFile, outputFile):
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

    with open(callsFile) as c:
        callsReader = csv.reader(c)
        # Calls are kept in an array since they are sorted
        # chronologically in the CSV file, and since it will simplify
        # outputting a CSV file later.
        calls = [call for call in callsReader]

    # Dummy algorithm which assigns calls as they appear
    # chronologically.
    amount = len(calls)
    i = 0
    while i < amount:
        for elevator in elevators:
            calls[i][5] = elevator
            i += 1
            if i == amount:
                break
        
    with open(outputFile, 'w') as output:
        outputWriter = csv.writer(output)
        outputWriter.writerows(calls)
            
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

import sys
import json
import csv

from elevator import Elevator # Our Elevator object.

def main(buildingFile, callsFile, outputFile):
    with open(buildingFile) as building:
        buildingData = json.load(building)

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

    with open(callsFile) as calls:
        callsReader = csv.reader(calls)
        # Calls are kept in an array since they are sorted
        # chronologically in the CSV file, and since it will simplify
        # outputting a CSV file later.
        calls = [call for call in callsReader]

    with open(outputFile, 'w') as output:
        outputWriter = csv.writer(output)
        for call in calls:
            outputCall = call
            outputCall[5] = 0
            outputWriter.writerow(outputCall)
            
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

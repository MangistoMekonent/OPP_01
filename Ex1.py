import sys
import json
import csv

from elevator import Elevator # Our Elevator object.
from call import Call

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

    # Each Call is added in the order it appears in the input file.
    with open(callsFile) as c:
        callsReader = csv.reader(c)
        calls = [Call(call) for call in callsReader]

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

import copy
from datetime import datetime
import country_states

backtracksNum = 0

#Function to inilialize assigned colors

def initializeColors(states):
    colorAssigned = {}
    for state in states:
        colorAssigned[state] = 'Null'
    return colorAssigned

#Function to initialize domain
def initializeDomain(states, numOfColors):
    domain = {}
    if numOfColors == 1:
        color = ['Red']
    elif numOfColors == 2:
        color = ['Red', 'Green']
    elif numOfColors == 3:
        color = ['Red', 'Green', 'Blue']
    elif numOfColors == 4:
        color = ['Red', 'Green', 'Blue', 'Yellow']
    else:
        color = ['Red', 'Green', 'Blue', 'Yellow', 'Black']
    for state in states:
        domain[state] = copy.deepcopy(color)
    return domain

def Backtrack(states, neighbours, colors, domain):
    global backtracksNum
    # Check if Successful
    if all(value != 'Null' for value in colors.values()):
        return "Success"
    # Pick a state to assign a color
    currentState = states[0]
    currentNeighbors = neighbours[currentState]
    coloredSpaces = list( map(colors.get, currentNeighbors))
    for color in domain[currentState]:
        if color not in coloredSpaces:
            # assign consistent color
            colors[currentState] = color
            # Temporarily remove currentState
            states.remove(currentState)
            #Recursively call the function
            output = Backtrack(states, neighbours, colors, domain)
            if output != "Failure":
                return "Success"
            colors[currentState] = 'Null'
            # add currentState back since assignment failed
            states.append(currentState)
    if colors[currentState] == 'Null':
        backtracksNum = backtracksNum + 1
        return "Failure"



def MRV_Heuristic(states, domain, neighbours):    
    states.sort(key=lambda x: (len(domain[x]),-len(neighbours[x])))
    currentSelection = states[0]
    return currentSelection

def LCV_Heuristic(currentState, domain, neighbors):
    currentDomain = domain[currentState]
    currentNeighbors = neighbors[currentState]
    orderedDomain ={}
    for color in currentDomain:
        count = 0
        for neighbor in currentNeighbors:
            if color in domain[neighbor]:
                count = count + 1
        orderedDomain[color] = count
    
    # Sort 
    orderedDomain = dict(sorted(orderedDomain.items(), key=lambda item: item[1]))
    return list(orderedDomain.keys())

def BacktrackWithHeuristics(states, neighbours, colors, domain):
    global backtracksNum
    if all(value != 'Null' for value in colors.values()):
        return "Success"
    # Use minimum remaining values heuristics( and degree heuristics ) to select next unassigned variable 
    currentState = MRV_Heuristic(states, domain, neighbours)
    currentNeighbors = neighbours[currentState]
    coloredSpaces = list( map(colors.get, currentNeighbors))
    # Use Least Constraint Values heuristic to get the color
    orderedDomain = LCV_Heuristic(currentState, domain, neighbours)
    for color in orderedDomain:
        if color not in coloredSpaces:
            # assign consistent color
            colors[currentState] = color
            # Temporarily remove currentState
            states.remove(currentState)
            output = BacktrackWithHeuristics(states, neighbours, colors, domain)
            if output != "Failure":
                return "Success"
            colors[currentState] = 'Null'
            # add currentState back since assignment failed
            states.append(currentState)
    if colors[currentState] == 'Null':
        backtracksNum = backtracksNum + 1
        return "Failure"

#Function to get the minimum chromatic number of the map
def chromatic_number(states, neighbors):
    copyStates = copy.deepcopy(states)
    count = 0
    while 1:
        count = count + 1
        copyStates = copy.deepcopy(states)
        colors = initializeColors(states)
        domain = initializeDomain(states, count)
        result = Backtrack(copyStates, neighbors, colors, domain)
        if result == 'Success':
            break
    return count                   


print("Select map: \n1. Australia \n2. USA")
mapChoice = int(input())
print("Select Heuristics or Without Heursitics: \n1 without heuristic \n2 with heuristic")
withheuristic = int(input())
startTime = datetime.now()
if(mapChoice == 1):
    states = copy.deepcopy(country_states.states_australia)
    neighbours = country_states.neighbours_australia
    min_number = chromatic_number(states, neighbours)
    print("Chromatic Number for Australia map: ", min_number)
elif(mapChoice == 2):
    states = copy.deepcopy(country_states.states_usa)
    neighbours = country_states.neighbours_usa
    min_number = chromatic_number(states, neighbours)
    print("Chromatic Number for USA map: ", min_number)
colors = initializeColors(states)
domain = initializeDomain(states, min_number)
backtracksNum = 0
if(withheuristic==1):
    result = Backtrack(states, neighbours, colors, domain)
else:
    result = BacktrackWithHeuristics(states, neighbours, colors, domain)
if result == 'Success':
    print(colors)
    print("Backtracks occurred: ", backtracksNum)
else:
    print("Failure")
    print(colors)
    print("Backtracks occurred: ", backtracksNum)
endTime = datetime.now()
elapsedTime = (endTime - startTime).microseconds / 1000
print("Time Taken: %sms" % (str(elapsedTime)))
import sys
import collections
import heapq

#global variables
totalNodesCreated  = 0
totalExpandedNodes = 0
depthLimit       = 0

#possible actions in the form of [chicken, wolf]
possibleAction  = [[1,0],[2,0],[0,1],[1,1],[0,2]]
supportedModes = ["bfs", "dfs", "iddfs", "astar"]

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def __len__(self):
        return len(self._queue)

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class Node():
    def __init__(self, leftSide, rightSide, depth, cost, parent, action):

        global totalNodesCreated
        totalNodesCreated += 1

        #sides of puzzle
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.state = tuple(self.leftSide + self.rightSide)

        #other attributes
        self.depth = depth
        self.cost = cost
        self.parent = parent
        self.action = action

class Result():
    def __init__(self, startSide, endSide, action, boatEndSide):
        startSide[0] = startSide[0] - action[0]
        startSide[1] = startSide[1] - action[1]
        endSide[0] = endSide[0] + action[0]
        endSide[1] = endSide[1] + action[1]

        if boatEndSide == "left":
            self.rightSide = startSide
            self.leftSide = endSide
            self.rightSide[2] = 0
            self.leftSide[2] = 1
        else:
            self.rightSide = endSide
            self.leftSide = startSide
            self.rightSide[2] = 1
            self.leftSide[2] = 0
        self.action = action

def main():
    #file IO
    initialStateData = getFileState(fileInitialState)
    goalStateData = getFileState(fileGoalState)

    #create states
    initialState = createNodeWithData(initialStateData)
    goalState = createNodeWithData(goalStateData)

    #execute based on alg argument
    if mode in supportedModes:
        if mode == "astar":
            fringe = PriorityQueue()
            resultState = aStarSearch(fringe, initialState, goalState)
        if mode == "bfs":
            fringe = collections.deque()
            resultState = breadthFirstSearch(fringe, initialState, goalState)
        if mode == "dfs":
            fringe = collections.deque()
            resultState = depthFirstSearch(fringe, initialState, goalState)
        if mode == "iddfs":
            fringe = collections.deque()
            resultState = iterativeDeepeningDFS(fringe, initialState, goalState)
    else:
        sys.exit("Invalid Algorithm")

    #print results (path len, nodes expanded)
    printToUser(resultState)

    #write results to file
    outputFile = open(fileOutput, 'w')
    outputFile.write(str(getNodePath(resultState)))
    outputFile.write('\n')
    outputFile.close()

if __name__ == "__main__":
    #check for correct number of arguments
    if len(sys.argv) < 5:
        sys.exit('Incorrect number of arguments:\n<initial> <goal> <mode> <output>')

    #get command line arguments
    fileInitialState = sys.argv[1]
    fileGoalState    = sys.argv[2]
    mode             = sys.argv[3]
    fileOutput       = sys.argv[4]


def getFileState(file):
    #read state from file
    with open(file) as f:
        stateData = f.readlines()
    return stateData

def createNodeWithData(data):
    #create node with data from file
    return Node(map(int, data[0].strip('\n').split(',')), map(int, data[1].strip('\n').split(',')), 0, 0, None, None)

def printToUser(resultState):
    #print results to terminal
    print "Total Expanded Nodes: {0}".format(totalExpandedNodes)
    print "Solution Path Length: {0}".format(len(getNodePath(resultState)))
    print getNodePath(resultState)

def breadthFirstSearch(fringe, initialState, goalState):
    global totalNodesCreated, totalExpandedNodes, depthLimit
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        #pop from fringe
        current = fringe.popleft()

        #check if in goal state
        if (current.leftSide == goalState.leftSide) and (current.rightSide == goalState.rightSide):
            return current

        #check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(fringe.append, expandNode(current))
            totalExpandedNodes += 1

def depthFirstSearch(fringe, initialState, goalState):
    global totalNodesCreated, totalExpandedNodes, depthLimit
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        #pop from fringe
        current = fringe.pop()

        # check if in goal state
        if (current.leftSide == goalState.leftSide) and (current.rightSide == goalState.rightSide):
            return current

        #check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            if current.depth > 400:
                continue
            closedList[current.state] = current.depth
            map(fringe.append, expandNode(current))
            totalExpandedNodes += 1

def iterativeDeepeningDFS(fringe, initialState, goalState):
    global totalNodesCreated, totalExpandedNodes, depthLimit
    closedList = {}
    fringe.append(initialState)
    while True:
        if len(fringe) == 0:
            if depthLimit > 400:
                sys.exit("Depth Limit Reached!")
            closedList = {}
            depthLimit += 1
            totalNodesCreated = 0
            fringe.append(initialState)
            continue

        #pop from fringe
        current = fringe.pop()

        #check if in goal state
        if (current.leftSide == goalState.leftSide) and (current.rightSide == goalState.rightSide):
            return current

        #check if in closed list and expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(fringe.append, expandNodeIDDFS(current))
            totalExpandedNodes += 1

def aStarSearch(fringe, initialState, goalState):
    global totalNodesCreated, totalExpandedNodes, depthLimit
    closedList = {}
    fringe.push(initialState, initialState.cost)

    while True:
        if len(fringe) == 0:
            sys.exit("No Solution Path Found")

        #pop from from
        current = fringe.pop()

        #check if in goal state
        if (current.leftSide == goalState.leftSide) and (current.rightSide == goalState.rightSide):
            return current

        #check if in closed list adn expand when necessary
        if current.state in closedList and current.depth >= closedList[current.state]:
            continue
        else:
            closedList[current.state] = current.depth
            map(lambda i: fringe.push(i, i.cost + aStarHeuristic(i, goalState)), expandNode(current))
            totalExpandedNodes += 1

def expandNode(node):
    #expand the current node
    global possibleAction
    successorNodes = []

    validAction = filter(lambda i: checkAction(i, node), possibleAction)
    expandedNodes = map(lambda j: executeAction(j, node), validAction)

    for successor in expandedNodes:
        updatedNode = Node(successor.leftSide, successor.rightSide, node.depth + 1, node.depth + 1, node, successor.action)
        successorNodes.append(updatedNode)
    return successorNodes

def expandNodeIDDFS(node):
    global possibleAction
    successorNodes = []

    if node.depth == depthLimit:
        expandedNodes = []
    else:
        validAction = filter(lambda i: checkAction(i, node), possibleAction)
        expandedNodes = map(lambda j: executeAction(j, node), validAction)

    for successor in expandedNodes:
        updatedNode = Node(successor.leftSide, successor.rightSide, node.depth + 1, node.depth + 1, node, successor.action)
        successorNodes.append(updatedNode)
    return successorNodes

def checkAction(action, node):
    #check if action is valid
    #check which side the boat is on 
    if node.leftSide[2] == 1:
        startSide = list(node.leftSide)
        endSide = list(node.rightSide)
    else:
        startSide = list(node.rightSide)
        endSide = list(node.leftSide)

    #execute action and check result
    startSide[0] = startSide[0] - action[0]
    startSide[1] = startSide[1] - action[1]
    endSide[0] = endSide[0] + action[0]
    endSide[1] = endSide[1] + action[1]

    #check number of wolves to chickens
    if (startSide[0] < 0) or (startSide[1] < 0) or (endSide[0] < 0) or (endSide[1] < 0):
        return False
    elif ((startSide[0] == 0) or (startSide[0] >= startSide[1])) and (endSide[0] == 0 or (endSide[0] >= endSide[1])):
        return True
    else:
        return False

def executeAction(action, node):
    #execute action and create result object
    if node.leftSide[2] == 1:
        result = Result(list(node.leftSide), list(node.rightSide), action, "right")
    else:
        result = Result(list(node.rightSide), list(node.leftSide), action, "left")
    return result

def aStarHeuristic(current, goalState):
    #check boat side  
    if goalState.rightSide[2] == 1:
        heuristic = (current.leftSide[0] + current.leftSide[1]) - 1
    else:
        heuristic = (current.rightSide[0] + current.rightSide[1]) - 1
    return heuristic

def getNodePath(node):
    #trace back through parents to get solution path to node
    currentNode = node
    pathToNode = []
    while True:
        try:
            if currentNode.parent == None:
                break
            pathToNode.append(currentNode.action)
        except:
            break
        currentNode = currentNode.parent
    return pathToNode[::-1]

main()
from tkinter import *
from random import *
import time
import numpy as np
import util

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'

# Detect elements in the map



window = Tk()
window.title('CityBusPlanner')
window.resizable(0,0)
width = 25
(x, y) = (22, 22)

totalsteps = 0

#建筑物的位置
buidings = [(0, 0), (1, 0), (2, 0), (3, 0), (7, 0), (8, 0), (11, 0), (12, 0), (13, 0),
            (17, 0), (18, 0), (21, 0), (21, 1), (2, 2), (5, 2), (8, 2), (9, 2), (12, 2),
            (14, 2), (15, 2), (16, 2), (17, 2), (21, 2), (2, 3), (4, 3), (5, 3), (7, 3),
            (8, 3), (11, 3), (17, 3), (18, 3), (19, 3), (2, 4), (4, 4), (5, 4), (8, 4),
            (9, 4), (14, 4), (15, 4),(17, 4), (18, 4), (19, 4), (0, 6), (2, 6), (4, 6),
            (7, 6), (8, 6), (11, 6), (12, 6), (14, 6), (15, 6),(16, 6), (18, 6), (19, 6),
            (2, 7), (5, 7), (21, 7), (0, 8), (2, 8), (11, 8), (14, 8), (15, 8), (17, 8),
            (18, 8), (21, 8), (4, 9), (5, 9), (7, 9), (9, 9), (11, 9), (14, 9), (21, 9),
            (2, 10), (7, 10), (14, 10), (17, 10), (19, 10), (0, 11), (2, 11), (4, 11),
            (5, 11), (7, 11), (8, 11), (9, 11), (11, 11), (12, 11), (14, 11), (15, 11),
            (16, 11), (17, 11), (18, 11), (19, 11), (0, 13), (2, 13), (3, 13), (5, 13),
            (7, 13), (8, 13), (9, 13), (14, 13), (17, 13), (18, 13), (21, 13), (2, 14),
            (3, 14), (5, 14), (7, 14),(9, 14), (12, 14), (14, 14), (15, 14), (17, 14),
            (18, 14), (21, 14), (2, 15), (3, 15), (5, 15), (7, 15), (9, 15), (12, 15),
            (15, 15), (19, 15), (21, 15), (0, 16), (21, 16), (0, 17), (3, 17), (5, 17),
            (7, 17),(9, 17), (11, 17), (14, 17), (15, 17), (17, 17), (18, 17), (21, 17),
            (2, 18), (3, 18), (5, 18), (7, 18),(9, 18), (11, 18), (14, 18), (17, 18),
            (18, 18), (3, 19), (5, 19), (7, 19), (9, 19), (11, 19), (12, 19), (14, 19),
            (17, 19), (18, 19), (0, 21), (1, 21), (2, 21), (5, 21), (6, 21), (9, 21),
            (10, 21), (11, 21), (12, 21), (15, 21), (16, 21), (18, 21), (19, 21), (21, 21)]
# 墙的位子
walls = [(10, 0), (0, 12), (21, 12), (14, 21)]
park = [(14, 0), (15, 0), (16, 0)]
# 机器人的起始位置
robotPos = (21, 12)

#生成画布
view = Canvas(window, width=x * width, height=y * width)
view.grid(row=0, column=0)
#生成按钮
searchMapButton = Button(window,text = 'search')
searchMapButton.grid(row = 0,column = 1)
#生成右侧的画布
robotView = Canvas(window,width=x * width, height=y * width)
robotView.grid(row = 0,column = 2)

def formatColor(r, g, b):
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

def cityMap():
    global width, x, y, buidings,walls,park,robot
    for i in range(x):
        for j in range(y):
            view.create_rectangle(
                i * width, j * width, (i + 1) * width, (j + 1) * width, fill='white', outline='gray', width=1)
    for (i, j) in buidings:
        view.create_rectangle(
            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='black', outline='gray', width=1)
    for (i,j) in walls:
        view.create_rectangle(
            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='blue', outline='gray', width=1)
    for (i,j) in park:
        view.create_rectangle(
            i * width, j * width, (i + 1) * width, (j + 1) * width, fill='red', outline='gray', width=1)

def robotCityMap():
    global width, x, y, buidings,walls,park,robot,robotPos
    for i in range(x):
        for j in range(y):
            robotView.create_rectangle(
                i * width, j * width, (i + 1) * width, (j + 1) * width, fill='black', width=1)
    robotView.create_rectangle(
                robotPos[0] * width, robotPos[1] * width, (robotPos[0] + 1) * width, (robotPos[1] + 1) * width, fill='white', outline='gray', width=1)
# Create City Map
cityMap()

# Create Robot View
robotCityMap()
# Create a robot
robot = view.create_rectangle(robotPos[0] * width + width * 2 / 10, robotPos[1] * width + width * 2 / 10,
                            robotPos[0] * width + width * 8 / 10, robotPos[1] * width + width * 8 / 10, fill="orange", width=1, tag="robot")
robotSelf = robotView.create_rectangle(robotPos[0] * width + width * 2 / 10, robotPos[1] * width + width * 2 / 10,
                            robotPos[0] * width + width * 8 / 10, robotPos[1] * width + width * 8 / 10, fill="orange", width=1, tag="robot")

visited = [robotPos]

def move(dx,dy):
    global robot,x,y,robotPos,robotSelf,view
    global totalsteps
    totalsteps = totalsteps + 1
    newX = robotPos[0] + dx
    newY = robotPos[1] + dy
    if (not isEdge(newX, newY)) and (not isBlock(newX, newY)):
        #print "move %d" % totalsteps
        #移动左图机器人的位置
        view.coords(robot, (newX) * width + width * 2 / 10, (newY) * width + width * 2 / 10,
                     (newX) * width + width * 8 / 10, (newY) * width + width * 8 / 10)
        #移动右图机器人的位置
        robotView.coords(robotSelf, (newX) * width + width * 2 / 10, (newY) * width + width * 2 / 10,
                     (newX) * width + width * 8 / 10, (newY) * width + width * 8 / 10)
        robotPos = (newX, newY)
        if robotPos not in visited:
            visited.append(robotPos)
            visitedPanel = robotView.create_rectangle(
                robotPos[0] * width, robotPos[1] * width, (robotPos[0] + 1) * width, (robotPos[1] + 1) * width, fill='white', outline='gray', width=1)
            robotView.tag_lower(visitedPanel,robotSelf)
    else:
        print ("move error")

def callUp(event):
    move(0,-1)

def callDown(event):
    move(0, 1)

def callLeft(event):
    move(-1, 0)

def callRight(event):
    move(1, 0)

def isBlock(newX,newY):
    global buidings,x,y


    for (i,j) in buidings:
        if (i == newX) and (j == newY):
            return True
    return False

def isEdge(newX,newY):
    global x,y

    if newX >= x or newY >= y or newX < 0 or newY < 0 :
        return True
    return False

def getSuccessors(robotPos):
    n = Directions.NORTH
    w = Directions.WEST
    s = Directions.SOUTH
    e = Directions.EAST
    successors = []
    posX = robotPos[0]
    posY = robotPos[1]

    if not isBlock(posX - 1, posY) and not isEdge(posX - 1,posY):
        successors.append(w)
    if not isBlock(posX, posY + 1) and not isEdge(posX,posY + 1):
        successors.append(s)
    if not isBlock(posX + 1, posY) and not isEdge(posX + 1,posY):
        successors.append(e)
    if not isBlock(posX, posY -1) and not isEdge(posX,posY - 1):
        successors.append(n)





    return successors

def getNewPostion(position,action):
    posX = position[0]
    posY = position[1]
    n = Directions.NORTH
    w = Directions.WEST
    s = Directions.SOUTH
    e = Directions.EAST
    if action == n:
        return (posX,posY - 1)
    elif action == w:
        return (posX - 1,posY)
    elif action == s:
        return (posX,posY + 1)
    elif action == e:
        return (posX + 1,posY)

delay = False
def runAction(actions):
    global delay
    n = Directions.NORTH
    w = Directions.WEST
    s = Directions.SOUTH
    e = Directions.EAST
    for i in actions:
        if delay:
            time.sleep(0.05)
        if i == n:
            #print "North"
            move(0, -1)
        elif i == w:
            #print "West"
            move(-1, 0)
        elif i == s:
            #print "South"
            move(0, 1)
        elif i == e:
            #sprint "East"
            move(1, 0)
        view.update()



def searchMapTest(event):
    global robotPos
    actions = []
    position = robotPos
    for i in range(100):
        successors = getSuccessors(position)
        successor = successors[randint(0, len(successors) - 1)]
        actions.append(successor)
        position = getNewPostion(position, successor)
    print (actions)
    runAction(actions)

def reverseSuccessor(successor):
    n = Directions.NORTH
    w = Directions.WEST
    s = Directions.SOUTH
    e = Directions.EAST
    if successor == n:
        return s
    elif successor == w:
        return e
    elif successor == s:
        return n
    elif successor == e:
        return w

roads = set()

detectedBuildings = {}
blockColors = {}
blockIndex = 0


def updateBuildings(detectedBuildings):
    global robotView,width
    for block,buildings in detectedBuildings.items():
        color = blockColors[block]
        for building in buildings:
            robotView.create_rectangle(
                building[0] * width, building[1] * width, (building[0] + 1) * width, (building[1] + 1) * width, fill=color, outline=color, width=1)





def addBuilding(position):
    global blockIndex,detectedBuildings
    isAdd = False
    addBlock = ''
    for block,buildings in detectedBuildings.items():
        for building in buildings:
            if building == position:
                return
            if util.manhattanDistance(position, building) == 1:
                if not isAdd:
                    buildings.add(position)
                    isAdd = True
                    addBlock = block
                    break
                else:
                    #merge two block
                    for building in detectedBuildings[block]:
                        detectedBuildings[addBlock].add(building)
                    detectedBuildings.pop(block)

    if not isAdd:
        newBlock = set([position])
        blockIndex = blockIndex + 1
        detectedBuildings['Block %d' % blockIndex] = newBlock
        color = formatColor(random(), random(), random())
        blockColors['Block %d' % blockIndex] = color
    updateBuildings(detectedBuildings)

def addRoad(position):
    global robotView,width,robotSelf
    visitedPanel = robotView.create_rectangle(
                position[0] * width, position[1] * width, (position[0] + 1) * width, (position[1] + 1) * width, fill='white', outline='gray', width=1)
    robotView.tag_lower(visitedPanel,robotSelf)

def showPath(positionA,positionB,path):
    global robotView,width,view
    view.create_oval(positionA[0] * width + width * 3 / 10, positionA[1] * width + width * 3 / 10,
                       positionA[0] * width + width * 7 / 10, positionA[1] * width + width * 7 / 10, fill='yellow', width=1)
    nextPosition = positionA
    for action in path:
        nextPosition = getNewPostion(nextPosition, action)
        view.create_oval(nextPosition[0] * width + width * 4 / 10, nextPosition[1] * width + width * 4 / 10,
                       nextPosition[0] * width + width * 6 / 10, nextPosition[1] * width + width * 6 / 10, fill='yellow', width=1)
    view.create_oval(positionB[0] * width + width * 3 / 10, positionB[1] * width + width * 3 / 10,
                       positionB[0] * width + width * 7 / 10, positionB[1] * width + width * 7 / 10, fill='yellow', width=1)
hasDetected = set()


def detectLocation(position):
    if position not in hasDetected:
        hasDetected.add(position)
        if isBlock(position[0],position[1]):
            addBuilding(position)
        elif not isEdge(position[0],position[1]):
            addRoad(position)

def detect(position):
    posX = position[0]
    posY = position[1]

    detectLocation((posX,posY + 1))
    detectLocation((posX,posY - 1))
    detectLocation((posX + 1,posY))
    detectLocation((posX - 1,posY))



def heuristic(positionA,positionB):
    return util.manhattanDistance(positionA,positionB)

def AstarSearch(positionA,positionB):
    "Step 1: define closed: a set"
    closed = set()
    "Step 2: define fringe: a PriorityQueue "
    fringe = util.PriorityQueue()
    "Step 3: insert initial node to fringe"
    "Construct node to be a tuple (location,actions)"
    initialNode = (positionA,[])
    initCost = 0 + heuristic(initialNode[0],positionB)
    fringe.push(initialNode,initCost)
    "Step 4: Loop to do search"
    while not fringe.isEmpty():
        node = fringe.pop()
        if node[0] == positionB:
            return node[1]
        if node[0] not in closed:
            closed.add(node[0])
            for successor in getSuccessors(node[0]):
                actions = list(node[1])
                actions.append(successor)
                newPosition = getNewPostion(node[0], successor)
                childNode = (newPosition,actions)
                cost = len(actions) + heuristic(childNode[0],positionB)
                fringe.push(childNode,cost)
    return []

def AstarSearchBetweenbuildings(building1,building2):
    "Step 1: define closed: a set"
    closed = set()
    "Step 2: define fringe: a PriorityQueue "
    fringe = util.PriorityQueue()
    "Step 3: insert initial node to fringe"
    "Construct node to be a tuple (location,actions)"
    initialNode = (building1,[])
    initCost = 0 + heuristic(initialNode[0],building2)
    fringe.push(initialNode,initCost)
    "Step 4: Loop to do search"
    while not fringe.isEmpty():
        node = fringe.pop()
        if util.manhattanDistance(node[0],building2) == 1:
            return node[1]
        if node[0] not in closed:
            closed.add(node[0])
            for successor in getSuccessors(node[0]):
                actions = list(node[1])
                actions.append(successor)
                newPosition = getNewPostion(node[0], successor)
                childNode = (newPosition,actions)
                cost = len(actions) + heuristic(childNode[0],building2)
                fringe.push(childNode,cost)
    return []

def calculatePositions(buildingA,path):
    positions = set()
    positions.add(buildingA)
    nextPosition = buildingA
    for action in path:
        nextPosition = getNewPostion(nextPosition, action)
        positions.add(nextPosition)
    return positions

def showRoad(fullRoad):
    global view,width
    for road in fullRoad:
        view.create_oval(road[0] * width + width * 4 / 10, road[1] * width + width * 4 / 10,
                       road[0] * width + width * 6 / 10, road[1] * width + width * 6 / 10, fill='yellow', width=1)
    view.update()


def search(node):
    successors = getSuccessors(node[0])
    detect(node[0])
    for successor in successors:
        nextPosition = getNewPostion(node[0], successor)
        if nextPosition not in roads:
            runAction([successor]) # to the next node
            roads.add(nextPosition)
            search((nextPosition,[successor],[reverseSuccessor(successor)]))
    runAction(node[2]) #back to top node

def searchConsiderTopVisit(node,topWillVisit):
    successors = getSuccessors(node[0])
    detect(node[0])
    newTopWillVisit = set(topWillVisit)
    for successor in successors:
        nextPosition = getNewPostion(node[0], successor)
        newTopWillVisit.add(nextPosition)
    for successor in successors:
        nextPosition = getNewPostion(node[0], successor)
        if nextPosition not in roads and nextPosition not in topWillVisit:
            runAction([successor]) # to the next node
            roads.add(nextPosition)
            newTopWillVisit.remove(nextPosition)
            searchConsiderTopVisit((nextPosition,[successor],[reverseSuccessor(successor)]),newTopWillVisit)
    runAction(node[2]) #back to top node


def searchShortestPathBetweenBlocks(block1,block2):
    shortestPath = []
    buildingA = (0,0)
    buildingB = (0,0)
    for building1 in block1:
        for building2 in block2:
            path = AstarSearchBetweenbuildings(building1, building2)
            if len(shortestPath) == 0:
                shortestPath = path
                buildingA = building1
                buildingB = building2
            elif len(path) < len(shortestPath):
                shortestPath = path
                buildingA = building1
                buildingB = building2
    return (buildingA,buildingB,shortestPath)

def addBuildingToBlocks(linkedBlock,buildingA):
    global detectedBuildings
    newLinkedBlock = linkedBlock.copy()
    for block,buildings in detectedBuildings.items():
        for building in buildings:
            if util.manhattanDistance(buildingA, building) == 1:
                    newLinkedBlock[block] = buildings
                    break
    return newLinkedBlock

def bfsSearchNextBlock(initBuilding,linkedBlock):
    global detectedBuildings
    closed = set()
    fringe = util.Queue()
    initNode = (initBuilding,[])
    fringe.push(initNode)
    while not fringe.isEmpty():
        node = fringe.pop()
        newLinkedBlock = addBuildingToBlocks(linkedBlock,node[0])
        if len(newLinkedBlock) == len(detectedBuildings):
            return node[1]
        if len(newLinkedBlock) > len(linkedBlock): # find a new block
            actions = list(node[1])
            '''
            if len(node[1]) > 0:
                lastAction = node[1][len(node[1]) - 1]
                for successor in getSuccessors(node[0]):
                    if successor == lastAction:
                        nextPosition = getNewPostion(node[0], successor)
                        actions.append(successor)
                        return actions + bfsSearchNextBlock(nextPosition, newLinkedBlock)
            '''
            return node[1] + bfsSearchNextBlock(node[0], newLinkedBlock)

        if node[0] not in closed:
            closed.add(node[0])
            for successor in getSuccessors(node[0]):
                actions = list(node[1])
                actions.append(successor)
                nextPosition = getNewPostion(node[0], successor)

                childNode = (nextPosition,actions)
                fringe.push(childNode)
    return []

def isGoal(node):
    global detectedBuildings,robotPos
    linkedBlock = {}
    positions = calculatePositions(robotPos, node[1])
    for position in positions:
        for block,buildings in detectedBuildings.items():
            for building in buildings:
                 if util.manhattanDistance(position, building) == 1:
                    linkedBlock[block] = buildings
    print (len(linkedBlock))
    if len(linkedBlock) == 17:
        return True
    else:
        return False

def roadHeuristic(road):
    return 0

def AstarSearchRoad():
    global robotPos,detectedBuildings
    "Step 1: define closed: a set"
    closed = set()
    "Step 2: define fringe: a PriorityQueue "
    fringe = util.PriorityQueue()
    "Step 3: insert initial node to fringe"
    "Construct node to be a tuple (location,actions)"
    initRoad = (robotPos,[])
    initCost = 0 + roadHeuristic(initRoad)
    fringe.push(initRoad,initCost)
    "Step 4: Loop to do search"
    while not fringe.isEmpty():
        node = fringe.pop()
        if isGoal(node):
            print (len(closed))
            return node[1]
        if node[0] not in closed:
            closed.add(node[0])
            for successor in getSuccessors(node[0]):
                actions = list(node[1])
                actions.append(successor)
                newPosition = getNewPostion(node[0], successor)
                childNode = (newPosition,actions)
                cost = len(actions) + roadHeuristic(childNode)
                fringe.push(childNode,cost)

    return []



def searchRoad(building):
    global detectedBuildings,robotPos
    linkedBlock = {}
    initBuilding = building

    return bfsSearchNextBlock(initBuilding,linkedBlock)

def searchShortestRoad():
    shortestRoad = []
    shortestPositions = set()
    for block,buildings in detectedBuildings.items():
        for building in buildings:
            road = searchRoad(building)
            positions = calculatePositions(building, road)
            if len(shortestPositions) == 0 or len(positions) < len(shortestPositions):
                shortestRoad = road
                shortestPositions = positions
    print (len(shortestPositions))
    showRoad(shortestPositions)

def searchMap(event):
    print ("Search Map")
    global robotPos,roads,detectedBuildings,delay
    actions = []
    #roads = set()s
    #roads.add(robotPos)
    #fringe = util.Stack()
    initNode = (robotPos,[],[])  # (position,forwardActions,backwarsdActions)
    #fringe.push(initNode)
    roads.add(robotPos)
    search(initNode)
    #searchConsiderTopVisit(initNode, set())
    print (detectedBuildings)
    print (len(detectedBuildings))
    #path = AstarSearchBetweenbuildings((6,21), (2, 18))
    #showPath((6,21),(2,18), path)
    '''
    shortestRoad = set()
    for block1 in detectedBuildings.values():
        roads = set()
        for block2 in detectedBuildings.values():
            if not block1 == block2:
                (buildingA,buildingB,path) = searchShortestPathBetweenBlocks(block1, block2)
                #showPath(buildingA,buildingB,path)
                positions = calculatePositions(buildingA,buildingB,path)
                roads = roads | positions
        if len(shortestRoad) == 0 or len(roads) < len(shortestRoad):
            shortestRoad = roads
        print len(shortestRoad)
    showRoad(shortestRoad)
    '''
    '''
    block1 = detectedBuildings.values()[3]
    print block1
    block2 = detectedBuildings.values()[5]
    print block2
    (buildingA,buildingB,path) = searchShortestPathBetweenBlocks(block1, block2)
    print buildingA,buildingB,path
    showPath(buildingA,buildingB,path)

    block1 = detectedBuildings.values()[10]
    print block1
    block2 = detectedBuildings.values()[20]
    print block2
    (buildingA,buildingB,path) = searchShortestPathBetweenBlocks(block1, block2)
    print buildingA,buildingB,path
    showPath(buildingA,buildingB,path)
    '''
    searchShortestRoad()

    '''
    path = searchRoad()
    #path = AstarSearchRoad()
    positions = calculatePositions(robotPos, path)
    print len(positions)
    showRoad(positions)
    delay = True
    #runAction(path)
    '''


window.bind("<Up>", callUp)
window.bind("<Down>", callDown)
window.bind("<Right>", callRight)
window.bind("<Left>", callLeft)
window.bind("s", searchMap)
searchMapButton.bind("<Button-1>",searchMap)
window.mainloop()
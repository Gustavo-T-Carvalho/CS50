import sys
import os
from random import choice


def main():
    mode = 1
    clear = lambda: os.system("cls")
    
    # Treat CMD Variable
    if len(sys.argv) == 2:
        validateMode(sys.argv[1])
        mode = int(sys.argv[1])

    winningConditions = getWinningConditions()
    clear()
    
    printLoading(0, mode)
    aiDecisionTreeBackupX = buildAiDecisionTree(mode, winningConditions, "x")
    clear()
    printLoading(1, mode)
    aiDecisionTreeBackupO = buildAiDecisionTree(mode, winningConditions, "o")
    clear()
    
    results = {
            "xWins": 0,
            "oWins": 0, 
            "ties":0
        }
    possibleResults = {0: "tie", 1: "x wins", 2: "o wins"}
    while(True):
        # Initiate Variables
        turn = 1
        result = 0
        clear()
        xo = getWhoStarts(mode)
        aiDecisionTree =  aiDecisionTreeBackupO if xo == "o" else aiDecisionTreeBackupX
        positions = [" "] * 9
        
        printBoard(positions, clear)
        
        # Game Loop
        while True:

            move = getNextMove(positions, xo, mode, aiDecisionTree, turn)
            positions[move] = xo
            if mode == 1:
                aiDecisionTree = updateAiTree(move, aiDecisionTree)
            printBoard(positions, clear)

            if turn >= 5:
                result = verifyWinning(winningConditions, positions, xo)
                if result != 0:
                    break

            if turn > 8:
                break
            turn += 1
            xo = changeXo(xo)
        
        if result == 0:
            results["ties"]+=1
        elif result == 1:
            results["xWins"] +=1
        else:
            results["oWins"] +=1      
        showResult(mode, turn, possibleResults[result], results)
        print("---------------------------------------------------------------")
        playAgain = input("Play again? (y/n): ")
        if(playAgain != "y"):
            break


def getWinningConditions():
    return [
        {0, 1, 2},
        {0, 3, 6},
        {0, 4, 8},
        {1, 4, 7},
        {2, 4, 6},
        {2, 5, 8},
        {3, 4, 5},
        {6, 7, 8},
    ]
def printLoading(step, mode):
    if(mode == 2): return
    print("###############################################################")
    print(r"#|¯|######|¯¯¯¯¯¯|#|¯¯¯¯¯¯|#|¯¯¯¯¯\##|¯¯|#|¯¯¯\##|¯|#|¯¯¯¯¯¯¯|#")
    print(r"#| |######| |##| |#| |##| |#| |##| |#|  |#| |\ \#| |#| |¯¯¯¯¯ #")
    print(r"#| |######| |##| |#| |##| |#| |##| |#|  |#| |#\ \| |#| |#|_¯¯|#")
    print(r"#| |____##| |##| |#|  __  |#| |##| |#|  |#| |##\   |#| |___| |#")
    print(r"#|______|#|______|#|_|  |_|#|_____/##|__|#|_|###\__|#|_______|#")
    print("###############################################################")
    print("###############################################################")
    if(step == 0):
        print("#|___________________________________________________________|#")
    else:
        print("#|##############################_____________________________|#")
    print("###############################################################")
    
    
def getWhoStarts(mode):
    phrases = {
        "2": "Pick who should start: Player X (x) or PLayer O (o): ",
        "1": "Pick who should start: Robot(r) or Human(h): "   
    }  
    
    while True:
        whoStart = input(phrases.get(str(mode))).lower()
        robotOptions = ["r", "robot", "o"] 
        humanOptions = ["h", "human", "x"]
        if whoStart in robotOptions:
            return "o"
        if whoStart in humanOptions:
            return "x"
        
    
    
def validateMode(mode):
    if mode != "1" and mode != "2":
        raise Exception("Mode must be either 1 or 2")


def getNextMove(positions, xo, mode, aiDecisionTree, turn):
    while True:
        if mode == 2 or xo == "x":
            move = getHumanMove(xo)
        else:
            move = getAiMove(aiDecisionTree, positions, turn)
            if(move == None):
                move = getBiggestChanceMove(aiDecisionTree)
            
        if validateMove(move, positions):
            return move


def getHumanMove(xo):
    print()
    while True:
        print(f"Turn: {xo}")
        move = input(f"Pick your next move (Use numbers from 1 to 9): ")
        if move >= "1" and move <= "9" and len(move) == 1:
            return int(move) - 1


def getAiMove(aiDecisionTree, positions, turn):
    move = None
    if existsAWinningMove(aiDecisionTree, "o"):
            move = getWinningMove(aiDecisionTree)
    elif isCornerCase(positions, turn):
        move = answerCornerCase(positions)
    elif existsALossPreventMove(aiDecisionTree):
        move = getPreventLossMove(aiDecisionTree)
    else:
        move = getBiggestChanceMove(aiDecisionTree)
    return move

def getBiggestChanceMove(aiDecisionTree):
    biggestValues = []
    for scenario in aiDecisionTree["possibleScenarios"]:
        if len(biggestValues) == 0:
            biggestValues.append(
                {"sum": scenario["sum"], "lastPlayed": scenario["lastPlayed"]}
            )
        else:
            if scenario["sum"] > biggestValues[0]["sum"]:
                biggestValues = [
                    {"sum": scenario["sum"], "lastPlayed": scenario["lastPlayed"]}
                ]
            elif scenario["sum"] == biggestValues[0]["sum"]:
                biggestValues.append(
                    {"sum": scenario["sum"], "lastPlayed": scenario["lastPlayed"]}
                )

    random = choice(biggestValues)

    return random["lastPlayed"]
    
def existsAWinningMove(aiDecisionTree, xo):
    expectedResult = 2 if xo == "o" else 1
    for scenario in aiDecisionTree["possibleScenarios"]:
        
        isWinning = verifyWinning(getWinningConditions(), scenario["positions"], xo) == expectedResult
        if(isWinning):
            return isWinning
    return False



def getWinningMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if(verifyWinning(getWinningConditions(), scenario["positions"], "o") == 2):
            return scenario["lastPlayed"]


def existsALossPreventMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if existsAWinningMove(scenario, "x"):
            return True
    return False


def getPreventLossMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if not existsAWinningMove(scenario, "x"):
            return scenario["lastPlayed"]


def validateMove(move, positions):
    if move < 0 or move > 8:
        return False
    return positions[move] == " "


def verifyWinning(winningConditions, positions, xo):
    playerPositions = getPositionsSet(positions, xo)

    for winningCondition in winningConditions:
        if winningCondition.issubset(playerPositions):
            return 1 if xo == "x" else 2
    return 0


def printBoard(positions, clear):

    clear()

    print(f"                              |     |     ")
    print(f"                           {positions[0]}  |  {positions[1]}  |  {positions[2]}  ")
    print(f"                         _____|_____|_____")
    print(f"                              |     |     ")
    print(f"                           {positions[3]}  |  {positions[4]}  |  {positions[5]}  ")
    print(f"                         _____|_____|_____")
    print(f"                              |     |     ")
    print(f"                           {positions[6]}  |  {positions[7]}  |  {positions[8]}  ")
    print(f"                              |     |     ")


def changeXo(xo):
    return "x" if xo == "o" else "o"


def getPositionsSet(positions, searchElement):
    positionsSet = set()
    for i, position in enumerate(positions):
        if position == searchElement:
            positionsSet.add(i)

    return positionsSet


def buildAiDecisionTree(mode, winningConditions, xo):
    if mode != 1:
        return None
    
    emptyState = {
        "sum": 0,
        "possibleScenarios": [],
        "positions": [" "] * 9,
        "lastPLayed": None,
    }

    fillPossibleScenarios(emptyState, winningConditions, xo)

    return emptyState


def fillPossibleScenarios(board, winningConditions, xo):

    if isGameFinished(board, winningConditions):
        board["sum"] = getBoardValue(board, winningConditions)
        return
    notPlayedPositions = getPositionsSet(board["positions"], " ")

    for i in notPlayedPositions:
        newPositions = list(board["positions"])
        newPositions[i] = xo
        newBoard = {
            "sum": 0,
            "possibleScenarios": [],
            "positions": newPositions,
            "lastPlayed": i,
        }
        board["possibleScenarios"].append(newBoard)
        fillPossibleScenarios(newBoard, winningConditions, changeXo(xo))
    board["sum"] = sumBoardValues(board["possibleScenarios"])


def isGameFinished(board, winningConditions):
    if (
        len(getPositionsSet(board["positions"], " ")) == 0
        or verifyWinning(winningConditions, board["positions"], "x")
        or verifyWinning(winningConditions, board["positions"], "o")
    ):
        return True

    return False


def getBoardValue(board, winningConditions):
    if verifyWinning(winningConditions, board["positions"], "x"):
        return -1
    elif verifyWinning(winningConditions, board["positions"], "o"):
        return 1
    else: 
        return 0


def sumBoardValues(possibleScenarios):
    sum = 0
    for scenario in possibleScenarios:
        sum += scenario["sum"]
    return sum


def updateAiTree(move, aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if scenario["lastPlayed"] == move:
            return scenario

def isCornerCase(positions, turn):
    # Case:
    # x - -  
    # - o x
    # - - -
    
    if(turn != 4): return False
    playerPositions = getPositionsSet(positions, "x")
    cornerCases = [
        {0, 5},
        {0, 7},
        {2, 3},
        {2, 7},
        {6, 1},
        {6, 5},
        {8, 1},
        {8, 3}
    ]
    
    for cornerCase in cornerCases:
        if cornerCase.issubset(playerPositions):
            return True
    return False
    
def answerCornerCase(positions):
    playerPositions = getPositionsSet(positions, "x")
    cornerCases = [
        {0, 5},
        {0, 7},
        {2, 3},
        {2, 7},
        {6, 1},
        {6, 5},
        {8, 1},
        {8, 3}
    ]
    answers = [2, 6, 0 , 8, 0, 8, 2 ,6]
    for i, cornerCase in enumerate(cornerCases):
        if cornerCase.issubset(playerPositions):
            return answers[i]
    

def showResult(mode, turn, lastResult, results):
    if(mode == 2):
        
        print(f"Match Result: {lastResult}. Turns played: {turn}")
        print(f"X wins: {results["xWins"]}")
        print(f"O wins: {results["oWins"]}")
        print(f"Ties: {results["ties"]}")
        
        
    else:
        if lastResult == "o wins":
            phrase = "I won   "
        elif lastResult == "tie":
            phrase = "We tie  "
        else:
            phrase = "I bugged"
        
        print( "       o                                                   ")
        print( "       |                                                   ")
        print( "  _|¯¯¯¯¯¯¯|_      |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|   ")
        print(f"-|@| 0   0 |@|-    | You Can't defeat me. {phrase}     |   ")
        print( "  ¯|   I   |¯     /  But don't feel bad, nobody can!   |   ")
        print(f"   |  ===  | ____/   I won: {results["oWins"]:03} Human won: {results["xWins"]:03}         |   ")
        print(f"   ¯¯¯|¯|¯¯¯     \   Ties: {results["ties"]:03}                         |   ")
        print(f" _____| |_____    \  The last game took {turn} turns        |   ")
        print( " | o  ---  o |     \___________________________________|   ")
            


main()

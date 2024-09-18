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
    aiDecisionTreeBackup = buildAiDecisionTree(mode, winningConditions, "x")
    
    while(True):
        # Initiate Variables
        turn = 1
        aiDecisionTree = aiDecisionTreeBackup 
        possibleResults = {0: "tie", 1: "x wins", 2: "o wins"}
        result = 0
        xo = choice(["x", "o"])
        positions = [" ","o","x"," ","x"," ","o","o","x"]#[" "] * 9
        

        printBoard(positions, clear)
        
        # Game Loop
        while True:

            move = getNextMove(positions, xo, mode, aiDecisionTree)
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

        print(f"Resultado: {possibleResults[result]}. Quantidade de rodadas: {turn}")
        playAgain = input("Jogar novamente?(s/n)")
        if(playAgain == "n"):
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


def validateMode(mode):
    if mode != "1" and mode != "2":
        raise Exception("Mode must be either 1 or 2")


def getNextMove(positions, xo, mode, aiDecisionTree):
    while True:
        if mode == 2 or xo == "x":
            move = getHumanMove(xo)
        else:
            move = getAiMove(positions, aiDecisionTree)
        if validateMove(move, positions):
            return move


def getHumanMove(xo):
    while True:
        move = input(f"{xo} player. Pick your next move (Use numbers from 1 to 9): ")
        if move >= "1" and move <= "9" and len(move) == 1:
            return int(move) - 1


def getAiMove(aiDecisionTree):
    if existsAWinningMove(aiDecisionTree):
        return getWinningMove(aiDecisionTree)
    elif existsALossPreventMove(aiDecisionTree):
        return getPreventLossMove(aiDecisionTree)
    else:

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


def existsAWinningMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if len(scenario["possibleScenarios"]) == 0:
            return True
    return False


def getWinningMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if len(scenario["possibleScenarios"]) == 0:
            return scenario["lastPlayed"]


def existsALossPreventMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if existsAWinningMove(scenario):
            return True
    return False


def getPreventLossMove(aiDecisionTree):
    for scenario in aiDecisionTree["possibleScenarios"]:
        if not existsAWinningMove(scenario):
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
    print(f"     |     |     ")
    print(f"  {positions[0]}  |  {positions[1]}  |  {positions[2]}  ")
    print(f"_____|_____|_____")
    print(f"     |     |     ")
    print(f"  {positions[3]}  |  {positions[4]}  |  {positions[5]}  ")
    print(f"_____|_____|_____")
    print(f"     |     |     ")
    print(f"  {positions[6]}  |  {positions[7]}  |  {positions[8]}  ")
    print(f"     |     |     ")


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
        "positions": [" ","o","x"," ","x"," ","o","o","x"],#[" "] * 9,
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


main()

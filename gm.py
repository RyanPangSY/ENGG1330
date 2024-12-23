import mainFunction
import steps
import hp
import ranking
import messages

def gamemode_2(mapList, keyRow, keyColumn, playerHP, currentValue, username, gamemode, numOfRound, playerMove, playerPos, numOfPlaying = 1):
    playerHP = hp.calculateHP(playerHP, currentValue)
    if playerHP <= 0:
        messages.diedMsg()
        mainFunction.printText('You are dead... \nCry about it\n')
        return True
    elif hp.isWin(currentValue) and not mainFunction.haveKey(keyRow, keyColumn, mapList):
        messages.diedMsg()
        mainFunction.printText('You don\'t have the key\n')
        mainFunction.printText('You are dead... \nCry about it\n')
        return True
    elif hp.isWin(currentValue) and mainFunction.haveKey(keyRow, keyColumn, mapList) and numOfPlaying == 1:
        steps.movePlayer(mapList, playerMove, playerPos, gamemode, numOfRound)
        mainFunction.clearLine(22)
        mainFunction.printMap(mapList, gamemode, username, numOfRound, None, playerHP, None)
        mainFunction.printText(f'Congrats {username}!\nYou have successfully escaped the Grand Hall',0.05,True)
        mainFunction.printText("Just Kidding",0.1,True)
        score_1 = playerHP / ((numOfRound+1)/100)
        # repeat the game
        playerHP = 30
        numOfRound = 1
        currentPath_2 = mainFunction.simulatePath(gamemode)
        while currentPath_2 == "pathfail":
            currentPath_2 = mainFunction.simulatePath(gamemode)
        currentPath_2[mainFunction.giveRowAndColumn(15)[0]][mainFunction.giveRowAndColumn(15)[1]] = "E"
        currentPath_2[mainFunction.giveRowAndColumn(96)[0]][mainFunction.giveRowAndColumn(96)[1]] = "P"
        keyRow, keyColumn = mainFunction.genKey(currentPath_2)
        mainFunction.fillOthers(currentPath_2, gamemode)
        mainFunction.printMap(currentPath_2, gamemode, username, numOfRound, None, playerHP)
        mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
        playerMove = input()
        while playerMove != 'q' and not steps.isWin(currentPath_2):
            if playerMove not in 'wasdq':
                mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
                playerMove = input()
                continue
            playerPos = steps.checkPlayerPos(currentPath_2)
            if steps.isMovable(currentPath_2, playerPos, playerMove):
                currentPlayerPos = steps.checkPlayerNextPos(currentPath_2, playerPos, playerMove)
                currentValue = currentPath_2[currentPlayerPos[0]][currentPlayerPos[1]]
                if gamemode_2(currentPath_2, keyRow, keyColumn, playerHP, currentValue, username, gamemode, numOfRound, playerMove, playerPos, 2):
                    break
                playerHP = hp.calculateHP(playerHP, currentValue) # calculate the HP of the player
                if playerHP <= 0:
                    messages.diedMsg()
                    mainFunction.printText('You are dead... \nCry about it\n')
                    return True
                numOfRound += 1
                steps.movePlayer(currentPath_2, playerMove, playerPos, gamemode, numOfRound, currentValue, currentPlayerPos) 
            else:
                currentPlayerPos = playerPos
            mainFunction.printMap(currentPath_2, gamemode, username, numOfRound, None, playerHP, None)
            if steps.isWin(currentPath_2) and mainFunction.haveKey(keyRow, keyColumn, currentPath_2):
                mainFunction.printText(f'Congrats {username}!\nYou have successfully escaped the Grand Hall\nI swear this time is real\n')
                score = str(round(score_1 + playerHP / ((numOfRound+1)/100)))
                ranking.printRanking(username, gamemode, playerHP, numOfRound, score)
                return True
            elif steps.isMovable(currentPath_2, currentPlayerPos, playerMove) == 'stucked' and playerHP != 0:
                mainFunction.printText('You are stucked...haha \nGame over')
                return True
            mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
            playerMove = input()
        return True
    else:
        return False

            # end of repeating the game

def gamemode_3(mapList, currentPlayerPos):
    row, column = currentPlayerPos
    if column != 15 and row != 6:
        mapList[row+1][column+1] = mapList[row+1][column+1][4:] if "hide" in mapList[row+1][column+1] else mapList[row+1][column+1]
    if column != 0 and row != 6:
        mapList[row+1][column-1] = mapList[row+1][column-1][4:] if "hide" in mapList[row+1][column-1] else mapList[row+1][column-1]
    if column != 15 and row != 0:
        mapList[row-1][column+1] = mapList[row-1][column+1][4:] if "hide" in mapList[row-1][column+1] else mapList[row-1][column+1]
    if column!=0 and row!=0:
        mapList[row-1][column-1] = mapList[row-1][column-1][4:] if "hide" in mapList[row-1][column-1] else mapList[row-1][column-1]
    if row != 0:
        mapList[row-1][column]= mapList[row-1][column][4:] if "hide" in mapList[row-1][column] else mapList[row-1][column]
    if row != 6:
        mapList[row+1][column]= mapList[row+1][column][4:] if "hide" in mapList[row+1][column] else mapList[row+1][column]
    if column != 0:
        mapList[row][column-1]= mapList[row][column-1][4:] if "hide" in mapList[row][column-1] else mapList[row][column-1]
    if column != 15:
        mapList[row][column+1]= mapList[row][column+1][4:] if "hide" in mapList[row][column+1] else mapList[row][column+1]

def gamemode_4(mapList, numOfRound, playerPos, currentPlayerPos, username, currentValue, playerHP, playerMove, colNineList):
    if numOfRound % 2 == 0 and numOfRound != 1:
        colNineList.clear()
        
        if currentPlayerPos[1] == 9:
            numOfBomb = mainFunction.checkBombNearby(mapList, currentPlayerPos)
            steps.movePlayer(mapList, playerMove, playerPos, 4, numOfRound, currentValue)
            playerHP = 0
            for i in range(7):
                mapList[i][9] = "█"
            playerHP = 0
            # mapList[currentPlayerPos[0]][9] = "█"
            numOfRound += 1
            mainFunction.printMap(mapList, 4, usernme, numOfRound, numOfBomb, playerHP)
            mainFunction.printText('You are dead... \nCry about it\n')
            # mapList[i][9]="█"
            return True

        for i in range(7):
            if mapList[i][9] == 'P' and playerMove == 'd':
                colNineList.append('ᐅ')
            elif mapList[i][9] == 'P' and playerMove == 'a':
                colNineList.append('ᐊ')
            else:
                colNineList.append(mapList[i][9])
            mapList[i][9] = "█"

    else:
        for i in range(7):
            mapList[i][9] = colNineList[i]
    
    if hp.isWin(currentValue) and not mainFunction.haveHiddenKey(mapList):
        mainFunction.printText('Seems you have missed something\nLet\'s try again\n', 0.05)
        
        return False


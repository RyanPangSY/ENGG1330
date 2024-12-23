import messages

def checkPlayerPos(mapList):
    for row, ele in enumerate(mapList):
        for col, _ in enumerate(ele):
            if mapList[row][col] == 'P':
                playerPos = [row, col]
                return playerPos

def checkPlayerNextPos(mapList, playerPos, playerMove):
    if playerMove == 'w':
        return [playerPos[0]-1, playerPos[1]]
    elif playerMove == 'a':
        return [playerPos[0], playerPos[1]-1]
    elif playerMove == 's':
        return [playerPos[0]+1, playerPos[1]]
    elif playerMove == 'd':
        return [playerPos[0], playerPos[1]+1]

def isMovable(mapList, playerPos, playerMove):
    movableDirection = []
    arrow = 'ᐃᐊᐁᐅ'
    
    if playerPos[0] != 0 and not playerPos[0]-1 < 0 and mapList[playerPos[0]-1][playerPos[1]] not in arrow:
        movableDirection.append('w')
    if playerPos[1] != 0 and not playerPos[1]-1 < 0 and mapList[playerPos[0]][playerPos[1]-1] not in arrow:
        movableDirection.append('a')
    if playerPos[0] != 6 and not playerPos[0]+1 > 6 and mapList[playerPos[0]+1][playerPos[1]] not in arrow:
        movableDirection.append('s')
    if playerPos[1] != 15 and not playerPos[1]+1 > 15 and mapList[playerPos[0]][playerPos[1]+1] not in arrow:
        movableDirection.append('d')

    if movableDirection == []:
        return 'stucked'
    elif playerMove in movableDirection:
        return True
    else:
        return False

def movePlayer(mapList, playerMove, playerPos, gamemode, numOfRound, currentValue = None, currentPlayerPos = None):
    # make the old position into arrows which point at the moving directing
    arrowList = {'w':'ᐃ', 'a':'ᐊ', 's':'ᐁ', 'd':'ᐅ'}
    mapList[playerPos[0]][playerPos[1]] = arrowList[playerMove]
    
    if gamemode == 4:
        # when player move into laser, replace 'P' by '█'
        if playerPos[1] == 9:
            mapList[playerPos[0]][playerPos[1]] = '█'
        # when the player has move on to a bomb
        if 'boom' in currentValue:
            messages.boomMsg()
            noDigitList = 'ᐃᐊᐁᐅ&E█'
            # multiply the surrounding value by 2
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0) and 0 <= currentPlayerPos[0]+i < 7 and 0 <= currentPlayerPos[0]+j < 16 and mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j] not in noDigitList:
                        # check if it's single digit or double digits
                        numOfDigit = 1
                        if len(currentValue) != 1 and mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j][-2:].isdigit():
                            numOfDigit += 1
                        # double the value of nearby numbers and make them bold
                        mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j] = 'bold' + mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j][:-numOfDigit] + str(int(mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j][-numOfDigit:])*2)

    # move the player to corresponding location
    if playerMove == 'w':
        mapList[playerPos[0]-1][playerPos[1]] = 'P'
    elif playerMove == 'a':
        mapList[playerPos[0]][playerPos[1]-1] = 'P'
    elif playerMove == 's':
        mapList[playerPos[0]+1][playerPos[1]] = 'P'
    elif playerMove == 'd':
        mapList[playerPos[0]][playerPos[1]+1] = 'P'

def isWin(mapList):
    if mapList[0][15] == 'P':
        return True
    else:
        return False

# import random
# import itertools
# import sys
# import time
# from platform import system

# local files here
import mainFunction
import steps
import hp
import ranking
import gm
import messages

def main(numOfTry = 1, username = ''):

  playerHP = 30
  numOfRound = 1
  numOfBomb = 0
  
  if numOfTry == 1:
    messages.welcomeMsg()

    # get the name of the player
    mainFunction.printText('Welcome! Please Enter Your Name: ', 0.015)
    username = input().title()
    while username == '':
        mainFunction.printText('Please enter a valid username: ', 0.015)
        username = input().title()

  # choosing game mode
  mainFunction.printText('Choose A gamemode [1. Standard/2. Hardcore/3. Darkage/4. Trap]: ', 0.015)
  gamemode = input()
  while not gamemode.isdigit() or int(gamemode) > 4 or int(gamemode) < 1:
    mainFunction.printText('Choose A VALID gamemode: ', 0.015)
    gamemode = input()
  gamemode = int(gamemode)
  if numOfTry == 1:
    mainFunction.printText("Try to reach 'E' as fast as you can\nGood luck!\n")

  
  # generate the map
  currentPath = mainFunction.simulatePath(gamemode)
  while currentPath == "pathfail":
    currentPath = mainFunction.simulatePath(gamemode)

  # place the player(P) and exit(E) on the map
  currentPath[mainFunction.giveRowAndColumn(15)[0]][mainFunction.giveRowAndColumn(15)[1]] = "E"
  currentPath[mainFunction.giveRowAndColumn(96)[0]][mainFunction.giveRowAndColumn(96)[1]] = "P"

  # generate key for gm 2 and return the coordinate of the key
  if gamemode == 2:
    keyRow, keyColumn = mainFunction.genKey(currentPath)

  # set lasers for gm 4
  if gamemode == 4:
    mainFunction.fillOthers(currentPath, gamemode)
    mainFunction.genBoom(currentPath) # generate boom
    mainFunction.genHiddenKey(currentPath) # generate hidden key
    colNineList = []
    for i in range(7):
        colNineList.append(currentPath[i][9])
    for i in range(7):
        currentPath[i][9] = "█"
    totalNumOfRound = 0
  
  # fill the remaining empty space in map
  mainFunction.fillOthers(currentPath, gamemode)

  mainFunction.printMap(currentPath, gamemode, username, numOfRound, None, playerHP, None)
  mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
  playerMove = input()

  while playerMove != 'q' and not steps.isWin(currentPath):
    if playerMove not in 'wasdq':
      mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
      playerMove = input()
      continue
  
    playerPos = steps.checkPlayerPos(currentPath) # give the coordinate of the player (before movement)
    if steps.isMovable(currentPath, playerPos, playerMove): # if the step is movable excute the following codes
      currentPlayerPos = steps.checkPlayerNextPos(currentPath, playerPos, playerMove) # give the coordinate of the player (after movement)
      currentValue = currentPath[currentPlayerPos[0]][currentPlayerPos[1]] # get the value of the block that the player is standing on
    
      # GAMEMODE 2
      if gamemode == 2:
        if gm.gamemode_2(currentPath, keyRow, keyColumn, playerHP, currentValue, username, gamemode, numOfRound, playerMove, playerPos):
          break
      
      # GAMEMODE 3
      if gamemode == 3:
        gm.gamemode_3(currentPath, currentPlayerPos)

      # GAMEMODE 4
      if gamemode == 4:
        if gm.gamemode_4(currentPath, numOfRound, playerPos, currentPlayerPos, username, currentValue, playerHP, playerMove, colNineList):
          break
        numOfBomb = mainFunction.checkBombNearby(currentPath, currentPlayerPos)
        currentValue = currentPath[currentPlayerPos[0]][currentPlayerPos[1]]
        if hp.isWin(currentValue) and not mainFunction.haveHiddenKey(currentPath):
          totalNumOfRound += numOfRound
          numOfRound = 1
          currentPath = mainFunction.simulatePath(4)
          while currentPath == "pathfail":
              currentPath = mainFunction.simulatePath(4)
          currentPath[mainFunction.giveRowAndColumn(15)[0]][mainFunction.giveRowAndColumn(15)[1]] = "E"
          currentPath[mainFunction.giveRowAndColumn(96)[0]][mainFunction.giveRowAndColumn(96)[1]] = "P"
          mainFunction.fillOthers(currentPath, 4)
          mainFunction.genBoom(currentPath) # generate boom
          mainFunction.genHiddenKey(currentPath) # generate hidden key
          colNineList = []
          for i in range(7):
              colNineList.append(currentPath[i][9])
          for i in range(7):
              currentPath[i][9] = "█"
          mainFunction.printMap(currentPath, gamemode, username, numOfRound, None, playerHP, numOfBomb)
          playerMove = 'None'
          continue

      playerHP = hp.calculateHP(playerHP, currentValue) # calculate the HP of the player
      if playerHP <= 0:
        messages.diedMsg()
        mainFunction.printText('Oops, You are dead... \nCry about it\n')
        break

      numOfRound += 1
      steps.movePlayer(currentPath, playerMove, playerPos, gamemode, numOfRound, currentValue, currentPlayerPos)

    else:
      currentPlayerPos = playerPos

    mainFunction.clearLine(22)
    mainFunction.printMap(currentPath, gamemode, username, numOfRound, None, playerHP, numOfBomb)
    
    if steps.isWin(currentPath):
      mainFunction.printText(f'Congrats {username}!\nYou have successfully escaped the Grand Hall\n')
      if gamemode == 4:
        numOfRound += totalNumOfRound
      break
    elif steps.isMovable(currentPath, currentPlayerPos, playerMove) == 'stucked' and playerHP != 0:
      mainFunction.printText('You are stucked...haha \nGame over')
      break

    mainFunction.printText('Your Move [w/a/s/d/q]: ', 0.02)
    playerMove = input()

  # after the game has ended
  if playerMove != 'q' and steps.isWin(currentPath) and gamemode != 2:
    ranking.printRanking(username, gamemode, playerHP, numOfRound)

  playerDecision = ''
  while playerDecision != 'Y' and playerDecision != 'N': # let the player to choose whether to play again or not
    mainFunction.printText('Wanna try again? [y/n] ')
    playerDecision = input().capitalize()
    if playerDecision == 'Y':
      main(2, username)
      break
    elif playerDecision == 'N':
      mainFunction.printText('Bye! See you next time.\n')
      break

main()


def printRanking(username, gamemode, playerHP, numOfRound, inputScore = 'no score here'):
  score = 0
  if inputScore.isdigit():
    score = int(inputScore)
  else:
    score = round(playerHP / (numOfRound/100))
  username = username.replace(' ', '_')
  inputData = f'{username} {gamemode} {score}'
  addRanking(inputData, score)
  print('\033[3mRanking\033[0m')
  print('    \033[4mUsername\033[0m             \033[4mGamemode\033[0m  \033[4mScore\033[0m')
  rankingFile = 'ranking/ranking.txt'
  with open(rankingFile, 'r') as ranking:
    rankings = ranking.readlines()
    # print(rankings)
    for i, line in enumerate(rankings):
      if line.startswith(inputData):
        # print out the ranking next to the player score
        for j in range(-3, 4):
          if (i+j >= 1) and (i+j <= len(rankings) - 1):
            rawData = rankings[i+j].replace('\n', '')
            if len(rawData.split(' ')) != 3:
              continue
            else:
              username, gamemode, score = rawData.split(' ')
            if len(username) > 19:
              username = username[:19] + '…'
            if j == 0: # blod the player's score
              print('\033[1m' + f'{i+j}.'.ljust(3), username.ljust(20), gamemode.ljust(9), score, '\033[0m')
            else:
              print(f'{i+j}.'.ljust(3), username.ljust(20), gamemode.ljust(9), score)
        print('⋮\n')
        break

def addRanking(inputData, score):

  rankingFile = 'ranking/ranking.txt'
  lineData = ''
  with open(rankingFile, 'r') as ranking: # open the ranking.txt file
    ranking.readline() # ignore the first row of line
    readingScore = 100000
    while readingScore > score:
      lineData = ranking.readline().replace('\n', '') # get the whole line
      # print(lineData.split(' '))
      readingScore = int(float((lineData.split(' '))[2])) # get the score on the next line
    ranking.close()

  lines = []
  with open(rankingFile, 'r+') as writeRanking: # open the ranking.txt file
    lines = writeRanking.readlines()
    writeRanking.close()
  with open(rankingFile,'w') as deleteFile:
    pass
  with open(rankingFile, 'r+') as writeRanking:
    for i, line in enumerate(lines):
        if line.startswith(lineData):
            line = inputData+'\n' + line
        writeRanking.write(line)
    writeRanking.close()

  

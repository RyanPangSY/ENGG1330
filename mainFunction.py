from time import sleep
import sys
import random
import itertools
# from platform import system

class colors:
    red = '\033[31m'
    lightRed = '\033[91m'
    blue = '\033[0;34m'
    lightBlue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    restart = '\033[0m'
    pink = '\033[95m'
    cyan = '\033[96m'
    lightGray = '\033[0;37m'
    bold = '\033[1m'
    faint = '\033[2m'
    italic = '\033[3m'
    crossed = "\033[4m"

def checking(l):
  Hp=30
  for i in l:
    if len(i)==1 or len(i)==2:
      Hp=Hp-int(i)
      if Hp<=0:
        return "dead"
      else:
        if 0<=int(i)<=10:
          Hp+=5
        elif 10<int(i)<=20:
          Hp+=10
        elif 20<int(i)<=30:
          Hp+=15
        elif 30<int(i)<=40:
          Hp+=20
        else:
          Hp+=25
    else:
      Hp+=int(i[4:])
  return "Good"

def printText(text, speed = 0.05, skipLine = False):
  for char in text:
    char = colors.bold + char + colors.restart
    print(char, end='')
    sleep(speed)
    # sys.stdout.write()
    sys.stdout.flush()
  if skipLine:
    print()

def giveRowAndColumn(index):
  column = index % 16
  row = index // 16
  return row, column

def simulatePath(gamemode):
  # generating the map size
  mapList = []
  for height in range(7):
    tempList = []
    for width in range(16):
      tempList.append('0')
    mapList.append(tempList)

  #possible path
  possiblePath = [
    [80,64,65,49,33,34,35,36,37,38,54,70,86,102,103,104,105,106,107,91,75,59,43,27,28,29,13,14],
    [80,64,48,49,50,51,52,53,54,55,56,57,58,42,26,10,11,12,28,44,60,76,77,78,62,46,30,14],
    [97,98,99,83,67,51,35,19,20,21,22,23,24,40,56,72,73,74,90,91,92,93,94,78,62,46,47,31],
    [97,81,82,66,67,51,35,36,37,38,54,55,56,57,73,74,75,76,60,44,43,27,11,12,13,29,30,31],
    [96,97,98,99,100,101,102,86,87,71,72,73,74,75,91,92,93,109,110,111,95,79,63,47,46,45,30,14]
  ]
  chosenPath = random.choice(possiblePath)
  randomNum = [random.choice(chosenPath[0:10]),random.choice(chosenPath[10:15]),random.choice(chosenPath[15:21]),random.choice(chosenPath[21:25]),random.choice(chosenPath[25:28])]
  for a,b,c,d,e in itertools.zip_longest(chosenPath[0:10],chosenPath[10:15],chosenPath[15:21],chosenPath[21:25],chosenPath[25:28],fillvalue="Null"):
    for p,n in zip([a,b,c,d,e],[str(random.randint(1,10)),str(random.randint(10,20)),str(random.randint(20,30)),str(random.randint(30,40)),str(random.randint(40,50))]):
      if "Null" not in str(p):
        row, column = giveRowAndColumn(p)
        mapList[row][column] = str(n)
  for i in range(5):
    row, column = giveRowAndColumn(randomNum[i])
    mapList[row][column] = "blue" + mapList[row][column]
  checkPath = []
  for i in chosenPath:
    row, column = giveRowAndColumn(i)
    checkPath.append(mapList[row][column])
  if checking(checkPath) == "dead":
    return 'pathfail'
  else:
    if gamemode != 3:
      return mapList
    else:
      for i in chosenPath:
        row, column = giveRowAndColumn(i)
        mapList[row][column] = "hide" + mapList[row][column]
      return mapList

def printMap(mapList,gamemode,u,r, X=None, hp=30, numOfBomb=0):
  if len(u) > 12:
    u = u[:12] + '…'
  for i in range(1,8):
    # upper section
    add = ''
    if i==1:
      add = f" {colors.bold}{u}'s HP:{colors.restart} {hp}"
    if gamemode == 4 and mapList[0][9] == '█':
      print("╔═══╗"*9+f"╔═{colors.lightRed}█{colors.restart}═╗"+"╔═══╗"*6+"┊" + add)
    else:
        print("╔═══╗"*16 + "┊" + add)
    # middle section
    add = ''
    for num in range((i-1)*16,(i-1)*16+16):
        row, col = giveRowAndColumn(num)[0], giveRowAndColumn(num)[1]
        element = mapList[row][col]
        add = ''
        if element == 'P':
            add += colors.pink + colors.bold
        elif element == 'E':
            add += colors.cyan + colors.bold
        elif element == '&':
            add += colors.yellow + colors.bold

        if 'bold' in element:
            add += colors.bold

        if 'hide' in element:
            element = '?'
        elif 'blue' in element:
            add += colors.lightBlue
        elif element in 'ᐃᐊᐁᐅ':
            add += colors.lightGray
        elif 'hiddenKey' in element:  
          add += colors.bold

        if len(element) <= 3:
          numOfDigit = len(element)
        else:
          numOfDigit = 1
          if element[-2:].isdigit():
            numOfDigit = 2
            if element[-3:].isdigit():
              numOfDigit = 3

        # print(numOfDigit)
        if numOfDigit == 1:
          print(f'║ {colors.lightRed}{add}{element[-1]}{colors.restart} ║', end = '')
        elif numOfDigit == 2:
          print(f'║{colors.lightRed}{add}{element[-2]} {element[-1]}{colors.restart}║', end = '')
        elif numOfDigit == 3:
          print(f'║{colors.lightRed}{add}{element[-3:]}{colors.restart}║', end = '')
        else:
          print('║   ║', end = '')
  
    add = ''
    if i == 1:
      add = f" {colors.bold}Round:{colors.restart} {r}"
    if gamemode == 4 and i == 7:
      if haveHiddenKey(mapList):
        add = colors.bold + ' Key ✓'
      else:
        add = f' Key not found...'
    print('┊' + add + colors.restart)
    # lower section
    add = ''
    if gamemode == 4 and i == 7:
      add = f' {colors.bold}Bombs nearby:{colors.restart} {numOfBomb}'
    if gamemode == 4 and mapList[0][9] == '█':
      print("╚═══╝"*9+f"╚═{colors.lightRed}█{colors.restart}═╝"+"╚═══╝"*6+"┊" + add + colors.restart)
    else:
      print("╚═══╝"*16+"┊" + add + colors.restart) 

def genKey(mapList):
  genKey = random.randint(0,111)
  while genKey == 96 or genKey == 15:
    genKey = random.randint(0,111)
  keyRow, keyColumn = giveRowAndColumn(genKey)
  mapList[keyRow][keyColumn] = "&"
  return keyRow, keyColumn

def genBoom(mapList, numOfBoom = 5):
  # generate a list of boom
  boomList = []
  while len(boomList) < numOfBoom:
    # generate individual boom
    boom = [random.randint(0,6), random.randint(0,15)]
    while boom == [6, 0] or boom == [0, 15] or boom == [5, 0] or boom == [6, 1] or boom == [2, 2] or boom == [3, 3] or boom in boomList or boom[1] == 9:
      boom = [random.randint(0,6), random.randint(0,15)]
    # print(boom)
    boomRow, boomColumn = boom[0], boom[1]
    mapList[boomRow][boomColumn] = "boom" + mapList[boomRow][boomColumn]
    # add boom to boomList
    boomList.append(boom)
  return boomList

def genHiddenKey(mapList):
  genHiddenKey = [random.randint(0,6), random.randint(0,15)]
  while genHiddenKey == [6, 0] or genHiddenKey == [0, 15] or genHiddenKey[1] == 9 or "blue" in mapList[genHiddenKey[0]][genHiddenKey[1]] or "boom" in mapList[genHiddenKey[0]][genHiddenKey[1]]:
    genHiddenKey = [random.randint(0,6), random.randint(0,15)]
  hiddenKeyRow, hiddenKeyColumn = genHiddenKey[0], genHiddenKey[1]
  mapList[hiddenKeyRow][hiddenKeyColumn] = 'hiddenKey' + mapList[hiddenKeyRow][hiddenKeyColumn]

def fillOthers(mapList, mode):
  for i in range(7):
    for j in range(16):
      c = random.choice([0,0,0,10,10,10,20,20,20,20,30,30,40])
      v = str(random.randint(1+c,10+c))
      if mapList[i][j] == "0":
        if mode != 3:
          mapList[i][j] = v
        else:
          mapList[i][j] = "hide" + v
      elif mapList[i][j] == 'boom':
        mapList[i][j] += v

def checkBombNearby(mapList, currentPlayerPos):
  numOfBomb = 0
  for i in range(-1,2):
    for j in range(-1,2):
      # print(mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j])
      if not (i == 0 and j == 0) and (currentPlayerPos[0]+i >= 0) and (currentPlayerPos[0]+i <= 6) and (currentPlayerPos[1]+j >= 0) and (currentPlayerPos[1]+j <= 15) and 'boom' in mapList[currentPlayerPos[0]+i][currentPlayerPos[1]+j]:
        numOfBomb += 1
  return numOfBomb

def haveKey(keyRow, keyColumn, mapList):
    arrow = 'ᐃᐊᐁᐅP'
    if mapList[keyRow][keyColumn] in arrow:
        return True
    else:
        return False

def haveHiddenKey(mapList):
    for row in mapList:
        for col in row:
            if 'hiddenKey' in col:
                return False
    return True

def clearLine(numOfLine = 1):
  LINE_UP = '\033[1A'
  LINE_CLEAR = '\x1b[2K'
  for i in range(numOfLine):
    print(LINE_UP, end=LINE_CLEAR)

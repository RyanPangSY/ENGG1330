def calculateHP(playerHP, currentValue):
    if '&' in currentValue or 'E' in currentValue:
        return playerHP

    numOfDigit = 0
    if len(currentValue) <= 3:
        numOfDigit = len(currentValue)
    else:
        numOfDigit = 1
        if currentValue[-2:].isdigit():
            numOfDigit = 2
            if currentValue[-3:].isdigit():
                numOfDigit = 3
    value = int(currentValue[-numOfDigit:])

    if 'blue' in currentValue:
        return playerHP + value
    else:
        if playerHP > value:
            if value > 40:
                return playerHP - value + 25 
            elif value > 30:
                return playerHP - value + 20
            elif value > 20:
                return playerHP - value + 15
            elif value > 10:
                return playerHP - value + 10
            elif value > 0:
                return playerHP - value + 5
        else:
            return 0
    return playerHP
    
def isWin(currentValue):
  if currentValue == 'E':
    return True

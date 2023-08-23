import os, pygame
from resources import Colours, Locations

BORDER_WIDTH = 5

class Tile:
  # index = (row, col)
  # boardRect = (left, top, width, height)
  def __init__(self, index, boardRect) -> None:
    self.colour = Colours.BACKGROUND
    self.letter = ''

    width = (boardRect[2] - 6 * BORDER_WIDTH) / 5
    height = (boardRect[3] - 7 * BORDER_WIDTH) / 6
    left = boardRect[0] + BORDER_WIDTH + index[0] * (width + BORDER_WIDTH)
    top = boardRect[1] + BORDER_WIDTH + index[1] * (height + BORDER_WIDTH)
    self.rect = pygame.Rect(left, top, width, height)

  def draw(self, surface):
    pygame.draw.rect(surface, self.colour, self.rect)

  def drawLetter(self, surface):
    pygame.draw.rect(surface, self.colour, self.rect)
    font = pygame.font.Font(None, 42)

    textColour = ''
    if self.colour == Colours.BACKGROUND: textColour = Colours.GRID_BORDER
    else: textColour = Colours.BACKGROUND

    text = font.render(self.letter, True, textColour)
    surface.blit(text, self.rect.center)

def InitBoard(boardRect):
  Board = []
  for i in range(5): 
    for j in range(6): 
      Board.append(Tile((i,j), boardRect))

  return Board

def GetWordList(filePath):
  with open(filePath, 'r') as file:
    return file.read()
  
def PrintBoard(board):
  # Clears terminal
  os.system('cls' if os.name == 'nt' else 'clear')

  for row in board:
    output = '|'
    for i in row: 
      output = output + i + '|' 
    print(output)

def CheckWord(currWord, answer, guessList, row, board, window):
  font = pygame.font.Font(None, 36)
  if currWord not in guessList:
    text = font.render("Not a valid Word!", True, Colours.GRID_BORDER)
    window.blit(text, Locations.BOARD_PRINTOUT)
    return False
  
  # Stops multiple tiles of same letter being flagged as valid
  # Can pull out all below into seperate function
  pattern = [0] * 5

  lettersRemaining = answer
  for i in range(5):
    index = row + i * 6
    if currWord[i] == answer[i]:
      board[index].colour = Colours.TILE_HIT
      board[index].drawLetter(window)
      lettersRemaining = lettersRemaining[:i] + lettersRemaining[i + 1:]

      # working on pattern identification
      pattern[i] = currWord[i]
    elif currWord[i] in lettersRemaining:
      board[index].colour = Colours.TILE_HIT_OTHER
      board[index].drawLetter(window)

      letterFoundIndex = lettersRemaining.index(currWord[i])
      lettersRemaining = lettersRemaining[:letterFoundIndex] + lettersRemaining[letterFoundIndex + 1:]
    
      # working on pattern identification
      pattern.append(currWord[i])
    else:
      board[index].colour = Colours.TILE_INVALID
      board[index].drawLetter(window)
    
    print(pattern)

  return True

# def GetPossibleWords(pattern, guessList):


# Used once off to create word frequency
def FilterWordFrequency(filePath, guessList):

  contents = ''
  with open(filePath, 'r') as file:
    contents = file.read()

  rows = contents.split('\n')
  output = {}
  totalInstances = 0
  for i in range(len(rows)):
    curr = rows[i].split(',')

    if len(curr[0]) == 5:
      if curr[0] in guessList:
        output[curr[0]] = curr[1]
        totalInstances += int(curr[1])
        guessList.remove(curr[0])

  writeToFile = []
  for i in output:
    output[i] = int(output[i]) / totalInstances

  # Get remainder from guesslist and give constant value
  for i in guessList:
    output[i] = 0.00000020036

  for i in output:
    with open('wordFrequency.csv', 'a') as file:
      file.write(str(i) + ',' + str(output[i]) + '\n')

  return output


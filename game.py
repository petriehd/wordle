import os, pygame
from resources import Colours

BORDER_WIDTH = 5

class Tile:
  # index = (row, col)
  # boardRect = (left, top, width, height)
  def __init__(self, index, boardRect) -> None:
    self.colour = Colours.BACKGROUND

    width = (boardRect[2] - 6 * BORDER_WIDTH) / 5
    height = (boardRect[3] - 7 * BORDER_WIDTH) / 6
    left = boardRect[0] + BORDER_WIDTH + index[0] * (width + BORDER_WIDTH)
    top = boardRect[1] + BORDER_WIDTH + index[1] * (height + BORDER_WIDTH)
    self.rect = pygame.Rect(left, top, width, height)

  def draw(self, surface):
    pygame.draw.rect(surface, self.colour, self.rect)

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

def CheckWord(word, currRow, answer, guessList, board):
  # Check correct length
  if (len(word) != 5): 
    print('Word not of length 5!') 
    return False
  # Check a valid word
  if (word not in guessList):
    print('Not a valid word!')
    return False
  
  # Check against answer
  # Need to update this to return these values or work on below
  greens = 0
  yellows = 0
  for i in range(5):
    if word[i] == answer[i]: 
      greens += 1
      continue
    if word[i] in answer:
      yellows += 1


  for i in range(5): board[currRow][i] = word[i]
  return True


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
    temp = file.read().split('\n')
    output = []
    for i in range(len(temp)):
      output.append(temp[i].split(','))
    
    return output
  
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
  if not WordInGuessList(currWord, guessList):
    text = font.render("Not a valid Word!", True, Colours.GRID_BORDER)
    window.blit(text, Locations.BOARD_PRINTOUT)
    return (False, None)
  
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

  return (True, pattern)

def GetPossibleWords(pattern, guessList):
  
  available = guessList
  for char in pattern:
    if char == 0:
      continue
    index = pattern.index(char)
    if index < 5:
      available = [guess for guess in available if char == guess[0][index]]
    else:
      available = [guess for guess in available if char in guess[0]]

  return available

def PrintAvailableWords(available, window):
  sortedWords = sorted(available, key=lambda x: x[1], reverse=True)
  count = len(sortedWords)
  top10 = sortedWords[:20]

  font = pygame.font.Font(None, 36)
  wordCount = font.render(f"Words Available: {count}", True, Colours.GRID_BORDER)
  window.blit(wordCount, Locations.AVAILABLE_WORD_COUNT)
  wordLocation = Locations.AVAILABLE_WORD
  for word in top10:
    wordText = font.render(f"{word[0]}", True, Colours.GRID_BORDER)
    window.blit(wordText, wordLocation)
    wordLocation = (wordLocation[0], wordLocation[1] + 25)


  return (count, top10)

def WordInGuessList(word, guessList):
  for guess in guessList:
    if guess[0] == word:
      return True
  
  return False

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


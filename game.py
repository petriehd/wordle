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

def InitScreen():
  width = 1100
  height = 700
  window = pygame.display.set_mode((width, height))
  pygame.display.set_caption('Wordle')
  window.fill(Colours.BACKGROUND)

  return window

def InitBoard(window):
  playBoardSize = (350,40,400,474)
  playBoardRect = pygame.Rect(playBoardSize)
  pygame.draw.rect(window, Colours.GRID_BORDER, playBoardRect)

  Board = []
  for i in range(5): 
    for j in range(6): 
      Board.append(Tile((i,j), playBoardRect))

  return Board

def GetWordList(filePath):
  with open(filePath, 'r') as file:
    temp = file.read().split('\n')
    output = []
    for i in range(len(temp)):
      output.append(temp[i].split(','))
    
    return output
  
def CheckWord(currWord, answer, guessList, row, board, window, pattern):
  font = pygame.font.Font(None, 36)
  if not WordInGuessList(currWord, guessList):
    text = font.render("Not a valid Word!", True, Colours.GRID_BORDER)
    window.blit(text, Locations.BOARD_PRINTOUT)
    return (False, None)
  
  pattern = CheckLetters(currWord, answer, row, board, window, pattern)

  return (True, pattern)

def CheckLetters(currWord, answer, row, board, window, pattern):
  lettersRemaining = answer
  for char in currWord:
    charIndex = currWord.index(char)
    boardIndex = row + charIndex * 6

    if char == answer[charIndex]:
      board[boardIndex].colour = Colours.TILE_HIT
      board[boardIndex].drawLetter(window)
      # Remove from available letters to avoid multiple hits for same letter
      lettersRemaining = lettersRemaining[:charIndex] + lettersRemaining[charIndex + 1:]
      # Add to pattern
      pattern[charIndex] = char
    elif char in lettersRemaining:
      board[boardIndex].colour = Colours.TILE_HIT_OTHER
      board[boardIndex].drawLetter(window)
      # Remove from available letters to avoid multiple hits for same letter
      letterIndex = lettersRemaining.index(char)
      lettersRemaining = lettersRemaining[:letterIndex] + lettersRemaining[letterIndex + 1:]
      # Add to pattern
      pattern.append(char)
    else:
      board[boardIndex].colour = Colours.TILE_INVALID
      board[boardIndex].drawLetter(window)

  return pattern



def GetPossibleWords(pattern, guessList, currWord):
  
  available = [guess for guess in guessList if guess[0] != currWord]
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
  # Reset available words board
  availWordBoardSize = (50,20, 280, 650)
  availWordBoardRect = pygame.Rect(availWordBoardSize)
  pygame.draw.rect(window, Colours.BACKGROUND, availWordBoardRect)

  # Sort Listt of words
  sortedWords = sorted(available, key=lambda x: x[1], reverse=False)
  count = len(sortedWords)
  top20 = sortedWords[:20]

  fontHeading = pygame.font.Font(None, 36)
  fontNormal = pygame.font.Font(None, 32)
  wordCountText = fontHeading.render(f"Words Available: {count}", True, Colours.GRID_BORDER)
  window.blit(wordCountText, Locations.AVAILABLE_WORD_COUNT)

  wordLocation = Locations.AVAILABLE_WORDS
  top20Text = fontNormal.render('Top 20 Words:', True, Colours.GRID_BORDER)
  window.blit(top20Text, wordLocation)

  for word in top20:
    wordLocation = (wordLocation[0], wordLocation[1] + 27)
    wordText = fontNormal.render(f"{word[0]}", True, Colours.GRID_BORDER)
    window.blit(wordText, wordLocation)


  return (count, top20)

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


import os, pygame
from resources import Colours, Locations
import pandas as pd

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
  output = pd.read_csv(filePath, header=None);
  output = output.iloc[:, :2]

  # Nomalise data
  min = output.iloc[:, 1].min()
  max = output.iloc[:, 1].max()
  output[2] = round((output.iloc[:, 1] - min) / (max - min), 5)

  return output
  
def CheckWord(currWord, answer, guessList, row, board, window, pattern, lettersNotInWord):
  font = pygame.font.Font(None, 36)

  if currWord not in guessList.iloc[:, 0].values:
    text = font.render("Not a valid Word!", True, Colours.GRID_BORDER)
    window.blit(text, Locations.BOARD_PRINTOUT)
    return (False, None)
  
  pattern = CheckLetters(currWord, answer, row, board, window, pattern, lettersNotInWord)

  return (True, pattern)

def CheckLetters(currWord, answer, row, board, window, pattern, lettersNotInWord):
  lettersRemaining = answer
  for charIndex, char in enumerate(currWord):
    boardIndex = row + charIndex * 6

    if char == answer[charIndex]:
      board[boardIndex].colour = Colours.TILE_HIT
      board[boardIndex].drawLetter(window)
      # Remove from available letters to avoid multiple hits for same letter
      lettersRemaining = lettersRemaining[:charIndex] + lettersRemaining[charIndex + 1:]
      # Add to pattern
      pattern[charIndex] = char
    elif char in answer and char in lettersRemaining:
      board[boardIndex].colour = Colours.TILE_HIT_OTHER
      board[boardIndex].drawLetter(window)
      # Remove from available letters to avoid multiple hits for same letter
      letterIndex = lettersRemaining.index(char)
      lettersRemaining = lettersRemaining[:letterIndex] + lettersRemaining[letterIndex + 1:]
      # Add to pattern
      if char not in pattern:
        pattern.append(char)
    else:
      board[boardIndex].colour = Colours.TILE_INVALID
      board[boardIndex].drawLetter(window)
      lettersNotInWord.append(char)



  return pattern

def GetPossibleWords(pattern, guessList, currWord, lettersNotInWord):
  
  available = guessList
  # First filter out words that contain letters that are not in the word
  for char in lettersNotInWord:
    available = available[~available.iloc[:,0].str.contains(char)]
  
  # Remove current word as it was most recently tested word
  available = available[available != currWord]

  # Then loop through pattern and filter down available words depending on location in pattern
  for char in pattern:
    if char == 0:
      continue
    index = pattern.index(char)
    if index < 5:
      available = available[available.iloc[:, 0].str[index] == char]
    else:
      available = available[available.iloc[:,0].str.contains(char)]

  return available

def PrintAvailableWords(available, window):
  # Reset available words board
  availWordBoardSize = (50,20, 280, 650)
  availWordBoardRect = pygame.Rect(availWordBoardSize)
  pygame.draw.rect(window, Colours.BACKGROUND, availWordBoardRect)

  # Sort List of words
  sortedWords = available.sort_values(by=available.columns[1], ascending=False)
  count = len(sortedWords)
  top20 = sortedWords.head(20)

  # Format headings and print headings
  fontHeading = pygame.font.Font(None, 36)
  fontNormal = pygame.font.Font(None, 32)
  wordCountText = fontHeading.render(f"Words Available: {count}", True, Colours.GRID_BORDER)
  window.blit(wordCountText, Locations.AVAILABLE_WORD_COUNT)

  wordLocation = Locations.AVAILABLE_WORDS
  top20Text = fontNormal.render('Top 20 Words:', True, Colours.GRID_BORDER)
  window.blit(top20Text, wordLocation)

  # Loop through top 20 and print out words and their probability
  for index, row in top20.iterrows():
    wordLocation = (wordLocation[0], wordLocation[1] + 27)
    wordText = fontNormal.render(f"{row[0]}", True, Colours.GRID_BORDER)
    window.blit(wordText, wordLocation)

    # # Not printing probabilities at the moment as taking up too much space
    # probLocation = (wordLocation[0] + 85, wordLocation[1])
    # probText = fontNormal.render(f"{float(row[2])}", True, Colours.GRID_BORDER)
    # window.blit(probText, probLocation)


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

def PlayGame(window, guessList):
  Board = InitBoard(window)
  for tile in Board:
    tile.draw(window)

  correct = guessList.sample(n = 1).iloc[0, 0]
  print(correct)

  play = True
  currRow = 0
  currCol = 0
  currWord = ''
  availableWords = []
  pattern = [0,0,0,0,0]
  lettersNotInWord = []
  endCondition = 0

  while (play):
    for event in pygame.event.get():
      index = currRow + currCol * 6

      if event.type == pygame.QUIT:
        play = False
        endCondition = -1

      if event.type == pygame.KEYDOWN:
        key = chr(event.key)
        if event.key == pygame.K_BACKSPACE and currCol > 0:
          currCol -= 1
          Board[index - 6].draw(window)
          currWord = currWord[:currCol] + currWord[currCol + 1:]

        if 'a' <= key <= 'z' and currCol < 5:
          Board[index].letter = key
          Board[index].drawLetter(window)
          currCol += 1
          currWord += key

        if event.key == pygame.K_RETURN and currCol == 5:
          outcome = CheckWord(currWord, correct, guessList, currRow, Board, window, pattern, lettersNotInWord)
          if outcome[0]:
            availableWords = GetPossibleWords(outcome[1], guessList, currWord, lettersNotInWord)
            PrintAvailableWords(availableWords, window)
            
            currRow += 1
            currCol = 0
            currWord = ''
            print(pattern)
            
            if CheckGameWon(pattern):
              play = False
              endCondition = 1
              break

    pygame.display.update()
  
  return endCondition

def CheckGameWon(pattern):
  for i in range(5):
    if pattern[i] == 0:
      return False
    
  return True


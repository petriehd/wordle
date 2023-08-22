from game import *
from resources import Colours
import random, pygame

guessList = GetWordList('guessList.txt').split('\n')
# wordList = GetWordList('wordList.txt').split('\n')
wordFrequency = {}
    
pygame.init()

# Screen formatting
windowWidth = 1100
windowHeight = 700
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Wordle')
window.fill(Colours.BACKGROUND)

# Playing board formatting
boardSize = (350,40,400,474)
boardRect = pygame.Rect(boardSize)
pygame.draw.rect(window, Colours.GRID_BORDER, boardRect)

Board = InitBoard(boardSize)
for tile in Board:
  tile.draw(window)

def main():
  correct = random.choice(guessList)



  totalInstances = 0
  words = FilterWordFrequency('unigram_freq.csv', guessList)
  for word in words:
    totalInstances += int(word[1])

  for word in words:
    wordFrequency[word[0]] = (int(word[1]) / totalInstances)
  print(wordFrequency)


  play = True
  currRow = 0
  currCol = 0
  currWord = ''
  while (play):
    for event in pygame.event.get():
      index = currRow + currCol * 6
      if event.type == pygame.QUIT:
        play = False
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
          if CheckWord(currWord, correct, guessList, currRow, Board, window):
            currRow += 1
            currCol = 0
            currWord = ''

        
    pygame.display.update()


main()



  
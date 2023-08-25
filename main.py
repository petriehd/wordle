from game import *
from resources import Colours
import random, pygame

guessList = GetWordList('wordFrequency.csv')

pygame.init()

def main():
  window = InitScreen()
  Board = InitBoard(window)
  for tile in Board:
    tile.draw(window)

  correct = random.choice(guessList)[0]
  print(correct)

  play = True
  currRow = 0
  currCol = 0
  currWord = ''
  availableWords = []
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
          outcome = CheckWord(currWord, correct, guessList, currRow, Board, window)
          if outcome[0]:
            currRow += 1
            currCol = 0
            currWord = ''

            availableWords = GetPossibleWords(outcome[1], guessList)
            PrintAvailableWords(availableWords, window)
            

        
    pygame.display.update()


main()



  
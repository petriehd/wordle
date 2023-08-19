from game import *
from resources import Colours
import random, pygame

# Can take this out into init function
Board = []
for i in range(5): 
  for j in range(6): 
    Board.append(Tile)
guessList = GetWordList('guessList.txt').split('\n')
wordList = GetWordList('wordList.txt').split('\n')
    
pygame.init()

# Screen formatting
windowWidth = 1100
windowHeight = 700
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Wordle')
window.fill(Colours.BACKGROUND)

# Playing board formatting
rect = pygame.Rect(350,40,400,600)
pygame.draw.rect(window, Colours.GRID_BORDER, rect)
for tile in Board:
  tile.draw()


def main():
  correct = random.choice(wordList)

  play = True
  count = 0
  while (play):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        play = False
    pygame.display.update()

    newWord = input('Enter word choice: ')
    if newWord == correct: 
      win = True  
      break
    if CheckWord(newWord, count, correct, guessList, board):
      PrintBoard(board)
      count += 1

    if count > 5:
      play = False

  if win:
    print('You Win!')
  else:
    print('GameOver')

main()



  
from game import *
from resources import Colours
import random, pygame
import pandas as pd

guessList = GetWordList('wordsFinal.csv')

pygame.init()

def main():
  window = InitScreen()
  Board = InitBoard(window)
  for tile in Board:
    tile.draw(window)

  PlayGame(window, Board, guessList)


main()
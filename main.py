from game import *
from resources import Colours
import random, pygame
import pandas as pd

guessList = GetWordList('wordsFinal.csv')

pygame.init()

def main():
  window = InitScreen()

  Active = True
  while(Active):
    gameCondition = PlayGame(window, guessList)
    if gameCondition == -1:
      Active = False

    # Can add in button to click replay below
    # For now, will just continue to rerun
    #else if gameCondition == 1:

  
  


main()
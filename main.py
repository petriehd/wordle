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

      
    # For creating restart button
    #   
    # elif gameCondition == 1:

    # just getting those commits bby

  
  


main()
import os, random
from colorama import Fore

def GetWordList(filePath):
  with open(filePath, 'r') as file:
    return file.read()

board = [[' ' for i in range(5)] for i in range(6)]
guessList = GetWordList('guessList.txt').split('\n')
wordList = GetWordList('wordList.txt').split('\n')

def PrintBoard():
  # Clears terminal
  os.system('cls' if os.name == 'nt' else 'clear')

  for row in board:
    output = '|'
    for i in row: 
      output = output + i + '|' 
    print(output)
    print("\033[0;37;42m Testing ")


def CheckWord(word, row):
  # Check correct length
  if (len(word) != 5): 
    print('Word not of length 5!') 
    return False
  
  # Check a valid word
  if (word not in guessList):
    print('Not a valid word!')
    return False
  

  for i in range(5): board[row][i] = word[i]
  return True


  


    
def main():

  word = random.choice(wordList)

  row = 0
  win = False
  while (row < 6):
    newWord = input('Enter word choice: ')
    if newWord == word: 
      win = True  
      break
    if CheckWord(newWord, row):
      PrintBoard()
      row += 1

  if win:
    print('You Win!')
  else:
    print('GameOver')

main()



  
import os


output = []

for i in range(1,11):
    fileName = "words" + str(i) + ".csv"

    with open(fileName, 'r') as file:
      temp = file.read()
      for i in temp:
        output.append(i)
      
print(output[5000])

with open('wordsFinal.csv', 'w') as file:
  for i in output:
    modified = i.replace("\"", "")
    file.write(modified)
    
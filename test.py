originalList = [1, 2, 3, 'String', "hooray"]
newList = [None]*5

newList[0:2] = originalList[2:5]
newList[3:4] = originalList[0:2]

print(newList)

newList[2] = "Shawty"

print(originalList)
print(newList)
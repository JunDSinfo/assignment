import random
class Cat:
    def __init__(self, name=None):
        self.name = name
        self.age = random.randint(5, 10)
        self.favoriteFood = None
        self.nameHistory = []

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getFavoriteFood(self):
        return self.favoriteFood

    def setName(self, newName):
        self.nameHistory.append(newName)
        self.name = newName

    def setAge(self, newAge):
        self.age = newAge

    def setFavoriteFood(self, newFavoriteFood):
        self.favoriteFood = newFavoriteFood

    def speak(self, message="Meow"):
        print(message)
        self.age += 1
        if self.age % 5 == 0:
            print("Happy birthday! I am now", self.age, "years old.")

    def getNames(self):
        return self.nameHistory

    def getAverageNameLength(self):
        nameLengths = [len(name) for name in self.nameHistory]
        if len(nameLengths) > 0:
            return sum(nameLengths) / len(nameLengths)
        else:
            return 0


class Habit:
    name = ""
    isDaily = False

    def __init__(self, name, isDaily):
        self.name = name
        self.isDaily = isDaily

    def getName(self):
        return self.name

    def getDayly(self):
        return self.isDaily
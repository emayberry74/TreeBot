class Player:
    username = ""
    points = 0
    def __init__(self, Username, Points):
        self.username = Username
        self.points = Points

    def pointSet(self, value):
        self.points = value
class Aclass:
    def __init__(self):
        self.x = 29


class Bclass:
    def __init__(self):
        self.y = 344


a = Aclass()
b = Bclass()

print(a)
print(b)

list = [a, b]

newlist = []

for x in range(5):
    newlist.append(a)

print(newlist)
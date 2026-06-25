from random import randrange

class Dice:

    def __init__(self, max: int):
        self.max = max
        self.avg = (max // 2) + 1

    def roll(self):
        return randrange(1, self.max+1)
    
D4 = Dice(4)
D6 = Dice(6)
D8 = Dice(8)
D10 = Dice(10)
D12 = Dice(12)
D20 = Dice(20)
D100 = Dice(100)

def roll_dice(roll_query):
        total = 0
        for item in roll_query.split('+'):
          item = item.strip()
          if 'd' in item:
            components = item.split('d')
            if components[0] != '':
                total += int(components[0]) * Dice(int(components[1])).roll()
            else:
                total += Dice(int(components[1])).roll()
          else:
            total += int(item)
        return total

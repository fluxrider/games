import random

# This deck does not pre-shuffle (i.e. the new order isn't stored in memory)
class Deck:
  def __init__(s, values):
    s.top = []
    s.shuffle = values
    s.bottom = []

  def deal(s):
    if s.top:
      return s.top.pop()
    if s.shuffle:
      i = len(s.shuffle) - 1
      j = random.randint(0, i)
      v = s.shuffle[j]
      s.shuffle[j] = s.shuffle[i]
      s.shuffle.pop()
      return v
    if s.bottom:
      return s.bottom.pop()
    raise Exception("Reached end of deck.")

  def place_top(s, value):
    s.top.append(value)

  def place_bottom(s, value):
    s.bottom.insert(0, value)

  def place_shuffle(s, value):
    s.shuffle.append(value)

  def reshuffle(s):
    s.shuffle.extend(s.top)
    s.shuffle.extend(s.bottom)
    s.top.clear()
    s.bottom.clear()

  # utils
  def __len__(s):
    return len(s.top) + len(s.shuffle) + len(s.bottom)

  # convenience
  def ndeal(s, n):
    hand = []
    while n != 0:
      hand.append(s.deal())
      n -= 1
    return hand

  def nplace_top(s, values):
    for v in reversed(values):
      s.place_top(v)

  def nplace_bottom(s, values):
    for v in values:
      s.place_bottom(v)

  def nplace_shuffle(s, values):
    s.shuffle.extend(values)

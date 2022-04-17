from lib import chessmen
import string

def get_move(current_party):
    place, to = input().translate({ord(c): 
        None for c in string.whitespace}).split("->")
    place = place.lower()
    to = to.lower()
    place = (ord(place[0]) - 97, ord(place[1]) - 49)
    to = (ord(to[0]) - 97, ord(to[1]) - 49)
    return (place, to)
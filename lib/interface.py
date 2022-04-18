from lib import chessmen
import string

def get_move(current_party):
    place, to = input().translate({ord(c): 
        None for c in string.whitespace}).split("->")
    place = place.lower()
    to = to.lower()
    place = (ord(place[0]) - 97, ord(place[1]) - 49)
    place = (7 - place[1], place[0])
    to = (ord(to[0]) - 97, ord(to[1]) - 49)
    to = (7 - to[1], to[0])

    return (place, to)
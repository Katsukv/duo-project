# здесь будут функции для генерации уровней
#
#

map_file = open("rooms/map.txt", encoding="UTF-8")



def read_room():
    room = []
    for s in map_file:
        room.append([i for i in s])
    return room
from src.GUI.popups import help_overlay, inventory_overlay
from .heals import Heals

def handle_keypress(event, root, my_player_id, game_state, maze, send_position_func, player):
    key = event.keysym.lower()
    dx, dy = 0, 0

    if key == "z":
        dx = -1
    elif key == "s":
        dx = 1
    elif key == "q":
        dy = -1
    elif key == "d":
        dy = 1
    elif key =="h":
        help_overlay(root)
    elif key == "i":
        inventory_overlay(root, player)

    if dx != 0 or dy != 0:
        try_move(dx, dy, my_player_id, game_state, maze, send_position_func, player)

def try_move(dx, dy, my_player_id, game_state, maze, send_position_func, player):
    pos = game_state.get(my_player_id)
    if not pos:
        return
    
    new_x = pos["x"] + dx
    new_y = pos["y"] + dy

    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
        if maze[new_x][new_y] == " ":
            pos["x"] = new_x
            pos["y"] = new_y
            send_position_func(pos)
        #elif maze[new_x][new_y] == "b":
        #TODO:figth overlay
        elif maze[new_x][new_y] == "h":
            pos["x"] = new_x
            pos["y"] = new_y
            player.add_heal(Heals.Bandages.name)
            #print the heal inventory
            print(player.get_heals())
            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)
        elif maze[new_x][new_y] == "H":
            pos["x"] = new_x
            pos["y"] = new_y
            player.add_heal(Heals.MediKit.name)
            #print the heal inventory
            print(player.get_heals())
            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)




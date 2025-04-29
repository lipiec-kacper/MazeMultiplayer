from src.GUI.popups import heal_overlay, help_overlay, inventory_overlay
from .heals import Heals
from .weapons import Weapons

def handle_keypress(event, root, my_player_id, game_state, maze, send_position_func, player, end_game_func):
    key = event.keysym.lower()
    dx, dy = 0, 0

    if key == "up":
        dx = -1
    elif key == "down":
        dx = 1
    elif key == "left":
        dy = -1
    elif key == "right":
        dy = 1
    elif key =="h":
        help_overlay(root)
    elif key == "i":
        inventory_overlay(root, player)
    elif key == "x":
        heal_overlay(root, player)

    if dx != 0 or dy != 0:
        try_move(dx, dy, my_player_id, game_state, maze, send_position_func, player, end_game_func)

def try_move(dx, dy, my_player_id, game_state, maze, send_position_func, player, end_game_func):
    pos = game_state.get(my_player_id)
    if not pos:
        return
    
    new_x = pos["x"] + dx
    new_y = pos["y"] + dy

    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):

 
        if new_x == 0  and new_y == 2:
            end_game_func()
            print("end of game")
        elif new_x == 0  and new_y == 3:
            end_game_func()
            print("end of game")


        #TODO:MODIFY THE BOSSES SKIP
        if (maze[new_x][new_y] == " " or maze[new_x][new_y] == "_") :
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
        elif maze[new_x][new_y] == "A" and new_x == 33 and new_y == 38:
            player.add_weapon(Weapons.KNIFE.name)
            pos["x"] = new_x
            pos["y"] = new_y

            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)
        elif maze[new_x][new_y] == "A" and new_x == 27 and new_y == 31:
            player.add_weapon(Weapons.GLOCK.name)
            pos["x"] = new_x
            pos["y"] = new_y

            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)
        
        elif maze[new_x][new_y] == "A" and new_x == 29 and new_y == 5:
            player.add_weapon(Weapons.AK47.name)
            pos["x"] = new_x
            pos["y"] = new_y

            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)
        
        elif maze[new_x][new_y] == "A" and new_x == 7 and new_y == 1:
            player.add_weapon(Weapons.RPG.name)
            pos["x"] = new_x
            pos["y"] = new_y

            row_as_list = list(maze[new_x])
            row_as_list[new_y] = ' '
            maze[new_x] = ''.join(row_as_list)
            send_position_func(pos)
               





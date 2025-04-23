# client.py
import socket
import threading
import pickle
import tkinter as tk
from tkinter import messagebox

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("", 5555))  # Replace with server IP if testing on LAN

# Get player ID
data = client.recv(1024)
info = pickle.loads(data)
my_player_id = info["player_id"]

game_state = {}

maze = [
    "+-  ----------------------------------------------------------------------------+",
    "|           |     H    h      H    H        b         b |H          |H          |",
    "|           +---------------+               +-------+   |   +---+   +-------+   |",
    "|                           |   h           |   H   |   |   |   |   |       |   |",
    "|                           +-------+  b    +---+ b +   |   | H |   +   +   +   |",
    "|                           B       |           |       |   |   |       |   b   |",
    "|-------------------------------+   +-------+   |   +---+   |   +-----------+   |",
    "|A          H                   |   b          h|   |       |       |           |",
    "|    H                      +   +---------------|   +---+   |---+   |   +-------|",
    "|                           |                   |         b |    b  |          H|",
    "|                           +---------------+   +-----------+   +---|    b      |",
    "|                    H     B#       |    b  |           |           |           |",
    "|                   +-----------+   |   +   +-------+   +-------+   +-------+   |",
    "|                   |H         h|   |   |           |        b  |       |h      |",
    "|                   |   +---+   |   |   +---+   +-----------+   +   +   |   +---|",
    "|         H     H   |      H|   |   |       |       |   b   |       |   |       |",
    "|   +-----------------------+   |   +-------|   +   +   +   +-------|   |---+   |",
    "|           |H       b          |   b       |   |       |           |   |H      |",
    "|-------+   |---+   +---------------+   +   +-------+   |-------+   +   |       |",
    "| H |       |       | H            h|   |           |   |     b |       | b     |",
    "|   +   +---+   +   |               +---|   +---+   |   |   +   +-------|       |",
    "|   B           |   |                   |      H|   |   |   |       |   |h      |",
    "|   +-------------------+      b        +-------+   |   +   |---+   +   +---+   |",
    "|      H|               #                b          |       |               |   |",
    "|   +---+           +   +---------------------------------------------------+   |",
    "|___+   #B          | H |h                     b   H|      H|          H| b     |",
    "|       +   +-----------|   +-------------------+   +   +   |   +---+   |   +---|",
    "|      h|   |H         H|   |  A               H|      h|   |   | H |   |   | H |",
    "| b +---+   |   +---+   +   +-------+           +-------+   |   |   |   |   |   |",
    "|   |A      |      h|     b |       |          B#   |H      |   |   |   |   |   |",
    "|   +-----------+   |-------+   +   +-----------+   |   |   |   |   |   +   |   |",
    "|         b        H|    b      |           |       |   |   |   |   |       |   |",
    "|   +-----------------------+   +-------+   |   +   |   +---|   +   +-------+   |",
    "|    h  |h  |                   |H    A |   |   |   |  b   H|          h| H     |",
    "|       |   +   +   +-----------|   +---+   |  h|   |---+   +-------+   |---+   |",
    "|     H |H    H |               |   |       |   | b | h |h             H|       |",
    "|   +---------------+   +---+   |   |   +---+   |   |   +---------------+       |",
    "|   |H     H       H|       |   |   |    b  H  H|   | H        b    |           |",
    "|   +     b         +-------+   |   +-----------+   +-------+   +   +           |",
    "|                               |H   B          #               |              h|",
    "+-------------------------------------------------------------------------------+"
]

root = tk.Tk()
root.title("Maze Client")

text_widget = tk.Text(root, font=("Courier", 12), bg="black", fg="lime", wrap="none")
text_widget.pack(fill=tk.BOTH, expand=True)

def help_overlay():
    overlay = tk.Frame(root, bg="black", width=300, height=200)
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label1 = tk.Label(overlay, text="Help window", fg="white", bg="black")
    label1.pack(pady=(10, 5))

    label2 = tk.Label(overlay, text="Use Z Q S D to move", fg="white", bg="black")
    label2.pack()

    label3 = tk.Label(overlay, text="h are bandages and H are medikits", fg="white", bg="black")
    label3.pack()

    label4 = tk.Label(overlay, text="A are weapons", fg="white", bg="black")
    label4.pack()

    label5 = tk.Label(overlay, text="b are small bosses and B are big bosses", fg="white", bg="black")
    label5.pack()   

    label6 = tk.Label(overlay, text="# are minigame doors", fg="white", bg="black")
    label6.pack()

    label7 = tk.Label(overlay, text="To finish the game find the way out", fg="white", bg="black")
    label7.pack()


    button = tk.Button(overlay, text="close", command=overlay.destroy)
    button.pack()

def draw_players():
    display = [list(row) for row in maze]
    tag_map = {}

    for player_id, pos in game_state.items():
        x, y = pos["x"], pos["y"]
        if 0 <= x < len(display) and 0 <= y < len(display[x]):
            display[x][y] = "@"
            tag_map[(x, y)] = "my_player" if player_id == my_player_id else "other_player"

    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)

    for i, row in enumerate(display):
        for j, ch in enumerate(row):
            tag = tag_map.get((i, j), "normal")
            text_widget.insert(tk.END, ch, tag)
        text_widget.insert(tk.END, "\n")

    text_widget.tag_config("normal", foreground="lime")
    text_widget.tag_config("my_player", foreground="white")
    text_widget.tag_config("other_player", foreground="red")
    text_widget.config(state=tk.DISABLED)

def handle_keypress(event):
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
        help_overlay()

    if dx != 0 or dy != 0:
        try_move(dx, dy)

def try_move(dx, dy):
    pos = game_state.get(my_player_id)
    if not pos:
        return
    
    new_x = pos["x"] + dx
    new_y = pos["y"] + dy

    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]):
        if maze[new_x][new_y] == " ":
            pos["x"] = new_x
            pos["y"] = new_y
            send_position(pos)

def send_position(pos):
    data = pickle.dumps({"id": my_player_id, "pos": pos})
    client.send(data)

def receive_updates():
    global game_state
    messagebox.showinfo("Info", "Your player is the white @ on the maze, Use z, s, q, d to move, For more help press h")

    while True:
        try:
            data = client.recv(4096)
            if data:
                game_state = pickle.loads(data)
                root.after(0, draw_players)
        except:
            break

threading.Thread(target=receive_updates, daemon=True).start()

root.bind("<Key>", handle_keypress)
root.mainloop()


import socket
import threading
import pickle
import tkinter as tk
from tkinter import messagebox
from GameScript.movements import handle_keypress

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

root.bind("<Key>", lambda event: handle_keypress(event, root, my_player_id, game_state, maze, send_position))
root.mainloop()

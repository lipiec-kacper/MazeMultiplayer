# client.py
import socket
import threading
import pickle
import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))  # Replace with server IP if testing on LAN

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
    for player_id, pos in game_state.items():
        x, y = pos["x"], pos["y"]
        if 0 <= x < len(display) and 0 <= y < len(display[x]):
            display[x][y] = "@"  # Just insert for display

    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)

    for i, row in enumerate(display):
        for j, ch in enumerate(row):
            tag = "player" if ch == "@" else "normal"
            text_widget.insert(tk.END, ch, tag)
        text_widget.insert(tk.END, "\n")

    text_widget.tag_config("normal", foreground="lime")
    text_widget.tag_config("player", foreground="red")
    text_widget.config(state=tk.DISABLED)

def receive_updates():
    global game_state
    while True:
        try:
            data = client.recv(4096)
            if data:
                game_state = pickle.loads(data)
                root.after(0, draw_players)
        except:
            break

threading.Thread(target=receive_updates, daemon=True).start()

root.mainloop()

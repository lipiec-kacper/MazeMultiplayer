# # server.py
import socket
import threading
import pickle
import random
import time

HOST = ""
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
game_state = {}

def broadcast_game_state():
    data = pickle.dumps(game_state)
    for client in clients[:]:
        try:
            client.send(data)
        except:
            clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW] {addr} connected.")
    clients.append(conn)

    player_id = addr[1]  # Use port as unique ID
    game_state[player_id] = {"x": random.randint(36, 39), "y": random.randint(69, 79)}
    time.sleep(0.1)

    conn.send(pickle.dumps({"player_id": player_id}))


    broadcast_game_state()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            update = pickle.loads(data)
            if "id" in update and "pos" in update :
                game_state[update["id"]] = update["pos"]
                broadcast_game_state()

    except:
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        if conn in clients:
            clients.remove(conn)
        if player_id in game_state:
            del game_state[player_id]
        broadcast_game_state()
        conn.close()

def start():
    print(f"[STARTING] Server is running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

start()

# server.py
import socket
import threading
import pickle
import random
import time

HOST = ""
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
game_state = {
    'players': {}  # No maze initialization here
}

# Broadcast the updated game state to all clients
def broadcast_game_state():
    data = pickle.dumps(game_state)
    for client in clients[:]:
        try:
            client.send(data)
        except:
            clients.remove(client)

# Handle each client's connection
def handle_client(conn, addr):
    print(f"[NEW] {addr} connected.")
    clients.append(conn)

    player_id = addr[1]  # Use port as unique ID
    game_state['players'][player_id] = {"x": random.randint(36, 39), "y": random.randint(70, 79)}
 # Random position within maze
    time.sleep(0.1)

    conn.send(pickle.dumps({"player_id": player_id}))  # Send the player's unique ID to the client

    # Wait for the client to send the maze (along with player position)
    broadcast_game_state()

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            update = pickle.loads(data)
            if "id" in update and "pos" in update:
                # Update player position
                game_state['players'][update["id"]] = update["pos"]
                # If the player updated the maze (e.g., collected an item or moved), also update the maze
                if "maze" in update:
                    game_state['maze'] = update["maze"]
                # Broadcast the updated game state to all clients
                broadcast_game_state()

    except:
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        if conn in clients:
            clients.remove(conn)
        if player_id in game_state['players']:
            del game_state['players'][player_id]
        # After a client disconnects, update the game state for everyone
        broadcast_game_state()
        conn.close()

# Start the server and accept client connections
def start():
    print(f"[STARTING] Server is running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

start()

import tkinter as tk
from src.GameScript.heals import Heals
from tkinter import messagebox

def help_overlay(root):
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

def fight_overlay(root):
    overlay = tk.Frame(root, bg="black", width=300, height=200)
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label1 = tk.Label(overlay, text="Fight window", fg="white", bg="black")
    label1.pack(pady=(10, 5))

def inventory_overlay(root, player):
    overlay = tk.Frame(root, bg="black", width=300, height=200)
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label1 = tk.Label(overlay, text="Inventory Window", fg="white", bg="black")
    label1.pack(pady=(10, 5))

    # Format the inventory
    weapons, heals = player.get_inventory()
    inventory_text = f"Weapons: {', '.join(weapons)}\nHeals: {', '.join(heals)}"

    label2 = tk.Label(overlay, text=inventory_text, fg="white", bg="black", justify="left")
    label2.pack()

    button = tk.Button(overlay, text="close", command=overlay.destroy)
    button.pack()

def heal_overlay(root, player):
    overlay = tk.Frame(root, bg="black", width=300, height=250)
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    label1 = tk.Label(overlay, text="Inventory Window", fg="white", bg="black")
    label1.pack(pady=(10, 5))

    heals = player.get_heals()
    bandages = [h for h in heals if h == "Bandages"]
    medikits = [h for h in heals if h == "MediKit"]

    text_bandages = ", ".join(bandages)
    text_medikits = ", ".join(medikits)

    inventory_text = f"1. {text_bandages}\n2. {text_medikits}"
    label2 = tk.Label(overlay, text=inventory_text, fg="white", bg="black", justify="left")
    label2.pack()

    label3 = tk.Label(overlay, text="Choose a heal to use (1 or 2):", fg="white", bg="black")
    label3.pack(pady=(10, 0))

    player_health = f"Player current health: {player.get_player_health()}"
    label4 = tk.Label(overlay, text=player_health, fg="white", bg="black", justify="left")
    label4.pack()

    entry = tk.Entry(overlay)
    entry.pack()

    def on_confirm():
        choice = entry.get()
        if choice == "1":
            player.heal_player(Heals.access_heal("Bandages"))
            print("Bandages selected")
            player.remove_heal(Heals.Bandages.name)
        elif choice == "2":
            player.heal_player(Heals.access_heal("MediKit"))
            print("MediKit selected")
            player.remove_heal(Heals.MediKit.name)
        else:
            print("Invalid choice")

        heals = player.get_heals()
        bandages = [h for h in heals if h == "Bandages"]
        medikits = [h for h in heals if h == "MediKit"]
        text_bandages = ", ".join(bandages)
        text_medikits = ", ".join(medikits)
        inventory_text = f"1. {text_bandages}\n2. {text_medikits}"
        label2.config(text=inventory_text)
        label4.config(text=f"Player current health: {player.get_player_health()}")

    confirm_button = tk.Button(overlay, text="Confirm", command=on_confirm)
    confirm_button.pack(pady=(5, 10))


    button = tk.Button(overlay, text="Close", command=overlay.destroy)
    button.pack()



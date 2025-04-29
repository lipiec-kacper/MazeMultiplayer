import tkinter as tk
from src.GameScript.weapons import Weapons
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

def fight_overlay(root, player, boss_health, boss_name, boss_dammages, on_battle_end):
    overlay = tk.Frame(root, bg="black", width=400, height=400)
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    player_health = [player.get_player_health()]
    boss_health_var = [boss_health]

    label1 = tk.Label(overlay, text="Fight window", fg="white", bg="black")
    label1.pack(pady=(10, 5))

    label_status = tk.Label(overlay, text="", fg="white", bg="black", wraplength=380, justify="left")
    label_status.pack()

    label_health = tk.Label(overlay, fg="white", bg="black")
    label_health.pack()

    def update_health_display():
        label_health.config(
            text=f"Your HP: {player_health[0]}   |   {boss_name}'s HP: {boss_health_var[0]}"
        )

    label3 = tk.Label(overlay, text="Choose the weapon you want to fight with (enter number):", fg="white", bg="black")
    label3.pack()

    weapons = player.get_weapons()
    weapon_list_text = "\n".join(f"{i + 1}. {w}" for i, w in enumerate(weapons)) if weapons else "No weapons available."
    label4 = tk.Label(overlay, text=weapon_list_text, fg="white", bg="black")
    label4.pack()

    entry = tk.Entry(overlay)
    entry.pack()

    def start_battle(selected_weapon):
        update_health_display()

        def boss_turn():
            player_health[0] -= boss_dammages
            update_health_display()

            if player_health[0] <= 0:
                label_status.config(text=f"{boss_name} hit you! You have 0 HP.\nYou are dead! Game over.")
                root.after(2000, lambda: (overlay.destroy(), on_battle_end(False)))
                return

            label_status.config(
                text=f"{boss_name} hit you! You have {player_health[0]} HP remaining.\nDo you want to use a heal? (Y/N)"
            )
            heal_prompt()

        def heal_prompt():
            heal_entry = tk.Entry(overlay)
            heal_entry.pack()

            def handle_heal_choice():
                choice = heal_entry.get().strip().lower()
                heal_entry.destroy()
                heal_confirm.destroy()

                if choice == "y":
                    heals = player.get_heals()
                    if not heals:
                        label_status.config(text="No heals left! You skip your turn.")
                        root.after(1000, player_turn)
                        return

                    heal_list_text = "\n".join(f"{i + 1}. {h}" for i, h in enumerate(heals))
                    label_status.config(text="Choose a heal to use:\n" + heal_list_text)
                    heal_index_entry = tk.Entry(overlay)
                    heal_index_entry.pack()

                    def use_heal():
                        index = heal_index_entry.get()
                        if index.isdigit():
                            index = int(index) - 1
                            if 0 <= index < len(heals):
                                selected_heal = heals[index]
                                player.heal_player(Heals.access_heal(selected_heal))
                                player.remove_heal(selected_heal)
                                player_health[0] = player.get_player_health()
                                update_health_display()
                                label_status.config(text=f"You used {selected_heal}. Your HP is now {player_health[0]}.")
                                heal_index_entry.destroy()
                                heal_use_button.destroy()
                                root.after(1000, player_turn)
                            else:
                                label_status.config(text="Invalid heal number.")
                        else:
                            label_status.config(text="Please enter a valid number.")

                    heal_use_button = tk.Button(overlay, text="Use Heal", command=use_heal)
                    heal_use_button.pack()

                elif choice == "n":
                    label_status.config(text="You chose not to heal.")
                    root.after(1000, player_turn)
                else:
                    label_status.config(text="Invalid input. Please enter Y or N.")
                    heal_prompt()

            heal_confirm = tk.Button(overlay, text="Confirm Heal Choice", command=handle_heal_choice)
            heal_confirm.pack()

        def player_turn():
            damage = Weapons.access_dammage(selected_weapon)
            boss_health_var[0] -= damage
            update_health_display()

            if boss_health_var[0] <= 0:
                label_status.config(text=f"You hit {boss_name} for {damage} damage.\n{boss_name} is defeated!")
                root.after(2000, lambda: (overlay.destroy(), on_battle_end(True)))
            else:
                label_status.config(text=f"You hit {boss_name} for {damage} damage.\n{boss_name} has {boss_health_var[0]} HP remaining.")
                root.after(1500, boss_turn)

        boss_turn()

    def on_confirm_weapon():
        choice = entry.get()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(weapons):
                selected_weapon = weapons[index]
                entry.destroy()
                confirm_button.destroy()
                label4.config(text=f"You selected: {selected_weapon}")
                root.after(1000, lambda: start_battle(selected_weapon))
            else:
                label_status.config(text="Invalid weapon number.")
        else:
            label_status.config(text="Please enter a number.")

    confirm_button = tk.Button(overlay, text="Confirm Weapon", command=on_confirm_weapon)
    confirm_button.pack(pady=(5, 10))

    close_button = tk.Button(overlay, text="Close", command=overlay.destroy)
    close_button.pack()

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



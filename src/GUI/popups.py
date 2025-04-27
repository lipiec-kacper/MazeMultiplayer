import tkinter as tk

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








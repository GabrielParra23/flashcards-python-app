from tkinter import * 
from tkinter import messagebox
from random import choice, randint, shuffle
import pandas as pd
import os
import sys

BACKGROUND_COLOR = "#B1DDC6"
word = {}
timer = None
if getattr(sys, 'frozen', False):
    data_path = os.path.dirname(sys.executable)
else:
    data_path = os.path.dirname(__file__)

# ---------------------------- PATH ------------------------------- #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# ---------------------------- DATA ------------------------------- #
output_path = os.path.join(data_path, "data/update_list.csv")

# Garante que a pasta 'data' existe onde o EXE está, senão o to_csv falha
if not os.path.exists(os.path.join(data_path, "data")):
    os.makedirs(os.path.join(data_path, "data"))

try:
    data = pd.read_csv(output_path)
except FileNotFoundError: 
    data = pd.read_csv(resource_path("data/english-words.csv"))

data_dict = data.to_dict(orient='records')


# ---------------------------- CARDS ------------------------------- #

def right_card():
    global data_dict, word, data
    data_dict.remove(word)
    total = len(data_dict)
    tx_total.config(text=f'Total words: {total}')
    new_data = pd.DataFrame(data_dict)
    new_data.to_csv(output_path, index=False)
    pick_card()
    
def pick_card():
    global word, timer
    if timer:
        window.after_cancel(timer)
    word = choice(data_dict)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text='English', fill='black')
    canvas.itemconfig(card_word, text=word['English'], fill='black')
    timer = window.after(3000, flip)

def flip():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text='Portugues', fill='white')
    canvas.itemconfig(card_word, text=word['Portugues'], fill='white')


# ---------------------------- UI SETUP ---------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=3)

pick_card()

total = len(data_dict)

# EUA_image = PhotoImage(file=resource_path("images/EUA.png"))
# EUA_button = Button(image=EUA_image, highlightthickness=0, command=pick_card, bd=0, bg=BACKGROUND_COLOR)
# EUA_button.grid(row=0, column=0)

cross_image = PhotoImage(file=resource_path("images/wrong.png"))
unknown_button = Button(image=cross_image, highlightthickness=0, command=pick_card, bd=0)
unknown_button.grid(row=2, column=0)

check_image = PhotoImage(file=resource_path("images/right.png"))
known_button = Button(image=check_image, highlightthickness=0, command=right_card, bd=0)
known_button.grid(row=2, column=2)

tx_total = Label(text=f'Total words: {total}', highlightthickness=0, bg=BACKGROUND_COLOR, bd=0, font=("Ariel", 30))
tx_total.grid(row=2, column=1 )

window.mainloop()

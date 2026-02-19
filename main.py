from tkinter import * 
from tkinter import messagebox
from random import choice, randint, shuffle
import pandas as pd
from pandas.errors import EmptyDataError
import os
import sys

BACKGROUND_COLOR = "#B1DDC6"
word = {}
timer = None
language = 'EUA'
data_dict = {}
concluido = False
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
def path():
    global output_path
    if language == 'EUA':
        output_path = os.path.join(data_path, "data/update_list_EUA.csv")
    elif language == 'French':
        output_path = os.path.join(data_path, "data/update_list_french.csv")
    elif language == 'spain':
        output_path = os.path.join(data_path, "data/update_list_spain.csv")

def Finished():
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text='Parabéns ', fill='black')
    canvas.itemconfig(card_word, text='Você completou a lista', fill='black', font=("Ariel", 40, "bold"))   
    tx_total.config(text=f'Total words: 0')

path()

# Garante que a pasta 'data' existe onde o EXE está, senão o to_csv falha
if not os.path.exists(os.path.join(data_path, "data")):
    os.makedirs(os.path.join(data_path, "data"))

try:
    data = pd.read_csv(output_path)
except FileNotFoundError: 
    data = pd.read_csv(resource_path("data/english_words.csv"))
except EmptyDataError:
    concluido = True

if not concluido:
    data_dict = data.to_dict(orient='records')


# ---------------------------- CARDS ------------------------------- #   
def on_resize(event):
    w, h = event.width, event.height
    canvas.coords(card_background, w/2, h/2)
    canvas.coords(card_title, w/2, h * 0.3)
    canvas.coords(card_word, w/2, h/2)
    canvas.itemconfig(card_word, width=w*0.8)

def change_languege_EUA():
    global data_dict, data, word, language, concluido
    language = 'EUA'
    path()
    print(output_path)
    try:
        data = pd.read_csv(output_path)
        concluido = False
    except FileNotFoundError: 
        data = pd.read_csv(resource_path("data/english_words.csv"))
        concluido = False
    except EmptyDataError:
        concluido = True
    if concluido:
        Finished()
    else:     
        data_dict = data.to_dict(orient='records')
        total = len(data_dict)
        tx_total.config(text=f'Total words: {total}')
        pick_card()

def change_languege_french():
    global data_dict, data, word, language, concluido
    language = 'French'
    path()
    print(output_path)
    try:
        data = pd.read_csv(output_path)
        concluido = False
    except FileNotFoundError: 
        data = pd.read_csv(resource_path("data/french_words.csv"))
        concluido = False
    except EmptyDataError:
        concluido = True
    if concluido:
        Finished()
    else:     
        data_dict = data.to_dict(orient='records')
        total = len(data_dict)
        tx_total.config(text=f'Total words: {total}')
        pick_card()

def change_languege_spain():
    global data_dict, data, word, language, concluido
    language = 'spain'
    path()
    print(output_path)
    try:
        data = pd.read_csv(output_path)
        concluido = False
    except FileNotFoundError: 
        data = pd.read_csv(resource_path("data/spain_words.csv")) 
        concluido = False 
    except EmptyDataError:
        concluido = True
    if concluido:
        Finished()
    else:     
        data_dict = data.to_dict(orient='records')
        total = len(data_dict)
        tx_total.config(text=f'Total words: {total}')
        pick_card()

def right_card():
    global data_dict, word, data
    if not concluido:
        data_dict.remove(word)
        total = len(data_dict)
        tx_total.config(text=f'Total words: {total}')
        new_data = pd.DataFrame(data_dict)
        new_data.to_csv(output_path, index=False)
        pick_card()
    
def pick_card():
    global word, timer
    total = len(data_dict)
    if timer:
        window.after_cancel(timer)
    if not concluido:
        word = choice(data_dict)
        current_keys = list(word.keys())
        foreign_language_key = [key for key in current_keys if key != 'Portugues'][0]

        canvas.itemconfig(card_title, text=foreign_language_key, fill='black')
        canvas.itemconfig(card_word, text=word[foreign_language_key], fill='black')
        canvas.itemconfig(card_background, image=card_front_img)
        timer = window.after(3000, flip)
    else:
        Finished()


def flip():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text='Portugues', fill='white')
    canvas.itemconfig(card_word, text=word['Portugues'], fill='white')


# ---------------------------- UI SETUP ---------------------------- #

window = Tk()
window.title("Flashy")
window.state('zoomed')
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

window.columnconfigure((0, 1, 2), weight=1)
window.rowconfigure(1, weight=1)

canvas = Canvas(window, bg=BACKGROUND_COLOR, highlightthickness=0, width=500, height=350)
canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")

card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))

card_background = canvas.create_image(0, 0, image=card_front_img)
card_title = canvas.create_text(0, 0, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(0, 0, text="", font=("Ariel", 60, "bold"))

canvas.bind("<Configure>", on_resize)


total = len(data_dict)

EUA_image = PhotoImage(file=resource_path("images/EUA.png"))
EUA_button = Button(image=EUA_image, highlightthickness=0, command=change_languege_EUA, bd=0, bg=BACKGROUND_COLOR)
EUA_button.grid(row=0, column=0, sticky="n", pady=10)

french_image = PhotoImage(file=resource_path("images/french.png"))
french_button = Button(image=french_image, highlightthickness=0, command=change_languege_french, bd=0, bg=BACKGROUND_COLOR)
french_button.grid(row=0, column=1, sticky="n", pady=10)

spain_image = PhotoImage(file=resource_path("images/spain.png"))
spain_button = Button(image=spain_image, highlightthickness=0, command=change_languege_spain, bd=0, bg=BACKGROUND_COLOR)
spain_button.grid(row=0, column=2, sticky="n", pady=10)


cross_image = PhotoImage(file=resource_path("images/wrong.png"))
unknown_button = Button(image=cross_image, highlightthickness=0, command=pick_card, bd=0)
unknown_button.grid(row=2, column=0, sticky="s", pady=10)

check_image = PhotoImage(file=resource_path("images/right.png"))
known_button = Button(image=check_image, highlightthickness=0, command=right_card, bd=0)
known_button.grid(row=2, column=2, sticky="s", pady=10)

tx_total = Label(text=f'Total words: {total}', highlightthickness=0, bg=BACKGROUND_COLOR, bd=0, font=("Ariel", 30))
tx_total.grid(row=2, column=1, sticky="s", pady=10)

if concluido:
    Finished()
else:
    pick_card()

window.mainloop()

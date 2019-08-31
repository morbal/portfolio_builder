from tkinter import *
window = Tk()

def source_switch():
    if symbol_btn["text"] == "from csv":
        symbol_btn.configure(text="from input")
    elif symbol_btn["text"] == "from input":
        symbol_btn.configure(text="from csv")

symbol_btn = Button(window, text="from csv", command=source_switch)
symbol_btn.pack()

window.mainloop()


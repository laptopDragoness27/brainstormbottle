import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('800x600')
root.title('Brainstorm in a Bottle')

ideaslist = []
ideasSym = []

def result():
    ideaslist.append(email_entry.get())
    ideasSym.append(ttk.Label(root,text=ideaslist[-1]).grid(column=0,row=len(ideaslist)+1))


email_entry = ttk.Entry(root, width=80)
email_entry.grid(column=0,row=0,sticky="nsew")

enterButton = ttk.Button(root, text="enter", command=result).grid(column=0,row=1,sticky="nsew")

root.grid_columnconfigure(0, weight=1)

root.mainloop()
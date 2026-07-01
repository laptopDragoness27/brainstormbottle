import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('300x200')
root.title('Brainstorm in a Bottle')

ideaslist = []
ideasSym = []

def result():
    ideaslist.append(email_entry.get())
    ideasSym.append(ttk.Label(root,text=ideaslist[-1]).pack(pady=5))
    print(ideaslist)


email_entry = ttk.Entry(root)
email_entry.pack(pady=5)

enterButton = ttk.Button(root, text="enter", command=result).pack(pady=5)

root.mainloop()
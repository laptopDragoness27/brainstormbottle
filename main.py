import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('800x600')
root.title('Brainstorm in a Bottle')

ideaslist = []
ideasSym = []
ideasRem = []

def remove(name,labelthing):
    name.destroy()
    labelthing.destroy()
    

def result():
    ideaslist.append(email_entry.get())
    label = ttk.Label(form_frame, text=ideaslist[-1])
    closebutton = ttk.Button(form_frame,width=2, text="X", command= lambda:remove(closebutton, label))
    closebutton.grid(column=1, row=len(ideaslist) + 1, columnspan=3)
    label.grid(column=0, row=len(ideaslist) + 1, columnspan=3)
    ideasSym.append(closebutton)
    ideasRem.append(label)


form_frame = ttk.Frame(root)
form_frame.place(relx=0.5, rely=0, anchor="n")

ttk.Label(form_frame, text="enter your ideas below:").grid(column=0, row=0, padx=(0, 6))
email_entry = ttk.Entry(form_frame, width=50)
email_entry.grid(column=1, row=0, padx=6)
enterButton = ttk.Button(form_frame, text="enter", command=result)
enterButton.grid(column=2, row=0, padx=(6, 0))

root.mainloop()
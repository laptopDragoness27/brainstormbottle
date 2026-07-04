import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry('800x600')
root.title('Brainstorm in a Bottle')

ideaslist = []
labellist = []

def remove(name,labelthing):
    name.destroy()
    labelthing.destroy()
    

def result():
    if email_entry.get()!="":
        #add the entered value to the list of ideas
        ideaslist.append(email_entry.get())
        #create a label from the latest idea in the list, put it on 1 lower than the length of the idea list so it's in the right place
        label = ttk.Label(list_frame, text=ideaslist[-1])
        label.grid(column=1, row=len(ideaslist) + 1, pady=10)
        #create the button to get rid of the item in the list 20 to the right and -3 up relative to the label
        closebutton = ttk.Button(list_frame,width=2, text="X", command= lambda:remove(closebutton, label))
        closebutton.place(in_=label,relx=1.0, x=20, y=-3)

        labellist.append(label)

        #make button to move item up
        changeplaceu=ttk.Button(list_frame, text="↑", command=lambda:moveup(labellist, labellist.index(label)), width=2)
        changeplaceu.place(in_=label,relx=0.0, x=-45, y=-3)
        #make button to move item down
        changeplaced=ttk.Button(list_frame, text="↓", command=lambda:movedown(labellist, labellist.index(label)), width=2)
        changeplaced.place(in_=changeplaceu,relx=0.0, x=-45)

def moveup(oglist,itemindex):
    if itemindex!=0:
        oglist.insert(itemindex-1,oglist.pop(itemindex))
        # Clear all labels from grid
        for x in range(len(oglist)):
            oglist[x].grid_forget()
        # Re-grid labels in new order
        for idx, lbl in enumerate(oglist):
            lbl.grid(row=idx, column=0, sticky='ew', pady=10)
        # Make columns expand
        root.columnconfigure(0, weight=1)

def movedown(oglist, indexofmoved):
    if indexofmoved!=len(oglist)-1:
        oglist.insert(indexofmoved+1,oglist.pop(indexofmoved))
        # Clear all labels from grid
        for x in range(len(oglist)):
            oglist[x].grid_forget()
        # Re-grid labels in new order
        for idx, lbl in enumerate(oglist):
            lbl.grid(row=idx, column=0, sticky='ew', pady=10)
        # Make columns expand
        root.columnconfigure(0, weight=1)

#creates a frame to work with that is centered.
form_frame = ttk.Frame(root)
form_frame.place(relx=0.5, rely=0, anchor="n")
#creates a lower frame to work with that is centered just for the list.
list_frame = ttk.Frame(root, width=8000, padding=(100,0))
list_frame.place(relx=0.5, rely=0, anchor="n", y=40)

#label placed to the left of the entry box
ttk.Label(form_frame, text="enter your ideas below:").grid(column=0, row=0, padx=(0, 6))
#the place where you type in your ideas
email_entry = ttk.Entry(form_frame, width=50)
email_entry.grid(column=1, row=0, padx=6)
#the enter button, runs the function that adds a new list item when pressed
enterButton = ttk.Button(form_frame, text="enter", command=result)
enterButton.grid(column=2, row=0, padx=(6, 0))


root.mainloop()
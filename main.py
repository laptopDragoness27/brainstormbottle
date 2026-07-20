import tkinter as tk
from tkinter import ttk,font,PhotoImage
from tkinter import filedialog
import json

root = tk.Tk()
root.geometry('800x600')
root.title('Brainstorm in a Bottle')

global ideaslist
ideaslist = []
global labellist
labellist = []

undonelist = []

#sets the font
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Times New Roman",size=10,weight=font.NORMAL)
root.option_add("*Font", "TkDefaultFont")

binpic = tk.PhotoImage(file="bin.png").subsample(16,16)
uparrow = tk.PhotoImage(file="uparrow.png").subsample(160,160)
downarrow = tk.PhotoImage(file="downarrow.png").subsample(40,40)

def undo(event=None):
    global ideaslist
    if undonelist:
        ideaslist = undonelist.pop()
        redraw()
    else:
        print("nothing to undo")

def save():
    def closewindow():
        if nameentry.get()!="":
            savename.withdraw()
    #creates a new window to enter the name of the list you're saving
    savename=tk.Toplevel()
    canvas = tk.Canvas(savename, height=100, width=250)
    canvas.pack()
    #a label
    label = tk.Label(canvas,text="enter list name:").pack()
    #the entry menu for the name of the saved file
    global nameentry
    nameentry = tk.Entry(canvas)
    nameentry.pack()
    #a button to save the file
    tk.Button(canvas,text="save", command=lambda:[finalsave(),closewindow()]).pack()

def finalsave():
        #saves the current list in its current order as a json file, with the name written by the user
        if nameentry.get()!="":
             with open((nameentry.get()+".json"), mode="w", encoding="utf-8") as write_file:json.dump(ideaslist, write_file)
        closewindow=True

def load():
    file_path = filedialog.askopenfilename(title="Select list file", filetypes=[("JSON file", ('*.json'))])
    if file_path!=None:
        with open(file_path, "r") as f:
            ideaslist=json.load(f)
            for x in range(len(ideaslist)):
                addlistitem(ideaslist[x])

#creates a menu to load and save in
menubar=tk.Menu(root)
root.config(menu=menubar)

def exit():
    #creates a new window to enter the name of the list you're saving
    savename=tk.Toplevel()
    canvas = tk.Canvas(savename, height=100, width=250)
    canvas.pack()
    tk.Label(canvas,text="did you remember to save?").pack()
    tk.Button(canvas,text="yes (exit)",command=root.destroy).pack()
    tk.Button(canvas,text="no (save)",command=save).pack()

#adds save button
menubar.add_command(
    label="Save",
    command=save
)
#adds load button
menubar.add_command(
    label="Load",
    command=load
)
#adds undo button
menubar.add_command(
    label="Undo",
    command=undo
)
#adds exit button
menubar.add_command(
    label="Exit",
    command=exit
)

savename = ""
nameentry = None


def remove(labelthing,remember):
    global ideaslist
    if remember:
        undonelist.append(ideaslist.copy())
    ideaslist.remove(labelthing.cget("text"))
    redraw()

#this function adds the string in the input as a new idea in the list visible to the user
def addlistitem(ideaname,remember):
    
    #create a label from the latest idea in the list, put it on 1 lower than the length of the idea list so it's in the right place
    if remember:
        undonelist.append(ideaslist[:])
    label = ttk.Label(list_frame, text=ideaname)
    if len(labellist)==0:
        label.grid(column=1, row=len(labellist), pady=10, sticky="ew")
    else:
        label.grid(column=1, row=len(labellist) + 1, pady=10, sticky="ew")
    #create the button to get rid of the item in the list 20 to the right and -3 up relative to the label
    closebutton = ttk.Button(list_frame,width=2, text="D", image=binpic, command= lambda:remove(label, True))
    closebutton.place(in_=label,relx=1.0, x=20, y=-3)

    labellist.append(label)
    ideaslist.append(ideaname)

    #make button to move item up
    changeplaceu=ttk.Button(list_frame, image=uparrow, command=lambda:moveup(labellist, labellist.index(label)), width=2)
    changeplaceu.place(in_=label,relx=0.0, x=-45, y=-3)
    #make button to move item down
    changeplaced=ttk.Button(list_frame, image=downarrow, command=lambda:movedown(labellist, labellist.index(label)), width=2)
    changeplaced.place(in_=changeplaceu,relx=0.0, x=-45)

    #changeplaced=ttk.Button(list_frame, text="✎", command=lambda:edit(label), width=2)
    #changeplaced.place(in_=closebutton,relx=1.0, x=18)

def redraw():
    global labellist
    for w in list_frame.winfo_children():
        w.destroy()
    labellist.clear()
    current=ideaslist.copy()
    ideaslist.clear()
    for idea in current:
        addlistitem(idea, False)

    #recentres all the items
    root.columnconfigure(0, weight=1)

def result():
    if email_entry.get()!="":
        #add the entered value to the list of ideas
        addlistitem(email_entry.get(), True)

def moveup(oglist,itemindex):
    if itemindex!=0:
        undonelist.append(ideaslist.copy())
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
        undonelist.append(ideaslist.copy())
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

root.bind("<Control-z>", undo)

root.mainloop()

import tkinter as tk
from tkinter import *
from tkinter import StringVar, ttk,font,PhotoImage,Entry
from tkinter import filedialog
import json

root = tk.Tk()
root.geometry('1000x800')
root.title('Brainstorm in a Bottle')

#sets the icon image to the logo (brainstormbottlelogo.png)
root.iconphoto(False, tk.PhotoImage(file='brainstormbottlelogo.png'))

#sets the background colour
backGroundColour = '#db9e43'
root.option_add("*Background", backGroundColour)
root.configure(bg=backGroundColour)

#sets accent colour
accentColour = "#c93975"
accentTextColour = "#eff77e"

global ideaslist
ideaslist = []
global labellist
labellist = []

undonelist = []

#list of all the cloud objects
global cloudlist
cloudlist=[]

def updatecolor(label,firstTime):
    rank=label.grid_info()['row']
    if firstTime:
        if rank == 0:
            label.config(bg='gold')
        elif rank==2:
            label.config(bg='silver')
        elif rank==3:
            label.config(bg='#cd7f32')
        else:
            label.config(bg=accentColour)
    else:
        if rank == 0:
            label.config(bg='gold')
        elif rank==1:
            label.config(bg='silver')
        elif rank==2:
            label.config(bg='#cd7f32')
        else:
            label.config(bg=accentColour)

# stolen code that allows for dynamic text wrapping
def update_text_height(label):
    # Update the height of the text widget to fit the content
    text_widget=label
    lines = len(label.get('1.0','end'))//52+1
    if lines>3:
        lines=3
    root.after(1, lambda: label.configure(height=lines))

#sets the font
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tuffy",size=11,weight=font.NORMAL)
root.option_add("*Font", "TkDefaultFont")

#subsample shrinks the x and y proportions down by that multiple, equal to that dimesion's size divided by 15
binpic = tk.PhotoImage(file="bin.png").subsample(4,4)
uparrow = tk.PhotoImage(file="uparrow.png").subsample(4,4)
downarrow = tk.PhotoImage(file="downarrow.png").subsample(4,4)
pencil = tk.PhotoImage(file="pencil.png").subsample(4,4)
cloudbackground = tk.PhotoImage(file="cloudbackground.png").subsample(3,3)
check = tk.PhotoImage(file="check.png").subsample(4,4)

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

def load():
    file_path = filedialog.askopenfilename(title="Select list file", filetypes=[("JSON file", ('*.json'))])
    if file_path!=None:
        #removes all the current entries to make way for the ones loaded in, if there's stuff to remove
        if len(labellist)>0:
            for y in range(len(labellist),-1,-1):
                labellist[y-1].destroy()
        #opens json file and creates a list entry for each idea in the json file 
        with open(file_path, "r") as f:
            ideaslist=json.load(f)
            for x in range(len(ideaslist)):
                addlistitem(ideaslist[x],False)

#creates a menu to load and save in
menubar=tk.Menu(root, bg=accentColour, fg=accentTextColour, borderwidth=2.0)
root.config(menu=menubar)

def exit():
    #creates a new window to enter the name of the list you're saving
    savename=tk.Toplevel()
    canvas = tk.Canvas(savename, height=100, width=250)
    canvas.pack()
    tk.Label(canvas,text="did you remember to save?").pack()
    tk.Button(canvas,text="yes (exit)",command=root.destroy).pack()
    tk.Button(canvas,text="no (save)",command=save).pack()

def edit(label,button):
    if label.cget("state") == "disabled":
        label.configure(state="normal")
        button.configure(image=check)
    else:
        button.configure(image=pencil)
        undonelist.append(ideaslist.copy())
        label.configure(state="disabled")
        ideaslist[labellist.index(label)] = label.get('1.0','end')
        if len(label.get('1.0','end'))==1:
            remove(label,False)
            return
        update_text_height(label)
        

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


def remove(labelthing,cloudthing,remember):
    global ideaslist
    if remember:
        undonelist.append(ideaslist.copy())

    ideaslist.remove(labelthing.get('1.0','end'))
    cloudlist.remove(cloudthing)
    redraw()

#this function adds the string in the input as a new idea in the list visible to the user
def addlistitem(ideaname,remember):
    #create a label from the latest idea in the list, put it on 1 lower than the length of the idea list so it's in the right place
    if remember:
        undonelist.append(ideaslist[:])

    #makes background cloud
    cloud = tk.Label(inner,image=cloudbackground)
    
    label = tk.Text(inner, width=50, height=1, wrap="word")
    label.insert('1.0',str(ideaname))
    update_text_height(label)
    label.configure(state="disabled")
    #this if statement places the first label at 0, then adds one to the rest.
    #I'm commenting this in post so honestly I don't know why that makes it work
    if len(labellist)==0:
        #places background cloud behind label
        cloud.grid(column=1, row=len(labellist), pady=10)
        #places label
        label.grid(column=1, row=len(labellist), pady=10)
    else:
        #places cloud behind label
        cloud.grid(column=1, row=len(labellist) + 1, pady=10)
        #places label
        label.grid(column=1, row=len(labellist) + 1, pady=10)
    updatecolor(label,True)
    
    #create the button to get rid of the item in the list 20 to the right and -3 up relative to the label
    closebutton = tk.Button(inner,width=16, text="D", image=binpic, command= lambda:remove(label,cloud, True), bg=accentColour)
    closebutton.place(in_=label,relx=1.0, x=20, y=-3)
    closebutton.lift()

    labellist.append(label)
    labellist[-1]=label
    ideaslist.append(ideaname)
    ideaslist[-1]=label.get('1.0','end')

    cloudlist.append(cloud)
    cloudlist[-1]=cloud

    #make button to move item up
    changeplaceu=tk.Button(inner, image=uparrow, command=lambda:moveup(labellist, labellist.index(label), cloudlist), width=16, bg=accentColour)
    changeplaceu.place(in_=label,relx=0.0, x=-45, y=-3)
    changeplaceu.lift()
    #make button to move item down
    changeplaced=tk.Button(inner, image=downarrow, command=lambda:movedown(labellist, labellist.index(label), cloudlist), width=16, bg=accentColour)
    changeplaced.place(in_=changeplaceu,relx=0.0, x=-45)
    changeplaced.lift()

    editbutton=tk.Button(inner, image=pencil, command=lambda:edit(label,editbutton), width=16, bg=accentColour)
    editbutton.place(in_=closebutton,relx=1.0, x=18)
    editbutton.lift()

    tup = ("Inconsolata", 10)  # Define font
    label.configure(font=tup)  # Apply font

    if remember:
        redraw()

def redraw():
    global labellist
    for w in inner.winfo_children():
        w.destroy()
    labellist.clear()
    cloudlist.clear()
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

def moveup(oglist,itemindex, cloudlist):
    if itemindex!=0:
        
        oglist.insert(itemindex-1,oglist.pop(itemindex))
        undonelist.append(ideaslist.copy())
        # Clear all labels from grid
        for x in range(len(oglist)):
            oglist[x].grid_forget()

        #move clouds with other stuff
        for idx, cld in enumerate(cloudlist):
            cld.grid(row=idx, column=0)
            cld.lower()
        
        # Re-grid labels in new order
        for idx, lbl in enumerate(oglist):
            lbl.grid(row=idx, column=0, pady=10)
            lbl.lift()
        for idx, lbl in enumerate(oglist):
            updatecolor(lbl,False)
        
        # Make columns expand
        root.columnconfigure(0, weight=1)

def movedown(oglist, indexofmoved, cloudlist):
    if indexofmoved!=len(oglist)-1:
        undonelist.append(ideaslist.copy())
        oglist.insert(indexofmoved+1,oglist.pop(indexofmoved))
        # Clear all labels from grid
        for x in range(len(oglist)):
            oglist[x].grid_forget()

        #move clouds with other stuff
        for idx, cld in enumerate(cloudlist):
            cld.grid(row=idx, column=0)
            cld.lower()
        
        # Re-grid labels in new order
        for idx, lbl in enumerate(oglist):
            lbl.grid(row=idx, column=0, pady=10)
            lbl.lift()
        for idx, lbl in enumerate(oglist):
            updatecolor(lbl,False)
        
        # Make columns expand
        root.columnconfigure(0, weight=1)

#creates a frame to work with that is centered.
form_frame = tk.Frame(root)
form_frame.place(relx=0.5, rely=0, anchor="n")

#label placed to the left of the entry box
tk.Label(form_frame, text="Enter Your Ideas Here:", bg=backGroundColour).grid(column=0, row=0, padx=6, pady=20)

#the place where you type in your ideas
email_entry = ttk.Entry(form_frame, width=50)
email_entry.grid(column=1, row=0, padx=6, pady=20)

#the enter button, runs the function that adds a new list item when pressed
enterButton = tk.Button(form_frame, text="enter", command=result, bg=accentColour, fg=accentTextColour, borderwidth=0)
enterButton.grid(column=2, row=0, padx=6, pady=20)

#a lower frame for the canvas
canvasFrame = tk.Frame(root)
canvasFrame.place(relx=0.5,rely=0.08,anchor="n")

#creates canvas for scrolling
root.update()
canvas = tk.Canvas(canvasFrame,width=710, height=root.winfo_height()-200, highlightthickness=0)

inner = tk.Frame(canvas)                       # your widgets go in here
bar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
inner_window = canvas.create_window((0, 0),window=inner)

canvas.configure(yscrollcommand=bar.set)
canvas.pack()

canvas.create_window((0, 0), window=inner, anchor="nw")
bar.pack(side="right",fill="y")


# without this the canvas never learns how tall the frame is
inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))



root.bind("<Control-z>", undo)
root.bind("<Return>", result)

root.mainloop()

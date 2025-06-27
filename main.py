# // imports
from tkinter import Label,Entry,Button,Text,Tk,END,SEL_FIRST,SEL_LAST,WORD,Menu,filedialog,messagebox,colorchooser
from keyboard import is_pressed
from tkinter.font import Font
from os import makedirs,path
from gc import enable
# // variables
autosave = False
font_size = 10
VERSION = "1.8"
filepath = ""
textmodes = {}
# // functions

enable() # // enables garbage colector

def init():

    """
    Creates all the files needed for the app to run (opened files and last filepath)
    """

    global filepath
    if not path.exists("C:/Np--"):
        makedirs("C:/Np--") # // on crée le dossier s'il n'existe pas
    with open("C:/Np--/info.txt","r") as f:
        filepath = f.read()

    try:
        opened_files = open("C:/Np--/opened_files.txt","r")
        opened_files.close()
    except:
        opened_files = open("C:/Np--/opened_files.txt","w")
        opened_files.close()

    try:
        with open(filepath,"r") as file:
            text.insert("1.0",file.read())
            window.title(f"Notepad-- V{VERSION} -- {filepath}")
    except:
        pass

def openedwindow():

    """
    Opens the window to see recently opened files
    """

    op_window = Tk()

    with open("C:/Np--/opened_files.txt","r") as file:
            dic = dict()
            duplicates = set()
            content : list = file.readlines()

            for path in content:
                if path in dic:
                    duplicates.add(path)
                else:
                    dic[path] = None
                    content.append(path)

            with open("C:/Np--/opened_files.txt","w"):pass

            with open("C:/Np--/opened_files.txt","a") as file:
                for j in content:
                    if not j in duplicates:
                        file.write(j)

            del dic,duplicates,content

    def loadFile(fp):

        """
        Loads a new file content from the opened window

        - Asks if user wants to save or not
        - Clears existing text
        - Loads a new file
        """

        global text
        global filepath
        filepath = fp

        with open("C:/Np--/info.txt","w") as info:
            info.write(fp)

        if messagebox.askquestion("Save",message="Do you want to save this file ?") == "yes":
            save()
            text.delete("1.0",END)
            try:
                with open(fp,"r") as file:
                    text.insert("1.0",file.read())
            except:
                with open("C:/Np--/opened_files.txt","r") as file:
                    textP = file.read().replace(fp,"")

                with open("C:/Np--/opened_files.txt","a") as file:
                    file.write(textP)

                del textP

        else:
            text.delete("1.0",END)
            try:
                with open(fp,"r") as file:
                    text.insert("1.0",file.read())
            except:
                with open("C:/Np--/opened_files.txt","r+") as file:
                    textP = file.read().replace(fp,"")
                with open("C:/Np--/opened_files.txt","w") as file:
                    file.write(textP)
                    
                del textP

        window.title(f"Notepad-- V{VERSION} -- {filepath}")
        

    with open("C:/Np--/opened_files.txt","r") as file:
        for f in file.readlines():
            if f != "\n" :#// sinon ca fonctionne pas :(
                FPbutton = Button(op_window,text=f,command=lambda k=f.replace("\n","") :loadFile(k))
                FPbutton.pack()

    update()
    window.title(f"Notepad-- V{VERSION} -- {filepath}")
    op_window.mainloop()

    del op_window

def save():
    """
    Saves a file
    
    - If already in a file -> saves to this file
    - Else uses savefile() to create a new file
    """
    if filepath == "":
        savefile()
    else:
        with open(filepath, "w") as file:
            file.write(text.get(1.0,END))

        with open("C:/Np--/info.txt","w") as info:
            info.write(filepath)
            
    window.title(f"Notepad-- V{VERSION} -- {filepath}")

def update(event=0): # // the event parameter is necessary
    """
    Code that is run every time an event is detected
    """

    char_label.config(text=f"characters: {len(text.get(1.0,END))-1}")

    if not filepath == "" and autosave:
        save()

    if is_pressed("ctrl+s"):
        save()
    elif is_pressed("ctrl+f"):
        find_window()

def openfile():

    """
    Opens file with file dialog
    """

    global filepath
    filepath = filedialog.askopenfilename(title="Open a text file",filetypes=[("Text files","*.txt"),("Python files","*.py"),("All files","*.*")])
    if filepath != "":

        text.delete("1.0",END)

        with open(filepath,"r") as file:
            text.insert("1.0",file.read())

        with open("C:/Np--/info.txt","w+") as info:
            info.write(filepath)

        with open("C:/Np--/opened_files.txt","r+") as opened:
            files = opened.read()
            if not filepath in files:
                opened.write(f"{files}\n{filepath}")
    window.title(f"Notepad-- V{VERSION} -- {filepath}")
    update()

def savefile():

    """
    Uses filedialog to create a new file / overwrite a file
    """

    global filepath
    
    file = filedialog.asksaveasfile(defaultextension=".txt",filetypes=[("Text files","*.txt"),("Python files","*.py"),("Javascript files","*.js"),("All files","*.*")])
    filepath = str(file).split("'")[1].replace("'","")
    
    if file:
        file.write(text.get("1.0",END))
        file.close()
        with open("C:/Np--/info.txt","w") as info:
            info.write(filepath)

def font_size_plus():

    """
    Increases font size
    """

    global font_size
    global testlabel
    textwid = text.winfo_width()
    font_size += 1
    text.config(font=("Arial",font_size),width=textwid+1)
    testlabel.config(text="Font size: "+str(font_size))

def font_size_minus():

    """
    Decreases font size
    """

    global font_size
    global testlabel
    if font_size > 1:
        textwid = text.winfo_width()
        font_size -= 1
        text.config(font=("Arial",font_size),width=textwid-1)
        testlabel.config(text="Font size: "+str(font_size))

def close():
    """Closes the window -_-"""
    new_window.destroy()

def settingwindow():

    """
    Opens the setting window
    """

    global testlabel
    global new_window

    def ChangeASState():

        """
        Changes the autosave setting to on or off
        """

        global autosave
        if autosave:
            autosave = False
            as_button.config(text="Enable auto-save")
        else:
            autosave = True
            as_button.config(text="Disable auto-save")

    new_window = Tk()
    new_window.title("Settings")
    new_window.geometry("200x100")

    testlabel = Label(new_window,text="Font size: "+str(font_size))
    testlabel.grid(column=1,row=1)

    plus_button = Button(new_window,text="+",command=font_size_plus)
    plus_button.grid(column=0,row=1,padx=(45,0))

    minus_button = Button(new_window,text="-",command=font_size_minus)
    minus_button.grid(column=2,row=1)

    as_button = Button(new_window,command=ChangeASState) # // autosave button
    if autosave:
        as_button.config(text="Disable auto-save")
    else:
        as_button.config(text="Enable auto-save")
    as_button.grid(column=0,row=2,columnspan=3,padx=(45,0))

    ok_button = Button(new_window,text="Ok",command=close)
    ok_button.grid(column=4,row=4,pady=(20,0),padx=(5,0))

    new_window.mainloop()

def del_window():
    window.destroy()

def delete_all():
    if messagebox.askquestion("Delete all",message="Are you sure you want to delete all of the text ?") == "yes":
        text.delete("1.0",END)

def replace_window():

    """
    Opens the replace window
    """

    global text

    def replace():
        rep_chars = old_entry.get().split(";")
        text_content = text.get(1.0,END)

        for i in rep_chars:
            text_content = text_content.replace(i,new_entry.get())

        text.delete(1.0,END)
        text.insert(1.0,text_content)

        del text_content

    def close():
        repwindow.destroy()

    repwindow = Tk()
    repwindow.title("Replace")
    repwindow.geometry("220x100")

    old_label = Label(repwindow,text="replace :")
    old_label.grid(row=2,column=1)

    new_label = Label(repwindow,text="with :")
    new_label.grid(row=3,column=1)

    old_entry = Entry(repwindow)
    old_entry.grid(row=2,column=2,columnspan=2)

    new_entry = Entry(repwindow)
    new_entry.grid(row=3,column=2,columnspan=2)

    ok_button = Button(repwindow,text="Apply",command=replace)
    ok_button.grid(column=3,row=4,pady=(30,0),padx=(0,0))

    close_button = Button(repwindow,text="Close",command=close)
    close_button.grid(column=4,row=4,pady=(30,0),padx=(0))

    repwindow.mainloop()


def delete_window():

    """
    Opens the delete window
    """

    global text

    def delete():

        del_chars = entry.get().split(";")
        text_content = text.get(1.0,END)

        for i in del_chars:
            text_content = text_content.replace(i,"")

        text.delete(1.0,END)
        text.insert(1.0,text_content)

    def close():
        delwindow.destroy()

    delwindow = Tk()
    delwindow.title("Replace")
    delwindow.geometry("220x100")

    old_label = Label(delwindow,text="Delete :")
    old_label.grid(row=2,column=1)

    entry = Entry(delwindow)
    entry.grid(row=2,column=2,columnspan=2)

    info_label = Label(delwindow,text="You can delete multible characters \nby separating them with a ';'")
    info_label.grid(column=1,row=3,columnspan=3)

    ok_button = Button(delwindow,text="Apply",command=delete)
    ok_button.grid(column=2,row=4)

    close_button = Button(delwindow,text="Close",command=close)
    close_button.grid(column=3,row=4,padx=(2,0))

    delwindow.mainloop()

def count_window():

    """
    Open the count window
    """

    def count():

        """
        Counts the amount of words
        """

        word = entry.get()
        amount = text.get(1.0,END).count(word)
        countwindow.destroy()
        messagebox.showinfo(title="Count",message=f"{amount} instances of '{word}' found in the text")

        del word,amount

    def close():
        countwindow.destroy()

    countwindow = Tk()
    countwindow.title("Count")
    countwindow.geometry("220x100")

    count_label = Label(countwindow,text="")
    count_label.grid(row=2,column=1)

    info_label = Label(countwindow,text="count :")
    info_label.grid(row=1,column=1)

    entry = Entry(countwindow)
    entry.grid(row=1,column=2,columnspan=2)

    count_button = Button(countwindow,text="Apply",command=count)
    count_button.grid(column=3,row=4,pady=(30,0))

    close_button = Button(countwindow,text="Close",command=close)
    close_button.grid(column=4,row=4,pady=(30,0),padx=(0))

    countwindow.mainloop()


def debug_window():

    """
    Opens the debug window
    """

    debugwindow = Tk()
    debugwindow.title("Debug")

    debug_label = Label(debugwindow,text=f"filepath : {filepath}")
    debug_label.pack()

    debug_autosave = Label(debugwindow,text=f"autosave : {autosave}")
    debug_autosave.pack()

    debugwindow.mainloop()

def changetext(mode):

    """
    Changes the style of the selected text :)
    """

    bold_font = Font(family="Helvetica", size=font_size, weight="bold")
    text.tag_configure("BOLD", font=bold_font)

    mode_list = ["HIGH","BOLD","C_CUSTOM"]

    if mode == "HIGH":
        try:
            color = colorchooser.askcolor()[1]
            text.tag_configure("HIGH",background=color)
            text.tag_add("HIGH", "sel.first", "sel.last")
            textmodes[f"{SEL_FIRST}/{SEL_LAST}"] = "HIGH"
        except:
            pass
    elif mode == "BOLD":
        try:
            text.tag_add("BOLD", "sel.first", "sel.last")
            textmodes[f"{SEL_FIRST}/{SEL_LAST}"] = "BOLD"
        except:
            pass
    elif mode == "C_CUSTOM":
        try:
            color = colorchooser.askcolor()[1]
            text.tag_configure("C_CUSTOM",foreground=color)
            text.tag_add("C_CUSTOM", "sel.first", "sel.last")
            textmodes[f"{SEL_FIRST}/{SEL_LAST}"] = "C_CUSTOM"
        except:
            pass
    elif mode == "CLEAR":
        for i in mode_list:
            text.tag_remove(i,1.0,END)


def find_window():

    """
    Opens the find window
    """

    def find():
        indx = 0
        text.tag_configure("F_HIGH",background="yellow")
        word = entry.get()
        found = text.search(word,1.0)
        text.tag_remove("F_HIGH",1.0,END)
        for i in range(len(found)):
            if found[i] == ".":
                indx = i
                break
        if found:
            text.tag_add("F_HIGH",found,f"{found[:indx]}.{int(found[indx+1:])+len(word)}")
            text.see(found)

    def close():
        findwindow.destroy()

    findwindow = Tk()
    findwindow.title("Find")
    findwindow.geometry("220x100")

    count_label = Label(findwindow,text="")
    count_label.grid(row=2,column=1)

    info_label = Label(findwindow,text="Find :")
    info_label.grid(row=1,column=1)

    entry = Entry(findwindow)
    entry.grid(row=1,column=2,columnspan=2)
    entry.focus()

    find_button = Button(findwindow,text="Apply",command=find)
    find_button.grid(column=3,row=4,pady=(30,0))

    close_button = Button(findwindow,text="Close",command=close)
    close_button.grid(column=4,row=4,pady=(30,0),padx=(0))

    findwindow.mainloop()

def see_window():

    """
    Opens the window to choose which line to look to
    """

    def see():

        line = entry.get()
        try:
            text.see(line)
        except:
            try:
                text.see(f"{line}.0")
            except:
                messagebox.showinfo(title="Syntax error",message=f"invalid syntax")
        seewindow.destroy()

    def close():
        seewindow.destroy()

    seewindow = Tk()
    seewindow.title("Look")
    seewindow.geometry("200x70")

    see_label = Label(seewindow,text="")
    see_label.grid(row=2,column=1)

    info_label = Label(seewindow,text="Look at line :")
    info_label.grid(row=1,column=1)

    entry = Entry(seewindow)
    entry.grid(row=1,column=2,columnspan=2)

    see_button = Button(seewindow,text="Apply",command=see)
    see_button.grid(column=2,row=4)

    close_button = Button(seewindow,text="Close",command=close)
    close_button.grid(column=3,row=4)

    seewindow.mainloop()


def newFileWindow():
    """
    Creates a new file
    """

    global filepath

    filepath = ""
    window.title(f"Notepad-- V{VERSION}")
    text.delete(1.0,END)


# // window

window = Tk()

menubar = Menu(window)
window.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="Open",command=openfile)
filemenu.add_command(label="New",command=newFileWindow)
filemenu.add_command(label="Save as",command=savefile)
filemenu.add_command(label="Save (ctrl+s)",command=save)
filemenu.add_command(label="Opened",command=openedwindow)
filemenu.add_separator()
filemenu.add_command(label="Close",command=del_window)

editmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Delete all",command=delete_all)
editmenu.add_command(label="View",command=see_window)
editmenu.add_separator()
editmenu.add_command(label="Replace",command=replace_window)
editmenu.add_command(label="Delete",command=delete_window)
editmenu.add_command(label="Count",command=count_window)
editmenu.add_command(label="Find (ctrl+f)",command=find_window)

settings_menu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Settings",menu=settings_menu)
settings_menu.add_command(label="Settings",command=settingwindow)
settings_menu.add_command(label="Debug",command=debug_window)

textmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Text",menu=textmenu)
textmenu.add_command(label="Bold",command=lambda : changetext("BOLD"))
textmenu.add_command(label="Highlight",command=lambda : changetext("HIGH"))
textmenu.add_command(label="Color",command=lambda : changetext("C_CUSTOM"))
textmenu.add_separator()
textmenu.add_command(label="Clear",command=lambda : changetext("CLEAR"))

text = Text(window,width=650,font=("Arial",10),wrap=WORD)
text.focus()
text.pack(fill="both",expand=True)

char_label = Label(text="characters: 0")
char_label.config(width=100)
char_label.pack(padx=(0,850),fill="both")

window.bind("<Key>",update)
window.geometry("950x650")
window.title(f"Notepad-- V{VERSION}")


init()
window.mainloop()

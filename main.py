##imports
from tkinter import *
from tkinter import filedialog,messagebox,colorchooser
from keyboard import is_pressed
from time import sleep
from tkinter.font import Font
import os
##variables
text_list = [""]
autosave = False
font_size = 10
VERSION = 1.5
filepath = ""
##functions

def undo():
    text.delete("1.0",END)
    text_list.remove(text_list[-1])
    text.insert("1.0",text_list[-1])
    if len(text_list) == 0:
        text_list.append("")

def save():
    if filepath == "":
        savefile()
    else:
        with open(filepath, "r+") as file:
            file.seek(0)
            file.write(text.get(1.0,END))
            file.close()

def update(event=0):
    new_len = len(text.get(1.0,END))-1
    char_label.config(text=f"characters: {new_len}")
    if autosave and not filepath == "":
        save()
    if len(text_list) > 0:
        if text.get("1.0",END) != text_list[-1] and not is_pressed("ctrl"):
            text_list.append(text.get("1.0",END))
        elif is_pressed("ctrl+z"):
            old_text_lines = text.get(1.0,END).splitlines()
            undo()
            new_text_lines = text.get(1.0,END).splitlines()
            for i in range(len(new_text_lines)):
                if old_text_lines[i] != new_text_lines[i]:
                    text.see(str(i)+".0")
                    break
        elif is_pressed("ctrl+s"):
            save()
        elif is_pressed("ctrl+f"):
            find_window()
    else:
        text_list.append("")

def openfile():
    global filepath
    filepath = filedialog.askopenfilename(title="Open a text file",filetypes=[("Text files","*.txt"),("Python files","*.py"),("All files","*.*")])
    if filepath != "":
        file = open(filepath,"r")
        text.insert("1.0",file.read())
        file.close()
    update()

def savefile():
    global filepath
    file = filedialog.asksaveasfile(defaultextension=".txt",filetypes=[("Text files","*.txt"),("Python files","*.py"),("All files","*.*")])
    filepath = str(file).split("'")[1].replace("'","")
    if file:
        filetext = str(text.get("1.0",END))
        file.write(filetext)
        file.close()

def font_size_plus():
    global font_size
    global testlabel
    textwid = text.winfo_width()
    font_size += 1
    text.config(font=("Arial",font_size),width=textwid+1)
    testlabel.config(text="Font size: "+str(font_size))

def font_size_minus():
    global font_size
    global testlabel
    if font_size > 1:
        textwid = text.winfo_width()
        font_size -= 1
        text.config(font=("Arial",font_size),width=textwid-1)
        testlabel.config(text="Font size: "+str(font_size))

def close():
    new_window.destroy()

def settingwindow():
    global testlabel
    global new_window

    def ChangeASState():
        global autosave
        if autosave:
            autosave= False
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

    as_button = Button(new_window,command=ChangeASState) ##autosave button
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
    text.delete("1.0",END)

def replace_window():
    global text

    def replace():
        rep_chars = old_entry.get().split(";")
        text_content = text.get(1.0,END)

        for i in rep_chars:
            text_content = text_content.replace(i,new_entry.get())

        text.delete(1.0,END)
        text.insert(1.0,text_content)

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

    def count():
        word = entry.get()
        amount = text.get(1.0,END).count(word)
        countwindow.destroy()
        messagebox.showinfo(title="Count",message=f"{amount} instances of '{word}' found in the text")

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
    debugwindow = Tk()
    debugwindow.title("Debug")

    debug_label = Label(debugwindow,text=f"filepath : {filepath}")
    debug_label.pack()

    debug_label_text_list = Label(debugwindow,text=f"text_list : {text_list}")
    debug_label_text_list.pack()

    debug_autosave = Label(debugwindow,text=f"autosave : {autosave}")
    debug_autosave.pack()

    debugwindow.mainloop()

def changetext(mode):
    bold_font = Font(family="Helvetica", size=font_size, weight="bold")
    text.tag_configure("BOLD", font=bold_font)

    mode_list = ["HIGH","BOLD","C_CUSTOM"]

    if mode == "HIGH":
        try:
            color = colorchooser.askcolor()[1]
            text.tag_configure("HIGH",background=color)
            text.tag_add("HIGH", "sel.first", "sel.last")
        except:
            pass
    elif mode == "BOLD":
        try:
            text.tag_add("BOLD", "sel.first", "sel.last")
        except:
            pass
    elif mode == "C_CUSTOM":
        try:
            color = colorchooser.askcolor()[1]
            text.tag_configure("C_CUSTOM",foreground=color)
            text.tag_add("C_CUSTOM", "sel.first", "sel.last")
        except:
            pass
    elif mode == "CLEAR":
        for i in mode_list:
            text.tag_remove(i,1.0,END)


def find_window():

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

##window

window = Tk()

menubar = Menu(window)
window.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="Open",command=openfile)
filemenu.add_command(label="Save as",command=savefile)
filemenu.add_command(label="Save (ctrl+s)",command=save)
filemenu.add_separator()
filemenu.add_command(label="Close",command=del_window)

editmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Delete all",command=delete_all)
editmenu.add_command(label="Undo (ctrl+z)",command=undo)
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

text = Text(window,width=650,font=("Arial",10))
text.focus()
text.pack(fill="both",expand=True)

char_label = Label(text="characters: 0")
char_label.config(width=100)
char_label.pack(padx=(0,850),fill="both")

window.bind("<Key>",update)
window.geometry("950x650")
window.title(f"Notepad-- V{VERSION}")
window.mainloop()

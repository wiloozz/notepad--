##imports
from tkinter import *
from tkinter import filedialog,messagebox
from keyboard import is_pressed
from time import sleep
##variables
text_list = [""]
autosave = 1
font_size = 10
VERSION = 1.1
filepath = ""
##functions
def undo():
    text.delete("1.0",END)
    text_list.remove(text_list[-1])
    text.insert("1.0",text_list[-1])
    if len(text_list) == 0:
        text_list.append("")

def update(event):
    char_label.config(text=f"characters: {len(text.get(1.0,END))-1}")
    if len(text_list) > 0:
        if text.get("1.0",END) != text_list[-1] and not is_pressed("ctrl"):
            text_list.append(text.get("1.0",END))
        elif is_pressed("ctrl+z"):
            undo()
        elif is_pressed("ctrl+s"):
            save()
    else:
        text_list.append("")

def openfile():
    global filepath
    filepath = filedialog.askopenfilename(title="Open a text file",filetypes=[("Text files","*.txt"),("Python files","*.py"),("All files","*.*")])
    if filepath != "":
        file = open(filepath,"r")
        text.insert("1.0",file.read())
        print(filepath)
        file.close()
        
def savefile():
    file = filedialog.asksaveasfile(defaultextension=".txt",filetypes=[("Text files","*.txt"),("Python files","*.py"),("All files","*.*")])
    filetext = str(text.get("1.0",END))
    file.write(filetext)
    file.close()

def save():
    if filepath == "":
        savefile()
    else:
        with open(filepath, "r+") as file:
            file.seek(0)
            file.write(text.get(1.0,END))
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
    new_window = Tk()
    new_window.title("Settings")
    new_window.geometry("200x100")

    testlabel = Label(new_window,text="Font size: "+str(font_size))
    testlabel.grid(column=1,row=1)

    plus_button = Button(new_window,text="+",command=font_size_plus)
    plus_button.grid(column=0,row=1,padx=(45,0))

    minus_button = Button(new_window,text="-",command=font_size_minus)
    minus_button.grid(column=2,row=1)

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
        old_text = text.get(1.0,END)
        text.delete(1.0,END)
        text.insert(1.0,old_text.replace(old_entry.get(),new_entry.get()))

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

def count_window():
    def count():
        amount = text.get(1.0,END).count(entry.get())
        messagebox.showinfo(title="Count",message=f"{amount} instances of '{entry.get()}' found in the text")

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

    debugwindow.mainloop()


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
editmenu.add_separator()
editmenu.add_command(label="Replace",command=replace_window)
editmenu.add_command(label="Count",command=count_window)

settings_menu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Settings",menu=settings_menu)
settings_menu.add_command(label="AutoSave",command=settingwindow)
settings_menu.add_command(label="Debug",command=debug_window)

text = Text(window,width=650,font=("Arial",10))
text.pack(fill="both",expand=True)

char_label = Label(text="characters: 0")
char_label.config(width=100)
char_label.pack(padx=(0,850),fill="x")

window.bind("<Key>",update)
window.geometry("950x650")
window.title(f"Notepad-- V{VERSION}")
window.mainloop()

from tkinter import *
from tkinter import messagebox

def analyze_line():
    global e
    string = e.get(1.0, 'end-1c')
    if (string == "hello" '\n' "punk"):
        messagebox.showinfo("You did it!", 'OK')
    else:
        messagebox.showinfo("Please try again.", 'OK')
        

root = Tk()

root.title('Name')

textBox=Text(root, height=3, width=50)
textBox.pack()
textBox.insert(INSERT, "Oh no, the door is locked!")
textBox.insert(END, '\n')
textBox.insert(INSERT, "Unlock the door by introducing \
yourself with a \ngreeting and your name stored in a variable.")
textBox.insert(END, '\n \n')
e = Text(root, height=5, width=50)
e.pack()
e.focus_set()

stat = False
b = Button(root,text='okay',command=analyze_line)
b.pack(side='bottom')


root.mainloop()


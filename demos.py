import tkinter as Tk # Because everyone has tkinter

def demo1():
    print('This is demo 1!')

def demo2():
    print('This is demo 2!')

root = Tk.Tk()
Tk.Button(root, text='Demo 1', command=demo1).pack()
Tk.Button(root, text='Demo 2', command=demo2).pack()
root.mainloop()

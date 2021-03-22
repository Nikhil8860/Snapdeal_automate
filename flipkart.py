from tkinter import *

root = Tk()
root.geometry("655x333")


def hello():
    print("Hello tkinter Buttons")


def name():
    print("Name is harry")


frame1 = Frame(root, borderwidth=6, bg="grey", relief=SUNKEN)
frame1.pack(side=LEFT, anchor="nw")

image = PhotoImage(file=r"C:\Users\nikhils3\Desktop\flipkart-logo.png")

image_label = Label(frame1, image=image, bg="grey")
image_label.pack(side=LEFT, padx=23)

frame = Frame(root, borderwidth=6, bg="grey", relief=SUNKEN)
frame.pack(side=LEFT, anchor="ne")

b1 = Button(frame, fg="red", text="Print now", command=hello)
b1.pack(side=LEFT, padx=23)

b2 = Button(frame, fg="red", text="Tell me name now", command=name)
b2.pack(side=LEFT, padx=23)

b3 = Button(frame, fg="red", text="Print now")
b3.pack(side=LEFT, padx=23)

b4 = Button(frame, fg="red", text="Print now")
b4.pack(side=LEFT, padx=23)
root.mainloop()

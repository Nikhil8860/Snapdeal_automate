from tkinter import *  
root = Tk()
root.geometry("744x444")
root.minsize(300, 200)

window_name = Label(text="Order shipped App", fg="Green", font=("19"))

image = PhotoImage(file=r"C:\Users\nikhils3\Desktop\flipkart-logo.png")
image_label = Label(image=image, bg="blue")

image_label.pack()
window_name.pack()

frame_1 = Frame(root, bg="red")
frame_1.pack(side=LEFT)
data = Label(frame_1, text="hello", bg='red')
data.pack(side=TOP)
root.mainloop()

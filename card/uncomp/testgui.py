from tkinter import *
root = Tk()
c0 = Canvas(root, width = 400, height = 300)
c0.pack()
image_data = PhotoImage(file = "card.gif")
c0.create_image(200, 150, image = image_data)
root.mainloop()
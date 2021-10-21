# import Tkinter
import tkinter as tk


comPort = 'COM3'
baudRate = 9600

# create a widow
window = tk.Tk()

canvas=tk.Canvas(window,width=800,height=600)
canvas.grid(rowspan=8,columnspan=4)

# give the window a title
window.title("Design (E.) 344")

canvas.grid_columnconfigure(0, weight=1)
canvas.grid_rowconfigure(0, weight=1)


# creates label
connectionLabelText = "Enter your Baud rate and COM Port below, and click connect."
connectionLabel = tk.Label(text=connectionLabelText)
connectionLabel.grid(column=0, row=0, columnspan=2)




window.mainloop()
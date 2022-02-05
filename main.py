from pathlib import Path
import sys,os
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import *
from tkinter.filedialog import askopenfile
import generate as generate

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def start():

    window = Tk()
    window.geometry("729x499")
    window.configure(bg = "#FFFFFF")
    window.title("Predictive Process Mining using N_Grams")

    def openFile() :
        file = askopenfile(parent=window, mode='rb', title="Choose a file", filetypes=[("Pdf file", "*.xes")])
        if file :
            sys.argv.append(file.name)
            window.destroy()
            generate.start()

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 499,
        width = 729,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:openFile(),
        relief="flat"
    )
    button_1.place(
        x=457.0,
        y=388.0,
        width=189.0,
        height=64.0
    )

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        179.0,
        249.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        552.0,
        92.0,
        image=image_image_2
    )

    canvas.create_text(
        470.0,
        360.0,
        anchor="nw",
        text="Please choose a File",
        fill="#000000",
        font=("Poppins", 18 * -1)
    )

    canvas.create_text(
        455.0,
        190.0,
        anchor="nw",
        text="Smart Process Analytics",
        fill="#000000",
        font=("Poppins", 18 * -1)
    )

    canvas.create_text(
        380.0,
        216.0,
        anchor="nw",
        text="Predictive Analysis of Event Log with N_Grams",
        fill="#000000",
        font=("Poppins", 16 * -1)
    )

    canvas.create_text(
        510.0,
        236.0,
        anchor="nw",
        text="Group 4",
        fill="#000000",
        font=("Poppins", 16 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == "__main__":
    start()

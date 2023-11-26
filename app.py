import tkinter as tk
from tkinter import Label

from src.screen_main import ScreenMain
from config.consts import width,height
root = tk.Tk()

root.title("Editor de Pontos")
root.geometry("%dx%d" %(1280, 864))
root.resizable(False, False)
main = ScreenMain(root)

print("Iniciando!")

root.mainloop()

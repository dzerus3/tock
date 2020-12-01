import os
import json
import time
import tkinter as tk
from tkinter import ttk

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, args, kwargs)

        progress.pack(pady=10)

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.progress = tk.Progressbar(
            self, orient=tk.HORIZONTAL,
            length=100, mode="determinate"
        )

        progress.pack(pady = 10)

        startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = self.start()
        )
        startButton.pack(side="bottom")


    def start(self):
        pass

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = json.load(setupFile)

def main():
    gui = Gui()

if __name__ = "__main__":
    main()

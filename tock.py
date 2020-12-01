import os
import json
import time
import tkinter as tk
from tkinter import ttk

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, args, kwargs)

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.loadSetup()

        n = tk.StringVar()
        self.presets = ttk.Combobox(window, width = 27, textvariable = n)
        self.presets['values'] = self.setup.keys()
        self.presets.current(0)

        createProgress(self.setup[self.presets.current()])

        startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = self.start()
        )
        startButton.pack(side="bottom")

    def createProgress(self, preset):
        for timer in preset:
            label = Label(self, text = timer)
            label.pack()

            prog = tk.Progressbar(
                self, orient=tk.HORIZONTAL,
                length=100, mode="determinate"
            )

            prog.pack(pady = 10)

    def start(self):
        pass

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

def main():
    gui = Gui()

if __name__ = "__main__":
    main()

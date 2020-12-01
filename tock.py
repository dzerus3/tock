import os
import json
import time
import tkinter as tk
from tkinter import ttk

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")

        mainTab = MainFrame(self)
        mainTab.pack()
        # tabControl = ttk.Notebook(self)
        # tabControl.add(mainTab)

        self.mainloop()

class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.loadSetup()

        # Dropdown box to select preset
        n = tk.StringVar()
        self.presets = ttk.Combobox(self, width = 27, textvariable = n)

        presetNames = list(self.setup.keys())
        self.presets['values'] = presetNames
        self.presets.pack()

        currentPreset = self.setup[self.presets.get()] #FIXME

        self.createProgress(currentPreset) #FIXME

        startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = lambda: self.start(currentPreset)
        )
        startButton.pack(side="bottom")

    # Creates appropriate ammount of progress bars based on preset
    def createProgress(self, preset):
        bars = []
        for timer in preset:
            label = tk.Label(self, text = timer)
            label.pack()

            barLen = preset[timer]["duration"]
            prog = ttk.Progressbar(
                self,
                orient = tk.HORIZONTAL,
                length = barLen, #TODO: Set to 100?
                value = barLen, #TODO: Set to max or set to 0?
                mode="determinate"
            )
            prog.pack(pady = 10)

            bars.append(prog)
        return bars

    def start(self, preset, bars):
        while True:
            time.sleep(1)
            for bar in bars:
                bar["value"] -= 1
            root.update_idletasks()

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

def main():
    gui = Gui()

if __name__ == "__main__":
    main()

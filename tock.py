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
        self.presets["values"] = presetNames
        self.presets.pack()

        currentPreset = self.setup[self.presets["values"][0]] #FIXME

        # createProgress returns reference to interact with the progress bars
        bars = self.createProgress(currentPreset) #FIXME

        startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = lambda: self.start(bars)
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
                length = 100,
                maximum = barLen,
                value = 0,
                mode="determinate"
            )
            prog.pack(pady = 10)

            breakLen = preset[timer]["break"]
            bars.append([prog, barLen, breakLen])
        return bars

    def start(self, bars):
        breakBar = ttk.Progressbar(
            self,
            orient = tk.HORIZONTAL,
            length = 100,
            value = 100,
            mode="determinate"
        )
        breakBar.pack(pady = 10)

        while True:
            self.updateProgressbars(bars)
            highestFinished = self.checkForBreak(bars)

            if highestFinished > -1:
                duration = bars[highestFinished][2]
                if duration:
                    self.takeBreak(breakBar, duration)

    def takeBreak(self, breakBar, duration):
        breakStep = 100/duration
        while breakBar["value"] > 0:
            time.sleep(1)
            breakBar["value"] -= breakStep
            self.update_idletasks()
        breakBar["value"] = 100

    def updateProgressbars(self, bars):
        time.sleep(1)
        for bar in bars:
            # bar[0]["value"] += (100/bar[1])
            bar[0]["value"] += 1
        self.update_idletasks()

    def checkForBreak(self, bars):
        highestFinished = -1
        #TODO: Add option for longest break instead of last in order
        for index in range(len(bars)):
            timerValue = bars[index][0]["value"]
            if timerValue >= bars[index][1]:
                if highestFinished < index:
                    highestFinished = index
                    bars[index][0]["value"] = 0
        return highestFinished

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

def main():
    gui = Gui()

if __name__ == "__main__":
    main()

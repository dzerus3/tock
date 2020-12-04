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
        self.timerRunning = 0
        self.loadSetup()

        # Dropdown box to select preset
        n = tk.StringVar()
        self.presets = ttk.Combobox(self, width = 27, textvariable = n)

        presetNames = list(self.setup.keys())
        self.presets["values"] = presetNames
        self.presets.pack()

        currentPreset = self.setup[self.presets["values"][0]] #FIXME

        # createProgress returns reference to interact with the progress bars
        self.createProgress(currentPreset) #FIXME

        self.startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = self.start
        )
        self.startButton.pack(side="bottom")

    # Creates appropriate ammount of progress bars based on preset
    def createProgress(self, preset):
        self.bars = []
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
            self.bars.append([prog, barLen, breakLen])

    def start(self):
        self.timerRunning = 1
        self.startButton["command"] = lambda: self.stopTimers(breakBar)
        self.startButton["text"] = "Stop"

        breakBar = ttk.Progressbar(
            self,
            orient = tk.HORIZONTAL,
            length = 100,
            value = 100,
            mode="determinate"
        )
        breakBar.pack(pady = 10)
        self.after(1000, self.updateProgressbars, breakBar)

    def stopTimers(self, breakBar):
        self.timerRunning = 0
        self.startButton["command"] = self.start
        self.startButton["text"] = "Start"
        #FIXME Make breakbar pack_forget'ed, rather than destroyed.
        breakBar.destroy()

    def takeBreak(self, breakBar, duration):
        breakStep = 100/duration
        while breakBar["value"] > 0:
            #FIXME Make this use tk.after()
            time.sleep(1)
            breakBar["value"] -= breakStep
            self.update_idletasks()
        breakBar["value"] = 100

    def updateProgressbars(self, breakBar):
        for bar in self.bars:
            bar[0]["value"] += 1
        self.update_idletasks()
        highestFinished = self.checkForBreak()

        if highestFinished > -1:
            duration = self.bars[highestFinished][2]
            if duration:
                self.takeBreak(breakBar, duration)
        if self.timerRunning:
            self.after(1000, self.updateProgressbars, breakBar)

    def checkForBreak(self):
        highestFinished = -1
        #TODO: Add option for longest break instead of last in order
        for index in range(len(self.bars)):
            timerValue = self.bars[index][0]["value"]
            if timerValue >= self.bars[index][1]:
                if highestFinished < index:
                    highestFinished = index
                    self.bars[index][0]["value"] = 0
        return highestFinished

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

class Timer():
    def __init__(self, frame, duration=0, breakDuration=0, repeating=True, message = ""):
        self.frame = frame
        self.duration = duration
        self.breakDuration = breakDuration
        self.repeating = repeating
        self.message = message

        self.createProgressBar()

    def createProgressBar(self):
        self.label = tk.Label(self.frame, text = timer)
        self.label.pack()

        self.progressBar = ttk.Progressbar(
            self.frame,
            orient = tk.HORIZONTAL,
            length = 100,
            maximum = self.duration,
            value = 0,
            mode="determinate"
        )
        self.progressBar.pack(pady = 10)

    def hideProgressBar(self):
        self.progressBar.pack_forget()

    def incrementProgress(self):
        self.progressBar["value"] += 1

    def getDuration(self):
        return self.duration

    def getGetBreakDuration(self):
        return self.breakDuration

    def isRepeating(self):
        return self.isRepeating

    def getMessage(self):
        return self.message

    # So that it doesn't get left over if object gets destroyed
    def __del__(self):
        self.label.destroy()
        self.progressBar.destroy()

def main():
    gui = Gui()

if __name__ == "__main__":
    main()

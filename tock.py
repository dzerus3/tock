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
        self.preset = Preset(self, currentPreset) #FIXME
        self.preset.showPreset()

        self.startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = self.start
        )
        self.startButton.pack(side="bottom")

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
        self.preset.incrementTimers()
        self.update_idletasks()
        breakDuration = self.preset.getBreakDuration()

        if breakDuration > 0:
            self.takeBreak(breakBar, breakDuration)
        if self.timerRunning:
            self.after(1000, self.updateProgressbars, breakBar)

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

class Preset():
    def __init__(self, frame, jsonPreset):
        self.timers = []

        for timer in jsonPreset:
            self.createTimer(frame, timer, jsonPreset[timer])

    def createTimer(self, frame, name, timer):
        duration = timer.get("duration")
        breakDuration = timer.get("break")
        msg = timer.get("message")
        buff = Timer(frame, name, duration, breakDuration, True, msg)

        self.timers.append(buff)

    def incrementTimers(self):
        for timer in self.timers:
            timer.incrementProgress()

    def showPreset(self):
        #TODO: Add to a frame within parent, rather than directly to window
        for timer in self.timers:
            timer.showProgressBar()

    def hidePreset(self):
        for timer in self.timers:
            timer.hideProgressBar()

    def getBreakDuration(self):
        breakDuration = 0
        for timer in self.timers:
            # print("Timer has " + str(timer.getProgress()) + " progress and " + str(timer.getDuration()) + " duration.")
            if timer.getProgress() >= timer.getDuration():
                breakDuration = timer.getBreakDuration()
                timer.resetProgress()
        return breakDuration

class Timer():
    def __init__(self, frame, name="Untitled", duration=0, breakDuration=0, repeating=True, message = ""):
        self.name = name
        self.frame = frame
        self.duration = duration
        self.breakDuration = breakDuration
        self.repeating = repeating
        self.message = message

        self.createProgressBar()

    #TODO: Maybe pack progress bar and label into single mini frame?
    def createProgressBar(self):
        self.label = tk.Label(self.frame, text = self.name)

        self.progressBar = ttk.Progressbar(
            self.frame,
            orient = tk.HORIZONTAL,
            length = 100,
            maximum = self.duration,
            value = 0,
            mode="determinate"
        )

    def showProgressBar(self):
        self.label.pack()
        self.progressBar.pack(pady = 10)

    def hideProgressBar(self):
        self.label.pack_forget()
        self.progressBar.pack_forget()

    def incrementProgress(self):
        self.progressBar["value"] += 1

    def getProgress(self):
        return self.progressBar["value"]

    def resetProgress(self):
        self.progressBar["value"] = 0

    def getDuration(self):
        return self.duration

    def getBreakDuration(self):
        return self.breakDuration

    def isRepeating(self):
        return self.isRepeating

    def getMessage(self):
        return self.message

    # So that widgets don't get left over if object gets destroyed
    # def __del__(self): #TODO: is this necessary?
    #     self.label.destroy()
    #     self.progressBar.destroy()

def main():
    gui = Gui()

if __name__ == "__main__":
    main()

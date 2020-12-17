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
            command = self.startTimers
        )
        self.startButton.pack(side="bottom")

        self.breakBar = ttk.Progressbar(
            self,
            orient = tk.HORIZONTAL,
            length = 100,
            value = 100,
            mode="determinate"
        )
        self.breakBar.pack(pady = 10)

    def startTimers(self):
        self.timerRunning = 1
        self.startButton["command"] = self.stopTimers
        self.startButton["text"] = "Stop"

        self.breakBar.pack(pady = 10)
        self.after(1000, self.updateProgressbars, self.breakBar)

    def stopTimers(self):
        self.timerRunning = 0
        self.startButton["command"] = self.startTimers
        self.startButton["text"] = "Start"
        self.breakBar.pack_forget()

    def takeBreak(self, breakBar, duration):
        #TODO: Make break bar run on same loop as other timers
        breakStep = 100/duration
        self.after(1000, self.incrementBreakBar, breakBar, breakStep)
        breakBar["value"] = 100

    def incrementBreakBar(self, breakBar, breakStep):
        if breakBar["value"] > 0:
            breakBar["value"] -= breakStep
            self.update_idletasks()
            self.after(1000, self.incrementBreakBar, breakBar, breakStep)
        else:
            self.preset.pauseTimers()

    def updateProgressbars(self, breakBar):
        self.preset.incrementTimers()
        self.update_idletasks()
        breakDuration = self.preset.getBreakDuration()

        if breakDuration > 0:
            self.preset.pauseTimers()
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
            if not timer.getPaused():
                timer.incrementProgress()

    def showPreset(self):
        #TODO: Add to a frame within parent, rather than directly to window
        for timer in self.timers:
            timer.showProgressBar()

    def hidePreset(self):
        for timer in self.timers:
            timer.hideProgressBar()

    def pauseTimers(self):
        for timer in self.timers:
            timer.togglePause()

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
        self.paused = False
        self.increment = 1000 #TODO

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

    def togglePause(self):
        self.paused = not self.paused

    def incrementProgress(self):
        self.progressBar["value"] += 1

    def resetProgress(self):
        self.progressBar["value"] = 0

    def getProgress(self):
        return self.progressBar["value"]

    def getDuration(self):
        return self.duration

    def getBreakDuration(self):
        return self.breakDuration

    def getRepeating(self):
        return self.repeating

    def getMessage(self):
        return self.message

    def getPaused(self):
        return self.paused

    # So that widgets don't get left over if object gets destroyed
    # def __del__(self): #TODO: is this necessary?
    #     self.label.destroy()
    #     self.progressBar.destroy()

def main():
    gui = Gui()

if __name__ == "__main__":
    main()

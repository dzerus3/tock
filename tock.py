import os
import json
import time
import tkinter as tk
from tkinter import ttk

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")

        mainTab = MainFrame()
        mainTab.pack()
        # tabControl = ttk.Notebook(self)
        # tabControl.add(mainTab)

        self.mainloop()

class MainFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.loadSetup()

        # Dropdown box to select preset
        n = tk.StringVar()
        self.presets = ttk.Combobox(self, width = 27, textvariable = n)

        presetNames = list(self.setup.keys())
        self.presets["values"] = presetNames
        self.presets.pack()

        currentPreset = self.setup[self.presets["values"][0]] #FIXME

        self.timerFrame = TimerFrame(self, currentPreset)

        # createProgress returns reference to interact with the progress bars
        self.timerFrame.pack()

        self.startButton = tk.Button(
            self,
            text="Start",
            width = 10,
            command = self.startTimers
        )
        self.startButton.pack(side="bottom")

    def startTimers(self):
        self.timerFrame.startTimers()
        self.startButton["command"] = self.stopTimers
        self.startButton["text"] = "Stop"

        self.after(1000, self.timerFrame.updateProgressbars)

    def stopTimers(self):
        self.timerFrame.stopTimers()
        self.startButton["command"] = self.startTimers
        self.startButton["text"] = "Start"

    def loadSetup(self):
        with open("setup.json", "r") as setupFile:
            self.setup = dict(json.load(setupFile))

class TimerFrame(tk.Frame):
    def __init__(self, parent, jsonPreset):
        tk.Frame.__init__(self, parent)

        self.preset = Preset(self, jsonPreset)
        self.preset.showPreset()
        self.timerRunning = False

        if self.preset.hasBreaks():
            self.breakBar = Timer(self, "Break", duration=100, repeating=False)

    def takeBreak(self, duration):
        #TODO: Make break bar run on same loop as other timers
        self.breakBar.setDuration(duration)
        self.after(1000, self.incrementBreakBar)
        self.breakBar.resetProgress()

    def incrementBreakBar(self):
        if self.breakBar.getProgress() < self.breakBar.getDuration():
            self.breakBar.incrementProgress()
            self.update_idletasks()
            self.after(1000, self.incrementBreakBar)
        else:
            self.preset.pauseTimers()

    def updateProgressbars(self):
        self.preset.incrementTimers()
        self.update_idletasks()
        breakDuration = self.preset.getBreakDuration()

        if breakDuration > 0:
            self.preset.pauseTimers()
            self.takeBreak(breakDuration)
        if self.timerRunning:
            self.after(1000, self.updateProgressbars)

    def startTimers(self):
        self.timerRunning = True
        self.breakBar.showProgressBar() #TODO Make breakbar optional

    def stopTimers(self):
        self.timerRunning = False
        self.breakBar.hideProgressBar()

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

    def hasBreaks(self):
        for timer in self.timers:
            if timer.getBreakDuration() > 0:
                return True
        return False

    # Finds timer with longest duration and returns that duration
    def getBreakDuration(self):
        breakDuration = 0
        for timer in self.timers:
            if timer.getProgress() >= timer.getDuration():
                breakDuration = timer.getBreakDuration()
                timer.resetProgress()
        return breakDuration

class Timer():
    def __init__(self, frame, name="Untitled", duration=0, breakDuration=0, repeating=True, message = ""):
        self.frame = frame
        self.name = name
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

    def setDuration(self, duration):
        self.duration = duration
        self.progressBar["maximum"] = self.duration

    def incrementProgress(self):
        self.progressBar["value"] += 1

    def setProgress(self, value):
        self.progressBar["value"] = value

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

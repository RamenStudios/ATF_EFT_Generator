#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.tix import *
import wsq
import os
from PIL import ImageTk, Image

FINGERPRINT_KEYS =  {
                        'Right Thumb': '1',
                        'Right Index': '2',
                        'Right Middle': '3',
                        'Right Ring': '4',
                        'Right Little': '5',
                        'Left Thumb': '6',
                        'Left Index': '7',
                        'Left Middle': '8',
                        'Left Ring': '9',
                        'Left Little': '10',
                        'Plain Right Thumb': '11',
                        'Plain Left Thumb': '12',
                        'Right Four': '13',
                        'Left Four': '14'
                    }

class PrintMatcherFrame:
    def __init__(self, master, row, col, choice, height=175, width=250, rowspan=1, colspan=1):
            # accounting for some of the weird parsing, lazy style
        if choice == 10:
            choice = 13
        elif choice == 11:
            choice = 12
        elif choice == 12:
            choice = 11
        elif choice == 13:
            choice = 10
        self.frame = ttk.Frame(master)
        self.frame.configure(height=height, relief="sunken", width=width)
        self.imglabel = ttk.Label(self.frame)
        self.imglabel.configure(text='No image found!')
        self.imglabel.grid(column=0, row=0)
        self.printType = ttk.Combobox(self.frame, state="readonly", values=[x for x in FINGERPRINT_KEYS.keys()])
        self.printType.grid(column=0, row=1)
        self.printType.current(choice)
        self.frame.grid(column=col, columnspan=colspan, padx=2, pady=2, ipadx=2, ipady=2, row=row, rowspan=rowspan)
        self.frame.grid_propagate(0)
        self.frame.grid_anchor("s")
        self.hasImg = False
        self.imgData = None
        self.default = choice

    def get_type(self):
        return self.printType.get()
    
    def display_print(self, imgData):
        print(imgData)
        self.imgData = imgData
        self.hasImg = True
        imgpath = imgData['raw']
        tempimg = (Image.open(imgpath))
        if self.default == 12 or self.default == 13:
            tempimg = tempimg.resize((int(tempimg.width/6),int(tempimg.height/6)))
        else:
            tempimg = tempimg.resize((int(tempimg.width/4),int(tempimg.height/4)))
        tempimg = ImageTk.PhotoImage(tempimg)
        self.imglabel.image = tempimg
        self.imglabel.configure(image=tempimg)

class ImportPickerApp:
    def __init__(self, master, parentContainer):
        # build ui
        self.parent = parentContainer
        self.main = tk.Toplevel(master)
        self.main.configure(height=200, width=200)
        frame1 = ttk.Frame(self.main)
        frame1.configure(height=720, width=1280)
        # create all the little windows for fingerprints. detail not needed here
        self.printWindows = []
        defaultChoice = 0 # allows us to (hopefully) automate this and minimize user input
        for i in range(3):
            for x in range(5):
                if i == 2 and x == 4:
                    break
                self.printWindows.append(PrintMatcherFrame(frame1, i, x, defaultChoice))
                defaultChoice += 1
        # buttons to do things. and stuff
        # why are you reading these anyways. sus ass mf
        buttonframe = ttk.Frame(master)
        buttonframe.configure(height=175, width=250)
        button1 = ttk.Button(frame1)
        button1.configure(text='Finish Import', command=self.finalize)
        button1.grid(column=4, row=2)
        button2 = ttk.Button(frame1)
        button2.configure(text='Cancel Import', command=self.main.destroy)
        button2.grid(column=4, row=3)
        # finish it. no fancy shit needed im not making this resizable 
        frame1.grid(column=0, ipadx=3, ipady=3, row=0, sticky="nw")
        frame1.grid_propagate(0)
        frame1.grid_anchor("center")
        # Main widget
        self.mainwindow = self.main

    # brings the fingerprints into the initial picker window
    def import_prints(self, fingerprints):
        i = 1
        print(fingerprints.keys())
        # iterate through the fingerprint images, which are numbered
        # if a number is missing, just skip it
        for x in self.printWindows:
            temp = fingerprints[f'{i}']
            x.display_print(temp)
            i += 1

    # passes the confirmed prints to root window
    def finalize(self):
        # verify that no two prints have the same designation
        tempkey = [x.printType.get() for x in self.printWindows]
        print(tempkey)
        if len(tempkey) != len(set(tempkey)):
            tk.messagebox.showwarning(title="INVALID DESIGNATIONS", message="No two fingerprints can have the same designation! Even if the prints are absent (i.e. missing fingers), give them a designation so they can be properly marked.")
            return
        # once validity is verified, match prints to root window counterparts by name
        for x in self.printWindows:
            tempkey = FINGERPRINT_KEYS[x.printType.get()]
            self.parent.FINGERPRINT_KEYS[tempkey].fingerprint = x.imgData
            tempimg = (Image.open(x.imgData['raw']))
            dims = self.parent.FINGERPRINT_KEYS[tempkey].resizer(tempimg.width, tempimg.height)
            tempimg = tempimg.resize((dims[0],dims[1]))
            tempimg = ImageTk.PhotoImage(tempimg)
            self.parent.FINGERPRINT_KEYS[tempkey].imglabel.image = tempimg
            self.parent.FINGERPRINT_KEYS[tempkey].imglabel.configure(image=tempimg)
        self.main.destroy()

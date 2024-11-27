#!/usr/bin/python3
import tkinter.filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk
import binascii
import base64
import math
import wsq
import os
from pypdf import PdfReader
from PIL import Image, ImageFile
from gui_utils import *

# main directory for navigating to things we need
MAINDIR = '/'.join((f'{os.getcwd()}'.split('\\'))[:-1])

INPUT_EXTS =        [
                        ('PNG', '*.png'),
                        ('JPG', '*.jpg')
                    ]

# these allow us to iterate easier. i am lazy.
nameToInt = {
                'Right Thumb': '1',
                'Right Index': '2',
                'Right Middle': '3',
                'Right Ring': '4',
                'Right Little': '5',
                'Plain Right Thumb': '11',
                'Right Four': '13',
                'Left Thumb': '6',
                'Left Index': '7',
                'Left Middle': '8',
                'Left Ring': '9',
                'Left Little': '10',
                'Plain Left Thumb': '12',
                'Left Four': '14'
            }

# container for fingerprint record UI
# makes GUI code more manageable
class FingerprintViewer:
    def __init__(self, parent=None, fname=None, row=0, col=0, fingerprint=None):
        columnspan = 1
        rowspan = 1
        self.width = 200
        height = 200
        if "Four" in fname:
            columnspan = 3
            self.width = 620
            height = 200
        self.fname = fname
        self.viewer = ttk.Labelframe(parent, name=f"{(fname.replace(' ', '_')).lower()}")
        self.viewer.configure(height=height, text=f'{fname}', width=self.width)
        self.imglabel = ttk.Label(self.viewer)
        self.imglabel.configure(text='No Image Available!')
        self.imglabel.grid( column=0, columnspan=2, padx=2, pady=2, row=0, rowspan=3, sticky="nsew" )
        self.clearer = ttk.Button(self.viewer, command=self.clearimg)
        self.clearer.configure(text='Clear Image')
        self.clearer.grid(column=2, row=3, padx=3)
        self.clearer.grid_anchor("sw")
        self.loader = ttk.Button(self.viewer, command=self.importer)
        self.loader.configure(text='Load New')
        self.loader.grid(column=3, row=3)
        self.loader.grid_anchor("sw")
        self.scannable = ttk.Combobox(self.viewer, state="readonly")
        self.scannable.configure(values='Scannable Amputated Bandaged/Other')
        self.scannable.grid(column=0, row=3)
        self.scannable.grid_anchor("sw")
        self.scannable.current(0)
        self.viewer.grid(column=col, ipadx=3, columnspan=columnspan, row=row, rowspan=rowspan, sticky="nsew")
        self.viewer.grid_anchor("sw")
        self.fingerprint = fingerprint
        # specify fingerprint viewer grid
        for i in range(0,2):
            tk.Grid.rowconfigure(self.viewer, i, weight=1)
            tk.Grid.columnconfigure(self.viewer, i, weight=1)
        tk.Grid.rowconfigure(self.viewer, 2, weight=1)
        
    # ez scannability return for amputation info
    def scannability(self):
        print(f'{self.fname} : {self.scannable.get()}')
        return self.scannable.get()
    
    # in case an image was placed accidentally
    def clearimg(self):
        self.imglabel.image = None
        self.imglabel.configure(image=None)

    # returns dimensions for resizing image
    def resizer(self, w, h):
        factor = w if w > h else h
        dividend = math.ceil(factor/self.width)
        return [(int(w/dividend)), (int(h/dividend))]

    # for the manual 
    def importer(self):
        # import the actual image file, either jpg or png
        file = fd.askopenfile(mode='r', filetypes=INPUT_EXTS)
        if file:
            try:
                print(f'FILE: {file}')
                filepath = os.path.abspath(file.name)
            except:
                tk.messagebox.showwarning(title="INVALID FILEPATH", message="The provided file does not exist, or is invalid! :(\nIf you pressed cancel, ignore this message!")
        else:
            tk.messagebox.showwarning(title="INVALID FILEPATH", message="The provided file does not exist, or is invalid! :(\nIf you pressed cancel, ignore this message!")
            return
        print(self.fname)
        self.fingerprint = image_importer(Image.open(f'{filepath}', mode='r'), MAINDIR, f'{nameToInt[self.fname]}.jpg', None, filepath)
        # display the shit !
        tempimg = (Image.open(self.fingerprint['raw']))
        dims = self.resizer(tempimg.width, tempimg.height)
        tempimg = tempimg.resize((dims[0],dims[1]))
        tempimg = ImageTk.PhotoImage(tempimg)
        self.imglabel.image = tempimg
        self.imglabel.configure(image=tempimg)
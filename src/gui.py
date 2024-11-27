#!/usr/bin/python3
import tkinter.filedialog as fd
import tkinter as tk
#import tkinter.ttk as ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import wsq
import os
import re
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import ImageTk, Image
from gui_containers import *
from import_picker import *
from serializer import *
from gui_utils import *

# agency's identifier
# original client for this software was diamondback shooting sports
ORI = 'DBACKSHTG'

# main directory for navigating to things we need
MAINDIR = '/'.join((f'{os.getcwd()}'.split('\\'))[:-1])

# these allow us to iterate easier. i am lazy.
RIGHT_HAND =        {
                        'Right Thumb': '1',
                        'Right Index': '2',
                        'Right Middle': '3',
                        'Right Ring': '4',
                        'Right Little': '5',
                        'Plain Right Thumb': '11',
                        'Right Four': '13'
                    }
LEFT_HAND =         {
                        'Left Thumb': '6',
                        'Left Index': '7',
                        'Left Middle': '8',
                        'Left Ring': '9',
                        'Left Little': '10',
                        'Plain Left Thumb': '12',
                        'Left Four': '14'
                    }

# unavailability codes
FINGER_CODES =      {
                        'Amputated': 'XX',
                        'Bandaged/Other': 'UP'
                    }

TRANSACTION_TYPES = {
                        "Criminal Tenprint Submission (Answer Required)": "CAR",
                        "Criminal Tenprint Submission (No Answer Necessary)": "CNA",
                        "Criminal Fingerprint Direct Route": "CPDR",
                        "Criminal Fingerprint Processing Non-Urgent": "CPNU",
                        "Departmental Order Channeling Electronic": "DOCE",
                        "Electronic In/Manual Out User Fee Submission": "EMUF",
                        "Federal Applicant (No Charge)": "FANC",
                        "Federal Applicant User Fee": "FAUF",
                        "Foreign Information Direct Route": "FIDR",
                        "Federal No Charge Direct Route": "FNDR",
                        "Non-Federal No Charge Direct Route": "NNDR",
                        "Non-Federal User Fee Expedite": "NFUE",
                        "Non-Federal Applicant User Fee": "NFUF",
                        "Miscellaneous Applicant Civil": "MAP", 
                        "Known Deceased": "DEK", 
                        "Unknown Deceased": "DEU", 
                        "Missing Person": "MPR",
                        "Amnesia Victim": "AMN",
                        "Latent Fingerprint Image Submission": "LFS",
                        "Rapid Fingerprint Identification Search": "RPIS",
                        "Electronic Fingerprint Disposition Submission": "FDSP"
                    }
EYE_COLORS =        {
                        "Black": "BLK",
                        "Blue": "BLU",
                        "Brown": "BRO",
                        "Gray": "GRY",
                        "Green": "GRN",
                        "Hazel": "HAZ",
                        "Maroon": "MAR",
                        "Multicolored": "MUL",
                        "Pink": "PNK",
                        "Unknown": "XXX"
                    }
HAIR_COLORS =       {
                        "Bald": "BAL",
                        "Black": "BLK",
                        "Blond/Strawberry": "BLN",
                        "Blue": "BLU",
                        "Brown": "BRO",
                        "Gray": "GRY",
                        "Green": "GRN",
                        "Orange": "ONG",
                        "Pink": "PNK",
                        "Purple": "PLE",
                        "Red/Auburn": "RED",
                        "Sandy": "SDY",
                        "Unknown": "XXX",
                        "White": "WHI"
                    }
RACES =             {
                        "Asian or Pacific Islander": "A",
                        "Black": "B",
                        "White or Hispanic": "W",
                        "Native American": "I",
                        "Indeterminable/Unknown": "U"
                    }
INPUT_EXTS =        [
                        ('PDF', '*.pdf')
                    ]
OUTPUT_EXTS =       [
                        ('EFT', '*.eft'),
                        ('All Files', '*')
                    ]

# help files will be in src folder for ease of access
HELP_FILES =        {
                        'About':'README.md',
                        'EBTS':'EBTS v11.0_Final_508.pdf',
                        'Manual':'EFT MANUAL.pdf',
                        'Nations':'nation_codes.txt'
                    }

class EFTGuiApp:
    def __init__(self, master=None):
        print(MAINDIR)
        # get today's date
        date = date_getter()
        # blank output holder
        self.output = NISTFile()
        # blank dict to allow us to store fingerprint info in order
        self.FINGERPRINT_KEYS = {}
        # blank dict to allow us to store section 1 data
        self.SECTION_ONE =  {
                                '1.01:': None,
                                '1.02:': None,
                                '1.03:': None,
                                '1.04:': None,
                                '1.05:': None,
                                '1.06:': None,
                                '1.07:': None,
                                '1.08:': None,
                                '1.09:': None,
                                '1.11:': None,
                                '1.12:': None
                            }
        # blank dict to allow us to store section 2 data
        self.SECTION_TWO =  {
                                '2.001:': None,
                                '2.002:': None,
                                '2.005:': None,
                                '2.016:': None,
                                '2.018:': None,
                                '2.020:': None,
                                '2.021:': None,
                                '2.022:': None,
                                '2.027:': None,
                                '2.029:': None,
                                '2.031:': None,
                                '2.032:': None,
                                '2.037:': None,
                                '2.038:': None,
                                '2.041:': None,
                                '2.067:': None,
                                '2.073:': None,
                                '2.084:': None
                            }
        
        # main window
        self.main = tk.Tk() if master is None else tk.Toplevel(master)
        self.main.configure(height=1080, takefocus=True, width=1920)
        self.main.geometry("1280x720")
        self.main.resizable(True, True)
        self.main.title("EFT Generator")
        panedwindow3 = ttk.Panedwindow(self.main, orient="horizontal")
        panedwindow3.configure(height=1080, width=1920)
        panedwindow2 = ttk.Panedwindow(panedwindow3, orient="horizontal")
        panedwindow2.configure(height=1080, width=1920)

        # the toplevel menu
        menubar = tk.Menu(self.main)
        filemenu = tk.Menu(menubar, tearoff=0) # menu with file options
        filemenu.add_command(label="Open", command=self.importer)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.main.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        exportmenu = tk.Menu(menubar, tearoff=0) # menu with finalization options
        exportmenu.add_command(label="Export EFT", command=self.exporter)
        exportmenu.add_command(label="Verify", command=self.save)
        menubar.add_cascade(label="Finalize", menu=exportmenu)
        helpmenu = tk.Menu(menubar, tearoff=0) # menu with help options
        helpmenu.add_command(label="Manual", command=self.open_help_docs)
        helpmenu.add_command(label="EBTS Docs", command=self.open_ebts_docs)
        helpmenu.add_command(label="Nation Codes", command=self.open_nations)
        helpmenu.add_command(label="About", command=self.open_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.main.config(menu=menubar)

        # specify main window grid
        tk.Grid.rowconfigure(self.main, 0, weight=1)
        for i in range(0,6):
            tk.Grid.columnconfigure(self.main, i, weight=1)
        
        ############### LABELS AND ENTRIES FOR SECTION 1 ################
        self.sectionOne = ttk.Labelframe(panedwindow2, name="sectionone")
        self.sectionOne.configure(height=200, text='Section 1', width=200)
        # label/entry for 1.02 
        label1 = ttk.Label(self.sectionOne)
        label1.configure(text='1.02 (VER) ')
        label1.grid(column=0, row=0, sticky="nsew")
        ToolTip(label1, text="Version Number")
        self.ver = ttk.Entry(self.sectionOne, name="ver")
        self.ver.configure(justify="left")
        _text_ = '0400'
        self.ver.delete("0", "end")
        self.ver.insert("0", _text_)
        self.ver.grid(column=1, row=0, sticky="nsew")
        # labels/entries for 1.03
        label2 = ttk.Label(self.sectionOne) # frc
        label2.configure(text='1.03:a (FRC)')
        label2.grid(column=0, row=1, sticky="nsew")
        ToolTip(label2, text="First Record Category Code")
        self.frc = ttk.Entry(self.sectionOne, name="frc")
        _text_ = '1'
        self.frc.delete("0", "end")
        self.frc.insert("0", _text_)
        label3 = ttk.Label(self.sectionOne) # crc
        label3.configure(text='1.03:b (CRC)')
        label3.grid(column=0, row=2, sticky="nsew")
        ToolTip(label3, text="Content Record Count")
        self.crc = ttk.Entry(self.sectionOne, name="crc")
        _text_ = '15'
        self.crc.delete("0", "end")
        self.crc.insert("0", _text_)
        self.crc.grid(column=1, row=2, sticky="nsew")
        label4 = ttk.Label(self.sectionOne) # rec
        label4.configure(text='1.03:a (REC)')
        label4.grid(column=0, row=3, sticky="nsew")
        ToolTip(label4, text="Record Category Code")
        self.frc.grid(column=1, row=1, sticky="nsew")
        self.rec = ttk.Entry(self.sectionOne, name="rec")
        _text_ = '2'
        self.rec.delete("0", "end")
        self.rec.insert("0", _text_)
        self.rec.grid(column=1, row=3, sticky="nsew")
        label5 = ttk.Label(self.sectionOne) # idc
        label5.configure(text='1.03:b (IDC)') 
        label5.grid(column=0, row=4, sticky="nsew")
        ToolTip(label5, text="Information Designation Code")
        self.idc1 = ttk.Entry(self.sectionOne, name="idc1")
        _text_ = '00'
        self.idc1.delete("0", "end")
        self.idc1.insert("0", _text_)
        self.idc1.grid(column=1, row=4, sticky="nsew")
        # label/entry for 1.04
        label6 = ttk.Label(self.sectionOne)
        label6.configure(text='1.04 (TOT)')
        label6.grid(column=0, row=5, sticky="nsew")
        ToolTip(label6, text="Type of Transaction\nDefault is FAUF")
        self.tot = AutocompleteCombobox(self.sectionOne, completevalues=[x for x in TRANSACTION_TYPES.keys()])
        self.tot.current(9)
        self.tot.grid(column=1, row=5, sticky="nsew")
        # label/entry for 1.05
        label7 = ttk.Label(self.sectionOne)
        label7.configure(text='1.05 (DAT)')
        label7.grid(column=0, row=6, sticky="nsew")
        ToolTip(label7, text="Date of Transaction\nyyyy/mm/dd")
        self.dat = ttk.Entry(self.sectionOne, name="dat")
        _text_ = date
        self.dat.delete("0", "end")
        self.dat.insert("0", _text_)
        self.dat.grid(column=1, row=6, sticky="nsew")
        # label/entry for 1.06
        label8 = ttk.Label(self.sectionOne)
        label8.configure(text='1.06 (PRY)')
        label8.grid(column=0, row=7, sticky="nsew")
        ToolTip(label8, text="Priority\nDon't change unless you know what you're doing.")
        self.pry = ttk.Entry(self.sectionOne, name="pry")
        self.pry.grid(column=1, row=7, sticky="nsew")
        _text_ = '2'
        self.pry.delete("0", "end")
        self.pry.insert("0", _text_)
        # label/entry for 1.07
        label9 = ttk.Label(self.sectionOne)
        label9.configure(text='1.07 (DAI)')
        label9.grid(column=0, row=8, sticky="nsew")
        ToolTip(label9, text="Destination Agency Identifier")
        self.dai = ttk.Entry(self.sectionOne, name="dai")
        self.dai.grid(column=1, row=8, sticky="nsew")
        _text_ = 'WVIAFIS0Z'
        self.dai.delete("0", "end")
        self.dai.insert("0", _text_)
        # label/entry for 1.08
        label10 = ttk.Label(self.sectionOne)
        label10.configure(text='1.08 (ORI)')
        label10.grid(column=0, row=9, sticky="nsew")
        ToolTip(label10, text="Originating Agency Identifier")
        self.ori = ttk.Entry(self.sectionOne, name="ori")
        self.ori.grid(column=1, row=9, sticky="nsew")
        _text_ = ORI
        self.ori.delete("0", "end")
        self.ori.insert("0", _text_)
        # label/entry for 1.09
        label11 = ttk.Label(self.sectionOne)
        label11.configure(text='1.09 (TCN)')
        label11.grid(column=0, row=10, sticky="nsew")
        ToolTip(label11, text="Transaction Control Number")
        self.tcn = ttk.Entry(self.sectionOne, name="tcn")
        self.tcn.grid(column=1, row=10, sticky="nsew")
        # label/entry for 1.11
        label12 = ttk.Label(self.sectionOne)
        label12.configure(text='1.11 (NSR)')
        label12.grid(column=0, row=11, sticky="nsew")
        ToolTip(label12, text="Native Scanning Resolution\nDon't change unless you know what you're doing.")
        self.nsr = ttk.Entry(self.sectionOne, name="nsr")
        self.nsr.grid(column=1, row=11, sticky="nsew")
        _text_ = '19.69'
        self.nsr.delete("0", "end")
        self.nsr.insert("0", _text_)
        # label/entry for 1.12
        label13 = ttk.Label(self.sectionOne)
        label13.configure(text='1.12 (NTR)')
        label13.grid(column=0, row=12, sticky="nsew")
        ToolTip(label13, text="Nominal Resolution\nDon't change unless you know what you're doing.")
        self.ntr = ttk.Entry(self.sectionOne, name="ntr")
        self.ntr.grid(column=1, row=12, sticky="nsew")
        _text_ = '19.69'
        self.ntr.delete("0", "end")
        self.ntr.insert("0", _text_)
        # button to generate tcn based on input
        self.tcnGeneratorButton = ttk.Button(self.sectionOne, name="tcngeneratorbutton")
        self.tcnGeneratorButton.configure(text='Generate TCN')
        self.tcnGeneratorButton.grid(column=1, padx=5, pady=10, row=13, sticky="nsew")
        self.tcnGeneratorButton.configure(command=self.tcn_getter)
        # button to update information in data containers
        self.sectionOneUpdaterButton = ttk.Button(self.sectionOne, name="sectiononeupdaterbutton")
        self.sectionOneUpdaterButton.configure(text='Save Changes')
        self.sectionOneUpdaterButton.grid(column=1, padx=5, pady=10, row=14, sticky="nsew")
        self.sectionOneUpdaterButton.configure(command=self.section_one_updater)
        # layout info for section one container
        self.sectionOne.grid(
            column=0,
            columnspan=2,
            row=0,
            rowspan=21,
            sticky="nsew")
        self.sectionOne.grid_anchor("nw")
        panedwindow2.add(self.sectionOne, weight="1")
        # specify section one grid
        for i in range(0,21):
            tk.Grid.rowconfigure(self.sectionOne, i, weight=1)
        for i in range(0,2):
            tk.Grid.columnconfigure(self.sectionOne, i, weight=1)
        
        ############### LABELS AND ENTRIES FOR SECTION 2 ################
        self.sectionTwo = ttk.Labelframe(panedwindow2, name="sectiontwo")
        self.sectionTwo.configure(height=200, text='Section 2', width=200)
        # label/entry for 2.002
        label16 = ttk.Label(self.sectionTwo)
        label16.configure(text='2.002 (IDC)')
        label16.grid(column=0, row=0, sticky="nsew")
        ToolTip(label16, text="Information Designation Character")
        self.idc2 = ttk.Entry(self.sectionTwo, name="idc2")
        _text_ = '00'
        self.idc2.delete("0", "end")
        self.idc2.insert("0", _text_)
        self.idc2.grid(column=1, row=0, sticky="nsew")
        # label/entry for 2.005
        label30 = ttk.Label(self.sectionTwo)
        label30.configure(text='2.005 (RET)')
        label30.grid(column=0, row=1, sticky="nsew")
        ToolTip(label30, text="Retention Code")
        self.ret = ttk.Entry(self.sectionTwo, name="ret")
        _text_ = 'Y'
        self.ret.delete("0", "end")
        self.ret.insert("0", _text_)
        self.ret.grid(column=1, row=1, sticky="nsew")
        # label/entry for 2.016
        label31 = ttk.Label(self.sectionTwo)
        label31.configure(text='2.016 (SOC)')
        label31.grid(column=0, row=2, sticky="nsew")
        ToolTip(label31, text="Social Security Account Number")
        self.soc = ttk.Entry(self.sectionTwo, name="soc")
        self.soc.grid(column=1, row=2, sticky="nsew")
        # label/entry for 2.018
        label32 = ttk.Label(self.sectionTwo)
        label32.configure(text='2.018 (NAM)')
        label32.grid(column=0, row=3, sticky="nsew")
        ToolTip(label32, text="Name (Last,First)")
        self.nam = ttk.Entry(self.sectionTwo, name="nam")
        self.nam.grid(column=1, row=3, sticky="nsew")
        # label/entry for 2.020
        label33 = ttk.Label(self.sectionTwo)
        label33.configure(text='2.020 (POB)')
        label33.grid(column=0, row=4, sticky="nsew")
        ToolTip(label33, text="Place of Birth\nIf not USA, look up country designation\nOtherwise, use state acronym")
        self.pob = ttk.Entry(self.sectionTwo, name="pob")
        self.pob.grid(column=1, row=4, sticky="nsew")
        _text_ = 'AZ'
        self.pob.delete("0", "end")
        self.pob.insert("0", _text_)
        # label/entry for 2.021
        label34 = ttk.Label(self.sectionTwo)
        label34.configure(text='2.021 (CTZ)')
        label34.grid(column=0, row=5, sticky="nsew")
        ToolTip(label34, text="Country of Citizenship")
        self.ctz = ttk.Entry(self.sectionTwo, name="ctz")
        self.ctz.grid(column=1, row=5, sticky="nsew")
        _text_ = 'US'
        self.ctz.delete("0", "end")
        self.ctz.insert("0", _text_)
        # label/entry for 2.022
        label35 = ttk.Label(self.sectionTwo)
        label35.configure(text='2.022 (DOB)')
        label35.grid(column=0, row=6, sticky="nsew")
        ToolTip(label35, text="Date of Birth")
        self.dob = ttk.Entry(self.sectionTwo, name="dob")
        _text_ = 'yyyy/mm/dd'
        self.dob.delete("0", "end")
        self.dob.insert("0", _text_)
        self.dob.grid(column=1, row=6, sticky="nsew")
        # label/entry for 2.024
        label36 = ttk.Label(self.sectionTwo)
        label36.configure(text='2.024 (SEX)')
        label36.grid(column=0, row=7, sticky="nsew")
        ToolTip(label36, text="Sex.\nCurrently only M/F for federal purposes")
        self.sex = ttk.Combobox(self.sectionTwo, state="readonly", name="sex", values=['M','F'])
        self.sex.grid(column=1, row=7, sticky="nsew")
        self.sex.current(0)
        # label/entry for 2.025
        label37 = ttk.Label(self.sectionTwo)
        label37.configure(text='2.025 (RAC)')
        label37.grid(column=0, row=8, sticky="nsew")
        ToolTip(label37, text="Race")
        self.rac = ttk.Combobox(self.sectionTwo, name="rac", state="readonly", values=[x for x in RACES.keys()])
        self.rac.grid(column=1, row=8, sticky="nsew")
        # label/entry for 2.027
        label38 = ttk.Label(self.sectionTwo)
        label38.configure(text='2.027 (HGT)')
        label38.grid(column=0, row=9, sticky="nsew")
        ToolTip(label38, text="Height")
        self.hgt = ttk.Entry(self.sectionTwo, name="hgt")
        self.hgt.grid(column=1, row=9, sticky="nsew")
        # label/entry for 2.029
        label39 = ttk.Label(self.sectionTwo)
        label39.configure(text='2.029 (WGT)')
        label39.grid(column=0, row=10, sticky="nsew")
        ToolTip(label39, text="Weight")
        self.wgt = ttk.Entry(self.sectionTwo, name="wgt")
        self.wgt.grid(column=1, row=10, sticky="nsew")
        # label/entry for 2.031
        label40 = ttk.Label(self.sectionTwo)
        label40.configure(text='2.031 (EYE)')
        label40.grid(column=0, row=11, sticky="nsew")
        ToolTip(label40, text="Eye Color")
        self.eye = ttk.Combobox(self.sectionTwo, name="eye", state="readonly", values=[x for x in EYE_COLORS.keys()])
        self.eye.grid(column=1, row=11, sticky="nsew")
        # label/entry for 2.032
        label41 = ttk.Label(self.sectionTwo)
        label41.configure(text='2.032 (HAI)')
        label41.grid(column=0, row=12, sticky="nsew")
        self.hai = ttk.Combobox(self.sectionTwo, name="hai", state="readonly", values=[x for x in HAIR_COLORS.keys()])
        ToolTip(label41, text="Hair Color")
        self.hai.grid(column=1, row=12, sticky="nsew")
        # label/entry for 2.037
        label42 = ttk.Label(self.sectionTwo)
        label42.configure(text='2.037 (RFP)')
        label42.grid(column=0, row=13, sticky="nsew")
        ToolTip(label42, text="Reason Fingerprinted")
        self.rfp = ttk.Entry(self.sectionTwo, name="rfp")
        self.rfp.grid(column=1, row=13, sticky="nsew")
        # label/entry for 2.038
        label43 = ttk.Label(self.sectionTwo)
        label43.configure(text='2.038 (DPR)')
        label43.grid(column=0, row=14, sticky="nsew")
        ToolTip(label43, text="Date Printed\nyyyy/mm/dd")
        self.dpr = ttk.Entry(self.sectionTwo, name="dpr")
        self.dpr.grid(column=1, row=14, sticky="nsew")
        _text_ = date
        self.dpr.delete("0", "end")
        self.dpr.insert("0", _text_)
        # label/entry for 2.041
        label44 = ttk.Label(self.sectionTwo)
        label44.configure(text='2.041 (RES)')
        label44.grid(column=0, row=15, sticky="nsew")
        ToolTip(label44, text="Address/Residence of Person Fingerprinted")
        self.res = ttk.Entry(self.sectionTwo, name="res")
        self.res.grid(column=1, row=15, sticky="nsew")
        # labels/entries for 2.067
        label45 = ttk.Label(self.sectionTwo)
        label45.configure(text='2.067:a (MAK)')
        label45.grid(column=0, row=16, sticky="nsew")
        ToolTip(label45, text="Make")
        self.mak = ttk.Entry(self.sectionTwo, name="mak")
        self.mak.grid(column=1, row=16, sticky="nsew")
        label46 = ttk.Label(self.sectionTwo)
        label46.configure(text='2.067:b (MODL)')
        label46.grid(column=0, row=17, sticky="nsew")
        ToolTip(label46, text="Model")
        self.modl = ttk.Entry(self.sectionTwo, name="modl")
        self.modl.grid(column=1, row=17, sticky="nsew")
        label47 = ttk.Label(self.sectionTwo)
        label47.configure(text='2.067:c (SERNO)')
        label47.grid(column=0, row=18, sticky="nsew")
        ToolTip(label47, text="Serial Number")
        self.serno = ttk.Entry(self.sectionTwo, name="serno")
        self.serno.grid(column=1, row=18, sticky="nsew")
        # label/entry for 2.073
        label48 = ttk.Label(self.sectionTwo)
        label48.configure(text='2.073 (CRI)')
        label48.grid(column=0, row=19, sticky="nsew")
        ToolTip(label48, text="Controlling Agency Identifier\nUsually the same as ORI")
        self.cri = ttk.Entry(self.sectionTwo, name="cri")
        self.cri.grid(column=1, row=19, sticky="nsew")
        _text_ = ORI
        self.cri.delete("0", "end")
        self.cri.insert("0", _text_)
        # button to update information in data containers
        self.sectionTwoUpdaterButton = ttk.Button(self.sectionTwo, name="sectiontwoupdaterbutton")
        self.sectionTwoUpdaterButton.configure(text='Save Changes')
        self.sectionTwoUpdaterButton.grid(column=1, padx=5, pady=10, row=20, sticky="nsew")
        self.sectionTwoUpdaterButton.configure(command=self.section_two_updater)
        self.sectionTwo.grid(
            column=0,
            columnspan=2,
            row=0,
            rowspan=21,
            sticky="nsew")
        self.sectionTwo.grid_anchor("nw")
        panedwindow2.add(self.sectionTwo, weight="1")
        panedwindow2.grid(column=0, row=0, rowspan=21, sticky="nsew")
        # specify section two grid
        for i in range(0,21):
            tk.Grid.rowconfigure(self.sectionTwo, i, weight=1)
        for i in range(0,2):
            tk.Grid.columnconfigure(self.sectionTwo, i, weight=1)
        
        ############### I/O FOR FINGERPRINT IMAGES ################
        panedwindow3.add(panedwindow2, weight="1")
        frame1 = ttk.Frame(panedwindow3)
        frame1.configure(height=1080, width=1920)
        notebook2 = ttk.Notebook(frame1)
        notebook2.configure(height=1080, width=1920)
        
        ############### DISPLAYING PRINTS ################
        # To display prints we create fingerprintviewer
        # # objects using the fingerprintviewer class.
        # To make things easy, we iterate through the
        # # global keys and use some for loops for the
        # # # rows and cols
        icol = 0
        irow = 0
        ############### RIGHT HAND ################
        frame2 = ttk.Frame(notebook2)
        frame2.configure(height=200, width=200)
        for key in RIGHT_HAND:
            self.FINGERPRINT_KEYS[RIGHT_HAND[key]] = FingerprintViewer(frame2, key, irow, icol, None)
            if icol == 2:
                icol = 0
                irow += 1
            else:
                icol += 1
        frame2.grid(column=0, row=0, sticky="nsew")
        # specify hand window grid
        for i in range(0,5):
            tk.Grid.rowconfigure(frame2, i, weight=1)
        for i in range(0,10):
            tk.Grid.columnconfigure(frame2, i, weight=1)
        frame2.grid_anchor("nw")
        notebook2.add(frame2, text='Right')
        ############### LEFT HAND ################
        frame3 = ttk.Frame(notebook2)
        frame3.configure(height=200, width=200)
        icol = 0
        irow = 0
        for key in LEFT_HAND:
            self.FINGERPRINT_KEYS[LEFT_HAND[key]] = FingerprintViewer(frame3, key, irow, icol, None)
            if icol == 2:
                icol = 0
                irow += 1
            else:
                icol += 1
        frame3.grid(column=0, row=0, sticky="nsew")
        # specify hand window grid
        for i in range(0,5):
            tk.Grid.rowconfigure(frame3, i, weight=1)
        for i in range(0,10):
            tk.Grid.columnconfigure(frame3, i, weight=1)
        frame3.grid_anchor("nw")
        notebook2.add(frame3, text='Left')
        notebook2.grid(column=0, row=0, sticky="nsew")
        
        frame1.grid(column=0, row=0, sticky="nsew")
        frame1.grid_anchor("nw")
        panedwindow3.add(frame1, weight="1")
        panedwindow3.grid(column=1, row=0, sticky="nsew")
        self.main.grid_anchor("nw")

        # Main widget
        self.mainsewindow = self.main

    def open_ebts_docs(self):
        os.startfile(HELP_FILES["EBTS"])

    def open_help_docs(self):
        os.startfile(HELP_FILES["Manual"])

    def open_nations(self):
        os.startfile(HELP_FILES["Nations"])

    def open_about(self):
        os.startfile(HELP_FILES["About"])

    def section_one_updater(self, generating=False):
        self.SECTION_ONE =  {
                                '1.02:': self.ver.get(),
                                '1.03:': [['1', '15'], ['2', '00']],
                                '1.04:': f'{self.tot.get()}'.upper(),
                                '1.05:': self.dat.get().replace('/',''),
                                '1.06:': self.pry.get(),
                                '1.07:': self.dai.get(),
                                '1.08:': self.ori.get(),
                                '1.09:': self.tcn.get(),
                                '1.11:': self.nsr.get(),
                                '1.12:': self.ntr.get()
                            }
        # verify that the necessary information has been provided
        if not generating:
            for key,value in self.SECTION_ONE.items():
                if len(value) <= 0:
                    tk.messagebox.showwarning(title="MISSING INPUT", message=f"Missing necessary field {key}. Aborting process.")
                    return
        # seeing which fingerprints are actually there
        i = 1
        for key,value in self.FINGERPRINT_KEYS.items():
            if value.scannability() == "Scannable":
                digstr = f'{key}'
                if len(digstr) == 1:
                    digstr = f'0{key}'
                self.SECTION_ONE['1.03:'].append(['4',digstr])
        # doing it this way means that if user wrote in acronym by muscle memory, it wont error
        if self.tot.get() in TRANSACTION_TYPES.keys():
            self.SECTION_ONE['1.04:'] = TRANSACTION_TYPES[self.tot.get()]
        print("SECTION ONE SAVED")

    def section_two_updater(self):
        self.SECTION_TWO =  {
                                '2.002:': self.idc2.get(),
                                '2.005:': self.ret.get(),
                                '2.016:': self.soc.get(),
                                '2.018:': self.nam.get(),
                                '2.020:': f'{self.pob.get()}'.upper(),
                                '2.021:': f'{self.ctz.get()}'.upper(),
                                '2.022:': self.dob.get().replace('/',''),
                                '2.024:': self.sex.get(),
                                '2.025:': self.rac.get(),
                                '2.027:': self.hgt.get(),
                                '2.029:': self.wgt.get(),
                                '2.031:': self.eye.get(),
                                '2.032:': self.hai.get(),
                                '2.037:':self.rfp.get(),
                                '2.038:':self.dpr.get().replace('/',''),
                                '2.041:': self.res.get(),
                                '2.067:': ' '.join([self.mak.get(), self.modl.get(), self.serno.get()]),
                                '2.073:': self.cri.get(),
                                '2.084:': []
                            }
        # make sure POB and CTZ have valid codes
        if len(self.SECTION_TWO['2.020:']) > 2 or len(self.SECTION_TWO['2.021:']) > 2:
            tk.messagebox.showwarning(title="INVALID POB OR CTZ CODE", message=f"POB and CTZ must be 2 character codes. Refer to help menu for valid codes. Aborting process.")
            return
        # make sure SSN has no illegal characters
        if len(self.SECTION_TWO['2.016:']) > 0:
            self.SECTION_TWO['2.016:'] = re.sub("\D", "", self.SECTION_TWO['2.016:'])
            print(self.SECTION_TWO['2.016:'])
        for key,value in self.SECTION_TWO.items():
            if len(value) <= 0 and key != '2.067:' and key != '2.084:':
                tk.messagebox.showwarning(title="MISSING INPUT", message=f"Missing necessary field {key}. Aborting process.")
                return
        # doing it this way means that if user wrote in acronym by muscle memory, it wont error
        if self.rac.get() in RACES.keys():
            self.SECTION_TWO['2.025:'] = RACES[self.rac.get()]
        if self.eye.get() in EYE_COLORS.keys():
            self.SECTION_TWO['2.031:'] = EYE_COLORS[self.eye.get()]
        if self.hai.get() in HAIR_COLORS.keys():
            self.SECTION_TWO['2.032:'] = HAIR_COLORS[self.hai.get()]
        # amputation info
        for key,value in self.FINGERPRINT_KEYS.items():
            scannability = value.scannability()
            digstr = f'{key}'
            if len(digstr) == 1:
                digstr = f'0{key}'
            if scannability == "Amputated":
                self.SECTION_TWO['2.084:'].append([digstr,'XX'])
            elif scannability == "Bandaged/Other":
                self.SECTION_TWO['2.084:'].append([digstr,'UP'])
        print("SECTION TWO SAVED")
    
    # get tcn
    def tcn_getter(self):
        self.save(True)
        _text_ = tcn_setter(self.SECTION_ONE['1.05:'], self.SECTION_ONE['1.08:'], self.SECTION_TWO['2.018:'], self.SECTION_ONE['1.04:'])
        self.tcn.delete("0", "end")
        self.tcn.insert("0", _text_)

    # just a quick saving func
    def save(self, generating=False):
        self.section_one_updater(generating)
        self.section_two_updater()

    # brings in fingerprints and basic info from preprinted card
    def importer(self):
        file = fd.askopenfile(mode='r', filetypes=INPUT_EXTS)
        if file:
             filepath = os.path.abspath(file.name)
        else:
            tk.messagebox.showwarning(title="INVALID FILEPATH", message="The provided file does not exist, or is invalid! :(\nIf you pressed cancel, ignore this message!")
            return
        images = parse_pdf(filepath, MAINDIR) # wrenches the images from the pdf's cold, dead hands
        # second window for imports
        import_picker = ImportPickerApp(self.main, self)
        import_picker.import_prints(images)
    
    # encodes and exports to EFT file format
    def exporter(self):
        self.output.clear_records()
        self.save()
        self.output.add_record(Record(1, self.SECTION_ONE))
        self.output.add_record(Record(2, self.SECTION_TWO))
        for key,value in self.FINGERPRINT_KEYS.items():
            # only need to serialize if scan is available
            if value.scannability() == "Scannable":
                print(f'Fingerprint {key} is Scannable')
                # getting h/w
                params = [0,0]
                # try except catches scannables that didnt have a provided print
                try:
                    with Image.open(value.fingerprint['raw']) as img:
                        w, h = img.size
                        params[0] = w
                        params[1] = h
                        print(params)
                    with open(value.fingerprint['wsq'], 'rb') as f:
                        self.output.add_record(Record(4, f.read(), key, params))
                except:
                    tk.messagebox.showwarning(
                                                title="MISSING FINGERPRINT", 
                                                message=f"Fingerprint {key} was marked as Scannable, but is missing a scanned image.\nYou will need to fix this error either by marking it as Amputated/Other, or providing a fingerprint.\nFailure to do so will cause unstable results and likely render your file invalid."
                                             )
                    continue
        file = fd.asksaveasfile(mode='wb', filetypes=OUTPUT_EXTS, defaultextension='.eft')
        if file:
            file.write(self.output.serialize())
        
    def run(self):
        self.mainsewindow.mainloop()


if __name__ == "__main__":
    app = EFTGuiApp()
    app.run()

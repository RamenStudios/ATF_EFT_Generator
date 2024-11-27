import tkinter.filedialog as fd
from pypdf import PdfReader
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageFile, ImageTk
from datetime import date
import wsq
import os
import re

# the below is how the sample text is parsed before extra shit
# ['RODRIGUEZ,JOSE ROMAN', '3222 N COTTONTAIL CIR, TUCSO 03 22 1983', 'N, AZ, 85749 US M W 511 190 BROBLK MM', '10/28/2023', 'NFA APPLICATION 600419036']
# returns some poorly parsed text
# TODO: actually finish implementing this
def extract_text(page):
    text = [re.sub(r"\s{2,}", " ", x) for x in page.extract_text(extraction_mode="layout").strip().split('\n') if len(x)>0 and not x.isspace()]
    #records =   {
      #              '
      #              '1.05:': ,
               #     
          #      }
    
# just returns a wsq and raw for the given image
def image_importer(image, maindir, filename, imagedir=None, filepath=None):
    # if image outside main directory, ask users where they want to save results
    dir = maindir
    if imagedir == None and filepath is not None:
        tk.messagebox.showinfo(title="NOTICE", message="You are going to be asked to choose where you want the resulting images saved. Inside your chosen folder, 2 subfolders will appear:\nraw\nwsq")
        imagedir = fd.askdirectory(mustexist=True)
        dir = imagedir
    else:
        dir = f'{dir}/{imagedir}'
        if not os.path.exists(dir):
            tk.messagebox.showerror(title="ERROR", message="Unexpected error while parsing directory name. For devs: error is likely in gui_utils.py. Aborting process.")
            return
    # extract image data
    # one converted, one for display
    img = image
    raw = image
    # make sure our image directories exist
    for fp in [f"{dir}/raw", f"{dir}/wsq"]:
        try:
            os.mkdir(fp)
        except:
            continue
    # save raw
    raw.save(f"{dir}/raw/{filename}")
    # Convert to grayscale image (important)
    img = img.convert("L")
    filename = filename.replace('.jpg','')
    img.save(f"{dir}/wsq/{filename}.wsq") # saving as wsq is how we convert and preserve for later
    returnDict = {"wsq":f"{dir}/wsq/{filename}.wsq", "raw":f"{dir}/raw/{filename}.jpg"}
    return returnDict

# TODO: make a better directory, specific to the name of the person?
# returns list of images
def extract_images(page, maindir, imagedir):
    images = {}
    # make sure the directories we need exist <3
    for dirname in [f"{maindir}/{imagedir}", f"{maindir}/{imagedir}/wsq", f"{maindir}/{imagedir}/raw"]:
        try:
            os.mkdir(dirname)
        except:
            continue
    # sift through the images
    for image_file_object in page.images:
        filename = (image_file_object.name).replace('Image', '')
        images[filename.split('.')[0]] = image_importer(image_file_object.image, maindir, filename, imagedir)
    return images
        
# returns a dict of image objects matched to their keys from pdf
# TODO: also returns whatever text data can be parsed
def parse_pdf(filepath, maindir):
    reader = PdfReader(filepath)
    page = reader.pages[0]
    print(page.get_contents())
    imagedir = f'images/' + (((filepath.split('\\'))[-1]).split('.'))[0]
    return extract_images(page, maindir, imagedir)
    #extract_text(page)

# ez function to format today's date in yyyy/mm/dd format
def date_getter():
    cdate = f'{date.today()}'.replace("-","/")
    return f'{cdate}'

# tcn generator
def tcn_setter(date, ori, name, tot):
    # if any of the necessary parameters are blank, show error
    failure = False
    try:
        if (len(date) == 0) or (len(ori) == 0) or (len(name) == 0) or (len(tot) == 0):
            failure = True
    except:
        failure = True
    if failure:
        tk.messagebox.showerror(title="MISSING FIELDS", message="Missing one of the following fields:\nDAT\nTOT\nORI\nNAM")
        return "ERROR"
    tcn = f'{ori}-{date.replace("/","")}-{name.replace(",","").replace(" ","")}'
    # remember to account for BOM in encoding
    # if too small, add tot 
    if len(tcn.encode('utf-8')) < 12:
        tcn += f'-{tot}'
    # if too big, truncate
    if len(tcn.encode('utf-8')) > 42:
        tcn = tcn[0:39]
    return tcn
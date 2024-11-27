# EFT GENERATOR FOR FIREARMS PURPOSES

> #### CREDITS 
> before I get into anything, I want to give due credit to the wsq library I used extensively, which can be found [here](https://github.com/idemia/python-wsq).  
> as well as the GUI I used to make GUI creation easier. [it's extremely underrated](https://github.com/alejandroautalan/pygubu)
> big thanks also to those who maintain pypdf, pil, and tkinter. could not have done this without you o7

## PURPOSE

This program was commissioned by Diamondback Shooting Sports to streamline their creation of client EFT files. It creates the records necessary for ATF forms, which currently only includes Types 1, 2 and 4. Further information on the EBTS format can be found [here](https://fbibiospecs.fbi.gov/file-repository/master-ebts-v11-0.pdf)  
This was created by Adamari Rodriguez of RamenStudios, whose GitHub you're either reading or can find [here](https://github.com/RamenStudios)  
NOTE: Diamondback never ended up paying me, because they thought me asking for field testing meant I was scamming them. So if you're reading this, congrats! You now have access to a free software. I WILL NOT BE MAINTAINING OR UPDATING THIS.

## STRUCTURE
All the important files are in the src folder
- gui.py : holds main tkinter GUI functionality and all the associated commands, as well as some important dictionaries
- gui_containers.py : probably should've renamed this, it makes the fingerprints into their own object for easier and cleaner coding
- gui_utils.py : just some functions I didn't want to rewrite over and over
- import_picker.py : the window for importing fingerprints from a pdf. not super well tested, so if it breaks let me know
- serializer.py : what it says on the tin

## KNOWN BUGS
- Currently when exporting the file, you have to manually type in the .eft extension. Annoying, will be fixed in a future update

## TODO
- In a future update, you will be able to save to something like a JSON or XML format, in case you need to come back to a file and don't want to rewrite everything. THAT IS IF I EVER RETURN TO UPDATING THIS
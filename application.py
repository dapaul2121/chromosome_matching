from tkinter import filedialog
from tkinter import *
from advanceddistancecalc import extractAnalyizeData
import sys
 
#function for when buttons are clicked
def clicked():
	window.filename1 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
	lblprotien1.configure(text= window.filename1)


def clickedtwo():
	window.filename2 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
	lblprotien2.configure(text= window.filename2)

def clickedthree():
	window.filename3 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("tif files","*.tif"),("all files","*.*")))
	lblchromo.configure(text= window.filename3)

def clickedfinal():
	if window.filename1 != "" and window.filename2 != "" and window.filename3 == "": 
		window.savedfile =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
		extractAnalyizeData(window.filename2, window.filename1, window.savedfile)
		lblcreatecsv.configure(text = "File " + window.savedfile + " succesfully created. Protien matching successful")
	elif window.filename1 != "" and window.filename2 != "" and window.filename3 != "": 
		window.savedfile =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
		extractAnalyizeData(window.filename2, window.filename1, window.savedfile, window.filename3)
		lblcreatecsv.configure(text = "File " + window.savedfile + " successfully created. Protien matching and chromosome matching sucessful")
	else:
		lblcreatecsv.configure(text = "Error: Select two .csv files (you may also have a .tif)")


#startup parameters
window = Tk()

window.filename1 = ''
window.filename2 = ''
window.filename3 = ''

#instructions 
window.title("Shortest Distance App")

lbltitle = Label(window, text= "Finds the shortest distance between protiens or between protiens and chromosomes")
lbltitle.grid(column=0, row=0)

#first file (protien .csv file)
lblprotien1 = Label(window, text="")
lblprotien1.grid(column=0, row=1)

btnprotien1 = Button(window, text="Find First .csv Protien File", bg="orange", fg="red", command = clicked)
btnprotien1.grid(column=0, row=2)


#second file (protien .csv file)
lblprotien2 = Label(window, text="")
lblprotien2.grid(column=0, row=5)

btnprotien2 = Button(window, text="Find Second .csv Protien File", bg="orange", fg="red", command = clickedtwo)
btnprotien2.grid(column=0, row=6)


#third file (optional chromo .tif file)
lblchromo = Label(window, text="")
lblchromo.grid(column=0, row=7)

btnchromo = Button(window, text="Find Chromosome .tif Black and White Image File", bg="orange", fg="red", command = clickedthree)
btnchromo.grid(column=0, row=8)


#create a third csv file
btncreatecsv = Button(window, text="Create Third .csv file", bg="orange", fg="red", command = clickedfinal)
btncreatecsv.grid(column=0, row=9)

lblcreatecsv = Label(window, text="")
lblcreatecsv.grid(column=0, row = 10)


window.mainloop()
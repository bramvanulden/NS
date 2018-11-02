from tkinter import *
from FetchNS import *

root = Tk()
station = ""
naarStation = ""
vanStation = ""
readStations = open("stations.txt", "r")


def ShowVertrektijden(station):
    i = 0
    FetchedVertrektijden = getVertrektijden(station)
    for c in FetchedVertrektijden:
        i += 1
        if i < 10:
            append = "De " + FetchedVertrektijden.get(c)[2] + " naar " + c + " vertrekt om " + FetchedVertrektijden.get(c)[0] + " vanaf spoor " + FetchedVertrektijden.get(c)[3]
            vertrektijden.insert(END, append)

def ShowVertragingen(station):
    i=0
    FetchedVertragingen = getStoringenWerkzaamheden(station)
    for c in FetchedVertragingen:
        i +=1
        if i < 10:
            append = c + "\n" + FetchedVertragingen.get(c)[0] + FetchedVertragingen.get(c)[1] + FetchedVertragingen.get(c)[2] + FetchedVertragingen.get(c)[3] + "\n"
            vertragingen.insert(END, append)

def CheckStation(input):
    for line in readStations:
        if input in line:
            return input
        else:
            continue

def login():
    global station
    station = CheckStation(loginfield.get())
    if station is not None:
        ShowVertragingen(station)
        ShowVertrektijden(station)
        toonHoofdFrame()
    else:
        logintext.configure(state=NORMAL)
        logintext.delete(0, END)
        logintext.insert(0, "Incorrect station!")
        logintext.configure(state="readonly")


def FetchReisAdvies():
    returnValue = CheckStation(inputfield.get())
    if returnValue is not None:
        reisadviezen = getReisadvies(station, returnValue)
        for advies in reisadviezen:
            append = "Om " +  reisadviezen.get(advies)[5] + " vertrekt er een " + reisadviezen.get(advies)[3] + " vanaf spoor " + reisadviezen.get(advies)[4] + ". Deze komt aan om " + reisadviezen.get(advies)[2] + ". Reistijd: " + reisadviezen.get(advies)[1]
            reisadvies.insert(END, append)




def toonHoofdFrame():
    print("Station:", station)
    loginframe.pack_forget()
    root.title(station)
    hoofdframe.pack(expand=True, fill="both", side=TOP)
    buttonframe.pack(expand=True, fill="both", side=BOTTOM)
    backbutton.pack(padx=10, pady=10, side=RIGHT)
    adviesbutton.pack(padx=10, pady=10, side=LEFT)
    vertrektijden.pack(side=LEFT, padx=30, pady=30)
    vertragingen.pack(side=LEFT, padx=30, pady=30)

def toonLoginFrame():
    hoofdframe.pack_forget()
    buttonframe.pack_forget()
    loginframe.pack()

def ReisAdvies():
    hoofdframe.pack_forget()
    buttonframe.pack_forget()
    reisadviesframe.pack(fill="both", expand=True)
    reisadviestext.pack()
    inputfield.pack(padx=20, pady=20)
    inputbutton.pack(padx=20, pady=20)
    reisadvies.pack(side=RIGHT)


#REISADVIES
reisadviesframe = Frame(master=root, bg="#f2ee0e")
reisadvies = Listbox(master=reisadviesframe, width=120)
inputbutton = Button(master=reisadviesframe, text='Zoek reisadvies', command=FetchReisAdvies)
reisadviestext = Entry(master=reisadviesframe, width=30)
reisadviestext.insert(0, "Voer uw aankomst-station in.")
reisadviestext.configure(state="readonly")
inputfield = Entry(master=reisadviesframe)

#HOOFDSCHERM
hoofdframe = Frame(master=root, bg="#f2ee0e", width=1000, height=500)
buttonframe = Label(master=root, bg="blue", width=400, height=100)
backbutton = Button(master=buttonframe, text='Kies een ander station', command=toonLoginFrame)
adviesbutton = Button(master=buttonframe, text='Vraag reisadvies', command=ReisAdvies)
vertrektijden = Listbox(master=hoofdframe, width=70)
vertragingen = Text(master=hoofdframe, width=70)

#LOGIN SCHERM
reisadviesframe.pack_forget()
loginframe = Frame(master=root, bg="#f2ee0e")
loginframe.pack(fill="both", expand=True)
loginfield = Entry(master=loginframe)
logintext = Entry(master=loginframe)
logintext.insert(0, "Voor een station in.")
logintext.configure(state="readonly")
logintext.pack()
loginfield.pack(padx=20, pady=20)
loginbutton = Button(master=loginframe, text='Ga!', command=login)
loginbutton.pack(padx=20, pady=20)



vertrektijden.insert(END, "Vertrektijden")
vertragingen.insert(END, "Vertragingen\n")


root.mainloop()
from tkinter import *
from FetchNS import *

root = Tk()
station = ""
# loginframe = Frame(master=root)
# loginframe.pack(fill="both", expand=True)
# loginfield = Entry(master=loginframe)
# loginfield.pack(padx=20, pady=20)
# loginbutton = Button(master=loginframe, text='login', command=login)
# loginbutton.pack(padx=20, pady=20)


hoofdframe = Frame(master=root, bg="#f2ee0e", width=1000, height=500)
buttonframe = Label(master=root, bg="blue", width=400, height=100)
backbutton = Button(master=buttonframe, text='Kies een ander station', command=None)
vertrektijden = Listbox(master=hoofdframe, width=70)
vertragingen = Listbox(master=hoofdframe)
reisadvies = Listbox(master=hoofdframe)

vertrektijden.insert(END, "Vertrektijden")
vertragingen.insert(END, "Vertragingen")
reisadvies.insert(END, "Reisadvies")

i = 0
FetchedVertrektijden = getVertrektijden("ut")
for c in FetchedVertrektijden:
    i+= 1
    if i < 10:
        append = "De " + FetchedVertrektijden.get(c)[2] + " naar " + c + " vertrekt om " + FetchedVertrektijden.get(c)[0] + " vanaf spoor " + FetchedVertrektijden.get(c)[3]
        vertrektijden.insert(END, append)


hoofdframe.pack(expand=True, fill="both", side=TOP)
buttonframe.pack(expand=True, fill="both", side=BOTTOM)
backbutton.pack(padx=10, pady=10)
vertrektijden.pack(side=LEFT, padx=30, pady=30)
vertragingen.pack(side=LEFT, padx=30, pady=30)
reisadvies.pack(side=LEFT, padx=30, pady=30)



root.mainloop()
import json
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image

with open("champions.txt","r") as ch:
    champions = ch.read().splitlines()

if not os.path.exists("save.json"):
    with open("save.json","w") as sf:
        saveFile = {}
        for champion in champions:
            saveFile[champion] = {"Played": False, "Score": [0, 0, 0], "TimesPlayed": 0}
        json.dump(saveFile, sf)

def openSaveFile():
    with open("save.json") as sf:
        global saveFile
        saveFile = json.load(sf)

def saveSaveFile():
    with open("save.json","w") as sf:
        global saveFile
        json.dump(saveFile,sf)

openSaveFile()

class App(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.varChampion = StringVar()
        self.varScore = StringVar()
        self.varTries = StringVar()
        self.enterScore = StringVar()
        self.varChampion.set(current[0])
        self.varTries.set(current[2])
        self.varScore.set(currentScore)
        self.champion_image = ImageTk.PhotoImage(
            Image.open(f"Pictures/{current[0]}.jpg").resize((120, 120), Image.LANCZOS)
        )
        self.create_button()
        self.create_labels()
        self.create_image()
    
    def create_image(self):
        self.championPicLabel = ttk.Label(self.master, image=self.champion_image)
        self.championPicLabel.grid(column=1, row=2)

    def create_labels(self):
        ttk.Label(self.master,text="Champion").grid(column=1,row=1,sticky=N)
        ttk.Label(self.master,text="Score").grid(column=3,row=1,sticky=N)
        ttk.Label(self.master,text="Tries").grid(column=2,row=1)
        ttk.Label(self.master,textvariable=self.varChampion).grid(column=1,row=3)
        ttk.Label(self.master,textvariable=self.varScore).grid(column=3,row=3,sticky=N)
        ttk.Label(self.master,textvariable=self.varTries).grid(column=2,row=2,sticky=N)
        
    def create_button(self):
        ttk.Button(self.master,text="Next Champion",command=self.nextChampion).grid(column=3,row=5,sticky=(S,W))
        ttk.Button(self.master,text="Previous Champion",command=self.previousChampion).grid(column=1,row=5)
        ttk.Button(self.master,text="Add Score",command=self.addScore).grid(column=3,row=2,sticky=N)
        ttk.Button(self.master,text="Clear Champion Stats",command=self.clearChampionStats).grid(column=2,row=5,sticky=(S,E))
        ttk.Button(self.master,text="Re-Create Save File",command=self.createSaveFile).grid(column=2,row=4,sticky=(S))
        ttk.Entry(self.master,textvariable=self.enterScore).grid(column=3,row=4,sticky=(W,E))

    def nextChampion(self):
        global championIndex
        championIndex += 1
        if championIndex > len(champions)-1:
            championIndex = 0
        self.setCurrent()

    def previousChampion(self):
        global championIndex
        championIndex -= 1
        if championIndex < 0:
            championIndex = len(champions)-1
        self.setCurrent()
    
    def setCurrent(self):
        global current
        current = self.getCurrent()
        currentScore = f"{current[1][0]}/{current[1][1]}/{current[1][2]}"
        self.varChampion.set(current[0])
        self.varScore.set(currentScore)
        self.varTries.set(current[2])
        self.champion_image = ImageTk.PhotoImage(
            Image.open(f"Pictures/{current[0]}.jpg").resize((120, 120), Image.LANCZOS)
        )
        self.championPicLabel.configure(image=self.champion_image)

    def getCurrent(self):
        openSaveFile()
        champion = champions[championIndex]
        return [champion,saveFile[champion]["Score"],saveFile[champion]["TimesPlayed"]]
    
    def addScore(self):
        openSaveFile()
        score = self.enterScore.get().split("/")
        if len(score) == 3:
            try:
                score = [int(s) for s in score]
                if all(0 <= s <= 100 for s in score):
                    saveFile[current[0]]["Score"][0] += score[0]
                    saveFile[current[0]]["Score"][1] += score[1]
                    saveFile[current[0]]["Score"][2] += score[2]
                    saveFile[current[0]]["TimesPlayed"] += 1
                    saveFile[current[0]]["Played"] = True
                    saveSaveFile()
                    self.varScore.set(f"{saveFile[current[0]]['Score'][0]}/{saveFile[current[0]]['Score'][1]}/{saveFile[current[0]]['Score'][2]}")
                    self.varTries.set(saveFile[current[0]]["TimesPlayed"])
                else:
                    print("Scores must be between 0 and 100.")
            except ValueError:
                print("Invalid score format. Please enter three integers separated by slashes.")
        else:
            print("Please enter a score in the format 'x/y/z'.")
    
    def clearChampionStats(self):
        openSaveFile()
        saveFile[current[0]]["Score"] = [0, 0, 0]
        saveFile[current[0]]["TimesPlayed"] = 0
        saveFile[current[0]]["Played"] = False
        saveSaveFile()
        self.varScore.set("0/0/0")
        self.varTries.set("0")
        self.enterScore.set("")

    def createSaveFile(self):
        global saveFile
        saveFile = {}
        for champion in champions:
            saveFile[champion] = {"Played": False, "Score": [0, 0, 0], "TimesPlayed": 0}
        saveSaveFile()

root = Tk()

root.title("Setup, please wait...")

root.iconbitmap("LoL_Icon.ico")
root.resizable(False, False)

if saveFile == {}:
    for champion in champions:
        saveFile[champion] = {}
        saveFile[champion] = {"Played": False,"Score":[0,0,0],"TimesPlayed":0}
    saveSaveFile()

def getFirst():
    openSaveFile()
    for champion in saveFile:
        if saveFile[champion]["Played"] == False:
            return [champion,saveFile[champion]["Score"],saveFile[champion]["TimesPlayed"]]
        
current = getFirst()
currentScore = f"{current[1][0]}/{current[1][1]}/{current[1][2]}"

root.title("LOL A-Z Challenge")

championIndex = champions.index(current[0])

mainframe = ttk.Frame(root,padding="4 4 12 12")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

app = App(mainframe)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5,pady=5)

root.bind("<Return>", lambda event: app.addScore())

root.mainloop()

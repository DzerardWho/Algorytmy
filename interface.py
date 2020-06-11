import tkinter as tk
from tkinter import filedialog
from typing import List, Iterable

window = tk.Tk()
window.title("AiSD II Projekt")
window.geometry("1000x640")


title = tk.Label(window, text="Wprowadź niezbędne parametry " 
                            "(lub wybierz domyślne)", 
                            font=('Arial', 12, 'bold'))
title.pack(pady=20)

frame = tk.LabelFrame(window, padx=5, pady=10)
frame.pack()

DEFAULT = [10, 3, 3, 3, 0.33, 0.33, 0.34, 0.33, 0.33, 0.34, 0.2, 0.2, 0.2, 0.2, 0.2]

def setValues(list):
    for i in range(0, 4):
        AllElements[i].delete(0, tk.END)
        AllElements[i].insert(0, list[i])

    for i in range(4, 15):
        AllElements[i].set(list[i])


def getValuse():
    lst = []
    for i in range(0,4):
        lst.append(str(AllElementsToSave[i].get()))
    
    for i in range(4, 15):
        lst.append(str(AllElementsToSave[i].cget('text')))
        
    return lst


def resetToDefault():
    entryAlfa.delete(0, tk.END)
    entryC.delete(0, tk.END)
    entryT.delete(0, tk.END)
    entryEpsilon.delete(0, tk.END)

    setValues(DEFAULT)


def sliderOper(v):
    beta = sliderBeta.get()
    gamma = sliderGamma.get()
    delta = sliderDelta.get()
    sum = float(beta) + float(gamma) + float(delta)
    if sum!=0:
        labelBeta.config(text=str(round(float(beta)/sum, 3)))
        labelGamma.config(text=str(round(float(gamma)/sum, 3)))
        labelDelta.config(text=str(round(float(delta)/sum, 3)))
    

def sliderChan(v):
    cost = sliderChCost.get()
    trans = sliderChTrans.get()
    use = sliderChU.get()
    sum = float(cost) + float(trans) + float(use)
    if sum!=0:
        labelChCost.config(text=str(round(float(cost)/sum, 3)))
        labelChTrans.config(text=str(round(float(trans)/sum, 3)))
        labelChU.config(text=str(round(float(use)/sum, 3)))


def sliderProc(v):
    cheapTask = sliderProcCheapTask.get()
    fastTask = sliderProcFastTask.get()
    tk = sliderProcTK.get()
    asbef = sliderProcAsBef.get()
    use = sliderProcUse.get()
    sum = float(cheapTask)+float(fastTask)+float(tk)+float(asbef)+float(use)
    if sum!=0:
        labelProcCheapTask.config(text=str(round(float(cheapTask)/sum, 3)))
        labelProcFastTask.config(text=str(round(float(fastTask)/sum, 3)))
        labelProcTK.config(text=str(round(float(tk)/sum, 3)))
        labelProcAsBef.config(text=str(round(float(asbef)/sum, 3)))
        labelProcUse.config(text=str(round(float(use)/sum, 3)))


def openConfig():
    window.openConfigName = filedialog.askopenfilename(title='Wybierz plik', filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    textGetFile.delete('1.0', tk.END)
    textGetFile.insert(tk.END, window.openConfigName)


def loadConfig():
    f = open(window.openConfigName, 'r')
    lines = f.readlines()
    f.close()
    lst = []
    for line in lines:
        lst.append(float(line))
    setValues(lst)

def chooseToSaveConfig():
    window.saveConfigName = filedialog.askopenfilename(title='Wybierz plik zapisu', filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    textSaveFile.delete('1.0', tk.END)
    textSaveFile.insert(tk.END, window.saveConfigName)


def saveConfig():
    f = open(window.saveConfigName, 'w')
    l = getValuse()
    for elem in l:
        f.write(elem + '\n')
    f.close()

def chooseGraph():
    window.saveChooseGraph = filedialog.askopenfilename(title='Wybierz plik', filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    textChooseGraph.delete('1.0', tk.END)
    textChooseGraph.insert(tk.END, window.saveChooseGraph)


### Buttons 

ButtonDefault = tk.Button(
                    frame,   
                    text='Przywróć domyślne', 
                    font = ('Arial', 11, 'bold'),
                    command = resetToDefault)
ButtonDefault.grid(row=8, column=0, sticky='w', padx=18)

ButtonStart = tk.Button(
                    frame,
                    text='Rozpocznij',
                    font = ('Arial', 11, 'bold'))  # Dodać funkcję pobierającą wszystkie argumenty 
ButtonStart.grid(row=8, column=1, sticky='e', padx=10)

quitButton =  tk.Button(
                    frame, 
                    text="Zakończ",
                    font = ('Arial', 11, 'bold'), 
                    command=window.quit)
quitButton.grid(row=8, column=2, sticky='e', padx=10)




### Entry Labels 
#### ALFA
frameAlfa = tk.LabelFrame(frame, text='Wartość parametru (alfa)')
frameAlfa.grid(row=0, column=0, padx=20, pady=20)
entryAlfa = tk.Entry(frameAlfa, width=20, borderwidth=5,)
entryAlfa.pack(padx=5)

#### EPSILON
frameEpsilon = tk.LabelFrame(frame, text='Wartość parametru epsilon')
frameEpsilon.grid(row=1, column=0, padx=20, pady=10)
entryEpsilon = tk.Entry(frameEpsilon, width=20, borderwidth=5,)
entryEpsilon.pack() 

#### C/T
frameCT = tk.LabelFrame(frame,text='Funkcja F=c*koszt+t*czas')
frameCT.grid(row=3, column=0, rowspan=4, padx=10, pady=5, sticky='n')

frameC = tk.LabelFrame(frameCT, text='Wartość parametru c')
frameC.grid(row=1, column=0, padx=12, pady=13)
entryC = tk.Entry(frameC, width=18, borderwidth=5)
entryC.pack()

frameT = tk.LabelFrame(frameCT, text='Wartość parametru t')
frameT.grid(row=2, column=0, padx=12, pady=13)
entryT = tk.Entry(frameT, width=18, borderwidth=5,)
entryT.pack()    

### Operator Sliders

frameSld = tk.LabelFrame(frame, text='Rozwiązania otrzymane poprzez')
frameSld.grid(row=0, column=1, rowspan=3, pady=10, padx=10)

sliderBeta = tk.Scale(frameSld, label='Operator Selekcji:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderOper)
sliderBeta.grid(row=0, column=0, pady=5)

sliderGamma = tk.Scale(frameSld, label='Operator Krzyżowania:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderOper)
sliderGamma.grid(row=1, column=0, pady=5)

sliderDelta = tk.Scale(frameSld, label='Operator Mutacji:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderOper)
sliderDelta.grid(row=2, column=0, pady=5)


### Operator Sliders Label

labelBeta = tk.Label(frameSld, text='0', width=5)
labelBeta.grid(row=0, column=1)

labelGamma = tk.Label(frameSld, text='0', width=5)
labelGamma.grid(row=1, column=1)

labelDelta = tk.Label(frameSld, text='0', width=5)
labelDelta.grid(row=2, column=1)


### Channels Sliders

frameChan = tk.LabelFrame(frame, text='Dla zasobów komunikacyjnych:')
frameChan.grid(row=3, column=1, rowspan=4, pady=5, padx=10, sticky='n')

sliderChCost = tk.Scale(frameChan, label='Najmniejszy wzrost kosztu:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderChan)
sliderChCost.grid(row=0, column=0, pady=5)

sliderChTrans = tk.Scale(frameChan, label='Najszybsza transmisja:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderChan)
sliderChTrans.grid(row=1, column=0, pady=5)

sliderChU = tk.Scale(frameChan, label='Najrzadziej używany:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderChan)
sliderChU.grid(row=2, column=0, pady=5)


### Operator Sliders Label

labelChCost = tk.Label(frameChan, text='0', width=5)
labelChCost.grid(row=0, column=1)

labelChTrans = tk.Label(frameChan, text='0', width=5)
labelChTrans.grid(row=1, column=1)

labelChU = tk.Label(frameChan, text='0', width=5)
labelChU.grid(row=2, column=1)


### Proc Sliders

frameProc = tk.LabelFrame(frame, text='Dla zasobów obliczeniowych:')
frameProc.grid(row=0, column=2, rowspan=5, pady=10, padx=20)

sliderProcCheapTask = tk.Scale(frameProc, label='Najtańsza impl. zadań:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderProc)
sliderProcCheapTask.grid(row=0, column=0, pady=5)

sliderProcFastTask = tk.Scale(frameProc, label='Najszybsza impl. zadań:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderProc)
sliderProcFastTask.grid(row=1, column=0, pady=5)

sliderProcTK = tk.Scale(frameProc, label='Najmniejsze t*k:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderProc)
sliderProcTK.grid(row=2, column=0, pady=5)

sliderProcAsBef = tk.Scale(frameProc, label='Jak dla poprzednika:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderProc)
sliderProcAsBef.grid(row=3, column=0, pady=5)

sliderProcUse = tk.Scale(frameProc, label='Najmniej obciążone:', 
                    from_=0, to=1, resolution=0.01, 
                    orient=tk.HORIZONTAL, 
                    length=250,
                    showvalue=0,
                    command = sliderProc)
sliderProcUse.grid(row=4, column=0, pady=5)


### Operator Sliders Label

labelProcCheapTask = tk.Label(frameProc, text='0', width=5)
labelProcCheapTask.grid(row=0, column=1)

labelProcFastTask = tk.Label(frameProc, text='0', width=5)
labelProcFastTask.grid(row=1, column=1)

labelProcTK = tk.Label(frameProc, text='0', width=5)
labelProcTK.grid(row=2, column=1)

labelProcAsBef = tk.Label(frameProc, text='0', width=5)
labelProcAsBef.grid(row=3, column=1)

labelProcUse = tk.Label(frameProc, text='0', width=5)
labelProcUse.grid(row=4, column=1)


### Open Config

frameSaveOpenConfig = tk.LabelFrame(frame, text='Zapisz/Wczytaj plik z parametrami', pady=4)
frameSaveOpenConfig.grid(row=5, column=2, rowspan=3, pady=10, padx=10)

labelOdczyt = tk.Label(frameSaveOpenConfig, text="Plik do odczytu:")
labelOdczyt.grid(row=0, column=0, sticky='w', pady=5)

buttonOdczyt = tk.Button(frameSaveOpenConfig, text="Wczytaj", width=6, command=loadConfig)
buttonOdczyt.grid(row=0,column=1)

buttonGetFile = tk.Button(frameSaveOpenConfig, text="...", command=openConfig, width=6)
buttonGetFile.grid(row=1, column=1, padx=3)

sBarGetFile = tk.Scrollbar(frameSaveOpenConfig, orient =tk.HORIZONTAL)
sBarGetFile.grid(row=2, column=0, sticky='we')

textGetFile = tk.Text(frameSaveOpenConfig, width=32, height=1, xscrollcommand = sBarGetFile.set, wrap ='none')
textGetFile.grid(row=1, column=0)

sBarGetFile.config(command=textGetFile.xview)

### Save Config

labelSave = tk.Label(frameSaveOpenConfig, text="Plik do zapisu:")
labelSave.grid(row=3, column=0, sticky='w', pady=5)

buttonOdczyt = tk.Button(frameSaveOpenConfig, text="Zapisz", width=6, command=saveConfig)
buttonOdczyt.grid(row=3,column=1)

buttonSaveFile = tk.Button(frameSaveOpenConfig, text="...", width=6, command=chooseToSaveConfig)
buttonSaveFile.grid(row=4, column=1, padx=3)

sBarSaveFile = tk.Scrollbar(frameSaveOpenConfig, orient =tk.HORIZONTAL)
sBarSaveFile.grid(row=5, column=0, sticky='we')

textSaveFile = tk.Text(frameSaveOpenConfig, width=32, height=1, xscrollcommand = sBarSaveFile.set, wrap ='none')
textSaveFile.grid(row=4, column=0)

sBarSaveFile.config(command=textSaveFile.xview)


### Choose graph

frameChooseGraph = tk.LabelFrame(frame, text='Wczytaj Graf')
frameChooseGraph.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky='e')

labelChooseGraph = tk.Label(frameChooseGraph, text="Wybierz Plik:")
labelChooseGraph.grid(row=0, column=0, sticky='w', pady=5)

buttonOdczyt = tk.Button(frameChooseGraph, text="Wczytaj", width=6)     ## dodać funkcję wczytywania
buttonOdczyt.grid(row=0,column=1)

buttonChooseGraph = tk.Button(frameChooseGraph, text="...", width=6, command=chooseGraph)
buttonChooseGraph.grid(row=1, column=1, padx=3)

sBarChooseGraph = tk.Scrollbar(frameChooseGraph, orient =tk.HORIZONTAL)
sBarChooseGraph.grid(row=2, column=0, sticky='we')

textChooseGraph = tk.Text(frameChooseGraph, width=54, height=1, xscrollcommand = sBarChooseGraph.set, wrap ='none')
textChooseGraph.grid(row=1, column=0)

sBarChooseGraph.config(command=textChooseGraph.xview)

AllElements = (entryAlfa, entryC, entryT, entryEpsilon, sliderBeta, sliderGamma,
            sliderDelta, sliderChCost, sliderChTrans, sliderChU, sliderProcCheapTask,
            sliderProcFastTask, sliderProcTK, sliderProcAsBef, sliderProcUse)

AllElementsToSave = (entryAlfa, entryC, entryT, entryEpsilon, labelBeta,
                labelGamma, labelDelta, labelChCost, labelChTrans, labelChU,
                labelProcCheapTask, labelProcFastTask, labelProcTK, labelProcAsBef,
                labelProcUse)

window.mainloop()

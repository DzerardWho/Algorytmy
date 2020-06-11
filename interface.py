from tkinter import Tk, Label, Text, Entry, LabelFrame, Button,\
    Scale, Scrollbar, HORIZONTAL, END, filedialog, messagebox
from configparser import ConfigParser


DEFAULT = {'alpha': 10.0,
            'epsilon': 3.0,
            'c': 3.0,
            't': 3.0,
            'reproduction': 0.33,
            'crossbread': 0.33,
            'mutate': 0.34,
            'k1': 0.33,
            'k2': 0.33,
            'k3': 0.34,
            'o1': 0.2,
            'o2': 0.2,
            'o3': 0.2,
            'o4': 0.2,
            'o5': 0.2}


values = DEFAULT.copy()


window = Tk()
window.title("AiSD II Projekt")
window.geometry("1000x640")


title = Label(window, text="Wprowadź niezbędne parametry "
              "(lub wybierz domyślne)",
              font=('Arial', 12, 'bold'))
title.pack(pady=20)

frame = LabelFrame(window, padx=5, pady=10)
frame.pack()


def setValues(newValues):
    # keys = list(values.keys())
    # for i in range(4):
    #     values[keys[i]] = float(lst[i])
    #     AllElements[i].delete(0, END)
    #     AllElements[i].insert(0, lst[i])

    # for i in range(4, 15):
    #     values[keys[i]] = float(lst[i])
    #     AllElements[i].set(lst[i])
    for k, v in newValues.items():
        values[k] = float(v)
        if type(AllElements[k]) is Scale:
            AllElements[k].set(v)
        else:
            AllElements[k].delete(0, END)
            AllElements[k].insert(0, v)


def loadFromTextInput():
    a = entryAlfa.get().strip()
    e = entryEpsilon.get().strip()
    c = entryC.get().strip()
    t = entryT.get().strip()
    if any(i == '' for i in [a, e, c, t]):
        messagebox.showerror('Błąd', 'Pola tekstowe nie mogą być puste.')
        return False
    values['alpha'] = float(a)
    values['epsilon'] = float(e)
    values['c'] = float(c)
    values['t'] = float(t)
    return True

# def getValues():
#     lst = []
#     for i in range(0, 4):
#         lst.append(str(AllElementsToGet[i].get()))

#     for i in range(4, 15):
#         lst.append(str(AllElementsToGet[i].cget('text')))

#     return lst


def resetToDefault():
    entryAlfa.delete(0, END)
    entryC.delete(0, END)
    entryT.delete(0, END)
    entryEpsilon.delete(0, END)

    setValues(DEFAULT)


def run():
    # TODO
    pass


def getGraph():
    # TODO
    pass


def sliderOper(v):
    beta = float(sliderBeta.get())
    gamma = float(sliderGamma.get())
    delta = float(sliderDelta.get())
    sum = beta + gamma + delta
    if sum != 0:
        labelBeta.config(text=str(round(beta/sum, 3)))
        values['reproduction'] = beta/sum
        labelGamma.config(text=str(round(gamma/sum, 3)))
        values['crossbread'] = gamma/sum
        labelDelta.config(text=str(round(delta/sum, 3)))
        values['mutate'] = delta/sum


def sliderChan(v):
    cost = float(sliderChCost.get())
    trans = float(sliderChTrans.get())
    use = float(sliderChU.get())
    sum = cost + trans + use
    if sum != 0:
        labelChCost.config(text=str(round(cost/sum, 3)))
        values['k1'] = cost / sum
        labelChTrans.config(text=str(round(trans/sum, 3)))
        values['k2'] = trans / sum
        labelChU.config(text=str(round(use/sum, 3)))
        values['k3'] = use / sum


def sliderProc(v):
    cheapTask = float(sliderProcCheapTask.get())
    fastTask = float(sliderProcFastTask.get())
    tk = float(sliderProcTK.get())
    asbef = float(sliderProcAsBef.get())
    use = float(sliderProcUse.get())

    sum = cheapTask + fastTask + tk + asbef + use
    if sum != 0:
        labelProcCheapTask.config(text=str(round(cheapTask/sum, 3)))
        values['o1'] = cheapTask / sum
        labelProcFastTask.config(text=str(round(fastTask/sum, 3)))
        values['o2'] = fastTask / sum
        labelProcTK.config(text=str(round(tk/sum, 3)))
        values['o3'] = tk / sum
        labelProcAsBef.config(text=str(round(asbef/sum, 3)))
        values['o4'] = asbef / sum
        labelProcUse.config(text=str(round(use/sum, 3)))
        values['o5'] = use / sum


def openConfig():
    name = filedialog.askopenfilename(
        title='Wybierz plik',
        filetypes=(("all files", "*.*"),)).strip()
    if name not in ['', '\n']:
        textGetFile.delete('1.0', END)
        textGetFile.insert(END, name)
    return name


def chooseToLoadConfig():
    name = filedialog.askopenfilename(
        title='Wybierz plik do wczytania',
        filetypes=(("ini files", "*.ini"),
                   ("all files", "*.*"))).strip()
    if name not in ['', '\n']:
        textGetFile.delete('1.0', END)
        textGetFile.insert(END, name)
    return name


def loadConfig():
    name = textGetFile.get(1.0, END).strip()
    if name in ['', '\n']:
        name = chooseToLoadConfig()
        if name in ['', '\n']:
            return
    config = ConfigParser()
    config.read(name)
    setValues(config['Values'])


def chooseToSaveConfig():
    name = filedialog.asksaveasfilename(
        title='Wybierz plik zapisu',
        filetypes=(("ini files", "*.ini"),)).strip()
    print(repr(name))
    if name != '\n':
        textSaveFile.delete('1.0', END)
        textSaveFile.insert(END, name)
    return name


def saveConfig():
    name = textSaveFile.get(1.0, END).strip()
    if name in ['', '\n']:
        name = chooseToSaveConfig()
        if name in ['', '\n']:
            return
    if not loadFromTextInput():
        return
    config = ConfigParser()
    config['Values'] = values
    with open(name, 'w') as f:
        config.write(f)


def chooseGraph():
    window.saveChooseGraph = filedialog.askopenfilename(
        title='Wybierz plik',
        filetypes=(("txt files", "*.txt"),
                   ("all files", "*.*")))
    textChooseGraph.delete('1.0', END)
    textChooseGraph.insert(END, window.saveChooseGraph)


# Buttons

ButtonDefault = Button(
    frame,
    text='Przywróć domyślne',
    font=('Arial', 11, 'bold'),
    command=resetToDefault)
ButtonDefault.grid(row=8, column=0, sticky='w', padx=18)

ButtonStart = Button(
    frame,
    text='Rozpocznij',
    font=('Arial', 11, 'bold'),
    command=run)
ButtonStart.grid(row=8, column=1, sticky='e', padx=10)

quitButton = Button(
    frame,
    text="Zakończ",
    font=('Arial', 11, 'bold'),
    command=window.quit)
quitButton.grid(row=8, column=2, sticky='e', padx=10)

# Entry Labels
# ALFA
frameAlfa = LabelFrame(frame, text='Wartość parametru (alfa)')
frameAlfa.grid(row=0, column=0, padx=20, pady=20)
entryAlfa = Entry(frameAlfa, width=20, borderwidth=5)
entryAlfa.pack(padx=5)

# EPSILON
frameEpsilon = LabelFrame(frame, text='Wartość parametru epsilon')
frameEpsilon.grid(row=1, column=0, padx=20, pady=10)
entryEpsilon = Entry(frameEpsilon, width=20, borderwidth=5)
entryEpsilon.pack()

# C/T
frameCT = LabelFrame(frame, text='Funkcja F=c*koszt+t*czas')
frameCT.grid(row=3, column=0, rowspan=4, padx=10, pady=5, sticky='n')

frameC = LabelFrame(frameCT, text='Wartość parametru c')
frameC.grid(row=1, column=0, padx=12, pady=13)
entryC = Entry(frameC, width=18, borderwidth=5)
entryC.pack()

frameT = LabelFrame(frameCT, text='Wartość parametru t')
frameT.grid(row=2, column=0, padx=12, pady=13)
entryT = Entry(frameT, width=18, borderwidth=5)
entryT.pack()

# Operator Sliders

frameSld = LabelFrame(frame, text='Rozwiązania otrzymane poprzez')
frameSld.grid(row=0, column=1, rowspan=3, pady=10, padx=10)

sliderBeta = Scale(frameSld, label='Operator Selekcji:',
                   from_=0, to=1, resolution=0.01,
                   orient=HORIZONTAL,
                   length=250,
                   showvalue=0,
                   command=sliderOper)
sliderBeta.grid(row=0, column=0, pady=5)

sliderGamma = Scale(frameSld, label='Operator Krzyżowania:',
                    from_=0, to=1, resolution=0.01,
                    orient=HORIZONTAL,
                    length=250,
                    showvalue=0,
                    command=sliderOper)
sliderGamma.grid(row=1, column=0, pady=5)

sliderDelta = Scale(frameSld, label='Operator Mutacji:',
                    from_=0, to=1, resolution=0.01,
                    orient=HORIZONTAL,
                    length=250,
                    showvalue=0,
                    command=sliderOper)
sliderDelta.grid(row=2, column=0, pady=5)


# Operator Sliders Label

labelBeta = Label(frameSld, text='0', width=5)
labelBeta.grid(row=0, column=1)

labelGamma = Label(frameSld, text='0', width=5)
labelGamma.grid(row=1, column=1)

labelDelta = Label(frameSld, text='0', width=5)
labelDelta.grid(row=2, column=1)


# Channels Sliders

frameChan = LabelFrame(frame, text='Dla zasobów komunikacyjnych:')
frameChan.grid(row=3, column=1, rowspan=4, pady=5, padx=10, sticky='n')

sliderChCost = Scale(frameChan, label='Najmniejszy wzrost kosztu:',
                     from_=0, to=1, resolution=0.01,
                     orient=HORIZONTAL,
                     length=250,
                     showvalue=0,
                     command=sliderChan)
sliderChCost.grid(row=0, column=0, pady=5)

sliderChTrans = Scale(frameChan, label='Najszybsza transmisja:',
                      from_=0, to=1, resolution=0.01,
                      orient=HORIZONTAL,
                      length=250,
                      showvalue=0,
                      command=sliderChan)
sliderChTrans.grid(row=1, column=0, pady=5)

sliderChU = Scale(frameChan, label='Najrzadziej używany:',
                  from_=0, to=1, resolution=0.01,
                  orient=HORIZONTAL,
                  length=250,
                  showvalue=0,
                  command=sliderChan)
sliderChU.grid(row=2, column=0, pady=5)


# Operator Sliders Label

labelChCost = Label(frameChan, text='0', width=5)
labelChCost.grid(row=0, column=1)

labelChTrans = Label(frameChan, text='0', width=5)
labelChTrans.grid(row=1, column=1)

labelChU = Label(frameChan, text='0', width=5)
labelChU.grid(row=2, column=1)


# Proc Sliders

frameProc = LabelFrame(frame, text='Dla zasobów obliczeniowych:')
frameProc.grid(row=0, column=2, rowspan=5, pady=10, padx=20)

sliderProcCheapTask = Scale(frameProc, label='Najtańsza impl. zadań:',
                            from_=0, to=1, resolution=0.01,
                            orient=HORIZONTAL,
                            length=250,
                            showvalue=0,
                            command=sliderProc)
sliderProcCheapTask.grid(row=0, column=0, pady=5)

sliderProcFastTask = Scale(frameProc, label='Najszybsza impl. zadań:',
                           from_=0, to=1, resolution=0.01,
                           orient=HORIZONTAL,
                           length=250,
                           showvalue=0,
                           command=sliderProc)
sliderProcFastTask.grid(row=1, column=0, pady=5)

sliderProcTK = Scale(frameProc, label='Najmniejsze t*k:',
                     from_=0, to=1, resolution=0.01,
                     orient=HORIZONTAL,
                     length=250,
                     showvalue=0,
                     command=sliderProc)
sliderProcTK.grid(row=2, column=0, pady=5)

sliderProcAsBef = Scale(frameProc, label='Jak dla poprzednika:',
                        from_=0, to=1, resolution=0.01,
                        orient=HORIZONTAL,
                        length=250,
                        showvalue=0,
                        command=sliderProc)
sliderProcAsBef.grid(row=3, column=0, pady=5)

sliderProcUse = Scale(frameProc, label='Najmniej obciążone:',
                      from_=0, to=1, resolution=0.01,
                      orient=HORIZONTAL,
                      length=250,
                      showvalue=0,
                      command=sliderProc)
sliderProcUse.grid(row=4, column=0, pady=5)


# Operator Sliders Label

labelProcCheapTask = Label(frameProc, text='0', width=5)
labelProcCheapTask.grid(row=0, column=1)

labelProcFastTask = Label(frameProc, text='0', width=5)
labelProcFastTask.grid(row=1, column=1)

labelProcTK = Label(frameProc, text='0', width=5)
labelProcTK.grid(row=2, column=1)

labelProcAsBef = Label(frameProc, text='0', width=5)
labelProcAsBef.grid(row=3, column=1)

labelProcUse = Label(frameProc, text='0', width=5)
labelProcUse.grid(row=4, column=1)


# Open Config

frameSaveOpenConfig = LabelFrame(
    frame, text='Zapisz/Wczytaj plik z parametrami', pady=4)
frameSaveOpenConfig.grid(row=5, column=2, rowspan=3, pady=10, padx=10)

labelOdczyt = Label(frameSaveOpenConfig, text="Plik do odczytu:")
labelOdczyt.grid(row=0, column=0, sticky='w', pady=5)

buttonOdczyt = Button(frameSaveOpenConfig, text="Wczytaj",
                      width=6, command=loadConfig)
buttonOdczyt.grid(row=0, column=1)

buttonGetFile = Button(frameSaveOpenConfig, text="...",
                       command=openConfig, width=6)
buttonGetFile.grid(row=1, column=1, padx=3)

sBarGetFile = Scrollbar(frameSaveOpenConfig, orient=HORIZONTAL)
sBarGetFile.grid(row=2, column=0, sticky='we')

textGetFile = Text(frameSaveOpenConfig,
                   width=32,
                   height=1,
                   xscrollcommand=sBarGetFile.set,
                   wrap='none')
textGetFile.grid(row=1, column=0)

sBarGetFile.config(command=textGetFile.xview)

# Save Config

labelSave = Label(frameSaveOpenConfig, text="Plik do zapisu:")
labelSave.grid(row=3, column=0, sticky='w', pady=5)

buttonOdczyt = Button(frameSaveOpenConfig, text="Zapisz",
                      width=6, command=saveConfig)
buttonOdczyt.grid(row=3, column=1)

buttonSaveFile = Button(frameSaveOpenConfig, text="...",
                        width=6, command=chooseToSaveConfig)
buttonSaveFile.grid(row=4, column=1, padx=3)

sBarSaveFile = Scrollbar(frameSaveOpenConfig, orient=HORIZONTAL)
sBarSaveFile.grid(row=5, column=0, sticky='we')

textSaveFile = Text(frameSaveOpenConfig,
                    width=32,
                    height=1,
                    xscrollcommand=sBarSaveFile.set,
                    wrap='none')
textSaveFile.grid(row=4, column=0)

sBarSaveFile.config(command=textSaveFile.xview)


# Choose graph

frameChooseGraph = LabelFrame(frame, text='Wczytaj Graf')
frameChooseGraph.grid(row=7, column=0, columnspan=2,
                      pady=10, padx=10, sticky='e')

labelChooseGraph = Label(frameChooseGraph, text="Wybierz Plik:")
labelChooseGraph.grid(row=0, column=0, sticky='w', pady=5)

buttonOdczyt = Button(frameChooseGraph, text="Wczytaj",
                      width=6, command=getGraph)
buttonOdczyt.grid(row=0, column=1)

buttonChooseGraph = Button(
    frameChooseGraph, text="...", width=6, command=chooseGraph)
buttonChooseGraph.grid(row=1, column=1, padx=3)

sBarChooseGraph = Scrollbar(frameChooseGraph, orient=HORIZONTAL)
sBarChooseGraph.grid(row=2, column=0, sticky='we')

textChooseGraph = Text(frameChooseGraph,
                       width=54,
                       height=1,
                       xscrollcommand=sBarChooseGraph.set,
                       wrap='none')
textChooseGraph.grid(row=1, column=0)

sBarChooseGraph.config(command=textChooseGraph.xview)

# Elem Lst

AllElements = {
    'alpha': entryAlfa,
    'epsilon': entryEpsilon,
    'c': entryC,
    't': entryT,
    'reproduction': sliderBeta,
    'crossbread': sliderGamma,
    'mutate': sliderDelta,
    'k1': sliderChCost,
    'k2': sliderChTrans,
    'k3': sliderChU,
    'o1': sliderProcCheapTask,
    'o2': sliderProcFastTask,
    'o3': sliderProcTK,
    'o4': sliderProcAsBef,
    'o5': sliderProcUse,
}


if __name__ == "__main__":
    resetToDefault()
    window.mainloop()

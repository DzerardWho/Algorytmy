genesProbability = None

taskData = None

# alpha * len(taskData.graph) * len(taskData.proc)
populationSize = None
reproduction = None
crossbread = None
mutate = None

# epsilon
stagnationLimit = None

constC = None
constT = None

__doc__ = """Plik przechowujący konfigurację potrzebną do działąnia reszty
programu.

Wartości:
    genesProbability (List[List[float]]): Lista prawdopodobieństw wyboru
        poszczególnych genów
    taskData (TaskData): Obiekt przechowujący informacje o zadaniu
    populationSize (int): rozmiar populacji
    reproduction (int): rozmiar populacji stworzonej w wyniku operatora
        selekcji
    crossbread (int): rozmiar populacji stworzonej w wyniku operatora
        krzyżowania
    mutate (int): rozmiar populacji stworzonej w wyniku operatora mutacji
    stagnationLimit (int): liczba generacji, po których algorytm zostanie
        przerwany, jeżeli nie zostanie znalezione lepsze rozwiązanie
    constC (int): stała do obliczania fitFunction
    constT (int): stała do obliczania fitFunction
"""

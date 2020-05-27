# Zadanie 11
Program testowany na systemie windows z zainstalowanym python'em 3.7.6  

## Przykładowe wywołanie programu
> python main.py graf.a

## Opis programu
  Program wczytuje graf z podanego pliku a następnie za pomocą algorytmu Dijkstry wyszukuje najkrótszą ścieżke od zadanego węzłą początkowego.

## Wynik działania dla przykładu
```
Cost: 25
Path: T0->T2->T4
```

#### Szczegóły uruchamiania
```
usage: main.py [-h] [-s S] file

positional arguments:
  file        plik do wczytania

optional arguments:
  -h, --help  show this help message and exit
  -s S        Numer węzła początkowego[domyślnie 0]
```
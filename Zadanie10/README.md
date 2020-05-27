# Zadanie 10
Program testowany na systemie windows z zainstalowanym python'em 3.7.6  

## Przykładowe wywołanie programu
> python main.py graf_10_1.txt  

## Opis programu
  Program wczytuje graf z podanego pliku a następnie szereguje listowo zadania w grafie i wypisuje je.

## Wynik działania dla przykładu
```
['T0', 'T1', 'T2', 'T5', 'T6', 'T8', 'T4', 'T3', 'T7', 'T9']
```


#### Szczegóły uruchamiania
```
usage: main.py [-h] [-p P] [-c C] file

positional arguments:
  file        plik do wczytania

optional arguments:
  -h, --help  show this help message and exit
  -p P        Numer zasobu do wykorzystania[domyślnie 0]
  -c C        Numer kanalu do transmisji[domyślnie 0]
```
Kamil Gierada

Zawartość:
    1.  Program znajduje składniki sumy podanej liczby z podanego przedziału. Stosuje algorytm genetyczny z selekcją rankingową.
        1) main.py              - główny program
        2) genetic.py           - plik zawierający klasę algorytmu genetycznego

Jak uruchomić:

```
usage: main.py [-h] [-v] [-g GENERATIONS] [-p POPULATION] [-s SELECT] [-c CLONE] [-m MUTATE] [-b] [-i]

Program znajduje liczby z zadanego przedziału, które sumują się do podanej liczby. Stosowany jest algorytm genetyczny. Używany selektor: selektor rankingowy.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Wypisuj informacje o kolejnych generacjach.
  -g GENERATIONS, --generations GENERATIONS
                        Maksymalna liczba generacji.
  -p POPULATION, --population POPULATION
                        Rozmiar populacji.
  -s SELECT, --select SELECT
                        Rozmiar populacji, która ma zostać użyta do stowrzenia nowej generacji.
  -c CLONE, --clone CLONE
                        Z jakim prawdopodobieństwem ma nowy genotym zostać stworzony w wyniku klonowania. Przedział [0, 20].
  -m MUTATE, --mutate MUTATE
                        Z jakim prawdopodobieństwem ma nowy genotym zostać stworzony w wyniku mutacji. Przedział [0, 20].
  -b, --printBest       Wypisz genotyp najlepszego wyniku w przypadku niepowodzenia.
  -i, --info            Wypisz ustawienia.
```

Wymagania:

W przypadku uruchamiania za pomocą pythona
- Python > 3.7
- Moduł `numpy` (`pip install numpy`)
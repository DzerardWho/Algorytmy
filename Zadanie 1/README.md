Kamil Gierada

Zawartość:
    1.  Program generuje drzewo rozpięte z danych z pliku podanego przy uruchomieniu
        1) main.py              - główny program
        2) Graph/node.py        - plik zawierający implementację węzła wymaganego przez graf i drzewo
        3) Graph/graph.py       - plik zawierający implementację grafu
        4) Graph/tree.py        - plik zawierający implementację drzewa
        5) GRAPH.10             - przykładowe dane
        6) GRAPH-WEIGHTS.10     - przykładowe dane
        7) GRAPH.30             - przykładowe dane
        8) Tree-builder.exe     - program wynikowy

Wymagany format danych wejściowych:

```
@tasks [liczba]
[etykieta_wierzchołka] [liczba_sąsiednich_wierzchołków] [indeks_wierzchołka(waga_krawędzi)]*[indeks_wierzchołka(waga_krawędzi)]
[etykieta_wierzchołka] [liczba_sąsiednich_wierzchołków] [indeks_wierzchołka(waga_krawędzi)]*[indeks_wierzchołka(waga_krawędzi)]
...
[etykieta_wierzchołka] [liczba_sąsiednich_wierzchołków] [indeks_wierzchołka(waga_krawędzi)]*[indeks_wierzchołka(waga_krawędzi)]
@[ciąg dalszy pliku...]
```

Jak uruchomić:

```
usage: Tree-builder.exe [-h] [-o [OUT]] [-og [OUTGRAPH]] [-g] [file]
usage: python main.py [-h] [-o [OUT]] [-og [OUTGRAPH]] [-g] [file]

Na podstawie danych z pliku wygeneruj graf, a z niego drzewo rozpięte.

positional arguments:
  file                  Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa rozpinającego. Dane wyjściowe są zapisywane
                        do plików .gv w języku "dot" i wymagany jest program "Graphviz" w celu wygenerowania grafu w formie graficznej.
                        Kolejne wierzchołki powinny być w formacie:
                            etykieta liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*liczba_wierzchołków

optional arguments:
  -h, --help            show this help message and exit
  -o [OUT], --out [OUT]
                        Nazwa docelowa pliku wyjściowego drzewa
  -og [OUTGRAPH], --outGraph [OUTGRAPH]
                        Nazwa docelowa pliku wyjściowego grafu. Jeżeli zapisywanie grafu jest wyłączone, argument jest pomijany.
  -g, --graph           Zapisz graf do pliku.
```

Wymagania:

W przypadku uruchamiania za pomocą pythona
- Python > 3.7
- Pakiet `graphviz` (`pip install graphviz`)
- Program [`Graphviz`](https://www.graphviz.org/)

W przypadku uruchamiania za pomocą pliku 8):
- Program [`Graphviz`](https://www.graphviz.org/)
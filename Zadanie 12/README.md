Kamil Gierada

Zawartość:
    1.  Program znajduje najkrótszą ścieżkę w grafie za pomocą algorytmu Dijkstry.
        1) main.py              - główny program
        2) channel.py           - plik zawierający klasę do przechowywania danych o kanałach komunikacyjnych
        3) proc.py              - plik zawierający klasę do przechowywania danych związanych z procesami
        4) graphData.py         - plik zawierający klasę do przechowywania danych o grafie zadań wczytanych z tekstu
        5) graphPaths.py        - plik zawierający klasy związane z operowaniem na ścieżkach
        6) Graph/node.py        - plik zawierający implementację węzła wymaganego przez graf
        7) Graph/graph.py       - plik zawierający implementację grafu
        8) Graph/Tree/node.py   - plik zawierający implementację węzła wymaganego przez drzewo
        9) Graph/Tree/tree.py   - plik zawierający implementację drzewa
        10) GRAPH.10            - przykładowe dane
        11) GRAPH.20            - przykładowe dane
        12) test.6              - przykładowe dane
        13) t1.txt              - przykładowe dane z ćwiczeń
        14) t2.txt              - przykładowe dane z ćwiczeń
        15) t3.txt              - przykładowe dane z ćwiczeń

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
usage: main.py [-h] file

Program znajduje najkrótszą ścieżkę w grafie za pomocą algorytmu Dijkstry.

positional arguments:
  file        Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa rozpinającego. Kolejne wierzchołki powinny być w formacie: etykieta liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*liczba_wierzchołków

optional arguments:
  -h, --help  show this help message and exit
```

Wymagania:

W przypadku uruchamiania za pomocą pythona
- Python > 3.7
- Pakiet `numpy` (`pip install numpy`)
- Pakiet `graphviz` (`pip install graphviz`)
- Program [`Graphviz`](https://www.graphviz.org/)

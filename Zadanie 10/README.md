Kamil Gierada

Zawartość:
    1.  Program szereguje zadania dla poszczególnego zasobu za pomocą algorytmu listowego.
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
usage: main.py [-h] [-p [PROC]] [-c [CHANN]] file

Program generuje szereg algorytmów za pomocą algorytmu listwego

positional arguments:
  file                  Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa rozpinającego. Kolejne wierzchołki powinny być w formacie: etykieta liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*liczba_wierzchołków

optional arguments:
  -h, --help            show this help message and exit
  -p [PROC], --proc [PROC]
                        Wybór zasobu
  -c [CHANN], --chann [CHANN]
                        Wybór kanału
```

Wymagania:

W przypadku uruchamiania za pomocą pythona
- Python > 3.7
- Pakiet `numpy` (`pip install numpy`)
- Pakiet `graphviz` (`pip install graphviz`)
- Program [`Graphviz`](https://www.graphviz.org/)

Kamil Gierada

Zawartość:
    1.  Program wczytuje z pliku graf oraz tworzy minimalne drzewo rozpinające za pomocą algorytmów Kurskala i Prima.
        1) main.py              - główny program
        2) Graph/node.py        - plik zawierający implementację węzła wymaganego przez graf
        3) Graph/graph.py       - plik zawierający implementację grafu
        4) Graph/Tree/node.py   - plik zawierający implementację węzła wymaganego przez drzewo
        5) Graph/Tree/tree.py   - plik zawierający implementację drzewa
        6) GRAPH.10             - przykładowe dane
        7) GRAPH.20             - przykładowe dane
        8) GRAPH_CYCLE.20       - przykładowe dane

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

Program wczytuje z pliku graf oraz tworzy minimalne drzewo rozpinające za pomocą algorytmów Kurskala i Prima.

positional arguments:
  file        Ścieżka do pliku zawierającego dane do stworzenia grafu i drzewa rozpinającego. Kolejne wierzchołki powinny być w formacie: etykieta liczba_wierzchołków indeks_wierzchołka(waga_krawędzi)*liczba_wierzchołków

optional arguments:
  -h, --help  show this help message and exit
```

Wymagania:

W przypadku uruchamiania za pomocą pythona
- Python > 3.7
- Pakiet `graphviz` (`pip install graphviz`)
- Program [`Graphviz`](https://www.graphviz.org/)

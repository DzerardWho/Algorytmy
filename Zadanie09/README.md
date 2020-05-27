# Zadanie 9
Program testowany na systemie windows z zainstalowanym python'em 3.7.6  
Jeśli została zainstalowana biblioteka graphviz oraz pliki [GraphViz2.38](https://www.graphviz.org/) znajdują się w PATH  
To grafy zamiast zostać wyświetlone na konsoli zostaną wygenerowane do obrazów

## Przykładowe wywołanie programu
> python main.py < graf_20_1.txt

## Opis programu
  Program wypisuje wczytany graf, graf po zastosowaniu algorutmu Kruskala oraz po zastosowaniu algorytmu Prima

## Wynik działania dla przykładu
#### Graf Wczytany
![Loaded](viz/loaded.gv.png "Loaded")
#### Kruskal
![Kruskal](viz/kruskal.gv.png "Kruskal")
#### Prim
![Prim](viz/prim.gv.png "Prim")
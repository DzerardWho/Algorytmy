Autor: Anna Grochal  
21.05.2020

Algorytm Dijkstry służy do wyszukiwania najkrótszej ścieżki między dwoma 
wierzchołkami. W tym przypadku najkrósze ścieżki są wyszukiwane pomiędzy korzeniem
a każdym innym wierzchołkiem.
Polega on na tym, że po dotarciu do wierzchołka jakąś ścieżką, sprawdzana jest 
waga tej ścieżki i jeśli jest on mniejsza niż dotychczasowa, to ta ścieżka jest 
najkrótsza.

======================

Program został napisany w Pythonie 3.8, aby go uruchomić, należy w terminalu 
wpisać komendę
` python dijkstra 1`
parametr 1 określa numer grafu wejściowego.
W tym przypadku można wybrać 1 lub 2

Przykładowe wywołanie programu:
>python dijkstra 2
>
graph: with 6 edges  
Node T0, children: ['T1', 'T2']  
Node T1, children: ['T5']  
Node T2, children: ['T3', 'T4']  
Node T3, children: ['T5']  
Node T4, children: []  
Node T5, children: []  

ścieżka:
0
waga:
0

ścieżka:
0 1
waga:
12

ścieżka:
0 2
waga:
24

ścieżka:
0 2 3
waga:
30

ścieżka:
0 2 4
waga:
30

ścieżka:
0 1 5
waga:
30


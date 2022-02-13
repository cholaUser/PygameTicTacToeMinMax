## Informacje ogólne

- Repozytorium związane jest z grą kółko i krzyżyk z algorytmem min_max. 
Wykorzystano moduł pygame.

## Sterowanie

- Wykonanie ruchu we wskazanym miejscu - dowolny przycisk myszy.
- Wykonanie ruchu przez program z wykorzystaniem algorytmu min_max - 
dowolny przycisk klawiatury.

## Wykorzystana grafika

- Załączone pliki - "O.png", "X.png" powinny znajdować się w katalogu "assets".

## Zmiana rozmiaru planszy (nie ilości pól)

- Należy zmienić "stałe" WIDTH,HEIGHT oraz LINEW (grubość linii).
WIDTH i HEIGHT powinny być równe i podzielne przez 3.

## Min-max

- Jest to metoda minimalizowania maksymalnych możliwych strat.
Alternatwnie – maksymalizacja minimalnego zysku. Metoda ta zakłada,
że przeciwnik zagra możliwie najlepiej – zatem właściwym posunięciem
jest minimalizacja zysków przeciwnika.

## Lista funkcji

- main() - główna funkcja, która uruchamia program
- start_game() - funkcja zaczynająca nową grę
- move_human() - funkcja związana z ruchem użytkownika
- move_ai() - funkcja związana z ruchem komputera
- check_win() - funkcja sprawdzająca czy nastąpiła wygrana jednego z graczy
- check_tie() - funkcja sprawdzająca czy nastąpił remis
- evaluation_func() - funkcja określająca jak dobra jest pozycja graczy 
w danym momencie gry
- min_max() - funkcja min_max - zwraca najlepsze posunięcie

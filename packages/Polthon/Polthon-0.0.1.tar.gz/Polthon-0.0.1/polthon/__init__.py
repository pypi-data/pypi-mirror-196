wydrukuj = print
nic = str
unosic_sie = float
calosc = int
zasieg = range
szesciopak = abs
najmniej = min
najwiencej = max
to_samo = lambda x,y: x == y
inne = lambda x,y: x != y
wieksze_niz = lambda x,y: x > y
mniejsze_niz = lambda x,y: x < y
rowne_lub_wieksze_niz = lambda x,y: x >= y
rowne_lub_mniejsze_niz = lambda x,y: x <= y
lub = lambda x,y: x or y
oraz = lambda x,y: x and y
w = lambda x,y: x in y
drobne_z_dywizji_rowne = lambda x,y,z:x % y == z
def potega(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik ** i
def drobne(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik % i
def dodaj(**zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik + i
def odejmij(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik - i
def dywizjuj(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik / i
def dywizjuj_calosc(*zmienne):
    wynik = 0
    for i in zmienne:
        wynik = wynik // i
wykonaj_dzialanie = eval
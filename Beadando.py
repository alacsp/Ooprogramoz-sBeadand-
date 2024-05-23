import tkinter as tk
from tkinter import Menu, messagebox
from datetime import datetime,timedelta
from abc import ABC, abstractmethod

# Osztályok létrehozás
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self._ar = None
        self._szobaszam = None
        self.set_ar(ar)
        self.set_szobaszam(szobaszam)

    def get_ar(self):
        return self._ar

    def set_ar(self, value):
        if value <= 0:
            raise ValueError("Az árnak pozitív számnak kell lennie.")
        self._ar = value

    def get_szobaszam(self):
        return self._szobaszam

    def set_szobaszam(self, value):
        if value <= 0:
            raise ValueError("A szobaszámnak pozitív számnak kell lennie.")
        self._szobaszam = value

    @abstractmethod
    def get_tipus(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def get_tipus(self):
        return "Egyágyas"

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def get_tipus(self):
        return "Kétágyas"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def add_szoba(self, szoba):
        if any(sz.get_szobaszam() == szoba.get_szobaszam() for sz in self.szobak):
            raise ValueError("A szállodában már van ilyen számú szoba.")
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szalloda, szoba, datum):
        self.szalloda = szalloda
        self.szoba = szoba
        self.datum = datum

class FoglalasKezelo:
    def __init__(self):
        self.szallodak = []
        self.foglalasok = []

    def add_szalloda(self, szalloda):
        if any(s.nev == szalloda.nev for s in self.szallodak):
            raise ValueError("Már létezik ilyen nevű szálloda.")
        self.szallodak.append(szalloda)

    def foglal_szoba(self, szalloda_nev, szobaszam, datum):
        szalloda = next((s for s in self.szallodak if s.nev == szalloda_nev), None)
        if szalloda is None:
            return "Nincs ilyen szálloda."
        
        if datum <= datetime.today().date():
            return "Dátum már elmúlt"
        
        for foglalas in self.foglalasok:
            if foglalas.szoba.get_szobaszam() == szobaszam and foglalas.datum == datum:
                return "A szoba már foglalt"
        
        for szoba in szalloda.szobak:
            if szoba.get_szobaszam() == szobaszam:
                uj_foglalas = Foglalas(szalloda, szoba, datum)
                self.foglalasok.append(uj_foglalas)
                return f"Foglalás sikeres! Ár: {szoba.get_ar()} Ft"
        return "Nincs ilyen szoba."

    def lemond_foglalas(self, szalloda_nev, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szalloda.nev == szalloda_nev and foglalas.szoba.get_szobaszam() == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return "Foglalás lemondva."
        return "Nincs ilyen foglalás."

    def listaz_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        result = "Foglalások listája:\n"
        for foglalas in self.foglalasok:
            result += f"Szálloda: {foglalas.szalloda.nev}, Szoba száma: {foglalas.szoba.get_szobaszam()}, Dátum: {foglalas.datum}\n"
        return result

    def listaz_szallodak_szobak(self):
        if not self.szallodak:
            return "Nincsenek szállodák."
        result = "Szállodák listája szobákkal:\n"
        for szalloda in self.szallodak:
            result += f"Szálloda: {szalloda.nev}\n"
            for szoba in szalloda.szobak:
                result += f"  Szoba száma: {szoba.get_szobaszam()}, Ár: {szoba.get_ar()} Ft, Típus: {szoba.get_tipus()}\n"
        return result


def update_szalloda_menu(menu):
    menu['menu'].delete(0, 'end')
    for szalloda in foglalaskezelo.szallodak:
        menu['menu'].add_command(label=szalloda.nev, command=tk._setit(szalloda_var, szalloda.nev))

def foglalas_felvetel():
    try:
        szalloda_nev = szalloda_var.get()
        szobaszam = int(szobaszam_entry.get())
        datum = datetime.strptime(datum_entry.get(), "%Y-%m-%d").date()
        eredmeny = foglalaskezelo.foglal_szoba(szalloda_nev, szobaszam, datum)
        eredmeny_label.config(text=eredmeny)
    except ValueError:
        eredmeny_label.config(text="Hiba: Érvénytelen adat.")

def foglalas_lemondas():
    try:
        szalloda_nev = szalloda_var.get()
        szobaszam = int(szobaszam_entry.get())
        datum = datetime.strptime(datum_entry.get(), "%Y-%m-%d").date()
        eredmeny = foglalaskezelo.lemond_foglalas(szalloda_nev, szobaszam, datum)
        eredmeny_label.config(text=eredmeny)
    except ValueError:
        eredmeny_label.config(text="Hiba: Érvénytelen adat.")

def foglalasok_listazasa():
    eredmeny = foglalaskezelo.listaz_foglalasok()
    eredmeny_label.config(text=eredmeny)

def szallodak_listazasa():
    eredmeny = foglalaskezelo.listaz_szallodak_szobak()
    eredmeny_label.config(text=eredmeny)

def szalloda_hozzaadasa():
    szerkeszto_ablak = tk.Toplevel(r)
    szerkeszto_ablak.geometry("400x200")
    szerkeszto_ablak.title("Új Szálloda Hozzáadása")

    szalloda_nev_label = tk.Label(szerkeszto_ablak, text="Szálloda neve:")
    szalloda_nev_label.pack(pady=5)
    szalloda_nev_entry = tk.Entry(szerkeszto_ablak)
    szalloda_nev_entry.pack(pady=5)

    def uj_szalloda():
        try:
            nev = szalloda_nev_entry.get()
            if nev:
                szalloda = Szalloda(nev)
                foglalaskezelo.add_szalloda(szalloda)
                messagebox.showinfo("Siker", f"Szálloda '{nev}' hozzáadva!")
                update_szalloda_menu(szalloda_menu)
            else:
                messagebox.showerror("Hiba", "A szálloda neve nem lehet üres.")
        except ValueError as e:
            messagebox.showerror("Hiba", str(e))

    szalloda_button = tk.Button(szerkeszto_ablak, text="Új Szálloda", command=uj_szalloda)
    szalloda_button.pack(pady=10)

def szoba_hozzaadasa():
    szerkeszto_ablak = tk.Toplevel(r)
    szerkeszto_ablak.geometry("400x400")
    szerkeszto_ablak.title("Új Szoba Hozzáadása")

    szalloda_nev_label = tk.Label(szerkeszto_ablak, text="Szálloda neve:")
    szalloda_nev_label.pack(pady=5)
    
    szalloda_var_add = tk.StringVar(szerkeszto_ablak)
    szalloda_menu_add = tk.OptionMenu(szerkeszto_ablak, szalloda_var_add, *[szalloda.nev for szalloda in foglalaskezelo.szallodak])
    szalloda_menu_add.pack(pady=5)

    szoba_ar_label = tk.Label(szerkeszto_ablak, text="Szoba ára:")
    szoba_ar_label.pack(pady=5)
    szoba_ar_entry = tk.Entry(szerkeszto_ablak)
    szoba_ar_entry.pack(pady=5)

    szoba_szam_label = tk.Label(szerkeszto_ablak, text="Szoba szám:")
    szoba_szam_label.pack(pady=5)
    szoba_szam_entry = tk.Entry(szerkeszto_ablak)
    szoba_szam_entry.pack(pady=5)

    szoba_tipus_label = tk.Label(szerkeszto_ablak, text="Szoba típusa:")
    szoba_tipus_label.pack(pady=5)
    szoba_tipus_var = tk.StringVar(value="egyagyas")
    tk.Radiobutton(szerkeszto_ablak, text="Egyágyas", variable=szoba_tipus_var, value="egyagyas").pack(pady=5)
    tk.Radiobutton(szerkeszto_ablak, text="Kétágyas", variable=szoba_tipus_var, value="ketagyas").pack(pady=5)

    def uj_szoba():
        try:
            nev = szalloda_var_add.get()
            szalloda = next((s for s in foglalaskezelo.szallodak if s.nev == nev), None)
            if szalloda is None:
                messagebox.showerror("Hiba", "Nincs ilyen szálloda.")
                return
            
            ar = int(szoba_ar_entry.get())
            szobaszam = int(szoba_szam_entry.get())
            szoba_tipus = szoba_tipus_var.get()
            if szoba_tipus == "egyagyas":
                szoba = EgyagyasSzoba(ar, szobaszam)
            else:
                szoba = KetagyasSzoba(ar, szobaszam)
            szalloda.add_szoba(szoba)
            messagebox.showinfo("Siker", f"Szoba hozzáadva a '{nev}' szállodához!")
        except ValueError as e:
            messagebox.showerror("Hiba", str(e))

    szoba_button = tk.Button(szerkeszto_ablak, text="Új Szoba", command=uj_szoba)
    szoba_button.pack(pady=10)

def pelda_hozzaadasa():
    try:
            pelda_szalloda = Szalloda("Példa Szálloda")
            pelda_szalloda.add_szoba(EgyagyasSzoba(10000, 101))
            pelda_szalloda.add_szoba(KetagyasSzoba(15000, 102))
            pelda_szalloda.add_szoba(KetagyasSzoba(15000, 103))
            foglalaskezelo.add_szalloda(pelda_szalloda)
            pelda_szalloda = Szalloda("Példa Szálloda2")
            pelda_szalloda.add_szoba(EgyagyasSzoba(10000, 201))
            pelda_szalloda.add_szoba(KetagyasSzoba(15000, 202))
            pelda_szalloda.add_szoba(KetagyasSzoba(15000, 203))
            foglalaskezelo.add_szalloda(pelda_szalloda)
            datum = datetime.today().date() + timedelta(days=1)
            foglalaskezelo.foglal_szoba("Példa Szálloda", 101, datum)
            foglalaskezelo.foglal_szoba("Példa Szálloda", 102, datum + timedelta(days=1))
            foglalaskezelo.foglal_szoba("Példa Szálloda", 103, datum + timedelta(days=2))
            foglalaskezelo.foglal_szoba("Példa Szálloda", 101, datum + timedelta(days=3))
            foglalaskezelo.foglal_szoba("Példa Szálloda", 102, datum + timedelta(days=4))
            update_szalloda_menu(szalloda_menu)
            messagebox.showinfo("Siker", "Példa Szálloda hozzáadva!")
    except ValueError as e:
            messagebox.showerror("Hiba", str(e))

# Kezelöfelület létrehozása
foglalaskezelo = FoglalasKezelo()


r = tk.Tk()
r.geometry("400x800")
r.title('Szálloda intéző')

menu = Menu(r)
r.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Új Szálloda Hozzáadása', command=szalloda_hozzaadasa)
filemenu.add_command(label='Új Szoba Hozzáadása', command=szoba_hozzaadasa)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=r.quit)

frame = tk.Frame(r)
frame.pack(pady=20)

szalloda_label = tk.Label(frame, text="Szálloda neve:")
szalloda_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')

szalloda_var = tk.StringVar()
szalloda_menu = tk.OptionMenu(frame, szalloda_var, "")
szalloda_menu.grid(row=0, column=1, padx=10, pady=5, sticky='w')

szobaszam_label = tk.Label(frame, text="Szoba szám:")
szobaszam_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
szobaszam_entry = tk.Entry(frame)
szobaszam_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

datum_label = tk.Label(frame, text="Dátum (YYYY-MM-DD):")
datum_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
datum_entry = tk.Entry(frame)
datum_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

foglalas_button = tk.Button(frame, text="Foglalás", command=foglalas_felvetel)
foglalas_button.grid(row=3, column=0, padx=10, pady=5, sticky='e')

lemondas_button = tk.Button(frame, text="Lemondás", command=foglalas_lemondas)
lemondas_button.grid(row=3, column=1, padx=10, pady=5, sticky='w')

listazas_button = tk.Button(frame, text="Foglalások Listázása", command=foglalasok_listazasa)
listazas_button.grid(row=4, column=0, columnspan=2, pady=5)

szallodak_listazas_button = tk.Button(frame, text="Szállodák Listázása", command=szallodak_listazasa)
szallodak_listazas_button.grid(row=5, column=0, columnspan=2, pady=5)

peldaszobak_button = tk.Button(frame, text="Példaszálloda hozzáadása", command=pelda_hozzaadasa)
peldaszobak_button.grid(row=6, column=0, columnspan=2, pady=5)

eredmeny_label = tk.Label(r, text="")
eredmeny_label.pack(pady=20)

r.mainloop()

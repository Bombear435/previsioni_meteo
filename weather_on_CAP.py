from bs4 import BeautifulSoup
import requests
from sys import exit
import keyboard
from time import sleep, strftime


def ask_CAP():
    zip_code = input("Inserisci il tuo CAP: ")
    if not zip_code.isnumeric() or (int(zip_code) < 1): # faccio le CE sul CAP
        exit("CAP non valido.")
    return zip_code


def ask_city(CAP):
    try:
        city_html = requests.get("https://zip-codes.nonsolocap.it/cap?c=&k=" + CAP)   # get request per trovare una città a quel CAP
    except:                                # la get deve andare a buon fine
        exit("Controllare la propria connessione e riprovare.")
        
    city_soup = BeautifulSoup(city_html.text, "html.parser")
    cities = city_soup.select(".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)")

    if cities:                        # se esiste un paese che corrisponde al CAP
        return cities[0].text   # prendo la prima città che trovo
    else:                            # altrimenti rip
        exit("CAP non valido. Controlla di aver digitato bene.")


def find_meteo(city):
    try:
        meteo_html = requests.get("https://www.ilmeteo.it/meteo/" + city.replace(' ', '+')) # cerco su ilmeteo.it
    except:                                      # la get deve andare a buon fine
        exit("Controllare la propria connessione e riprovare.")
        
    meteo_soup = BeautifulSoup(meteo_html.text, "html.parser")
    ora = input("Quale orario ti interessa? (Tra le 0 e le 23): ")         # l'ora serve in formato da 24
    tempo = meteo_soup.select("#h" + ora + "-" + strftime("%d").replace("0", "") + "-1 > td:nth-child(3)") # cerco il tempo in base all'ora      

    if tempo:
        print("Alle ore " + ora + " è previsto " + tempo[0].text + ".")
    elif not ora.isnumeric():                                                             # se è invalida   
        exit("Ora inserita invalida.")
    elif (int(ora) < 24) and (int(ora) >= 0):                                        # se è già passata
        exit("Sembra che ques'ora sia già passata.")


def routine(citta):
    if not citta:
        citta = ask_city(ask_CAP())         # trovo la citta a partire dal cap
    find_meteo(citta)                             # trovo il meteo a partire dalla citta
    replay(citta)                                    # chiedo se si vuole continuare 


def replay(citta):
    sleep(0.35)                       # pausa per evitare che vengano contati tasti precedentemente premuti
    print("Se si desidera continuare premere 'S': ") 
    choice_1 = keyboard.read_key(suppress=True)
    if choice_1 == 's':             # se si preme s
        sleep(0.35)                  # pausa per evitare sia contata la s anche per i passaggi dopo
        print("Premere 'O' se si vuole cambiare l'ora,\nPremere 'C' se si vuole cambiare codice postale,\nPremere qualsiasi altro tasto se si vuole terminare la sessione.")
        choice_2 = keyboard.read_key(suppress=True)
        if choice_2 == 'o':     
            routine(citta)            # se si preme o rimane la citta di prima
        elif choice_2 == 'c':
            routine('')                 # se si preme c si riparte da capo
            
    else:                               # se non si ha premuto s
        print("Arrivederci!")


if __name__ == "__main__":
    routine('')

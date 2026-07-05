import urllib.request
import urllib.error
from datetime import datetime
import time

URL = "https://www.google.com" 
SLA = 99.5
MKosten = 50

def Webcheck(url):
    
    anfrage = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        ping = urllib.request.urlopen(anfrage, timeout=9)
        if ping.status == 200:
            return True, "OK" 
    except Exception as e:
        return False, str(e) 
    return False, "Unbekannter Fehler"

def KostenRechner(a_down, e_down, MKosten):
    sekunden = (e_down - a_down).total_seconds()
    Minuten = sekunden / 60
    Schaden = MKosten * Minuten
    return Minuten, Schaden

def main():
    Website_Online = True
    Downtime_Start = None 
    g_pings = 0
    e_pings = 0

    print(f"Starte Monitoring für {URL}...\n")

    try:
        while True: 
            g_pings = g_pings + 1
            
            ist_online, fehlermeldung = Webcheck(URL)

            if ist_online:
                e_pings = e_pings + 1 

                if not Website_Online:
                    downtime_ende = datetime.now()
                    Minuten, Schaden = KostenRechner(Downtime_Start, downtime_ende, MKosten)
                    print(f"Website {URL} ist wieder Online!")
                    print(f"-> Website war down für {Minuten:.2f} Minuten. Schaden: {Schaden:.2f} €\n")
                    
                    Website_Online = True
                    Downtime_Start = None
                else:
                    print(f"Website ist online (SLA: {(e_pings/g_pings)*100:.2f}%)")
            
            else:
                if Website_Online: 
                    Downtime_Start = datetime.now() 
                    Website_Online = False
                    print(f"Website DOWN! Grund: {fehlermeldung}")
                else:
                    print("Website ist weiterhin DOWN...")

            print("-" * 40)
            time.sleep(10) 
            
    except KeyboardInterrupt:
        print("\nMonitoring beendet.")

if __name__ == "__main__":
    main()

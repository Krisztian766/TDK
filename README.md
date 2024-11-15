


Hálózati és Weboldal Tesztelő

Ez a Python alkalmazás lehetővé teszi a felhasználók számára, hogy szkenneljék a hálózati eszközeiket, ellenőrizzék a portokat és teszteljék a weboldalak elérhetőségét. A program grafikus felhasználói felületet (GUI) kínál a hálózati biztonság egyszerű tesztelésére és az eredmények exportálására.
Funkciók

    Hálózati eszközök szkennelése: Az alkalmazás ARP szkennelést végez, hogy megtalálja a helyi hálózaton elérhető eszközöket (IP és MAC címek).
    Port szkennelés: Ellenőrzi az általánosan használt portok (pl. 22, 80, 443) állapotát és a lehetséges sebezhetőségeket.
    Weboldal tesztelés: Lehetővé teszi a felhasználók számára, hogy HTTP/HTTPS weboldalakat teszteljenek, és információkat nyújtson a válasz kódról, IP címről és válaszidőről.
    Eredmények exportálása: A program lehetőséget ad az eredmények exportálására szöveges fájlba.

    Telepítés

A program futtatásához szükséges a következő Python könyvtárak telepítése:

    PyQt5 – A grafikus felhasználói felülethez
    scapy – A hálózati szkenneléshez
    psutil – A helyi hálózati interfész információkhoz
    requests – Weboldal teszteléshez
    ipaddress – IP címek kezeléséhez

Telepítés:

pip install pyqt5 scapy psutil requests

Használat

    Hálózati eszközök szkennelése:
        Adja meg az IP tartományt (pl. 192.168.1.0/24) vagy válassza az automatikus észlelést a helyi hálózathoz.
        Kattintson a "Szkennelés" gombra, hogy megtalálja az aktív eszközöket.

    Port szkennelés:
        Miután elvégezte a hálózati eszközök szkennelését, válasszon egy IP címet a listából.
        Kattintson a "Port szkennelés" gombra, hogy ellenőrizze a kiválasztott IP portjait és azok sebezhetőségeit.

    Weboldal tesztelés:
        Adja meg a weboldal URL-jét, majd kattintson a "Weboldal teszt" gombra.
        Az alkalmazás megjeleníti a válasz időt, a válasz kódot és egyéb adatokat.

    Eredmények exportálása:
        Kattintson az "Eredmények exportálása" gombra, és válasszon egy fájlt, ahová elmentheti a teszt eredményeit.

  Kódban használt főbb könyvtárak

    PyQt5 – GUI fejlesztéshez
    scapy – Hálózati szkenneléshez
    psutil – A helyi hálózati interfészek információinak kezeléséhez
    requests – HTTP/HTTPS weboldal elérhetőség ellenőrzéséhez
    socket – Hálózati kapcsolat kezelése
    time – Időzítéshez
    ipaddress – IP címek kezeléséhez

Hibaelhárítás

    Nem található a hálózati interfész: Ellenőrizze, hogy megfelelően van-e csatlakozva a hálózathoz (Wi-Fi vagy Ethernet).
    Weboldal nem elérhető: Ha a weboldal nem válaszol, próbálja meg újra később vagy ellenőrizze az URL-t.
    Port szkennelés nem működik: Bizonyos portok tűzfal által lehetnek blokkolva.

    

import sys
import socket
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QTextEdit, QProgressBar, QFileDialog
from PyQt5.QtGui import QTextCursor, QColor
from PyQt5.QtCore import Qt
import scapy.all as scapy
import ipaddress
import requests
import time

common_ports = [22, 80, 443, 21, 25, 110, 143, 3389, 8080, 53]
vulnerabilities = {
    22: "SSH - Elavult verziók könnyen kihasználhatók.",
    80: "HTTP - HTTPS-re kellene átállni, hogy elkerüljük az adatok lehallgatását.",
    443: "HTTPS - Ha nem megfelelően konfigurált, lehetőség van SSL/TLS támadásokra.",
    21: "FTP - Titkosítatlan adatátvitel, jelszavak könnyen lehallgathatók.",
    25: "SMTP - Lehetőség van spam küldésére, ha nincs megfelelően biztosítva.",
    110: "POP3 - Titkosítatlan kommunikáció, érzékeny adatok támadásoknak vannak kitéve.",
    143: "IMAP - Lehetőség van adatok szivárgására titkosítatlan kapcsolat esetén.",
    3389: "RDP - Brute force támadásokkal sebezhető.",
    8080: "HTTP alternatív port - Még akkor is nyitva lehet, ha az alapértelmezett 80-as portot lezárták.",
    53: "DNS - DNS Cache poisoning lehetséges, ha nincs megfelelően konfigurálva."
}

def check_http_https(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "Hiba: Kérem, adjon meg egy teljes URL-t a http:// vagy https:// előtaggal."

    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = round((time.time() - start_time) * 1000)
        domain = url.split("//")[1].split("/")[0]
        ip_address = socket.gethostbyname(domain)

        if response.status_code == 200:
            result = (f"URL: {url}\n"
                      f"IP cím: {ip_address}\n"
                      f"HTTP válasz kód: {response.status_code} (OK)\n"
                      f"Válasz idő: {response_time} ms\n"
                      f"Tartalom típusa: {response.headers.get('Content-Type', 'N/A')}\n"
                      f"Szerver: {response.headers.get('Server', 'N/A')}\n")
        else:
            result = f"Hiba történt a weboldal elérésében."
        return result

    except socket.gaierror:
        return "Hiba: A domain nem található. Ellenőrizze az URL-t."
    except requests.exceptions.RequestException as e:
        return f"{url} nem elérhető! Hiba: {e}"

class NetworkScanner:
    def __init__(self, target):
        self.target = target

    def scan_arp(self):
        arp_request = scapy.ARP(pdst=self.target)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        client_list = []
        for response in answered_list:
            client_dict = {"IP": response[1].psrc, "MAC": response[1].hwsrc}
            client_list.append(client_dict)
        return client_list

def scan_ports(target, common_ports, progress_bar):
    result_text = ""
    for i, port in enumerate(common_ports):
        progress_bar.setValue(int((i+1) / len(common_ports) * 100))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        
        if result == 0:
            result_text += f"<font color='green'>{port} port nyitva - Sebezhetőség: {vulnerabilities.get(port, 'Nincs adat a sebezhetőségről.')}</font><br>"
        else:
            result_text += f"<font color='red'>{port} port zárva</font><br>"
        
        s.close()

    return result_text

def get_local_network(interface="Wi-Fi"):
    interfaces = psutil.net_if_addrs()
    if interface in interfaces:
        ip_address = interfaces[interface][1].address
        subnet_mask = interfaces[interface][1].netmask
        network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
        network_range = f"{network.network_address}/{network.prefixlen}"
        return network_range
    return None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hálózati és Weboldal Tesztelő")
        self.layout = QVBoxLayout()

        # Beállítások
        self.ip_label = QLabel("Adja meg az IP tartományt (pl.: 192.168.0.0/24):")
        self.layout.addWidget(self.ip_label)

        self.ip_entry = QLineEdit()
        self.layout.addWidget(self.ip_entry)

        self.url_label = QLabel("Adja meg a weboldal URL-jét (pl. http://example.com):")
        self.layout.addWidget(self.url_label)

        self.url_entry = QLineEdit()
        self.layout.addWidget(self.url_entry)

        self.network_interface_label = QLabel("Válassza ki a hálózati interfészt (Wi-Fi vagy Ethernet):")
        self.layout.addWidget(self.network_interface_label)

        self.network_interface_combobox = QComboBox()
        self.network_interface_combobox.addItems(["Wi-Fi", "Ethernet"])
        self.layout.addWidget(self.network_interface_combobox)

        self.auto_detect_button = QPushButton("Auto észlelés")
        self.auto_detect_button.clicked.connect(self.auto_detect)
        self.layout.addWidget(self.auto_detect_button)

        self.scan_button = QPushButton("Szkennelés")
        self.scan_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.scan_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.message_label = QLabel("")
        self.layout.addWidget(self.message_label)

        self.ip_list_widget = QListWidget()
        self.layout.addWidget(self.ip_list_widget)

        self.port_scan_button = QPushButton("Port szkennelés")
        self.port_scan_button.setEnabled(False)
        self.port_scan_button.clicked.connect(self.scan_selected_ports)
        self.layout.addWidget(self.port_scan_button)

        self.port_scan_result_label = QTextEdit()
        self.port_scan_result_label.setReadOnly(True)
        self.layout.addWidget(self.port_scan_result_label)

        self.website_test_button = QPushButton("Weboldal teszt")
        self.website_test_button.clicked.connect(self.test_website)
        self.layout.addWidget(self.website_test_button)

        self.website_test_result_label = QLabel("")
        self.layout.addWidget(self.website_test_result_label)

        self.export_button = QPushButton("Eredmények exportálása")
        self.export_button.clicked.connect(self.export_results)
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)

    def start_scan(self):
        target = self.ip_entry.text()  
        if not target:
            self.message_label.setText("Kérem adjon meg egy IP tartományt vagy válassza az 'Auto' opciót a helyi hálózathoz.")
            return

        self.ip_entry.setEnabled(False)
        self.scan_button.setEnabled(False)
        self.progress_bar.setValue(0)

        scanner = NetworkScanner(target)
        scan_result = scanner.scan_arp()
        self.ip_list_widget.clear()
        for client in scan_result:
            self.ip_list_widget.addItem(f"{client['IP']} - {client['MAC']}")

        self.ip_entry.setEnabled(True)
        self.scan_button.setEnabled(True)
        self.port_scan_button.setEnabled(True)

    def scan_selected_ports(self):
        selected_ips = self.ip_list_widget.selectedIndexes()
        if not selected_ips:
            self.message_label.setText("Kérem válasszon ki legalább egy IP címet.")
            return

        self.port_scan_result_label.clear()
        for selected_ip_index in selected_ips:
            selected_ip = self.ip_list_widget.item(selected_ip_index.row()).text().split(" ")[0]
            self.port_scan_result_label.append(f"<b>Szkennelés: {selected_ip}...</b>")
            result_text = scan_ports(selected_ip, common_ports, self.progress_bar)
            self.port_scan_result_label.append(result_text)

    def test_website(self):
        url = self.url_entry.text()
        if not url:
            self.message_label.setText("Kérem adja meg a weboldal URL-jét.")
            return

        result = check_http_https(url)
        self.website_test_result_label.setText(result)

    def auto_detect(self):
        interface = self.network_interface_combobox.currentText()
        network_range = get_local_network(interface)

        if network_range:
            self.ip_entry.setText(network_range)
            self.start_scan()
        else:
            self.message_label.setText("Nem található megfelelő hálózati interfész.")

    def export_results(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Eredmények exportálása", "", "Szöveges fájl (*.txt)")
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.port_scan_result_label.toPlainText())
                f.write("\n")
                f.write(self.website_test_result_label.text())
                self.message_label.setText(f"Eredmények exportálva ide: {file_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

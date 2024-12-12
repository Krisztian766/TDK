Network and Website Tester

This Python application allows users to scan their network devices, check ports, and test the availability of websites. The program provides a graphical user interface (GUI) for easy network security testing and exporting the results.

Features:

 Network Device Scanning:
    The application performs ARP scanning to find devices on the local network (IP and MAC addresses).

Port Scanning:
    Checks the status of commonly used ports (e.g., 22, 80, 443) and possible vulnerabilities.

 Website Testing:
    Allows users to test HTTP/HTTPS websites and provides information on response code, IP address, and response time.

Export Results:
    The program provides the option to export the results to a text file.

To run the program, you need to install the following Python libraries:
pip install pyqt5 scapy psutil requests

Usage:

Network Device Scanning:

 Enter the IP range (e.g., 192.168.1.0/24) or select automatic detection for the local network.
    Click the "Scan" button to find active devices.

Port Scanning:

After completing the network device scan, select an IP address from the list.
    Click the "Port Scan" button to check the selected IP's ports and possible vulnerabilities.

Website Testing:

 Enter the website URL and click the "Website Test" button.
    The application will display the response time, response code, and other details.

Export Results:

 Click the "Export Results" button and choose a file where you can save the test results.

Main Libraries Used in the Code:

PyQt5: For GUI development
    scapy: For network scanning
    psutil: For handling local network interface information
    requests: For HTTP/HTTPS website availability checks
    socket: For handling network connections
    time: For timing purposes
    ipaddress: For managing IP addresses

Troubleshooting:

 Network interface not found:
    Check if you are properly connected to the network (Wi-Fi or Ethernet).

Website not available:
    If the website does not respond, try again later or check the URL.

Port scanning not working:
    Certain ports may be blocked by a firewall.

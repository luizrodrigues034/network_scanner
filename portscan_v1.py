#!/usr/bin/env python3

import socket
import argparse
import threading
import sys
import regex as re
from time import perf_counter 

vermelho = "\033[31m"
verde = "\033[32m"
reset = "\033[0m"

regex_ipv4 = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def defaul_ports() -> list:
    ports = []
    with open("./common-web-ports.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                ports.append(int(line))
    return ports


def reverse_dns(tgt_ip) -> str:
    try:
        tgt_name = socket.gethostbyaddr(tgt_ip)
        return tgt_name[0]
    except: 
        return "DNS Reverso falhou"

def dns_resolver(tgt_name) -> str:
    try:
        tgt_ip = socket.gethostbyname(tgt_name)
        return tgt_ip
    except: 
        return None

def scan_port(host: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0) 
        
        if sock.connect_ex((host, port)) == 0:
            print(f"[{verde}*{reset}] Port {port} is open")
            try:
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n') 
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    print(f"   |-> Banner: {banner[:50]}...") 
            except:
                pass
        sock.close()
    except:
        pass

def main():
    parser = argparse.ArgumentParser(
        description="Scanner de Portas Simples",
        epilog="Exemplo: python3 script.py -H google.com -P 80,443"
    )
    parser.add_argument("-H", "--host", required=True, help="Host ou IP a ser escaneado")
    parser.add_argument("-P", "--port", default=defaul_ports(), help="Portas (separadas por vírgula)")
    parser.add_argument("-R", "--reverse-resolver", action="store_true", help="Tenta DNS Reverso")
    
    args = parser.parse_args()


    target_ip = args.host
    
    if re.match(regex_ipv4, args.host):

        print(f"Target IP: {args.host}")
        if args.reverse_resolver:
            print(f"Hostname: {reverse_dns(args.host)}")
    else:

        resolved_ip = dns_resolver(args.host)
        if resolved_ip:
            print(f"Domain: {args.host}")
            print(f"Resolved IP: {resolved_ip}")
            target_ip = resolved_ip 
        else:
            print(f"[{vermelho}!{reset}] Não foi possível resolver o domínio {args.host}")
            sys.exit(1)

    port_list = []
    try:
        if isinstance(args.port, list):
            port_list = args.port 
        else:
            
            raw_ports = args.port.split(',')
            
            for item in raw_ports:
                if "-" in item:
                    
                    start, end = map(int, item.split('-'))
                    port_list.extend(range(start, end + 1))
                else:
                    
                    port_list.append(int(item))

    except ValueError:
        print(f"[{vermelho}!{reset}] Erro: Formato de porta inválido. Use ex: 80 ou 1-100")
        sys.exit(1)

    start_time = perf_counter()
    
    threads = []
    count = 0

    for port in port_list:
        count+=1
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    end_time = perf_counter()
    print(f"\nScan finalizado em: {(end_time - start_time):.4f}s")
    print(f"POrtas escaneadas: {count}")

if __name__ == "__main__":
    main()
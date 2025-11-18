#!/bin/python3

import socket
import argparse
import threading
import ipaddress
import sys
from time import perf_counter 
import regex as re

vermelho = "\033[31m"
verde = "\033[32m"
reset = "\033[0m"
regex_ipv4 = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def main():


    parser = argparse.ArgumentParser(
    description="Scanner de Portas Simples",
    epilog="Exemplo: python script.py -H 192.168.0.1 -P 80"
)
    parser.add_argument("-H","--host",help="Host a ser escaneado")
    parser.add_argument("-P", "--port", help="Porta a ser escaneada.Multiplas portas: <PORT>,<PORT>,<PORT>,<PORT>")
    parser.add_argument("-R", "--reverse-resolver", action="store_true", help="Tenta descobrir o nome do host (DNS Reverso)")
    
    args = parser.parse_args()



    if args.host is None or args.port is None:
        print(parser.print_help())
        sys.exit(1)

    try:
        threads = []
        port_list = [int(p) for p in args.port.split(",")]
        if re.match(regex_ipv4, args.host) and args.reverse_resolver:
            print(f"Scan no host:{args.host}")
            print(f"Name:{reverse_dns(args.host)}")

        elif(not re.match(regex_ipv4, args.host)): 
            print(f"Domain:{args.host}")
            print(f"Target Ip:{dns_resolver(args.host)}")
        else:
            print(f"Scan no host:{args.host}")
        
        start_time = perf_counter()
        
        for port in port_list:
            thread = threading.Thread(target=scan_port, args=(args.host, port))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        
        end_time = perf_counter()
        print(f"Scan finalizado em: {(end_time - start_time):.4f}s")

    except Exception as error:
        print(f"[{vermelho}*{reset}]Erro ocorrido:{error}")


def scan_port(host:str,port:int) ->list:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    if sock.connect_ex((host,port)) == 0:
        print(f"[{verde}*{reset}]Port {port} is open")
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            print(f"Banner: {banner}")
        except:
            pass
        
                  
    sock.close()


def reverse_dns(tgt_ip)-> str:
    try:
        tgt_name = socket.gethostbyaddr(tgt_ip)
        return tgt_name[0]
    except: 
        return "Não foi possivel resolver o dns"


def dns_resolver(tgt_name)->str or None:
    try:
        tgt_ip = socket.gethostbyname(tgt_name)
    
        return tgt_ip
    
    except: 
        return "Não foi possivel resolver o dns"
    
if __name__ == "__main__":
    main()
#!/bin/python3

import socket
import argparse
import threading
import ipaddress
import sys
from time import perf_counter 

vermelho = "\033[31m"
verde = "\033[32m"
reset = "\033[0m"

def main():
    
    parser = argparse.ArgumentParser(
    description="Scanner de Portas Simples",
    epilog="Exemplo: python script.py -H 192.168.0.1 -P 80"
)
    parser.add_argument("-H","--host",help="Host a ser escaneada")
    parser.add_argument("-P", "--port",type=int, help="Porta a ser escaneada")

    args = parser.parse_args()
    if args.host is None or args.port is None:
        print(parser.print_help())
        sys.exit(1)
    try:    
        scan_port(args.host, args.port)
        
    except Exception as error:
        print(f"[{vermelho}*{reset}]Erro ocorrido:{error}")


def scan_port(host:str,port:int):
    start_time = perf_counter()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("teste")
    if sock.connect_ex((host,port)) == 0:
        print(f"[{verde}*{reset}]Port {port} is open")
        end_time = perf_counter()
        print(f"[{verde}*{reset}]Scanning time:{(start_time - end_time):.4f}")
    sock.close()
    
if __name__ == "__main__":
    main()
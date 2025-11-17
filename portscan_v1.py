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
    parser.add_argument("-H","--host",help="Host a ser escaneado")
    parser.add_argument("-P", "--port", help="Porta a ser escaneada.Multiplas portas: <PORT>,<PORT>,<PORT>,<PORT>")
    args = parser.parse_args()



    if args.host is None or args.port is None:
        print(parser.print_help())
        sys.exit(1)
    
    # elif not ipaddress.ip_address(args.host):
    #     try:
    #         tgt_ip = resolve_dns(args.host)
    
    #     except:
    #         print("[*] Invalid host!")
    
    # else:
    #     try:
    #         tgt_name = resolve_reverse_dns(args.host)
    #     except:
    #         continue
    try:
        
        threads = []
        port_list = [int(p) for p in args.port.split(",")]

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


def scan_port(host:str,port:int):
    # start_time = perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex((host,port)) == 0:
        print(f"[{verde}*{reset}]Port {port} is open")
                  
    sock.close()
    # end_time = perf_counter()
    # print(f"[{verde}*{reset}]Scanning time:{(start_time - end_time):.4f}")

    
if __name__ == "__main__":
    main()
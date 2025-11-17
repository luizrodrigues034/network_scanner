#!/bin/python3
import socket
import argparse


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def scan_port(host:str,port:int):
    if sock.connect_ex((host,port)):#connect_ex() retorna connect_ex em erro(true), e 0 se conseguir conectar
        print(f"Connection on port {port} refused")
    else:
         print(f"Connection on port {port} accepted")
    sock.close()
        
parser = argparse.ArgumentParser(description="É necessario especificar o host e a porta a ser escaneada")

parser.add_argument("host",help="Host a ser escaneado")
parser.add_argument("port",type=int, help="Porta a ser escaneado")

args = parser.parse_args()



scan_port(args.host, args.port)

#!/usr/bin/env python3

from colors import Style
from Subnetting import Subnetting
import operations
from gsheets import GSheets

from signal import signal, SIGINT
from sys import exit
import re

def signal_handler(signal_received, frame):
    exit(1)

def main():
    signal(SIGINT, signal_handler)
    run()

def run():
    ip_rangos = {}
    
    while True:
        ip = input("Introduce la IP inicial: ")
        match = re.fullmatch("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)

        if match is None:
            print(f"{Style.BOLD}{Style.RED}Introduce una IP válida!{Style.RESET}\n")
        else:
            del match
            break


    while True:
        redes = input("Cuantas redes habrá?: ")
        redes = int(redes) if redes.isdigit() else redes

        if type(redes) == str:
            print(f"{Style.BOLD}{Style.RED}Introduce una cantidad válida!{Style.RESET}\n")
        elif redes == 0:
            print(f"{Style.BOLD}{Style.RED}Seguro?{Style.RESET}\n")
        else:
            break

    gs = GSheets("Examen", 0)

    for i in range(redes):
        print(f"\n{Style.BOLD}{Style.GREEN}------------------------------{Style.RESET}")
        print(f"{Style.BOLD}{Style.GREEN}Red {i + 1}{Style.RESET}")
        
        subnetting = Subnetting(ip)

        ips = input("Cuantas IPs son necesarias?: ")
        
        potencia = subnetting.potencia((int(ips)))
        mascara_bin = subnetting.mascara_nueva(potencia)
        mascara_dec = subnetting.mascara_decimal(mascara_bin)
        salto = subnetting.salto_pos(mascara_bin)[0]
        posicion = subnetting.salto_pos(mascara_bin)[1]

        print(potencia)
        print(mascara_bin)
        print(mascara_dec)
        print(salto)
        print(posicion)

        for i in range(redes):
            limite_inf = gs.get_cellvalue(2 + i, 2)
            limite_sup = gs.get_cellvalue(2 + i, 5)
            print(limite_inf)
            print(limite_sup)
            if limite_inf == None or limite_sup == None: break


        # red_num = input("Red utilizable (int): ")

        # for red in range(red_num - 1):
        #     id_red = suma(ip, salto)


        print(f"\n{Style.BLUE}Impresion{Style.RESET}")
        print(f"{Style.BOLD}{Style.GREEN}------------------------------{Style.RESET}\n")

if __name__ == "__main__":
    main()

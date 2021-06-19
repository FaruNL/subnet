#!/usr/bin/env python3

from colors import Style
from Subnetting import Subnetting
from operations import int_to_ip, ip_to_int, suma, suma_salto, resta
from gsheets import GSheets

from signal import signal, SIGINT
from sys import exit
import re

ips_dict = dict()

def signal_handler(signal_received, frame):
    exit(1)

def main():
    signal(SIGINT, signal_handler)
    run()

def lectura_datos(rep, gs):
    limite_inf = ip_to_int(gs.get_cellvalue(2 + rep, 2))
    limite_sup = ip_to_int(gs.get_cellvalue(2 + rep, 5))

    ips_dict[limite_inf] = limite_sup

def ordenar_ips():
    global ips_dict

    dict_items = ips_dict.items()
    ips_ordenadas = sorted(dict_items)

    ips_dict = __list_into_dict(ips_ordenadas)

def __list_into_dict(list) -> dict:
    it = iter(list)
    r_dict = dict(zip(it, it))
    return r_dict

def primera_vez(gs, ip, salto, posicion, mascara):
    red_disp = input("Que red disponible?: ")
    nueva_ip = ip

    if int(red_disp) > 1:
        for i in range(int(red_disp) - 1):
            nueva_ip = suma_salto(ip, salto, posicion)
    
    primera_red = suma(nueva_ip, 1)
    broadcast = resta(suma_salto(nueva_ip, salto, posicion), 1)
    ultima_red = resta (broadcast, 1)

    gs.set_cellvalue("B2", nueva_ip)
    gs.set_cellvalue("C2", primera_red)
    gs.set_cellvalue("D2", ultima_red)
    gs.set_cellvalue("E2", broadcast)
    gs.set_cellvalue("F2", mascara)

    lectura_datos(0, gs)
    print(ips_dict)

def continuacion(rep, gs, ip, salto, posicion, mascara, ips_max):
    global ips_dict

    red_disp = input("Que red disponible?: ")
    nueva_ip = ip

    print(f"\nSalto: {salto}\nPos: {posicion}\nIPs_max: {ips_max}\n")

    lectura_datos(rep, gs)
    ordenar_ips()
    print(ips_dict)
    
    for i in range(rep):
        print("+++++++")
        limite_inf = ip_to_int(gs.get_cellvalue(2 + i, 2))
        limite_sup = ip_to_int(gs.get_cellvalue(2 + i, 5))
        
        check = ip_to_int(nueva_ip)
        
        
        while(limite_inf <= check <= limite_sup):
            print(f"{int_to_ip(limite_inf)} <= {int_to_ip(check)} <= {int_to_ip(limite_sup)}")
            nueva_ip = suma_salto(nueva_ip, salto, posicion)
            check = ip_to_int(nueva_ip)
            print(f"Check: {int_to_ip(check)}")
        
        # if limite_inf == None or limite_sup == None: break

    if int(red_disp) > 1:
        for i in range(int(red_disp) - 1):
            print("otra mas")
            nueva_ip = suma_salto(nueva_ip, salto, posicion)
    
    primera_red = suma(nueva_ip, 1)
    broadcast = resta(suma_salto(nueva_ip, salto, posicion), 1)
    ultima_red = resta (broadcast, 1)

    gs.set_cellvalue("B" + str(2 + rep), nueva_ip)
    gs.set_cellvalue("C" + str(2 + rep), primera_red)
    gs.set_cellvalue("D" + str(2 + rep), ultima_red)
    gs.set_cellvalue("E" + str(2 + rep), broadcast)
    gs.set_cellvalue("F" + str(2 + rep), mascara)

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

    for red in range(redes):
        print(f"\n{Style.BOLD}{Style.GREEN}------------------------------{Style.RESET}")
        print(f"{Style.BOLD}{Style.GREEN}Red {red + 1}{Style.RESET}")
        
        subnetting = Subnetting(ip)

        ips = input("Cuantas IPs son necesarias?: ")
        
        ips_max = subnetting.ips_max(int(ips))
        potencia = subnetting.potencia(int(ips))
        mascara_bin = subnetting.mascara_nueva(potencia)
        mascara_dec = subnetting.mascara_decimal(mascara_bin)
        salto = subnetting.salto_pos(mascara_bin)[0]
        posicion = subnetting.salto_pos(mascara_bin)[1]

        if red == 0:
            primera_vez(gs, ip, salto, posicion, mascara_dec)
        else:
            continuacion(red, gs, ip, salto, posicion, mascara_dec, ips_max)

        

        print(f"\n{Style.BLUE}Impresion{Style.RESET}")
        print(f"{Style.BOLD}{Style.GREEN}------------------------------{Style.RESET}\n")

if __name__ == "__main__":
    main()

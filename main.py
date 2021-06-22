#!/usr/bin/env python3

from subnetting import ips_max, potencia, mascara_nueva, mascara_decimal, salto_pos
from operations import int_to_ip, ip_to_int, suma, suma_salto, resta
from gsheets import GSheets
from colorama import init, deinit, Fore, Style

from os import path
from signal import signal, SIGINT
from sys import exit, argv
from re import fullmatch

ips_dict = dict()

def signal_handler(signal_received, frame):
    deinit()
    exit(1)

def main():
    init(autoreset=True)
    signal(SIGINT, signal_handler)
    run()
    deinit()
    


def lectura_datos(rep, gs):
    limite_inf = ip_to_int(gs.get_cellvalue(2 + rep, 2))
    limite_sup = ip_to_int(gs.get_cellvalue(2 + rep, 5))

    ips_dict[limite_inf] = limite_sup

def ordenar_ips(ips_dict):
    dict_items = ips_dict.items()
    ips_ordenadas = sorted(dict_items)

    return dict(ips_ordenadas)

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

def continuacion(rep, gs, ip, salto, posicion, mascara, ips_max):
    global ips_dict

    red_disp = input("Que red disponible?: ")
    nueva_ip = ip

    print(f"\n{Style.BRIGHT}Salto: {Style.RESET_ALL}{salto}\n{Style.BRIGHT}Pos: {Style.RESET_ALL}{posicion}\n{Style.BRIGHT}IPs_max: {Style.RESET_ALL}{ips_max}\n")

    red_disp_ok = 0
    error = False

    check = ip_to_int(nueva_ip)
    check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))

    while red_disp_ok < int(red_disp):
        for i in ips_dict.items():
            if check >= i[0] and check <= i[1]:
                print(f"{Style.DIM}{Fore.BLUE}{int_to_ip(i[0])}{Style.RESET_ALL} <- {Style.BRIGHT}{Fore.RED}{int_to_ip(check)}{Style.RESET_ALL} -> {Style.DIM}{Fore.BLUE}{int_to_ip(i[1])}{Style.RESET_ALL} <- {Style.BRIGHT}{Fore.RED}{int_to_ip(check_last)}{Style.RESET_ALL}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check >= i[0] and check_last <= i[1]:
                print(f"{Style.DIM}{Fore.BLUE}{int_to_ip(i[0])}{Style.RESET_ALL} <- {Style.BRIGHT}{Fore.RED}{int_to_ip(check)}{Style.RESET_ALL} -- {Style.BRIGHT}{Fore.RED}{int_to_ip(check_last)}{Style.RESET_ALL} -> {Style.DIM}{Fore.BLUE}{int_to_ip(i[1])}{Style.RESET_ALL}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check_last >= i[0] and check_last <= i[1]:
                print(f"{Style.BRIGHT}{Fore.RED}{int_to_ip(check)}{Style.RESET_ALL} -> {Style.DIM}{Fore.BLUE}{int_to_ip(i[0])}{Style.RESET_ALL} <- {Style.BRIGHT}{Fore.RED}{int_to_ip(check_last)}{Style.RESET_ALL} -> {Style.DIM}{Fore.BLUE}{int_to_ip(i[1])}{Style.RESET_ALL}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check <= i[0] and check_last >= i[1]:
                print(f"{Style.BRIGHT}{Fore.RED}{int_to_ip(check)}{Style.RESET_ALL} -> {Style.DIM}{Fore.BLUE}{int_to_ip(i[0])}{Style.RESET_ALL} -- {Style.DIM}{Fore.BLUE}{int_to_ip(i[1])}{Style.RESET_ALL} <- {Style.BRIGHT}{Fore.RED}{int_to_ip(check_last)}{Style.RESET_ALL}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False

            #### Versión resumida sin impresiones
            # if ((check >= i[0] and check <= i[1]) or
            #     (check >= i[0] and check_last <= i[1]) or
            #     (check_last >= i[0] and check_last <= i[1]) or
            #     (check <= i[0] and check_last >= i[1])):

            #     nueva_ip = suma_salto(nueva_ip, salto, posicion)
            #     check = ip_to_int(nueva_ip)
            #     check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
            #     error = True
            #     break
            # else:
            #     error = False

        if not error:
            red_disp_ok += 1 
            print(f"{Style.BRIGHT}{Fore.GREEN}{int_to_ip(check)}{Style.RESET_ALL} --> {Style.BRIGHT}{Fore.GREEN}{int_to_ip(check_last)}{Style.RESET_ALL}")
                
        if not error and red_disp_ok < int(red_disp):
            nueva_ip = suma_salto(nueva_ip, salto, posicion)
            check = ip_to_int(nueva_ip)
            check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))

    primera_red = suma(nueva_ip, 1)
    broadcast = resta(suma_salto(nueva_ip, salto, posicion), 1)
    ultima_red = resta (broadcast, 1)

    gs.set_cellvalue("B" + str(2 + rep), nueva_ip)
    gs.set_cellvalue("C" + str(2 + rep), primera_red)
    gs.set_cellvalue("D" + str(2 + rep), ultima_red)
    gs.set_cellvalue("E" + str(2 + rep), broadcast)
    gs.set_cellvalue("F" + str(2 + rep), mascara)

    lectura_datos(rep, gs)
    ips_dict = ordenar_ips(ips_dict)

def run():

    if len(argv) < 4:
        print(f"{Fore.RED}{Style.BRIGHT}Falta argumentos{Style.RESET_ALL}\n")
        print("Sintáxis del comando:")
        print(f"{Fore.GREEN}main {Fore.RESET}[JSON] [Nombre GSheet] [Numero Hoja | Nombre Hoja]{Style.RESET_ALL}")
        print(f"\t{Style.DIM}{Fore.GREEN}main {Fore.YELLOW}\"/home/usuario/API.json\" \"Examen\" {Fore.RESET}0{Style.RESET_ALL}")
        print(f"\t{Style.DIM}{Fore.GREEN}main {Fore.YELLOW}\"/home/usuario/API.json\" \"Examen\" \"Hoja 1\"{Style.RESET_ALL}")
        deinit()
        exit(1)
    
    file = argv[1]
    spreadsheet = argv[2]
    worksheet = argv[3]
    
    if path.isfile(file):
        gs = GSheets(file, spreadsheet, worksheet)
    else:
        print("El archivo JSON no se encontró en la ruta especificada")
        deinit()
        exit(1)

    while True:
        ip = input("Introduce la IP inicial: ")
        match = fullmatch("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)

        if match is None:
            print(f"{Fore.RED}Introduce una IP válida!{Style.RESET_ALL}\n")
        else:
            del match
            break


    while True:
        redes = input("Cuantas redes habrá?: ")
        redes = int(redes) if redes.isdigit() else redes

        if type(redes) == str:
            print(f"{Fore.RED}Introduce una cantidad válida!{Style.RESET_ALL}\n")
        elif redes == 0:
            print(f"{Fore.RED}Seguro?{Style.RESET_ALL}\n")
        else:
            break

    for red in range(redes):
        print(f"\n{Style.BRIGHT}{Fore.GREEN}------------------------------{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.GREEN}Red {red + 1}{Style.RESET_ALL}")
        
        # subnet = Subnetting(ip)

        ips = input("Cuantas IPs son necesarias?: ")
        
        ips_mx = ips_max(int(ips))
        pot = potencia(int(ips))
        mascara_bin = mascara_nueva(pot)
        mascara_dec = mascara_decimal(mascara_bin)
        salto = salto_pos(mascara_bin)[0]
        posicion = salto_pos(mascara_bin)[1]

        if red == 0:
            primera_vez(gs, ip, salto, posicion, mascara_dec)
        else:
            continuacion(red, gs, ip, salto, posicion, mascara_dec, ips_mx)

if __name__ == "__main__":
    main()

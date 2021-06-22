#!/usr/bin/env python3

from colors import Style
from Subnetting import Subnetting
from operations import int_to_ip, ip_to_int, suma, suma_salto, resta
from gsheets import GSheets

from signal import signal, SIGINT
from sys import exit
from re import fullmatch

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

    print(f"\nSalto: {salto}\nPos: {posicion}\nIPs_max: {ips_max}\n")

    red_disp_ok = 0
    error = False
    encontrado = False

    check = ip_to_int(nueva_ip)
    check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))

    while red_disp_ok < int(red_disp):
        for i in ips_dict.items():
            if check >= i[0] and check <= i[1]:
                print(f"{Style.BOLD}{Style.RED}{int_to_ip(check)}{Style.RESET} >= {Style.BLUE}{int_to_ip(i[0])}{Style.RESET} && {Style.BOLD}{Style.RED}{int_to_ip(check)}{Style.RESET} <= {Style.BLUE}{int_to_ip(i[1])}{Style.RESET}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check >= i[0] and check_last <= i[1]:
                print(f"{Style.BOLD}{Style.RED}{int_to_ip(check)}{Style.RESET} >= {Style.BLUE}{int_to_ip(i[0])}{Style.RESET} && {Style.BOLD}{Style.RED}{int_to_ip(check_last)}{Style.RESET} <= {Style.BLUE}{int_to_ip(i[1])}{Style.RESET}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check_last >= i[0] and check_last <= i[1]:
                print(f"{Style.BOLD}{Style.RED}{int_to_ip(check_last)}{Style.RESET} >= {Style.BLUE}{int_to_ip(i[0])}{Style.RESET} && {Style.BOLD}{Style.RED}{int_to_ip(check_last)}{Style.RESET} <= {Style.BLUE}{int_to_ip(i[1])}{Style.RESET}")
                nueva_ip = suma_salto(nueva_ip, salto, posicion)
                check = ip_to_int(nueva_ip)
                check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
                error = True
                break
            else:
                error = False
            
            if check <= i[0] and check_last >= i[1]:
                print(f"{Style.BOLD}{Style.RED}{int_to_ip(check)}{Style.RESET} <= {Style.BLUE}{int_to_ip(i[0])}{Style.RESET} && {Style.BOLD}{Style.RED}{int_to_ip(check_last)}{Style.RESET} >= {Style.BLUE}{int_to_ip(i[1])}{Style.RESET}")
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
            print(f"\n{Style.BOLD}{Style.GREEN}{int_to_ip(check)}{Style.RESET} --> {Style.BOLD}{Style.GREEN}{int_to_ip(check_last)}{Style.RESET}")
                
        if not error and red_disp_ok < int(red_disp):
            nueva_ip = suma_salto(nueva_ip, salto, posicion)
            check = ip_to_int(nueva_ip)
            check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))


    # if int(red_disp) > 1:
    #     for i in range(int(red_disp) - 1):
    #         print("otra mas")
    #         nueva_ip = suma_salto(nueva_ip, salto, posicion)
    
    # for i in ips_dict.items():
    #     print("+++++++")
    #     check = ip_to_int(nueva_ip)
        
    #     while(i[0] <= check <= i[1] or i[0] <= check_last <= i[1]):
    #         print(f"{int_to_ip(i[0])} <= {int_to_ip(check)} <= {int_to_ip(i[1])}")
    #         nueva_ip = suma_salto(nueva_ip, salto, posicion)
    #         check = ip_to_int(nueva_ip)
    #         print(f"Check: {int_to_ip(check)}")
    
    # for i in ips_dict.items():
    #     print("+++++++")
    #     check = ip_to_int(nueva_ip)
    #     check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
        
    #     while(i[0] >= check and i[1] <= check_last):
    #         print(f"{int_to_ip(i[0])} <= {int_to_ip(check)} <= {int_to_ip(i[1])}")
    #         nueva_ip = suma_salto(nueva_ip, salto, posicion)
    #         check = ip_to_int(nueva_ip)
    #         check_last = ip_to_int(resta(suma_salto(nueva_ip, salto, posicion), 1))
    #         print(f"Check: {int_to_ip(check)}")
    #         print(f"Check_Last: {int_to_ip(check_last)}")
    
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
    
    while True:
        ip = input("Introduce la IP inicial: ")
        match = fullmatch("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip)

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

    gs = GSheets("/home/farid/python-projects/subnetting/Python-Sheets-API-Key.json", "Examen", 0)

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

if __name__ == "__main__":
    main()

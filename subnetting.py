import math
import re

def ips_max(ips: int) -> int:
    '''
    Encuentra el numero de IPs necesarios que satisfaga ips

    ips: IPs requeridas
    '''
    ips = ips - 1
    ips |= ips >> 1
    ips |= ips >> 2
    ips |= ips >> 4
    ips |= ips >> 8
    ips |= ips >> 16
    return ips + 1

def potencia(ips: int) -> int:
    '''
    Encuentra a que potencia de 2 se elevó un numero

    ips: Valor dado
    '''
    ips_mx = ips_max(ips)
    return int(math.log2(ips_mx))

def mascara_nueva(potencia: int) -> str:
    default_mascara = "11111111.11111111.11111111.11111111"
    els_mascara = list(default_mascara)

    count = 0
    for i in range(len(els_mascara) - 1, 0, -1):
        if els_mascara[i] == "1" and count < potencia:
            els_mascara[i] = "0"
            count += 1

        if count == potencia:
            break

    return "".join(els_mascara)

def mascara_decimal(mascara_bin: str) -> str:
    numeros_dec = list()
    numeros_bin = mascara_bin.split(".")

    for i in range(len(numeros_bin)):
        tmp_bin = numeros_bin[i]
        bin_to_dec = int(tmp_bin, 2)
        numeros_dec.append(str(bin_to_dec))

    return (".".join(numeros_dec))

def salto_pos(mascara_bin: str) -> int:
    numeros_bin = mascara_bin.split(".")

    for i in range(len(numeros_bin) - 1, 0, -1):
        if numeros_bin[i] != "00000000":
            matches = re.findall("0", numeros_bin[i])

            salto = int(math.pow(2, len(matches)))
            posicion = i

            return [salto, posicion]

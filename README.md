
[![MIT License](https://img.shields.io/badge/licence-MIT-green?style=for-the-badge)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs) [![Python version](https://img.shields.io/badge/python-3.8.5-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/release/python-385/)

# Subnet

Programa que realiza el subneteo de acuerdo al "VLSM" usado por cierto profesor... :unamused:

- Determina la ***n-ésimas** subred disponible* para cierta cantidad de IPs dada una red base y un numero determinado de subredes.
- Directo en un worksheet de Google Sheets


## Requistos

### Habilita el acceso a la API para un proyecto

- Dirígete a [Google Developers Console](https://console.developers.google.com/project) y crea un nuevo proyecto (o selecciona el que ya tienes).
- En el cuadro denominado "Búsqueda de API y servicios", busca "API de Google Drive" y habilítalo.
- En el cuadro denominado "Búsqueda de API y servicios", busca "Google Sheets API" y habilítalo.

### Uso de la cuenta de servicio

- Despliega la barra lateral izquierda, y dirigete a "APIs & Services > Credentials" y elige "Create credentials > Service account key".
- Rellena el formulario
- Pulsa "Create" y "Done".
- Pulsa "Manage service accounts" arriba de "Service Accounts".
- Pulse en ⋮ cerca de la cuenta de servicio recién creada y selecciona "Manage keys". 
- Pulsa "ADD KEY > Create new key".
- Selecciona el tipo de clave JSON y pulse "Create".

Se decargará un archivo JSON, guardalo en un lugar que recuerdes.

- Dirigete a tu hoja de cálculo (spreadsheet) y compártela con el `cliente_email` que se menciona en el archivo JSON
  ```json
  {
    "type": "service_account",
    "project_id": "api-project-XXX",
    "private_key_id": "2cd … ba4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    "client_id": "473 … hd.apps.googleusercontent.com",
    ...
  }
  ```
  
### Video explicativo

[![MIT License](https://i.ytimg.com/vi/ddf5Z0aQPzY/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDPvyguE9Zug3z8ObFnhLw-yHA4Yg)](https://youtu.be/ddf5Z0aQPzY?t=63)

## Desarrollo

### Requisitos

- pip
  ```
  sudo apt install python3-pip
  ```
- venv
  ```
  sudo apt install python3-venv
  ```
### Trabajando

1. Clona o descarga el zip del repositorio y ubicate dentro de la carpeta.
  ```
  git clone git@github.com:FaruNL/subneteo.git Subnet
  cd Subnet
  ```
2. Crea un entorno con el nombre que gustes, por ejemplo `env`
  ```
  python3 -m venv env
  ```
3. Activa el entorno virtual
  ```
  source ./env/bin/activate
  ```
4. Verifica que los ejecutables `pip` y `python` apunten hacia los ejecutables dentro de la carpeta bin (i.e `./env/bin`)
  ```
  ❯ which pip
  /home/usuario/Subneteo/env/bin/pip
  ❯ which python
  /home/usuario/Subneteo/env/bin/python
  ```
5. Instala las dependencias
  ```
  pip install -r requirements.txt
  ```
6. Ya puedes ejecutar el programa
  ```
  ./main.py "/ruta/a/archivo/json" "Nombre de Spreadsheet" "Nombre de Worksheet"
  ```
  ```
  ./main.py "/ruta/a/archivo/json" "Nombre de Spreadsheet" {0...}
  ```


## Demo

![Demo](https://imgur.com/WnVM4xJ.gif)


## Uso

Sintáxis:
```
main [JSON] [Nombre GSheet] [Numero Hoja | Nombre Hoja]
```

Ejemplos:
```
main "/home/farid/API.json" "Examen" 0
```
```
main "/home/farid/API.json" "Examen" "Hoja 1"
```

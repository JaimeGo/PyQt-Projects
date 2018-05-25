from hashlib import pbkdf2_hmac
from os import urandom
from base64 import b64encode
from binascii import hexlify


def encriptar_y_guardar(usuario, contraseña):
    salt = urandom(64)

    contraseña = contraseña.encode()
    salt_str = b64encode(salt).decode('utf-8')
    nueva_salt = salt_str.encode("utf-8")

    contraseña_final = pbkdf2_hmac("sha256", contraseña, nueva_salt, 100000)

    contraseña_final_str = hexlify(contraseña_final).decode()

    with open("base_datos_registro", "a+") as archivo:
        mensaje_guardado = usuario + ":::" + salt_str + ":::" + contraseña_final_str + "\n"
        archivo.write(mensaje_guardado)


def comparar_usuario(usuario, contraseña):
    with open("base_datos_registro") as archivo:

        for linea in archivo.readlines():

            lista_linea = linea.split(":::")

            usuario_base = lista_linea[0]
            salt_base = lista_linea[1].encode("utf-8")
            contraseña_final_base = lista_linea[2][:-1]

            if usuario == usuario_base:
                nueva_contraseña_final = pbkdf2_hmac("sha256", contraseña.encode(), salt_base, 100000)

                nueva_str = hexlify(nueva_contraseña_final).decode()

                if nueva_str == contraseña_final_base:
                    return True

        return False

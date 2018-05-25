def obtener_tiempo():
    tiempo_max_sim = int

    while True:
        try:
            tiempo_max_sim = int(input("\nIngrese el tiempo máximo de simulación: "))
            break
        except ValueError:
            print("\nNo ingresó un número")

    return tiempo_max_sim


def obtener_raza(anterior=None):
    raza = str

    while True:
        try:
            raza = input("\nIngrese la raza del ejército: ")
            raza = raza.lower()

            if raza not in ["muertos vivientes", "orcos", "humanos"]:
                raise ValueError

            if anterior != None:
                if raza == anterior.lower():
                    raise Exception

            break

        except ValueError:
            print("\nNo ingresó una raza correcta. Las opciones son: ",
                  "Muertos Vivientes, Orcos y Humanos, con minúsculas o mayúsculas")

        except Exception:
            print("\nEsta raza debe ser distinta a la anterior")

    return raza


def obtener_dios(anterior=None):
    dios = str

    while True:
        try:

            dios = input("\nIngrese el dios del ejército: ")
            dios = dios.lower()

            if dios not in ["godpezoa", "jundead", "godessflo", "godolfo"]:
                raise ValueError

            if anterior != None:
                if dios == anterior.lower():
                    raise Exception

            break


        except ValueError:
            print("\nNo ingresó un dios correcto. Las opciones son: ",
                  "GodPezoa, Jundead,GodessFlo y Godolfo, con minúsculas o mayúsculas")

        except Exception:
            print("\nEste dios debe ser distinto al anterior")

    dios = modificar_dios(dios)
    return dios


def obtener_intervalo():
    intervalo_creacion = str

    while True:
        try:
            intervalo_creacion = input("\nIngrese el intervalo de creación de guerreros, " +
                                       "arqueros y mascotas (ej: 2:1:2): ")
            valores = intervalo_creacion.split(":")

            largo_correcto = True if len(valores) == 3 else False

            valores_correctos = True if valores[0].isdigit() and valores[1].isdigit() and valores[
                2].isdigit() else False

            if not largo_correcto:
                raise ValueError

            if not valores_correctos:
                raise Exception

            break
        except ValueError:
            print("\nNo ingresó un intervalo de tres números separados por ':'")

        except Exception:
            print("\nAl menos uno de los valores que ingresó no es un número")

    return intervalo_creacion


def obtener_tasa_heroe():
    tasa_heroe = int

    while True:
        try:
            tasa_heroe = int(input("\nIngrese la tasa de invocación del héroe: "))
            break
        except ValueError:
            print("\nNo ingresó un número")

    return tasa_heroe


def modificar_dios(dios):
    if dios.lower() == "godpezoa":
        dios = "pezoa"
    if dios.lower() == "jundead":
        dios = "june"
    if dios.lower() == "godessflo":
        dios = "flo"
    if dios.lower() == "godolfo":
        dios = "rodolfo"

    return dios

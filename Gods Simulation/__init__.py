

from simulacion import Simulacion
from obtener_datos import obtener_dios,obtener_intervalo,obtener_raza,obtener_tiempo,obtener_tasa_heroe
import gui




print("Bienvenido a una lucha interplanetaria de dimensiones",
      "épicas. Los dioses de la programación esperarán pacientemente",
      "a que decida las condiciones del combate.")

#Obtenemos los siguientes datos: tiempo,dios,raza,intervalo,tasa_invocacion

tiempo_simulacion=obtener_tiempo()

print("\nPor favor ingrese los parámetros del ejercito 1")

dios_1=obtener_dios()
raza_1=obtener_raza()
intervalo_1=obtener_intervalo()
tasa_invocacion_1=obtener_tasa_heroe()

print("\nPor favor ingrese los parámetros del ejercito 2")

dios_2=obtener_dios(dios_1)
raza_2=obtener_raza(raza_1)
intervalo_2=obtener_intervalo()
tasa_invocacion_2=obtener_tasa_heroe()







sim=Simulacion(tiempo_simulacion,dios_1,raza_1,tasa_invocacion_1,intervalo_1,dios_2,raza_2,tasa_invocacion_2,intervalo_2)
gui.set_size(1024, 680)
gui.run(sim.tick)














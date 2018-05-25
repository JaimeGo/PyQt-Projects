def efecto_pezoa(simul):
    if simul.dios_1 == "pezoa":
        simul.pezoa_funcionando_1 = True

    if simul.dios_2 == "pezoa":
        simul.pezoa_funcionando_2 = True


def efecto_jundead(simul):
    if simul.dios_1 == "jundead":
        simul.jundead_funcionando_1 = True

    if simul.dios_2 == "jundead":
        simul.jundead_funcionando_2 = True


def efecto_flo(simul):
    if simul.dios_1 == "flo":
        mas_grande = 0

        prop_guerr = simul.guerreros_ciclo_1
        prop_arq = simul.arqueros_ciclo_1
        prop_masc = simul.mascotas_ciclo_1

        for elem in [prop_guerr, prop_arq, prop_masc]:
            if elem > mas_grande:
                mas_grande = elem

        simul.mascotas_ciclo_1 = mas_grande + 2

        print("GodessFlo cambió la proporción de mascotas a ", simul.mascotas_ciclo_1)

    if simul.dios_2 == "flo":
        mas_grande = 0
        prop_guerr = simul.guerreros_ciclo_2
        prop_arq = simul.arqueros_ciclo_2
        prop_masc = simul.mascotas_ciclo_2

        for elem in [prop_guerr, prop_arq, prop_masc]:
            if elem > mas_grande:
                mas_grande = elem

        simul.mascotas_ciclo_2 = mas_grande + 2

        print("GodessFlo cambió la proporción de mascotas a ", simul.mascotas_ciclo_2)

    if simul.dios_1 == "flo":
        simul.no_mover_mascotas_1 = True

    if simul.dios_2 == "flo":
        simul.no_mover_mascotas_2 = True


def efecto_godolfo(simul):
    if simul.dios_1 == "rodolfo":
        simul.godolfo_funcionando_1 = True

    if simul.dios_2 == "rodolfo":
        simul.godolfo_funcionando_2 = True

import random
import csv

CATEGORIAS = ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"]


def tirar_dados():
    dados = []
    for i in range(5):
        dados.append(random.randint(1, 6))
    return dados


def relanzar_dados(dados, posiciones):
    i = 0
    while i < len(posiciones):
        pos = posiciones[i] - 1
        dados[pos] = random.randint(1, 6)
        i += 1
    return dados


def contar_repeticiones(dados):
    conteo = [0] * 7
    i = 0
    while i < len(dados):
        conteo[dados[i]] += 1
        i += 1
    return conteo


def es_escalera(dados):
    ordenados = sorted(dados)
    return ordenados == [1, 2, 3, 4, 5] or ordenados == [2, 3, 4, 5, 6]


def es_full(dados):
    conteo = contar_repeticiones(dados)
    hay_tres = False
    hay_dos = False
    i = 1
    while i <= 6:
        if conteo[i] == 3:
            hay_tres = True
        if conteo[i] == 2:
            hay_dos = True
        i += 1
    return hay_tres and hay_dos


def es_poker(dados):
    conteo = contar_repeticiones(dados)
    i = 1
    while i <= 6:
        if conteo[i] == 4:
            return True
        i += 1
    return False


def es_generala(dados):
    conteo = contar_repeticiones(dados)
    i = 1
    while i <= 6:
        if conteo[i] == 5:
            return True
        i += 1
    return False


def puntaje_numero(dados, numero):
    suma = 0
    i = 0
    while i < len(dados):
        if dados[i] == numero:
            suma += dados[i]
        i += 1
    return suma


def calcular_puntaje(dados, categoria, primera_tirada):
    puntos = 0

    if categoria == "E":
        if es_escalera(dados):
            puntos = 20
            if primera_tirada:
                puntos += 5

    elif categoria == "F":
        if es_full(dados):
            puntos = 30
            if primera_tirada:
                puntos += 5

    elif categoria == "P":
        if es_poker(dados):
            puntos = 40
            if primera_tirada:
                puntos += 5

    elif categoria == "G":
        if es_generala(dados):
            puntos = 50
            if primera_tirada:
                puntos += 30

    else:
        puntos = puntaje_numero(dados, int(categoria))

    return puntos


def crear_planilla():
    planilla = []
    i = 0
    while i < len(CATEGORIAS):
        planilla.append([-1, -1])   
        i += 1
    return planilla


def buscar_indice_categoria(categoria):
    i = 0
    while i < len(CATEGORIAS):
        if CATEGORIAS[i] == categoria:
            return i
        i += 1
    return -1


def mostrar_planilla(planilla):
    print("\nPLANILLA")
    print("Cat\tJ1\tJ2")
    i = 0
    while i < len(CATEGORIAS):
        v1 = planilla[i][0]
        v2 = planilla[i][1]

        if v1 == -1:
            t1 = "-"
        else:
            t1 = str(v1)

        if v2 == -1:
            t2 = "-"
        else:
            t2 = str(v2)

        print(CATEGORIAS[i] + "\t" + t1 + "\t" + t2)
        i += 1


def guardar_csv(planilla):
    archivo = open("jugadas.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(archivo)

    writer.writerow(["jugada", "j1", "j2"])

    i = 0
    while i < len(CATEGORIAS):
        j1 = planilla[i][0]
        j2 = planilla[i][1]

        if j1 == -1:
            j1 = ""
        if j2 == -1:
            j2 = ""

        writer.writerow([CATEGORIAS[i], j1, j2])
        i += 1

    archivo.close()


def mostrar_dados(dados):
    print("Dados:", dados)


def leer_posiciones():
    print("Ingresá posiciones de dados a relanzar (1 a 5), separadas por espacio.")
    print("Si no querés relanzar, apretá Enter.")
    entrada = input(">> ")

    posiciones = []

    if entrada != "":
        partes = entrada.split()
        i = 0
        while i < len(partes):
            if partes[i].isdigit():
                pos = int(partes[i])
                if pos >= 1 and pos <= 5:
                    if pos not in posiciones:
                        posiciones.append(pos)
            i += 1

    return posiciones


def categoria_disponible(planilla, jugador, categoria):
    indice = buscar_indice_categoria(categoria)
    if indice == -1:
        return False
    return planilla[indice][jugador] == -1


def mostrar_categorias_disponibles(planilla, jugador):
    print("Categorías disponibles:", end=" ")
    i = 0
    primera = True
    while i < len(CATEGORIAS):
        if planilla[i][jugador] == -1:
            if not primera:
                print(",", end=" ")
            print(CATEGORIAS[i], end="")
            primera = False
        i += 1
    print()


def elegir_categoria(planilla, jugador):
    categoria = ""
    valida = False

    while not valida:
        mostrar_categorias_disponibles(planilla, jugador)
        categoria = input("Elegí una categoría: ").upper()
        if categoria_disponible(planilla, jugador, categoria):
            valida = True
        else:
            print("Categoría inválida o ya usada.")

    return categoria


def copia_lista(lista):
    nueva = []
    i = 0
    while i < len(lista):
        nueva.append(lista[i])
        i += 1
    return nueva


def turno_jugador(planilla, jugador, nombre):
    print("\nTurno de", nombre)

    dados = tirar_dados()
    dados_primera = copia_lista(dados)
    tirada_numero = 1
    seguir = True

    while tirada_numero <= 3 and seguir:
        print("Tirada", tirada_numero)
        mostrar_dados(dados)

        if tirada_numero < 3:
            posiciones = leer_posiciones()
            if len(posiciones) == 0:
                seguir = False
            else:
                dados = relanzar_dados(dados, posiciones)

        tirada_numero += 1

    categoria = elegir_categoria(planilla, jugador)

    primera_tirada = False
    if dados == dados_primera:
        primera_tirada = True

    puntos = calcular_puntaje(dados, categoria, primera_tirada)
    indice = buscar_indice_categoria(categoria)
    planilla[indice][jugador] = puntos

    generala_real = False
    if categoria == "G" and es_generala(dados) and primera_tirada:
        generala_real = True

    print(nombre, "anotó", puntos, "puntos en", categoria)
    return generala_real


def planilla_completa_jugador(planilla, jugador):
    i = 0
    while i < len(planilla):
        if planilla[i][jugador] == -1:
            return False
        i += 1
    return True


def total_jugador(planilla, jugador):
    total = 0
    i = 0
    while i < len(planilla):
        if planilla[i][jugador] != -1:
            total += planilla[i][jugador]
        i += 1
    return total


def main():
    planilla = crear_planilla()
    guardar_csv(planilla)

    fin = False
    ganador_generala_real = 0  

    while not fin:
        mostrar_planilla(planilla)

        if not planilla_completa_jugador(planilla, 0):
            gr1 = turno_jugador(planilla, 0, "Jugador 1")
            guardar_csv(planilla)
            if gr1:
                fin = True
                ganador_generala_real = 1

        if not fin and not planilla_completa_jugador(planilla, 1):
            mostrar_planilla(planilla)
            gr2 = turno_jugador(planilla, 1, "Jugador 2")
            guardar_csv(planilla)
            if gr2:
                fin = True
                ganador_generala_real = 2

        if planilla_completa_jugador(planilla, 0) and planilla_completa_jugador(planilla, 1):
            fin = True

    print("\nFIN DEL JUEGO")
    mostrar_planilla(planilla)

    total1 = total_jugador(planilla, 0)
    total2 = total_jugador(planilla, 1)

    print("\nTotal Jugador 1:", total1)
    print("Total Jugador 2:", total2)

    if ganador_generala_real == 1:
        print("Ganó Jugador 1 por Generala Real")
    elif ganador_generala_real == 2:
        print("Ganó Jugador 2 por Generala Real")
    else:
        if total1 > total2:
            print("Ganó Jugador 1")
        elif total2 > total1:
            print("Ganó Jugador 2")
        else:
            print("Empate")


main()
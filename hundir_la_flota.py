import random

# ==========================================
# CONSTANTES Y ESTRUCTURAS DE CONVERSIÓN
# ==========================================
LISTA_LETRAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
MAP_LETRAS = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
    'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9
}

# Flota reglada: 1 de 4, 2 de 3, 3 de 2 y 4 de 1 casilla (Total: 10 naves)
FLOTA = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


# ==========================================
# 1. REPRESENTACIÓN DEL CAMPO (10x10)
# ==========================================
def crear_tablero():
    """
    Crea una matriz de 10x10 mediante listas anidadas usando .append() 
    tanto para las casillas de cada fila como para las filas del tablero.
    """
    tablero = []
    for i in range(10):
        fila = []
        for j in range(10):
            fila.append('-')   # append de cada celda a la fila
        tablero.append(fila)   # append de la fila al tablero
    return tablero


def imprimir_tablero(tablero):
    """Imprime el tablero siguiendo el formato exacto de la traza del enunciado."""
    print("   " + "".join(LISTA_LETRAS))
    for i in range(10):
        # Alineación para que del 1 al 9 ocupen el mismo ancho que el 10
        etiqueta_fila = f"{i + 1:2d}:"
        contenido_fila = "".join(tablero[i])
        print(f"{etiqueta_fila}{contenido_fila}")
    print()


# ==========================================
# 2. CONVERSIÓN DE COORDENADAS
# ==========================================
def humano_a_indices(coord_texto):
    """
    Traduce formato humano (ej. 'B3' o 'A10') a tupla de índices.
    Nota: Sigue el convenio del enunciado donde 'B3' -> (1, 2) (columna, fila).
    """
    coord_texto = coord_texto.strip().upper()
    letra_col = coord_texto[0]
    num_fila = int(coord_texto[1:])
    
    j = MAP_LETRAS[letra_col]  # Índice de columna (0 a 9)
    i = num_fila - 1           # Índice de fila (0 a 9)
    return (j, i)


def indices_a_humano(j, i):
    """
    Traduce índices (columna j, fila i) a formato humano (ej. (1, 2) -> 'B3').
    """
    letra_col = LISTA_LETRAS[j]
    num_fila = str(i + 1)
    return letra_col + num_fila


# ==========================================
# 3. ALGORITMO DE COLOCACIÓN ALEATORIA
# ==========================================
def celda_y_entorno_libres(tablero, fila, col):
    """
    Comprueba que la celda (fila, col) y todas sus vecinas (incluyendo diagonales)
    estén libres ('-') para garantizar 1 casilla de separación.
    """
    for f in range(fila - 1, fila + 2):
        for c in range(col - 1, col + 2):
            # Controlar que no nos salgamos de los límites de la matriz 10x10
            if 0 <= f < 10 and 0 <= c < 10:
                if tablero[f][c] != '-':
                    return False
    return True


def gestionar_barco(tablero, fila, col, tamano, orientacion, situar):
    """
    Comprueba o sitúa un barco en función del parámetro booleano 'situar'.
    - orientacion: 0 para vertical, 1 para horizontal.
    - situar: False solo comprueba si es válido; True coloca el barco ('O').
    """
    for k in range(tamano):
        if orientacion == 0:  # Vertical
            f, c = fila + k, col
        else:                 # Horizontal
            f, c = fila, col + k

        if not situar:
            if not celda_y_entorno_libres(tablero, f, c):
                return False
        else:
            tablero[f][c] = 'O'

    return True


def distribuir_flota(tablero):
    """Coloca aleatoriamente los 10 barcos de la flota en el tablero."""
    for tamano in FLOTA:
        colocado = False
        while not colocado:
            # 0: Vertical, 1: Horizontal
            orientacion = random.randint(0, 1)

            if orientacion == 0:  # Vertical
                i = random.randint(0, 10 - tamano)  # Fila inicial
                j = random.randint(0, 9)            # Columna inicial
            else:                 # Horizontal
                i = random.randint(0, 9)            # Fila inicial
                j = random.randint(0, 10 - tamano)  # Columna inicial

            # Primero comprobamos (situar=False); si es True, lo colocamos (situar=True)
            if gestionar_barco(tablero, i, j, tamano, orientacion, False):
                gestionar_barco(tablero, i, j, tamano, orientacion, True)
                colocado = True


# ==========================================
# BLOQUE DE PRUEBA (SESIÓN 1)
# ==========================================
if __name__ == "__main__":
    print("Bienvenido a Hundir la Flota!!!")
    print("Voy a distribuir mis barcos")
    
    tablero_ordenador = crear_tablero()
    tablero_disparos = crear_tablero()
    
    distribuir_flota(tablero_ordenador)
    
    print("Ya está. Podemos empezar:\n")
    print("--- TABLERO DEL ORDENADOR (Barcos 'O') ---")
    imprimir_tablero(tablero_ordenador)
    
    print("--- TABLERO DE DISPAROS ---")
    imprimir_tablero(tablero_disparos)
    
    # Prueba de conversión de coordenadas según especificación 5.3
    coord_ejemplo = "B3"
    indices = humano_a_indices(coord_ejemplo)
    retorno = indices_a_humano(indices[0], indices[1])
    print(f"Prueba de coordenadas: '{coord_ejemplo}' -> {indices} -> '{retorno}'")
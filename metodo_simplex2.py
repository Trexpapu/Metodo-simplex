import columbaBase as c
def CreasRestricciones(Cantidad_restricciones):
    restricciones = {}
    for i in range(Cantidad_restricciones):
        x = float(input(f"Ingrese el valor de x de la restriccion {i+1}\n"))
        y = float(input(f"Ingrese el valor de y de la restriccion {i+1}\n"))
        solucion = float(input(f"Ingrese el valor de solución de la restriccion {i+1}\n"))

        restricciones[i] = [x, y, solucion]

    print("\nLas restricciones son las siguientes: \n", restricciones)
    return restricciones

def CrearTablaInicial(restricciones, Cantidad_restricciones, X, Y):
    # Aumentar el número de columnas para incluir la columna z
    
    columnas = c.columna + Cantidad_restricciones  # Solución, x, y, s1, s2, s3, z
    filas = Cantidad_restricciones + 1

    # Crear el arreglo bidimensional (lleno de ceros)
    tabla = [[0 for _ in range(columnas)] for _ in range(filas)]

    # Rellenar la tabla con los valores de restricciones
    for i in range(Cantidad_restricciones):
        tabla[i][0] = restricciones[i][2]  # Solución
        tabla[i][1] = restricciones[i][0]  # Coeficiente de x
        tabla[i][2] = restricciones[i][1]  # Coeficiente de y
        tabla[i][3 + i] = 1  # Columna de variables slack (s1, s2, ..., sn)
        tabla[i][-1] = 0  # Columna de z, que es 0 en las restricciones

    # Agregar la fila de la función objetivo
    tabla[Cantidad_restricciones][1] = -X  # Coeficiente de x
    tabla[Cantidad_restricciones][2] = -Y  # Coeficiente de y
    tabla[Cantidad_restricciones][0] = 0   # Valor de Z (objetivo)
    tabla[Cantidad_restricciones][-1] = 1  # Z en la fila de la función objetivo es 1

    # Imprimir la tabla
    print("\nTabla inicial:")
    headers = ["Solución", "x", "y"]  # Encabezados
    for i in range(Cantidad_restricciones):
        headers.append(f"s{i+1}")
    headers.append("z")
    print(f"{' | '.join(headers)}")
    print("-" * 50)

    for fila in tabla:
        print(" | ".join([f"{v:.2f}" for v in fila]))

    return tabla

def dibujarTablaNueva(tabla, contador, Cantidad_restricciones):
    print(f"\nTabla actualizada: {contador}")
    headers = ["Solución", "x", "y"]  # Encabezados
    for i in range(Cantidad_restricciones):
        headers.append(f"s{i+1}")
    headers.append("z")
    print(f"{' | '.join(headers)}")
    print("-" * 50)

    for fila in tabla:
        print(" | ".join([f"{v:.4f}" for v in fila]))
    print("-" * 50)


def metodo_simplex(tabla, Cantidad_restricciones, X, Y):
    NegativosEnZeta = True
    contadorDeTablas = 0
    tablaAux = tabla
    columnaY = 2
    columnaX = 1
    NuevaFilaY = -1
    NuevaFilaX = -1

    while NegativosEnZeta:
        # Paso 1: Verificar cuál será la columna del pivote (la más negativa en la fila de la función objetivo)
        ultima_fila = tablaAux[-1]  # Última fila (función objetivo)
        
        
        valor_minimo = min(ultima_fila[1:])  # Excluimos la primera columna

        # Obtener el índice de ese valor, ajustando por la exclusión del primer valor
        columna_pivote = ultima_fila.index(valor_minimo, 1)  # Comenzamos la búsqueda desde el índice 1
        
        print(f"Columna del pivote: {columna_pivote}, Valor: {valor_minimo:.4f}")
        
        # Paso 2: Identificar la fila del pivote
        fila_pivote = -1
        min_ratio = float('inf')  # Inicializar con un valor muy grande

        # Iterar sobre las filas (excepto la última fila)
        for fila in range(Cantidad_restricciones):
            if tablaAux[fila][columna_pivote] > 0:  # Solo considerar valores positivos
                ratio = tablaAux[fila][0] / tablaAux[fila][columna_pivote]  # Dividir solución entre valor en columna pivote
                if ratio <= min_ratio:
                    min_ratio = ratio
                    fila_pivote = fila  # Guardar el índice de la fila pivote
        
        print(f"Fila del pivote: {fila_pivote}, Ratio mínimo: {min_ratio:.3f}, Valor: {tablaAux[fila_pivote][columna_pivote]:.3f}")

        #guardamos en cual de las columnas x o y se encontró el pivote
        if columna_pivote == columnaY:
            NuevaFilaY = fila_pivote 
        elif columna_pivote == columnaX:
            NuevaFilaX = fila_pivote


        # Paso 3: Crear la fila entrante dividiendo la fila pivote por el elemento pivote
        pivote = tablaAux[fila_pivote][columna_pivote]
        for columna in range(len(tablaAux[0])):  # Iterar sobre todas las columnas de la fila pivote
            tablaAux[fila_pivote][columna] /= pivote
        
        print(f"Fila pivote después de normalizar: {[f'{valor:.4f}' for valor in tablaAux[fila_pivote]]}")

        

        # Paso 4: Actualizar el resto de las filas... La formula es filaNueva = filaVieja - pivoteDeLaFila * filaEntrante
        for fila in range(Cantidad_restricciones + 1): #se suma 1 para incluir la fila z 
            pivoteDeFila = tablaAux[fila][columna_pivote]
            for columna in range(c.columna + Cantidad_restricciones ):# Solución, x, y, s1, s2, sn..., z
                if fila != fila_pivote:
                    filaVieja = tablaAux[fila][columna] 
                    filaEntrante = tablaAux[fila_pivote][columna]    
                    tablaAux[fila][columna] = filaVieja - pivoteDeFila * filaEntrante

        # Paso 5: Dibujar la tabla actualizada
        dibujarTablaNueva(tablaAux, contadorDeTablas, Cantidad_restricciones)

        #paso 6  verificar que no haya valores negativos en la fila z 
        UltimaFilaAux = tablaAux[-1]  # Última fila (función objetivo)
        ValorMinimoAuxiliar = min(UltimaFilaAux)  # Obtener el valor más negativo
        if ValorMinimoAuxiliar >= 0:
            break
        contadorDeTablas += 1



    if NuevaFilaY != -1:
        valorDeY = tablaAux[NuevaFilaY][0]
        print(f"El valor de Y esta el la fila {NuevaFilaY} columna 0 el cual es {valorDeY:.4f}\n")
    else:
        print("El valor de Y es 0")
    if NuevaFilaX != -1:
        valorDeX = tablaAux[NuevaFilaX][0]
        print(f"El valor de X esta en la fila {NuevaFilaX} columna 0 el cual es {valorDeX:.4f}\n")
    else:
        print("EL valor de X es 0")
    
    # Obtener la última fila
    ultima_fila = len(tablaAux) - 1  # Última fila en tablaAux

    # Extraer el valor de z de la primera columna (columna de la solución)
    z = tablaAux[ultima_fila][0]
    print(f"Sustituyendo los valores, la función objetivo se puede maximizar hasta Z = {z:.4f}")





def main():
    try:
        print("Bienvenido al método simplex de Emmanuel...\n")
        print("Ingrese los valores de la función objetivo: \n")
        X = float(input("Ingrese el valor de x: \n"))
        Y = float(input("Ingrese el valor de y: \n"))
        Cantidad_restricciones = int(input("Ingrese la cantidad de restricciones: \n"))
        
        restricciones = CreasRestricciones(Cantidad_restricciones)
        tabla = CrearTablaInicial(restricciones, Cantidad_restricciones, X, Y)
        metodo_simplex(tabla, Cantidad_restricciones, X, Y)
    
    except ValueError:
        print("Error: Ingrese valores numéricos.\n")

main()

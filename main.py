from multipledispatch import dispatch
from fractions import Fraction
import time


class Vector:
    """clase envoltorio de una lista de numeros, no hereda por cuestiones de limitaciones"""

    def __init__(self, vector):

        self.vector = [Fraccion(element) if not isinstance(element, Fraccion) else element for element in vector]

    def __add__(self, new_vector):
        if not len(new_vector.vector) == len(self.vector):
            return 'Error, los vectores deben medir lo mismo'
        vector_final = list()
        for i in range(len(new_vector.vector)):
            value = Fraccion(self.vector[i] + new_vector.vector[i])
            vector_final.append(value)
        return Vector(vector_final)

    def __sub__(self, new_vector):
        if not len(new_vector) == len(self.vector):
            return 'Error, los vectores deben medir lo mismo'
        vector_final = list()
        for i in range(len(new_vector)):
            value = Fraccion(self.vector[i] - new_vector.vector[i])
            vector_final.append(value)
        return Vector(vector_final)

    def mul(self, number):
        vector_final = list()
        for i in range(len(self.vector)):
            value = Fraccion(self.vector[i] * number)
            vector_final.append(value)
        return Vector(vector_final)

    @dispatch(object)
    def __mul__(self, new_vector):

        if isinstance(new_vector, Fraction) or isinstance(new_vector, float):
            if not isinstance(new_vector, Fraccion):
                new_vector = Fraccion(new_vector)
            return self.mul(new_vector.numerator / new_vector.denominator)

        if len(self.vector) != len(new_vector.vector):
            return "los vectores deben medir lo mismo"
        filas_matriz = list()
        for i in range(len(self.vector)):
            value = Fraccion(new_vector * self.vector[i])
            filas_matriz.append(value)
        return Matriz(filas_matriz)

    # funcion que utiliza para multiplicar cada elemento del vector A
    # por el elemento correspondiente del vector B
    # se lee: A operando SOBRE el comportamiento de B
    # se utiliza la division entera para dejar libre
    # la division normal en caso de ser necesario
    def __floordiv__(self, vector):
        if len(self.vector) != len(vector.vector):
            return "ERROR"
        vector_resultante = list()
        for i in range(len(vector.vector)):
            number1 = self.vector[i] if isinstance(self.vector[i], Fraccion) else Fraccion(self.vector[i])
            number2 = vector.vector[i] if isinstance(vector.vector[i], Fraccion) else Fraccion(vector.vector[i])
            value = Fraccion(number1 * number2).simplify()
            vector_resultante.append(value)

        return vector_resultante

    def normalize(self):
        copy = self.vector.copy()
        for i in range(len(self.vector)):
            copy[i] = Fraccion(self.vector[i])

    def __str__(self):
        res = ''
        res += str([str(i.limit_denominator()) for i in self.vector])

        return res

    def __len__(self):
        return len(self.vector)


class Matriz:
    """clase envoltorio de una lista matriz (compuesta de mas listas), no hereda por cuestiones de limitacion"""

    def __init__(self, filas):
        self.filas = filas
        self.normalize()

    def __add__(self, new_matriz):
        if (not len(new_matriz.filas) == len(self.filas) and not len(new_matriz.filas[0].vector) == len(
                self.filas[0].vector)):
            return 'Error, las matrices deben tener las mismas dimensiones'
        vector_final = list()
        for i in range(len(new_matriz.filas)):
            vector_final.append(self.filas[i] + new_matriz.filas[i])
        return Matriz(vector_final)

    def __sub__(self, new_matriz):
        if (not len(new_matriz.filas) == len(self.filas) and not len(new_matriz.filas[0].vector) == len(
                self.filas[0].vector)):
            return 'Error, las matrices deben tener las mismas dimensiones'
        vector_final = list()
        for i in range(len(new_matriz.filas)):
            vector_final.append(self.filas[i] - new_matriz.filas[i])
        return Matriz(vector_final)

    def __mul__(self, new_matriz):
        """se ejecuta la multiplicacion de matriz*matriz
            en la que debemos comprobar que la cantidad de columnas de la matriz A
            sea igual a la cantidad de filas de la columna B
        """
        if isinstance(new_matriz, Fraction):
            matriz_final = self.copy()
            for i in range(len(self.filas)):
                matriz_final.filas[i] = (self.filas[i] * new_matriz)
            return matriz_final

        new_matriz.normalize()
        if len(self.filas[0].vector) != len(new_matriz.filas):
            return "Error, la matriz A debe tener la misma cantidad de columnas que la matriz B de filas"

        matriz_final = list()
        columna = 0
        # este ciclo itera sobre las filas de la matriz
        for x in range(len(self.filas)):
            vector_fila = list()
            # este ciclo itera sobre las columnas de la matriz
            for i in range(len(new_matriz.filas[0].vector)):
                # esta declaracion indica que se debe extraer la columna n
                # de la segunda matriz con la que se esta trabajando
                vector_columna = extract_column(new_matriz, i)
                # vector resultante es el vector que se da cuando se multiplican
                # los valores correspondientes de los vectores fila y columna que
                # se estan manejando en la iteracion
                vector_resultante = self.filas[x] // vector_columna
                suma = sumatoria(vector_resultante)
                vector_fila.append(suma)
                columna += 1

            matriz_final.append(Vector(vector_fila))

        return Matriz(matriz_final)

    def __pow__(self, value):
        """aqui se eleva una matriz a una potencia x"""
        if len(self.filas) != len(self.filas[0].vector):
            return "Error, la matriz solo puede elevarse a la {value} si es cuadrada"

        if value >= 2:
            """
                si la potencia es mayor o igual a 2, declaramos que el inicio de la matriz
                es la matriz al cuadrado y ya si el numero es mayor a 2, se continua de manera
                normal para evitar errores
            """
            matriz_final = self * self
            if value > 2:
                for i in range(value):
                    matriz_final *= self

            return matriz_final
        elif value == 1:
            """si la potencia es igual a 1, entonces, 
            no hace falta realizar operaciones y se devuelve la misma matriz"""
            return self
        else:
            return 1

    def normalize(self):
        for i in self.filas:
            i.normalize()

    def identidad(self, show=True):
        matriz_res = self.copy()
        # RECUERDA QUE LA IDENTIDAD SE RESUELVE COLUMNA POR COLUMNA PERO OPERANDO CON FILAS
        # resolvemos fila por fila
        if show:
            print(matriz_res)
        for i in range(len(self.filas)):
            matriz_res, _ = volver1(matriz_res, pivote=i, show=show)
            for x in range(len(self.filas)):
                if i == x:
                    continue
                matriz_res, _ = volver0(matriz_res, pivote=i, fila=x, show=show)
        if show:
            print()
            print(matriz_res)
        return matriz_res

    def determinante(self):
        # el determinante se obtiene por medio de la multiplicacion recursiva de los determinantes inferiores
        # hasta que se llegue al determinante de 2x2
        if len(self.filas) != len(self.filas[-1].vector):
            return "La matriz debe ser cuadrada para poder sacar un determinante"
        matriz = self.copy()

        def determinate(matriz_original):
            determinante = 0
            if len(matriz_original.filas) == 2 and len(matriz_original.filas[0].vector) == 2:
                return matriz_original.filas[0].vector[0] * matriz_original.filas[1].vector[1] - matriz_original.filas[1].vector[0] * \
                       matriz_original.filas[0].vector[1]
            for i in range(len(matriz_original.filas[-1].vector)):
                matriz_op = matriz_original.copy()
                pivote = matriz_op.filas[0].vector[i]
                matriz_op = matriz_op.remove_row(0)
                matriz_op = matriz_op.remove_col(i)
                det = pivote * determinate(matriz_op)
                determinante += pow(-1, i) * det
            return determinante

        return determinate(matriz)

    def gauss_jordan(self):
        res = list()
        for i in self.filas:
            lista = list()
            lista.append(i.vector[-1])
            res.append(lista)
        matriz_res = create_matrix(res)
        return self.inversa(matriz_res)

    def transversa(self):
        matriz_res = self.copy()
        for i in range(len(self.filas)):
            for j in range(len(self.filas[-1].vector)):
                matriz_res.filas[i].vector[j] = self.filas[j].vector[i]
        return matriz_res

    def fast_inversa(self):
        determinante = self.determinante()
        if determinante == 0:
            return "La matriz no tiene inversa ya que su determinante es 0"
        else:
            print('determinante=', determinante)
        matriz_res = self.copy()
        for x in range(len(matriz_res.filas)):
            for y in range(len(matriz_res.filas[-1].vector)):
                matriz = self.copy()
                matriz = matriz.remove_col(y)
                matriz = matriz.remove_row(x)
                if len(matriz.filas) == 2 and len(matriz.filas[0].vector) == 2:
                    determinante = matriz.filas[0].vector[0] * matriz.filas[1].vector[1] - matriz.filas[1].vector[0] * \
                                   matriz.filas[0].vector[1]
                else:
                    determinante = determinante(matriz)
                matriz_res.filas[x].vector[y] = pow(-1, x + y) * determinante

        matriz_res.normalize()
        matriz_res = matriz_res.transversa()
        matriz_res = matriz_res * (1 / determinante)
        return matriz_res

    def inversa(self, matriz_res=None):
        matriz_operada = self.copy()
        print(matriz_operada)
        if matriz_res is None:
            determinante = self.determinante()
            if determinante == 0:
                return "La matriz no tiene inversa ya que su determinante es 0"
            else:
                print('determinante=', determinante)
            matriz_res = matriz_operada.identidad(False)
        else:
            print(matriz_res)
            for i in matriz_operada.filas:
                i.vector.pop()
        # resolvemos fila por fila
        for i in range(len(self.filas)):
            matriz_operada, matriz_res = volver1(matriz_operada, matriz_res, i)
            for x in range(len(self.filas)):
                if i == x:
                    continue
                matriz_operada, matriz_res = volver0(matriz_operada, matriz_res, i, x)
        print()
        return matriz_res

    def copy(self):
        matriz = []
        for i in self.filas:
            vector = list()
            for x in i.vector:
                vector.append(x)
            matriz.append(vector)
        res = create_matrix(matriz)
        return res

    def remove_row(self, index):
        matriz = self.copy()
        if index == 0:
            matriz.filas = matriz.filas[1:]
        else:
            matriz.filas = matriz.filas[:index] + matriz.filas[index + 1:]
        return matriz

    def remove_col(self, index):
        matriz = self.copy()
        for i in matriz.filas:
            fila = i.vector.copy()
            if index == 0:
                fila = fila[1:]
            else:
                if index == 1:
                    fila = [fila[0]] + fila[2:]
                elif index < (len(matriz.filas[-1].vector) - 1):
                    fila = fila[:index] + fila[index + 1:]
                else:
                    fila = fila[:index]
            i.vector = fila
        return matriz

    def __str__(self):
        """devuelve el 'valor' de la matriz mostrando fila por fila sus valores"""
        resultado = ""
        for i in self.filas:
            resultado += str(i) + '\n'
        return resultado

    def __len__(self):
        return len(self.filas)


class Fraccion(Fraction):
    """
        clase envoltorio de Fraccion con la que hacemos ciertas operaciones fraccionales de manera mas
        comoda para el programador
    """

    @dispatch(object)
    def __truediv__(self, fraccion):
        if self.numerator == 0 or fraccion.denominator == 0:
            return 0
        frac_res = Fraccion(self.numerator * fraccion.denominator, self.denominator * fraccion.numerator)
        return frac_res.simplify()

    @dispatch(int)
    def __truediv__(self, numero):
        if self.numerator == 0:
            return 0
        frac_res = Fraccion(self.numerator, self.denominator * numero)
        return frac_res.simplify()

    def mul(self, value):
        frac_n = Fraccion(value)
        frac_res = self * frac_n

        return frac_res.simplify()

    @dispatch(object)
    def __mul__(self, fraccion):
        if isinstance(fraccion, int) or isinstance(fraccion, float):
            return self.mul(fraccion)

        if self.numerator == 0 or fraccion.numerator == 0:
            return Fraccion(0)
        frac_res = Fraccion(self.numerator * fraccion.numerator, self.denominator * fraccion.denominator)
        return frac_res.simplify()

    @dispatch(object)
    def __add__(self, fraccion):
        numerador = self.numerator * fraccion.denominator + fraccion.numerator * self.denominator
        denominador = self.denominator * fraccion.denominator
        frac_res = Fraccion(numerador, denominador)
        return frac_res.simplify()

    @dispatch(int)
    def __sub__(self, numero):
        frac_num = Fraccion(numero)
        frac_res = self + frac_num
        return frac_res

    @dispatch(object)
    def __sub__(self, fraccion):
        numerador = self.numerator * fraccion.denominator - fraccion.numerator * self.denominator
        denominador = self.denominator * fraccion.denominator
        fracRes = Fraccion(numerador, denominador)
        return fracRes.simplify()

    def simplify(self):
        new_frac = self.limit_denominator()
        new_frac = new_frac.limit_denominator() if isinstance(new_frac, Fraccion) else new_frac
        if isinstance(new_frac, Fraccion):
            real_val = new_frac.numerator / new_frac.denominator
            if new_frac.numerator == 0:
                return 0
            elif real_val % 1 == 0:
                return real_val // 1
        return Fraccion(new_frac)

    def __str__(self):
        res = self.limit_denominator()
        return '{}/{}'.format(res.numerator, res.denominator)


def sumatoria(coleccion, index=0):
    """funcion que suma todos los elementos de un vector"""
    value = Fraccion(coleccion[index]) if not isinstance(coleccion[index], Fraccion) else coleccion[index]
    if index + 1 == len(coleccion):
        return value
    return value + sumatoria(coleccion, index + 1)


def extract_column(matriz, column_index):
    vector_columna = list()
    for i in matriz.filas:  # type: Vector
        """se extraen los valores referentes a la columna indicada por columnIndex de la segunda matriz"""
        value = Fraccion(i.vector[column_index]) if isinstance(i, int) else i.vector[column_index]
        vector_columna.append(value)
    return Vector(vector_columna)


def create_matrix(matriz_arreglo):
    # extraemos los elementos de la matriz original y colocamos cada lista componente en
    # un vector para que se pueda manipular facilmente y creamos una lista con esos vectores
    vectores = [Vector(element) for element in matriz_arreglo]
    matriz_resultado = Matriz(vectores)
    return matriz_resultado


def volver1(matriz=None, identidad=None, pivote=1, show=True):
    if identidad is None:
        identidad = matriz.copy()
    pivote_dat = matriz.filas[pivote].vector[pivote].real
    if show:
        print("R{}->({})R{}".format(pivote + 1, 1 / pivote_dat, pivote + 1))
    fila = matriz.filas[pivote] * (1 / pivote_dat)
    fila2 = identidad.filas[pivote] * (1 / pivote_dat)
    identidad.filas[pivote] = fila2
    matriz.filas[pivote] = fila
    return matriz, identidad


def volver0(matriz=None, identidad=None, pivote=1, fila=1, show=True):
    if identidad is None:
        identidad = matriz.copy()
    valor_a_cambiar = matriz.filas[fila].vector[pivote]
    if valor_a_cambiar == 0:
        return matriz, identidad
    fila_piv = matriz.filas[pivote]
    if show:
        print("R{}->R{}+(({})R{})".format(fila + 1, fila + 1, -valor_a_cambiar, pivote + 1))
    row = fila_piv * (-valor_a_cambiar) + matriz.filas[fila]
    row2 = identidad.filas[pivote] * (-valor_a_cambiar) + identidad.filas[fila]
    identidad.filas[fila] = row2
    matriz.filas[fila] = row
    return matriz, identidad


matrizL1 = [
    [1, -2, 10],
    [2, 3, -8],
]
matriz1 = create_matrix(matrizL1)
inversaR = matriz1.gauss_jordan()
print(inversaR)

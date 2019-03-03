from multipledispatch import dispatch
from fractions import Fraction

class Vector:
    """clase envoltorio de una lista de numeros, no hereda por cuestiones de limitaciones"""
    def __init__(self, vector):
        
        self.vector = [Fraccion(element) if not isinstance(element,Fraccion) else element for element in vector]

    def __add__(self, newVector):
        if (not len(newVector.vector)==len(self.vector)):
            return 'Error, los vectores deben medir lo mismo'
        vectorFinal = list()
        for i in range(len(newVector.vector)):
            value = Fraccion(self.vector[i]+newVector.vector[i])
            vectorFinal.append(value)
        return Vector(vectorFinal)

    def __sub__(self, newVector):
        if (not len(newVector)==len(self.vector)):
            return 'Error, los vectores deben medir lo mismo'
        vectorFinal = list()
        for i in range(len(newVector)):
            value = Fraccion(self.vector[i]-newVector.vector[i])
            vectorFinal.append(value)
        return Vector(vectorFinal)

    def mul(self, number):
        vectorFinal = list()
        for i in range(len(self.vector)):
            value = Fraccion(self.vector[i]*number)
            vectorFinal.append(value)
        return Vector(vectorFinal)

    @dispatch(object)
    def __mul__(self, newVector):
        
        if(isinstance(newVector, Fraction) or isinstance(newVector,float)):
            if not isinstance(newVector,Fraccion):
                newVector = Fraccion(newVector)
            return self.mul(newVector.numerator/newVector.denominator)

        if(len(self.vector) != len(newVector.vector)):
            return "los vectores deben medir lo mismo"
        filasMatriz = list()
        for i in range(len(self.vector)):
            value = Fraccion(newVector*self.vector[i])
            filasMatriz.append(value)
        return Matriz(filasMatriz)
    
    #funcion que utiliza para multiplicar cada elemento del vector A
    #por el elemento correspondiente del vector B
    #se lee: A operando SOBRE el comportamiento de B
    #se utiliza la division entera para dejar libre 
    #la division normal en caso de ser necesario
    def __floordiv__(self, vector):
        if len(self.vector) != len(vector.vector):
            return "ERROR"
        vectorResultante = list()
        for i in range(len(vector.vector)):
            number1 =self.vector[i]if isinstance(self.vector[i],Fraccion)else Fraccion(self.vector[i])
            number2 =vector.vector[i]if isinstance(vector.vector[i],Fraccion)else Fraccion(vector.vector[i])
            value = Fraccion(number1 * number2).simplify()
            vectorResultante.append(value)

        return vectorResultante
    
    def normalize(self):
        copy = self.vector.copy()
        for i in range(len(self.vector)):
            copy[i] = Fraccion(self.vector[i])

    def __str__(self):
        res = ''
        res+=str([str(i.limit_denominator()) for i in self.vector])

        return res
    
    def __len__(self):
        return len(self.vector)

class Matriz:
    """clase envoltorio de una lista matriz (compuesta de mas listas), no hereda por cuestiones de limitacion"""
    def __init__(self, filas):
        self.filas = filas
        self.normalize()

    def __add__(self, newMatriz):
        if (not len(newMatriz.filas)==len(self.filas) and not len(newMatriz.filas[0].vector)==len(self.filas[0].vector)):
            return 'Error, las matrices deben tener las mismas dimensiones'
        vectorFinal = list()
        for i in range(len(newMatriz.filas)):
             vectorFinal.append(self.filas[i]+newMatriz.filas[i])
        return Matriz(vectorFinal)

    def __sub__(self, newMatriz):
        if (not len(newMatriz.filas)==len(self.filas) and not len(newMatriz.filas[0].vector)==len(self.filas[0].vector)):
            return 'Error, las matrices deben tener las mismas dimensiones'
        vectorFinal = list()
        for i in range(len(newMatriz.filas)):
             vectorFinal.append(self.filas[i]-newMatriz.filas[i])
        return Matriz(vectorFinal)
    
    @dispatch(int)
    def __mul__(self, value):
        matrizFinal = list()
        for i in range(len(self.filas)):
            matrizFinal.append(Fraccion(self.filas[i]*value))
        return Matriz(matrizFinal)
    
    @dispatch(object)
    def __mul__(self, newMatriz):
        """se ejecuta la multiplicacion de matriz*matriz
            en la que debemos comprobar que la cantidad de columnas de la matriz A
            sea igual a la cantidad de filas de la columna B
        """
        newMatriz.normalize()
        if len(self.filas[0].vector) != len(newMatriz.filas):
            return "Error, la matriz A debe tener la misma cantidad de columnas que la matriz B de filas"
        
        matrizFinal = list()
        columna =0
        #este ciclo itera sobre las filas de la matriz
        for x in range(len(self.filas)):
            vectorFila = list()
            #este ciclo itera sobre las columnas de la matriz
            for i in range(len(newMatriz.filas[0].vector)):
                #esta declaracion indica que se debe extraer la columna n
                #de la segunda matriz con la que se esta trabajando
                vectorColumna = extractColumn(newMatriz, i)
                #vector resultante es el vector que se da cuando se multiplican
                #los valores correspondientes de los vectores fila y columna que
                #se estan manejando en la iteracion
                vectorResultante = self.filas[x]//(vectorColumna)
                suma = sumatoria(vectorResultante)
                vectorFila.append(suma)
                columna+=1
            
            matrizFinal.append(Vector(vectorFila))
                 
        return Matriz(matrizFinal)

    def __pow__(self, value):
        """aqui se eleva una matriz a una potencia x"""
        if(len(self.filas)!=len(self.filas[0].vector)):
            return "Error, la matriz solo puede elevarse a la {value} si es cuadrada"

        if(value >= 2):
            """
                si la potencia es mayor o igual a 2, declaramos que el inicio de la matriz
                es la matriz al cuadrado y ya si el numero es mayor a 2, se continua de manera
                normal para evitar errores
            """
            matrizFinal = self * self
            if(value > 2):
                for i in range(value):
                    matrizFinal *= self

            return matrizFinal
        elif(value==1):
            """si la potencia es igual a 1, entonces, 
            no hace falta realizar operaciones y se devuelve la misma matriz"""
            return self
        else:
            return 1

    def normalize(self):
        for i in self.filas:
            i.normalize()

    def identidad(self,show = True):
        matrizRes = self.copy()
        #RECUERDA QUE LA IDENTIDAD SE RESUELVE COLUMNA POR COLUMNA PERO OPERANDO CON FILAS
        #resolvemos fila por fila
        if show:
            print(matrizRes)
        for i in range(len(self.filas)):
            matrizRes,_ = volver1(matrizRes,pivote=i,show=show)
            for x in range(len(self.filas)):
                if(i==x):
                    continue
                matrizRes,_ = volver0(matrizRes,pivote=i,fila=x,show=show)
        if show:
            print()
            print(matrizRes)
        return matrizRes
    def determinante(self):
        #el determinante se obtiene por medio de la multiplicacion recursiva de los determinantes inferiores
        #hasta que se llegue al determinante de 2x2
        matriz = self.copy()
        def determinate(matriz):
            if(len(matriz.filas)==2 and len(matriz.filas[0].vector)==2):
                return matriz.filas[0].vector[0]*matriz.filas[1].vector[1]-matriz.filas[1].vector[0]*matriz.filas[0].vector[1]
            determinante = 0
            for i in range(len(matriz.filas[0].vector)):
                matrizOp = matriz.copy()
                pivote = matrizOp.filas[0].vector[i]
                matrizOp = matrizOp.removeRow(0)
                matrizOp = matrizOp.removeCol(i)
                det = pivote*determinate(matrizOp)
                determinante +=pow(-1,i)*det
            return determinante

        return determinate(matriz)

    def inversa(self):
        determinante = self.determinante()
        if determinante == 0:
            return "La matriz no tiene inversa ya que su determinante es 0"
        matrizOperada = self.copy()
        print(matrizOperada)
        print('determinante=',determinante)
        matrizRes = matrizOperada.identidad(False)
        #resolvemos fila por fila
        for i in range(len(self.filas)):
            matrizOperada,matrizRes = volver1(matrizOperada,matrizRes,i)
            for x in range(len(self.filas)):
                if(i==x):
                    continue
                matrizOperada,matrizRes = volver0(matrizOperada,matrizRes,i,x)
        print()
        return matrizRes
    def copy(self):
        matriz = []
        for i in self.filas:
            vector = list()
            for x in i.vector:
                vector.append(x)
            matriz.append(vector)
        res = createMatrix(matriz)
        return res
    
    def removeRow(self, index):
        matriz = self.copy()
        if(index==0):
            matriz.filas = matriz.filas[1:]
        else:
            pass
        return matriz

    def removeCol(self,index):
        matriz = self.copy()
        for i in matriz.filas:
            fila = i.vector.copy()
            if(index==0):
                fila = fila[1:]
            else:
                if index==1:
                    fila = [fila[0]]+fila[2:]
                elif index < (len(matriz.filas[-1].vector)-1):
                    fila = fila[:index]+fila[index+1:]
                else:
                    fila = fila[:index]
            i.vector = fila
        return matriz
    def __str__(self):
        """devuelve el 'valor' de la matriz mostrando fila por fila sus valores"""
        resultado = ""
        for i in self.filas:
            resultado += str(i)+'\n'
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
        if(self.numerator==0 or fraccion.denominator==0):
            return 0
        fracRes = Fraccion(self.numerator*fraccion.denominator,self.denominator*fraccion.numerator)
        return fracRes.simplify()
    @dispatch(int)
    def __truediv__(self, numero):
        if(self.numerator==0):
            return 0
        fracRes = Fraccion(self.numerator,self.denominator*numero)
        return fracRes.simplify()
    
    def mul(self, value):
        fracN = Fraccion(value)
        fracRes = self*fracN
        
        return fracRes.simplify()

    @dispatch(object)
    def __mul__(self, fraccion):
        if(isinstance(fraccion, int) or isinstance(fraccion,float)):
            return self.mul(fraccion)

        if(self.numerator==0 or fraccion.numerator==0):
            return Fraccion(0)
        fracRes = Fraccion(self.numerator*fraccion.numerator,self.denominator*fraccion.denominator)
        return fracRes.simplify()
    
    @dispatch(object)
    def __add__(self, fraccion):
        numerador = self.numerator*fraccion.denominator+fraccion.numerator*self.denominator
        denominador = self.denominator*fraccion.denominator
        fracRes = Fraccion(numerador,denominador)
        return fracRes.simplify()
    
    @dispatch(int)
    def __sub__(self, numero):
        fracNum = Fraccion(numero)
        fracRes = self+fracNum
        return fracRes
    
    @dispatch(object)
    def __sub__(self, fraccion):
        numerador = self.numerator*fraccion.denominator-fraccion.numerator*self.denominator
        denominador = self.denominator*fraccion.denominator
        fracRes = Fraccion(numerador,denominador)
        return fracRes.simplify()
    
    def simplify(self):
        self =self.limit_denominator()
        newFrac = self
        newFrac = newFrac.limit_denominator()if isinstance(newFrac,Fraccion) else self
        if(isinstance(newFrac,Fraccion)):
            realVal = newFrac.numerator/newFrac.denominator
            if newFrac.numerator==0:
                return 0
            elif realVal%1==0:
                return realVal//1
        return Fraccion(newFrac)

    def __str__(self):
        res = self.limit_denominator()
        return '{}/{}'.format(res.numerator,res.denominator)

def sumatoria(coleccion,index=0):
    """funcion que suma todos los elementos de un vector"""
    value = Fraccion(coleccion[index]) if not isinstance(coleccion[index],Fraccion) else coleccion[index]
    if(index+1 == len(coleccion)):
        return value
    return value+sumatoria(coleccion,index+1)

def extractColumn(matriz, columnIndex):
    vectorColumna = list()
    for i in matriz.filas:
        """se extraen los valores referentes a la columna indicada por columnIndex de la segunda matriz"""
        value = Fraccion(i.vector[columnIndex]) if isinstance(i,int) else i.vector[columnIndex]
        vectorColumna.append(value)
    return Vector(vectorColumna)

def createMatrix(matrizArreglo):
    #extraemos los elementos de la matriz original y colocamos cada lista componente en
    #un vector para que se pueda manipular facilmente y creamos una lista con esos vectores
    vectores = [Vector(element) for element in matrizArreglo]
    matrizResultado = Matriz(vectores)
    return matrizResultado

def volver1(matriz=None,identidad=None,pivote=1,show=True):
    if identidad==None:
        identidad=matriz.copy()
    pivoteDat = matriz.filas[pivote].vector[pivote].real
    if show:
        print("R{}->({})R{}".format(pivote+1,1/pivoteDat,pivote+1))
    fila = matriz.filas[pivote]*(1/pivoteDat) 
    fila2 = identidad.filas[pivote]*(1/pivoteDat)
    identidad.filas[pivote] = fila2
    matriz.filas[pivote] = fila
    return matriz,identidad
def volver0(matriz=None,identidad=None,pivote=1,fila=1,show=True):
    if identidad==None:
        identidad=matriz.copy()
    valorACambiar = matriz.filas[fila].vector[pivote]
    if(valorACambiar==0):
        return matriz,identidad
    filaPiv = matriz.filas[pivote]
    if show:
        print("R{}->R{}+(({})R{})".format(fila+1,fila+1,-valorACambiar,pivote+1))
    row = filaPiv*(-valorACambiar)+matriz.filas[fila]
    row2 = identidad.filas[pivote]*(-valorACambiar)+identidad.filas[fila]
    identidad.filas[fila] = row2
    matriz.filas[fila] = row
    return matriz,identidad

matrizL1 = [
    [1,1,1,1],
    [1,2,-1,2],
    [1,-1,2,1],
    [1,3,3,2],
]
matriz1 = createMatrix(matrizL1)
print(matriz1.inversa())
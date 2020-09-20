import numpy as np

#Entrada: 
#Salida:        arreglo de bits definido en el mismo  código
#Descripción:   crea un arreglo de bits de tamaño fijo
def generarSenal(largo):
    senal = np.random.randint(2,size = largo)
    return senal




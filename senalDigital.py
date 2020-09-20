import numpy as np

# Entradas: largo -> entero que representa el largo del array a crear
#Salidas:   void
#------------------------------------------
#Esta funcion genera una señal digital aleatoria
def generarSenal(largo):
    senal = np.random.randint(2,size = largo)
    return senal




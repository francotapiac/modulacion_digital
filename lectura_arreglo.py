import numpy as np

#Entrada: 
#Salida:        arreglo de bits definido en el mismo  código
#Descripción:   crea un arreglo de bits de tamaño fijo
def crearArregloBits():
    return [1,1,0,1,0,0,1,1,0,1,0,1,0,0] 


#Entrada:       frecuencia de la portadora y arreglo de tiempo de la portadora
#Salida:        señal portadora representada como un coseno
#Descripción:   se crea una señal portadora, para lo cual se utiliza un coseno donde sus parámetros son la
#               frecuencia de la portadora y el tiempo de la portadora
def obtenerPortadora(frecuenciaPortadora,tiempoPortadora):
    portadora = np.cos(2*np.pi*frecuenciaPortadora*tiempoPortadora)
    return portadora

#Entrada:       tasa de bits definido como bps, frecuencia de muestreo de la portadora
#Salida:        tiempo de la señal portadora
#Descripción:   crea un arreglo de tiempos el cual inicia de 0 y termina en 1/tasa de bits
def obtenerTiempoPortadora(bps,frecuenciaMuestreoPortadora):
    tiempoPortadora = np.linspace(0,1/bps,frecuenciaMuestreoPortadora)   
    return tiempoPortadora



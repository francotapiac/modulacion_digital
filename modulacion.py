import numpy as np
import scipy as sc
import graficar as graf
from scipy import integrate
# Entradas: senal -> array con los datos de la señal
#           bps -> Tasa de bits por segundo utilizada
#           freqPortadora -> frecuencia de la señal portadora utilizada
#           freqMuestreoPortadora -> frecuencia de muestreo de la señal portadora utilizada
#           cond -> booleano utilizado para saber si se grafica o no
# Salidas:  senalModulada -> array con los datos de la señal modulada
#           tiempoModulada -> array que representa el tiempo
#------------------------------------------
# En esta funcion primero se genera una señal portadora dependiendo del bps ingresado. 
# Luego para cada bit en la señal digital ingresada se multiplicada por cada dato de la 
# señal portadora y el resultado se guarda en un array
# Finalmente, se obtiene el tiempo de la señal modulada.
def modularASK(senal, bps, freqPortadora, freqMuestreoPortadora, cond):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #Graficar Portadora en el tiempo
    if(cond):
        graf.graficar(portadora, tiempoPortadora, "Señal Portadora en el tiempo", "Tiempo (s)", "Amplitud","f(t) = 3*cos(2pi*f*t)")

    #Algoritmo para modular
    senalModulada = []
    for bit in senal:
        for dato in portadora:
            senalModulada.append(3*bit*dato)
        #modulador = np.concatenate([modulador,(bit*portadora)])   
    tiempoModulada = np.linspace(0,len(senal)/bps,len(senalModulada))
    return np.array(senalModulada),tiempoModulada
    #Generar intervalo de tiempo para la modulada

# Entradas: senal -> array con los datos de la señal modulada
#           bps -> Tasa de bits por segundo utilizada
#           freqPortadora -> frecuencia de la señal portadora utilizada
#           freqMuestreoPortadora -> frecuencia de muestreo de la señal portadora utilizada
# Salidas:  demodulada -> array con los datos de la señal demodulada
#------------------------------------------  
# En esta funcion primero se genera una portadora. Luego se calcula 
# un area aproximada de la portadora. Despues se recorre la señal modulada
# por cada segmento que representa un bit. A dicho segmento se le calcula 
# el area y se compara con el area ya calculada. Si el area es mayor o igual
# es un bit 1 sino es 0. Dichos bits se van guardando en un arreglo
# Finalmente se retorna el arreglo.
def demodularASK(modulada, bps,freqPortadora, freqMuestreoPortadora):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    areaEstandar = integrate.trapz(2*portadora*portadora, tiempoPortadora)
    inicio = 0
    fin = len(tiempoPortadora)
    demodulada = []
    for i in range(0,len(modulada), len(tiempoPortadora)):
        area = integrate.trapz(portadora*modulada[inicio:fin], tiempoPortadora)
        if(area >= areaEstandar):
            demodulada.append(1)
        else:
            demodulada.append(0)
        inicio = fin
        fin = fin + len(tiempoPortadora)
    return demodulada
import numpy as np
import scipy as sc
import graficar as graf
from scipy import integrate
from scipy.signal import butter, lfilter, freqz

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
    portadora = 3*np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #Graficar Portadora en el tiempo
    if(cond):
        graf.graficar(portadora, tiempoPortadora, "Señal Portadora en el tiempo", "Tiempo (s)", "Amplitud","f(t) = 3*cos(2pi*f*t)")

    #Algoritmo para modular
    senalModulada = []
    for bit in senal:
        for dato in portadora:
            senalModulada.append(bit*dato)
        #modulador = np.concatenate([modulador,(bit*portadora)])   
    tiempoModulada = np.linspace(0,len(senal)/bps,len(senalModulada))
    return np.array(senalModulada),tiempoModulada

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
def demodularASK(modulada, tiempoModulada, bps,freqPortadora, freqMuestreoPortadora):
    order = 4
    fs = 90.0       # sample rate, Hz
    cutoff = 1.3
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = 3*np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    inicio = 0
    fin = len(tiempoPortadora)
    demodulada = []
    for i in range(0,len(modulada), len(tiempoPortadora)):
        rectificada = portadora*modulada[inicio:fin]
        filtrada = butter_lowpass_filter(rectificada, cutoff, fs, order)
        #Estapa de desicion
        avg = np.average(filtrada)
        if(avg > 2.5):
            demodulada.append(1)
        else:
            demodulada.append(0)
        inicio = fin
        fin = fin + len(tiempoPortadora)
    return demodulada

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
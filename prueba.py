#Librerias
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import graficar as graf
import senalDigital as senal
import modulacion as mod
import simulacion as sim
from numpy.random import rand, randn
from scipy import integrate
from scipy.signal import butter, lfilter, freqz

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
def demodularASK(modulada, tiemporModulada, bps,freqPortadora, freqMuestreoPortadora):
    #Generar Intervalo de tiempo para la portadora
    tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
    #Generar Portadora
    portadora = np.cos(2*np.pi*freqPortadora*tiempoPortadora)
    #modulada = lowPassFilter(modulada,10000,80,1000,0)
    areaEstandar = integrate.trapz(portadora*portadora, tiempoPortadora)
    inicio = 0
    fin = len(tiempoPortadora)
    demodulada = []
    for i in range(0,len(modulada), len(tiempoPortadora)):
        area = integrate.trapz(portadora*modulada[inicio:fin], tiemporModulada[inicio:fin])
        if(area > 0):
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

def generarSenal(largo):
    senal = np.random.randint(2,size = largo)
    return senal

#Datos Iniciales
largoSenal = 10
bps = 10
freqPortadora = 3*bps
freqMuestreoPortadora = 5*freqPortadora
snrDb1 = 1
snrDb2 = 10

########################################################################################################
#Prueba para un caso pequeño
#         Generar Señal
#senalDigital = [0,0,0,1,0,0,1,0,0,1]
senalDigital = generarSenal(10000)
tiempo = np.linspace(0,len(senalDigital)/bps,len(senalDigital))
plt.figure()
plt.plot(tiempo,senalDigital)
plt.title("Senal")
#          Modular la Señal
modulada, tiempoModulada = mod.modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, True)
plt.figure()
plt.plot(tiempoModulada,modulada)
plt.title("Modulada")
#          Agregar Ruido

moduladaRuido1 = sim.simuladorRuido(modulada, tiempoModulada, snrDb1, False)     #SNR = 7
plt.figure()
plt.plot(tiempoModulada,moduladaRuido1)
plt.title("Modulada ruido 1 snr")
moduladaRuido2 = sim.simuladorRuido(modulada, tiempoModulada, snrDb2, False) #SNR = 1
plt.figure()
plt.plot(tiempoModulada,moduladaRuido2)
plt.title("Modulada ruido 10 snr")
"""
port = portadora = 3*np.cos(2*np.pi*freqPortadora*tiempoModulada)
new = port * modulada
plt.figure()
plt.plot(tiempoModulada,new)
plt.title("Modulada ruido 1 snr multiplicada por portadora")

#Rectificador
new2 = port * modulada
plt.figure()
plt.plot(tiempoModulada,new2)
plt.title("Modulada ruido 10 snr multiplicada por portadora")

order = 4
fs = 90.0       # sample rate, Hz
cutoff = 1.3

#LPF
y = butter_lowpass_filter(new, cutoff, fs, order)
plt.figure()
plt.plot(tiempoModulada,y)
plt.title("Modulada ruido 1 snr multiplicada por portadora FILTRADA")
print(y)
y = butter_lowpass_filter(new2, cutoff, fs, order)
plt.figure()
plt.plot(tiempoModulada,y)
plt.title("Modulada ruido 10 snr multiplicada por portadora FILTRADA")

print(y)
print("------------------------")
tiempoPortadora = np.linspace(0,1/bps,freqMuestreoPortadora)
inicio = 0
fin = len(tiempoPortadora)
dem = []
for i in range(0,len(y), len(tiempoPortadora)):
    avg = np.average(y[inicio:fin])
    print("avg: "+str(avg))
    if(avg > 2):
        dem.append(1)
    else:
        dem.append(0)
    inicio = fin
    fin = fin + len(tiempoPortadora)

cont = 0
for i in range(len(dem)):   
    if(senalDigital[i] != dem[i]):
        cont = cont +1
ber = cont/len(dem)

print("ber calculado: "+str(ber))    

#plt.show()
#          Demodular la Señal
#demodulada = mod.demodularASK(moduladaRuido, tiempoModulada, bps, freqPortadora, freqMuestreoPortadora)

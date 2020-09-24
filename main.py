##########################################################################################################
###########################      Laboratorio 4: Modulador Digital       ##################################
###########################         Sebastian Orellana Verdejo          ##################################
###########################            Franco Tapia Cabañas             ##################################
###########################                                             ##################################
###########################            Redes de Computadores            ##################################
##########################################################################################################
###########################    Nota: si l señal a generar es muy        ##################################
###########################    grande es programa se puede demorar      ##################################
###########################    en ejecutarse.                           ##################################
##########################################################################################################

#Librerias
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import graficar as graf
import senalDigital as senal
import modulacion as mod
import simulacion as sim
from numpy.random import rand, randn

########################################################################################################
#Datos Iniciales
largoSenal = 10
bps = 5
freqPortadora = 30
freqMuestreoPortadora = 2000//bps
snrDb = 1

########################################################################################################
#Prueba para un caso pequeño
#         Generar Señal
print("Generando Simulacion para señal pequeña...")
senalDigital = [1,0,0,1,0,0,1,1,0,0]
tiempo = np.linspace(0,len(senalDigital)/bps,len(senalDigital))
graf.graficarSenalDigital(senalDigital, tiempo, "Señal Digital en el Tiempo", "Tiempo (s)", "Amplitud", "BPS = 5")

#          Modular la Señal
print("Modulando señal...")
modulada, tiempoModulada = mod.modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, True)
graf.graficar(modulada, tiempoModulada, "Señal Modulada en ASK", "Tiempo (s)", "Amplitud", "Modulada")

#          Agregar Ruido
moduladaRuido = sim.simuladorRuido(modulada, tiempoModulada, 10, True)
moduladaRuido = sim.simuladorRuido(modulada, tiempoModulada, snrDb, True) #SNR = 1
graf.graficar(moduladaRuido, tiempoModulada, "Señal Modulada con Ruido AWGN", "Tiempo (s)", "Amplitud", "ASK con SNR = 1")

#          Generar grafico de señal Rectificada
print("Demodulando señal...")
portadora = 3*np.cos(2*np.pi*freqPortadora*tiempoModulada)
rectificada = portadora * moduladaRuido
graf.graficar(rectificada, tiempoModulada, "Señal ASK Rectificada", "Tiempo (s)", "Amplitud", "Señal ASK*portadora")

#          Generar grafico de señal Filtrada (Filtro pasa Bajos)
order = 4
fs = 90.0       # sample rate, Hz
cutoff = 1.3
filtrada = mod.butter_lowpass_filter(rectificada, cutoff, fs, order)
graf.graficar(filtrada, tiempoModulada, "Señal Filtrada", "Tiempo (s)", "Amplitud", "filtrada")

#          Demodular la Señal
demodulada = mod.demodularASK(moduladaRuido, tiempoModulada, bps, freqPortadora, freqMuestreoPortadora)
graf.graficarSenalDigital(demodulada, tiempo, "Señal Demodulada", "Tiempo (s)", "Amplitud", "ASK demodulada")

########################################################################################################
#Simulacion Caso grande
print("Generando Simulacion para señal grande...")
largoSenal = 10000
arraySNRinDb = range(-1,17)
arrayBPS = [5,10,15]
resultadoSimulacion = [None]*len(arrayBPS)
i = 0
# Para cada bps
for bps in arrayBPS:
    print("Simulando canal de comunicacion para señal de "+str(bps)+" bps...")
    BER = []
    freqPortadora = 30
    freqMuestreoPortadora = 2000//bps
    senalDigital = senal.generarSenal(largoSenal)
    print("Modulando señal...")
    modulada, tiempoModulada = mod.modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, False)
    print("Demodulando señal...")
    BER = sim.simulacion(senalDigital, modulada, tiempoModulada, arraySNRinDb, freqPortadora, freqMuestreoPortadora, bps)
    resultadoSimulacion[i] = BER
    i = i+ 1
graf.graficarResultadosBER(resultadoSimulacion, arraySNRinDb)

########################################################################################################
#Mostrar resultados
graf.mostrarGraficos()



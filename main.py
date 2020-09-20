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
freqPortadora = 3*bps
freqMuestreoPortadora = 5*freqPortadora
snrDb = 1

########################################################################################################
#Prueba para un caso pequeño
#         Generar Señal
senalDigital = [0,0,0,1,0,0,1,0,0,1]
tiempo = np.linspace(0,len(senalDigital)/bps,len(senalDigital))
graf.graficarSenalDigital(senalDigital, tiempo, "Señal Digital en el Tiempo", "Tiempo (s)", "Amplitud", "BPS = 5")

#          Modular la Señal
modulada, tiempoModulada = mod.modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, True)
graf.graficar(modulada, tiempoModulada, "Señal Modulada en ASK", "Tiempo (s)", "Amplitud", "Modulada")

#          Agregar Ruido
moduladaRuido = sim.simuladorRuido(modulada, tiempoModulada, 7, True)     #SNR = 7
moduladaRuido = sim.simuladorRuido(modulada, tiempoModulada, snrDb, True) #SNR = 1
graf.graficar(moduladaRuido, tiempoModulada, "Señal Modulada con Ruido AWGN", "Tiempo (s)", "Amplitud", "ASK con SNR = 1")

#          Demodular la Señal
demodulada = mod.demodularASK(moduladaRuido, bps, freqPortadora, freqMuestreoPortadora)

########################################################################################################
#Simulacion Caso grande
largoSenal = 10000
arraySNRinDb = range(-2,20)
arrayBPS = [10,15,20]
resultadoSimulacion = [None]*len(arrayBPS)
i = 0
# Para cada bps
for bps in arrayBPS:
    BER = []
    freqPortadora = 2*bps
    freqMuestreoPortadora = 3*freqPortadora
    senalDigital = senal.generarSenal(largoSenal)
    modulada, tiempoModulada = mod.modularASK(senalDigital, bps, freqPortadora, freqMuestreoPortadora, False)
    BER = sim.simulacion(senalDigital, modulada, tiempoModulada, arraySNRinDb, freqPortadora, freqMuestreoPortadora, bps)
    resultadoSimulacion[i] = BER
    i += 1
graf.graficarResultadosBER(resultadoSimulacion, arraySNRinDb)

########################################################################################################
#Mostrar resultados
graf.mostrarGraficos()



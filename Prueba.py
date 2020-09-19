"""
Laboratorio 4 de Redes de Computadores por Shalini Ramchandani & Javier Arredondo
"""
###################################################
################## Importaciones ##################
###################################################
from numpy import linspace, pi, cos, random, concatenate, asarray
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy import integrate
import warnings
warnings.filterwarnings('ignore')

"""
Implementación de de modulación por desplazamiento de amplitud  [Amplitude-shift keying (ASK)]:
Es una forma de modulación en la cual se representan los datos digitales como variaciones de amplitud de la onda portadora en función de los datos a enviar.
La amplitud de una señal portadora analógica varía conforme a la corriente de bit (modulando la señal), manteniendo la frecuencia y la fase constante. 
El nivel de amplitud puede ser usado para representar los valores binarios 0s y 1s. Podemos pensar en la señal portadora como un interruptor ON/OFF. 
En la señal modulada, el valor lógico 0 es representado por la ausencia de una portadora, así que da ON/OFF la operación de pulsación y de ahí el nombre dado. 
La técnica ASK también es usada comúnmente para transmitir datos digitales sobre la fibra óptica. 
Para los transmisores LED, el valor binario 1 es representado por un pulso corto de luz y el valor binario 0 por la ausencia de luz.
"""

# FUNCIONES
"""
Función que se encarga de abrir archivos .wav y obtiene la frecuencia e información de la señal.
Entrada:
        name-> nombre del archivo con extensión .wav
Salida:
        rate  -> frecuencia de muestreo.
        info  -> datos de la señal.
        times -> tiempo para cada dato en info.
"""
def openWav(name):
        rate, info = read(name)
        dimension = info[0].size
        if(dimension == 1):
                data = info
        else:
                data = info[:,dimension-1]
        n = len(data)
        Ts = n / rate
        times = linspace(0, Ts, n)
        return (rate, data, times)
"""
Transformación de entero a binario, con n-bits.
Entrada:
        num-> Número a transformar
        bits-> Cantidad de bits utilizados para convertir a binario
Salida:
        String que representa el número en binario.
"""
def intToBin(num, bits):
        numBin = format(num, "b").zfill(bits)
        if(numBin[0] == "-"):
                return "1"+numBin[1:]
        return numBin
"""
Calculo de la cantidad de bits máximos que se deben ocupar.
Entrada:
        maxi-> El número mayor de la señal de entrada.
Salida:
        Cantidad de bits a utilizar
"""
def sizeBin(maxi):
        return len(format(maxi, "b")) + 1

"""
Transformacion de un arreglo de enteros a binario.
Entrada:
        signal-> señal leída.
Salida:
        Señal de entrada convetida en binario. Cada número de la señal se transforma a binario
        luego se agrega a una lista única.
"""
def arrayToBin(signal):
	dataBin = []
	bits = sizeBin(max(signal))
	for data in signal:
                _bin = intToBin(data, bits)
                for i in _bin:
                        dataBin.append(int(i))
	return dataBin

"""
Graficar arreglo de binarios
Entrada:
        binSignal-> Arreglo de numeros binarios.
        duration-> duracion del audio
        sample-> muestra a graficar
        title-> titulo del grafico
"""
def graphDigitalData(binSignal, duration, sample, bps, title):
        binFixed = []
        for i in binSignal:
                for j in range(0, bps):
                        binFixed.append(i)
        t = linspace(0, duration, len(binFixed))
        t = t[:sample*bps]
        plt.plot(t, binFixed[:sample*bps])
        plt.ylim(0, 2)
        plt.xlim(0, t[-1])
        plt.xlabel('Tiempo [s]');
        plt.ylabel('Amplitud [dB]');
        plt.title(title);
        plt.grid(True)
        plt.savefig("images/"+title+".png")
        plt.show()
"""
Funcion que grafica el audio
Entrada:
        data-> datos del audio
        time-> vector tiempo del audio
        title-> titulo del grafico
        sample-> muestra a graficar
"""
def graphData(data, time, sample, bps, title):
        total = sample * bps
        plt.plot(time[0:total], data[0:total], color = "green")
        plt.ylim(-6, 6)
        plt.xlim(0, time[-1])
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Amplitud [dB]')
        plt.title(title)
        plt.grid(True)
        plt.savefig("images/"+title + ".png")
        plt.show()
"""
Modulacion ASK
Entrada:
        signal-> señal en binario
        bps-> bits por segundo para portadora
        duration-> duracion del audio
        sample-> muestra para realizar ASK
Salida:
        - Arreglo con modulacion ASK
        - Arreglo de tiempo para modulacion ASK
"""
def ASKmodulation(signal, bps, duration, sample):
        A = 4  # Amplitudes de cada coseno
        B = 2
        f = 2  # Frecuencia de carrier
        timeCarrier = linspace(0, 1 - 1/bps, bps)       # Tiempo de un coseno, 1 seg -> 100 muestras
        dataCarrier = cos(2 * pi * f * timeCarrier)     # Carrier: onda coseno
        sizeBin = len(signal)                           # Hay 1169808 elementos. Cantidad de bits totales en el audio.
        cutBin = signal[0:sample]                       # Recortamos la muestra. Tomamos los 10000 primeros
        ASK = []
        for i in  cutBin:
                if(i == 1):
                        ASK = concatenate([ASK, (A * dataCarrier)])
                else:
                        ASK = concatenate([ASK, (B * dataCarrier)])
        duration = len(cutBin) * duration / len(signal)
        t = linspace(0, duration, len(ASK)) # Creamos un vector tiempo para graficar. Dura 9s con un total de muchos puntos.
        return ASK, t

"""
Función que agrega ruido a la señal modulada.
Entrada: signal->señal modulada
         snr-> razón de ruido
Salida:
        - señal con ruido
        - ruido
"""
def addNoise(signal, snr):
        noise = random.normal(0.0, snr, len(signal))
        signal = signal + noise
        return noise+signal, noise
"""
Función que realiza la demodulacion ASK de la señal modulada.
Entrada:
        askSignal-> señal modulada ASK
        bps-> bits por segundo. Se utiliza para saber cuantos bits hay en un segundo.
Salida:
        señal demodulada. Señal digital
"""
def ASKdemodulation(askSignal, bps):
        f = 2
        A = 4
        timeCarrier = linspace(0, 1 - 1/bps, bps)   # Tiempo de un coseno, 1 seg, 100 muestras, con 100 queda bien, 50 queda horrible
        dataCarrier = cos(2 * pi * f * timeCarrier)     # Carrier: onda coseno
        one = integrate.trapz(A * dataCarrier * dataCarrier, timeCarrier)        
        back = 0 # Con back y front manejamos los intervalos de integración
        signalDemotulated = []
        for i in range(0, len(askSignal), len(timeCarrier)): # En toda la señal recorreremos trozos del tamaño de la portadora
                front = back + len(timeCarrier)
                sliceSignal = dataCarrier * askSignal[back:front]
                area = integrate.trapz(sliceSignal, timeCarrier)
                if(area >= one):
                        signalDemotulated.append(1)
                else:
                        signalDemotulated.append(0)
                back = front
        return signalDemotulated

"""
Función que se utiliza para obtener la cantidad porcentual de bits erroneos, respecto a la señal digital original con la digital demodulada.
Entrada:
        signal-> señal digital original
        demodulate-> señal demodulada. (esta señal debería tener ruido)
Salida:
        porcentaje de bits erroneos
"""
def getError(signal, demodulate):
        error = asarray(demodulate) - asarray(signal)
        count = 0
        for i in error:
                if i == 0:
                        count = count + 1
        return 1 - count/len(signal)

print("Modulación ASK")
bps = 100         # Bits por segundo
sample = 1000  # Muestra de datos a tomar, para los graficos. Muestra total 1169808
snr = 0.1
# Procedimientos:
#       1. Leer audio y calcular tiempo de duracion.
print("> Lectura del archivo")
rate, data, times = openWav("handel.wav")
totalTime = len(data)/rate
#       2. Binarizar audio
print("> Binarización de audio")
dataBin = arrayToBin(data)
graphDigitalData(dataBin, totalTime, sample, bps, "Señal digital")
#       3. Aplicar modulacion ASK
print("> Modulación ASK")
askData, askTime = ASKmodulation(dataBin, bps, totalTime, sample)
graphData(askData, askTime, sample, bps, "Señal con modulacion ASK")
#       4. Agregar ruido a la señal
print("> Generando ruido")
askNoise, noise = addNoise(askData, snr)
print("> Agregando ruido a señal modulada")
graphData(noise, askTime, sample, bps, "Ruido con razon de " + str(snr))
graphData(askNoise, askTime, sample, bps, "Señal ASK + ruido")
#       5. Aplicar demodulacion a la señal
print("> Demodulando")
demodulation = ASKdemodulation(askNoise, bps)
timeAux = len(demodulation) * totalTime / len(dataBin)
graphDigitalData(demodulation, timeAux, sample, bps, "Señal demodulada")
error = getError(dataBin[:sample], demodulation)
print("Hay un error del " + str(error * 100) + "%, respecto a la señal original")
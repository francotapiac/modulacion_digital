import matplotlib.pyplot as plt

# Entradas: ruido -> array 
#           titulo -> String
#           xlabel -> String
#           ylabel -> String
#           labelPlot -> String
#Salidas:   void
#------------------------------------------
#Esta funcion grafica el ruido AWGN obtenido
def graficarRuido(ruido, titulo, xLabel, yLabel, labelPlot):
    plt.figure(figsize=[10,5])
    plt.plot(ruido, label=labelPlot)
    plt.legend(loc='upper right')
    plt.title(titulo)
    plt.ylim([-3, 3])
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()
    plt.savefig('resultados_obtenidos/'+titulo+'.png')

# Entradas: senal -> array con los datos de la señal
#           tiempo -> array que representa el tiempo
#           titulo -> String
#           xlabel -> String
#           ylabel -> String
#           labelPlot -> String
#Salidas:   void
#------------------------------------------
#Esta funcion grafica la señal modulada en ASK en el tiempo
def graficar(senal, tiempo, titulo, xLabel, yLabel, labelPlot):
    plt.figure(figsize=[10,5])
    plt.plot(tiempo, senal, label=labelPlot)
    plt.legend(loc='upper right')
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()
    plt.savefig('resultados_obtenidos/'+titulo+'.png')

# Entradas: senal -> array con los datos de la señal digital
#           tiempo -> array que representa el tiempo
#           titulo -> String
#           xlabel -> String
#           ylabel -> String
#           labelPlot -> String
#Salidas:   void
#------------------------------------------
#Esta funcion grafica la señal digital en el tiempo
def graficarSenalDigital(senal, tiempo, titulo, xLabel, yLabel, labelPlot):
    plt.figure(figsize=[10,5])
    plt.plot(tiempo,senal, drawstyle='steps-pre', label=labelPlot)
    plt.legend(loc='upper right')
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()
    plt.savefig('resultados_obtenidos/'+titulo+'.png')

# Entradas: resultado -> array que contiene los BER para cada señal con distinto BPS
#           arraySNR -> array que contiene los SNR en dB utilizados
#Salidas:   void
#------------------------------------------
#Esta funcion grafica los resultados de la simulación
def graficarResultadosBER(resultado, arraySNR):
    plt.figure()
    plt.plot(arraySNR, resultado[0], 'o-',color="red" , label="bps = 10")
    plt.plot(arraySNR, resultado[1], 'o-', color="blue", label="bps = 15")
    plt.plot(arraySNR, resultado[2], 'o-', color="green", label="bps = 20")
    #plt.axis([0, 10, 1e-6, 0.1])
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('SNR(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BER vs SNR')
    plt.legend(loc='lower left')
    plt.savefig('resultados_obtenidos/'+'BER vs SNR.png')

# Entradas: void
#Salidas:   void
#------------------------------------------
#Esta funcion muestra los graficos generados
def mostrarGraficos():
    plt.show()
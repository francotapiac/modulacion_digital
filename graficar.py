import matplotlib.pyplot as plt

def graficar(senal, tiempo, titulo, xLabel, yLabel):
    plt.figure()
    plt.plot(tiempo, senal)
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

def graficarSenalDigital(senal, tiempo, titulo, xLabel, yLabel):
    plt.figure()
    plt.plot(tiempo,senal, drawstyle='steps-pre')
    plt.title(titulo)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.grid()

def graficarResultadosBER(resultado, arraySNR):
    plt.figure()
    plt.plot(arraySNR, resultado[0], 'bo', arraySNR, resultado[0], 'k',color="red" )
    plt.plot(arraySNR, resultado[1], 'bo', arraySNR, resultado[1], 'k', color="blue")
    plt.plot(arraySNR, resultado[2], 'bo', arraySNR, resultado[2], 'k', color="green")
    #plt.axis([0, 10, 1e-6, 0.1])
    plt.xscale('linear')
    plt.yscale('log')
    plt.xlabel('SNR(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BER vs SNR')

def mostrarGraficos():
    plt.show()
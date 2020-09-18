import matplotlib.pyplot as plt

def graficar(modulador, tiempoModulador, titulo):
    plt.plot(tiempoModulador,modulador)
    plt.title(titulo)
    plt.grid()
    plt.show()

def crearSubGrafico(dato,valorEjeX,titulo,xLabel,yLabel,color,filas,columnas,posicion):
    plt.subplot(filas,columnas,posicion)
    plt.title(titulo)
    plt.plot(valorEjeX,dato,color=color)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
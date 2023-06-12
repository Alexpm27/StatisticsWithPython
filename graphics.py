import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import formulas
import numpy as np


def histogram(data, window):
    plt.hist(formulas.absolute_frequency(data))
    fig, ax = plt.subplots(figsize=(7, 7), dpi=50)
    plt.hist(data, bins=10)
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.title('Histograma')
    plt.savefig('graph/histograma.PNG')
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    return canvas.get_tk_widget()


def frequency_polygon(data, window):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=50)
    mark = formulas.class_mark(data)
    frequency = formulas.absolute_frequency(data).values.tolist()
    mark.insert(0, 0)
    frequency.append(0)
    plt.plot(mark, frequency, marker='o')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.title('Polígono de frecuencias')

    plt.grid(True)
    plt.savefig('graph/frec_pol.PNG')
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    return canvas.get_tk_widget()


def warheads(data, window):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=50)
    frequency = formulas.absolute_frequency(data).values.tolist()
    frequency.insert(0, 0)
    frequency_acu = np.cumsum(frequency)

    plt.plot(frequency_acu, marker='o')
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia acumulada')
    plt.title('Gráfico de Ojiva')
    plt.ylim(0)
    plt.grid(True)
    plt.savefig('graph/warheads.PNG')
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    return canvas.get_tk_widget()


def bars(data, window):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=50)
    if data.dtype == "object":
        frequency = data.value_counts()
        index = frequency.index
    else:
        frequency = formulas.absolute_frequency(data).values.tolist()
        index = formulas.class_mark(data)

    plt.bar(index, frequency)
    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.title('Gráfico de Barras')
    plt.savefig('graph/bars.PNG')
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    return canvas.get_tk_widget()


def cake(data, window):
    fig, ax = plt.subplots(figsize=(7, 7), dpi=50)
    if data.dtype != "object":
        frequency = formulas.absolute_frequency(data).values.tolist()
        label = formulas.absolute_frequency(data).values.tolist()
    else:
        frequency = data.value_counts()
        label = frequency.index

    plt.pie(frequency, labels=label, autopct='%1.1f%%')
    plt.title('Gráfico de Pastel')
    plt.legend(label)
    plt.axis('equal')
    plt.savefig('graph/cake.PNG')
    plt.show()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    return canvas.get_tk_widget()


def temporal_mean(data, window):
    new_window = tk.Toplevel(window)
    new_window.title("Media temporal")

    temporal = formulas.temporal(data, 13)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    x = np.arange(len(temporal))

    ax.plot(data, label="Valores")
    ax.plot(x, temporal, color='r', linestyle='--', label="Media temporal")
    ax.legend()

    ax.set_xticks(x)
    ax.set_xticklabels(temporal)

    fig.savefig('graph/temporal.PNG')

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()

    return canvas.get_tk_widget()
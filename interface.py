import pandas as pd
from tkinter import Label, Button, filedialog, messagebox, CENTER, END
import tkinter as tk
from tkinter import ttk
import graphics
import formulas
import csv

window = tk.Tk()

window.geometry("1280x720")

data_select = ""

label = Label(window, text="Selecciona un archivo CSV")

label.pack()

tb = ttk.Treeview(window)
pm = Label(window, text=" ")
pmu = Label(window, text=" ")
st = Label(window, text=" ")
stu = Label(window, text=" ")
stu.place(x=1000, y=570)
st.place(x=1000, y=500)
pmu.place(x=100, y=570)
pm.place(x=100, y=500)


def clean_table():
    pm.config(text="")
    pmu.config(text="")
    st.config(text="")
    stu.config(text="")
    rows = tb.get_children()
    for row in rows:
        tb.delete(row)


def export_csv():
    data = []
    for row in tb.get_children():
        valores = tb.item(row)['values']
        data.append(valores)

    file_csv = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('Archivos CSV', '*.csv')])

    if file_csv:
        with open(file_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def show_graphs(data, windowc):
    clean_table()
    frequency_distributions(data)
    if data.dtype != "object":
        formulas.print_all(data)
        show_tables(data)

    for widget in container.winfo_children():
        widget.destroy()
    graphics.bars(data, windowc).pack(side=tk.LEFT)
    graphics.cake(data, windowc).pack(side=tk.LEFT)
    if data.dtype != "object":
        graphics.histogram(data, windowc).pack(side=tk.LEFT)
        graphics.frequency_polygon(data, windowc).pack(side=tk.LEFT)
        graphics.warheads(data, windowc).pack(side=tk.LEFT)

    button_table.place(x=930, y=400)
    button_table.configure(background="#0092DA")
    button_tem = tk.Button(window, text="Mostrar temporal", command=lambda: show_temporal(data))
    button_tem.place(x=730, y=400)
    button_tem.configure(background="#0092DA")


def show_temporal(data):
    graphics.temporal_mean(data, window).pack(side=tk.LEFT)


def frequency_distributions(data):
    column_widths = [30, 100, 100, 50, 100, 100, 100, 140, 100]
    tb.place(x=160, y=150)
    columns = list(formulas.table(data).columns)
    tb["columns"] = columns
    tb.column("#0", width=0, stretch=tk.NO)
    for i, column in enumerate(columns):
        tb.column(column, anchor=tk.CENTER, width=column_widths[i])
        tb.heading(column, text=column)

    for index, row in formulas.table(data).iterrows():
        tb.insert("", tk.END, values=list(row))


def show_tables(data):
    list = formulas.sampling_conglomerates(data, 50)
    df = pd.DataFrame({'Columna': list})
    dataC = df['Columna']

    label1 = Label(window, text="Parametricos", justify='center')
    label1.place(x=300, y=400)

    label1 = Label(window, text="Agrupado", justify='center')
    label1.place(x=250, y=450)
    pm.configure(text=formulas.grouped_table(data))

    label2 = Label(window, text="No agrupado", justify='center')
    label2.place(x=250, y=550)
    pmu.configure(text=formulas.ungrouped_table(data))

    label3 = Label(window, text="Estadisticos", justify='center')
    label3.place(x=1200, y=400)

    label4 = Label(window, text="Agrupado", justify='center')
    label4.place(x=1200, y=450)
    st.configure(text=formulas.grouped_table(dataC))

    label5 = Label(window, text="No agrupado", justify='center')
    label5.place(x=1200, y=550)
    stu.configure(text=formulas.ungrouped_table(dataC))

    button_tem2 = tk.Button(window, text="Mostrar temporal", command=lambda: show_temporal(dataC))
    button_tem2.place(x=1300, y=400)
    button_tem2.configure(background="#0092DA")


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if filepath:
        dataset = pd.read_csv(filepath)
        attribute_options = tk.StringVar(window)
        attribute_options.set(dataset.columns[0])
        label = Label(window, text="Selecciona un atributo")
        label.pack(side=tk.TOP)
        select = tk.OptionMenu(window, attribute_options, *dataset.columns)
        select.pack(side=tk.TOP)
        select.configure(background="#0092DA")

        button_graph = Button(window, text="Graficar",
                              command=lambda: show_graphs(dataset[attribute_options.get()], container))
        button_graph.pack(side=tk.TOP)
        button_graph.configure(background="#0092DA")


button = Button(window, text="Buscar archivo", command=open_file)

button.pack()
button.configure(background="#00FA5F")

container = tk.Label(window)
container.place(x=110, y=650)
container.configure(background="white")

button_table = tk.Button(window, text="Exportar CSV", command=lambda: export_csv())

window.mainloop()

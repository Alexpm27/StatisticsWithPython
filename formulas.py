import math
import pandas as pd
import statistics as sc
from statistics import median, mode, variance, pvariance
import numpy as np
import random
import scipy.stats as stats


def range_in(data):
    min_value = min(data)
    max_value = max(data)
    return max_value - min_value


def number_classes(data):
    return round(1 + 3.3 * math.log10(len(data)))


def class_width(data):
    if data.dtype != "float64":
        result = round(range_in(data) / number_classes(data))
    else:
        result = range_in(data) / number_classes(data)
    return result


def lower_limits(data):
    min_value = min(data)
    class_width_value = class_width(data)
    num_classes = number_classes(data)
    values = [min_value + (i * class_width_value) for i in range(num_classes)]
    return values


def upper_limits(data):
    lower_limits_values = lower_limits(data)
    class_width_value = class_width(data)
    values = [limit + class_width_value for limit in lower_limits_values]
    return values


def class_mark(data):
    values = []
    for i in range(number_classes(data)):
        value = (lower_limits(data)[i] + upper_limits(data)[i]) / 2
        values.append(value)
    return values


def absolute_frequency(data):
    lower = lower_limits(data)
    upper = upper_limits(data)

    labels = [f'[{lower[i]}, {upper[i]}]' if i == 0 else f'({lower[i]}, {upper[i]}]' for i in range(len(lower))]
    af = pd.cut(data, bins=[float('-inf')] + upper, labels=labels, right=False).value_counts().sort_index()

    last_label = af.index[-1]
    af.rename(index={last_label: last_label[:-1] + ']'}, inplace=True)

    return af


def relative_frequency(data):
    return absolute_frequency(data) / len(data)


def cumulative_frequency(frequency, data):
    values = []
    for i in range(number_classes(data)):
        if i == 0:
            values.append(frequency[i])
        else:
            values.append(frequency[i] + values[i - 1])
    return values


def class_mark_for_freq_abs(mc, fq_abs):
    return [value * fq_abs[i] for i, value in enumerate(mc)]


def median_arithmetic(data):
    return sum(class_mark_for_freq_abs(class_mark(data), absolute_frequency(data).values.tolist())) / len(data)


def mode_g(data):
    fc = absolute_frequency(data)
    index = fc.argmax()
    return class_mark(data)[index]


def median_g(data):
    return median(class_mark(data))


def biasung(data):
    bias_result = stats.skew(data)

    if bias_result > 0:
        bine_all = "Sesgo a la derecha"
    elif bias_result == 0:
        bine_all = "Al centro"
    else:
        bine_all = "Sesgo a la izquierda"

    return bine_all


def bias(average, median, mode):
    result = ""
    if average < median < mode:
        result = "Sesgado a la izquierda"
    elif average == median == mode:
        result = "Simetrico"
    elif mode < median < average:
        result = "Sesgado a la derecha"
    else:
        result = "Inderteminada"

    return result


def p_variance(data, mean):
    return pvariance(data, mean)


def grouped_variance(data, mean):
    clas_marks = class_mark(data)
    freq_absolute = absolute_frequency(data)
    i = 0
    abs_marks = []
    cmq = []
    total = 0
    for freq in freq_absolute.values:
        cmqp = clas_marks[i] ** 2
        cmq.append(cmqp)
        fm = freq * cmq[i]
        abs_marks.append(fm)
        total = total + abs_marks[i]
        i = i + 1
    meanq = mean ** 2

    am = total - (len(data) * meanq) / len(data) - 1
    return am


def standard_deviation(variance):
    return math.sqrt(variance)


def geometry(data):
    try:
        return sc.geometric_mean(data)
    except:
        print("An exception occurred")


def trim(data, percentage):
    sorted_values = sorted(data)

    percentage = percentage / 100
    n = int(percentage * len(sorted_values))

    trim_values = sorted_values[n:-n]

    trim_median = sum(trim_values) / len(trim_values)

    return trim_median


def sampling_conglomerates(data, size):
    n = len(data) // size
    conglomerates = []

    for i in range(n):
        start = i * size
        end = start + size

        cluster = data[start:end]

        conglomerates.append(cluster)

    return random.choice(conglomerates)


def temporal(data, window_size):
    weights = np.ones(window_size) / window_size
    media_temporal = np.convolve(data, weights, mode='valid')
    return media_temporal


def table(data):

    if data.dtype != "object":
        frequency_table = pd.DataFrame({
            'Clase': [i for i in range(number_classes(data))],
            'L. inf.': lower_limits(data),
            'L. sup.': upper_limits(data),
            'M. C.': class_mark(data),
            'Frec. abs.': absolute_frequency(data).values.tolist(),
            'Frec. abs. acum.': cumulative_frequency(absolute_frequency(data).values.tolist(), data),
            'Frec. rel.': relative_frequency(data).values.tolist(),
            'Frec. rel. acum.': cumulative_frequency(relative_frequency(data).values.tolist(), data),

        })
    else:
        frequency_table = pd.DataFrame({
            'Clase': data.value_counts().index,
            'Frec. abs.': data.value_counts(),
        })

    return frequency_table


def grouped_table(data):
    parametric = pd.DataFrame({
        'Media': [median_arithmetic(data)],
        'Mediana.': [median_g(data)],
        'Moda': [mode_g(data)],
        'varianza': [p_variance(data, median_arithmetic(data))],
        'Desviacion E.': [standard_deviation(p_variance(data, median_arithmetic(data)))],
        'Geometrica': [geometry(data)],
        'Truncada': [trim(data, 20)],
        'Sesgo': [biasung(data)],
        'Rango': [range_in(data)]
    })
    parametric_str = parametric.to_string(index=False, justify='center', col_space=20)

    return parametric_str


def ungrouped_table(data):
    parametric = pd.DataFrame({
        'Media': [sc.mean(data)],
        'Mediana.': [sc.median(data)],
        'Moda': [sc.mode(data)],
        'varianza': [p_variance(data, sc.mean(data))],
        'Desviacion E.': [standard_deviation(p_variance(data, sc.mean(data)))],
        'Geometrica': [geometry(data)],
        'Truncada': [trim(data, 20)],
        'Sesgo': [biasung(data)],
        'Rango': [range_in(data)]
    })
    parametric_str = parametric.to_string(index=False, justify='center', col_space=20)
    return parametric_str


def print_something(data):
    print("Media a")
    print(median_arithmetic(data))
    print("Media n")
    print(data.mean())
    print("moda a")
    print(mode_g(data))
    print("moda n")
    print(data.mode())
    print("mediana a")
    print(median_g(data))
    print("mediana n")
    print(data.median())
    print(bias(median_arithmetic(data), median_g(data), mode_g(data)))
    print(range_in(data))
    print("varianza")
    print(p_variance(data, median_arithmetic(data)))
    print(p_variance(data, median_arithmetic(data)))
    print("desv")
    print(standard_deviation(p_variance(data, median_arithmetic(data))))
    #print("vonglomerados")
    #print(get_conglomerates(data, 100))
    print("truncada")
    print(trim(data, 10))
    print(geometry(data))
    print(grouped_table(data))
    print(ungrouped_table(data))
    print(grouped_table(sampling_conglomerates(data, 100)))
    print(ungrouped_table(sampling_conglomerates(data, 100)))


def print_all(data):
    print("range")
    print(range_in(data))
    print("N clases")
    print(number_classes(data))
    print("ancho")
    print(class_width(data))
    print("limites")
    print(lower_limits(data))
    print(upper_limits(data))
    print("marca class")
    print(class_mark(data))
    print("fa")
    print(absolute_frequency(data))
    print("faa")
    print(cumulative_frequency(absolute_frequency(data).values.tolist(), data))
    print("fr")
    print(relative_frequency(data))
    print("fra")
    print(cumulative_frequency(relative_frequency(data).values.tolist(), data))
    print("-------------------------------------------------------------------------------")
    print(table(data))

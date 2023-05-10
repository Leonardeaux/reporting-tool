import csv
from math import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

FILENAME = './data/usagers-2021.csv'
ENCODING = 'utf-8'
SEPARATOR = ';'

DATA_TYPE_CATEGORICAL = "CAT"
DATA_TYPE_TEXT = "TXT"
DATA_TYPE_NUMERICAL = "NUM"
DATA_TYPE_INDEX = "INDEX"
MAX_CATEGORICAL_VALUES = 32

DISPLAY_VALUES = 5
MAX_PIE_BINS = 10

MISSING_VALUES = {'atm': ['-1'], 'col': ['-1'],
                  'circ': ['-1'], 'vosp': ['-1'],
                  'secu1': ['-1'], 'secu2': ['-1'],
                  'senc': ['-1'], 'secu3': ['-1'],
                  'obs': ['-1'], 'obsm': ['-1'],
                  'choc': ['-1'], 'manv': ['-1'],
                  'prof': ['-1'], 'plan': ['-1'],
                  'motor': ['-1'], 'sexe': ['-1']}


class UnivariateStats:
    def __init__(self, dataset, headers, column):
        self.__data = []
        self.__header = headers[column]
        for line in dataset:
            self.__data.append(line[column])
        self.__sparsity = 0
        self.__filter()
        self.__convert()
        self.__build_histogram()

    def __build_histogram(self):
        self.__histogram = {}
        for d in self.__data:
            if d in self.__histogram:
                self.__histogram[d] += 1
            else:
                self.__histogram[d] = 1

    def __filter(self):
        size = len(self.__data)
        self.__data = list(filter(lambda x: x.strip(), self.__data))

        if self.__header in MISSING_VALUES:
            missing_values = MISSING_VALUES[self.__header]
            self.__data = list(filter(lambda x: x.strip() not in missing_values, self.__data))
        self.__sparsity = 1.0 - len(self.__data) / float(size)

    def __try_convert(self, f):
        tmp = []
        for value in self.__data:
            try:
                tmp.append(f(value))
            except:
                return None
        return tmp

    def __convert(self):
        tmp = []
        done = True

        if self.values_count == len(self.__data):
            self.__type = DATA_TYPE_INDEX
        else:
            self.__type = DATA_TYPE_TEXT

            if self.values_count <= MAX_CATEGORICAL_VALUES:
                self.__type = DATA_TYPE_CATEGORICAL

            tmp = self.__try_convert(int)
            if tmp:
                self.__type = DATA_TYPE_CATEGORICAL
                self.__data = tmp

                if self.values_count > MAX_CATEGORICAL_VALUES:
                    self.__type = DATA_TYPE_NUMERICAL
            else:
                tmp = self.__try_convert(lambda v: float(v.strip().replace(',', '.')))
                if tmp:
                    self.__type = DATA_TYPE_NUMERICAL
                    self.__data = tmp

    def __repr__(self):
        res = f'{self.__header} [{self.__type}]'
        if self.__sparsity > 0:
            res += f'\n\tsparsity: {100 * self.__sparsity:.2f}%'
        if self.__type in [DATA_TYPE_CATEGORICAL]:
            res += f'\n\tdistinct values : {self.values_count}'
        elif self.__type in [DATA_TYPE_NUMERICAL]:
            median, mean = np.median(self.__data), np.mean(self.__data)
            skew, kurtosis = stats.skew(self.__data), stats.kurtosis(self.__data)
            res += f'\n\tkurtosis : {kurtosis}, skew : {skew}'

        if self.values_count <= MAX_CATEGORICAL_VALUES:
            res += '\n\t' + ' '.join(map(str, self.__histogram.keys()))

        return res

    @property
    def values_count(self):
        values = set()
        for value in self.__data:
            values.add(value)
        return len(values)

    def draw_pie(self, axes):
        values = self.__histogram.values()
        if self.__type in [DATA_TYPE_CATEGORICAL] and \
                len(values) > 1 and len(values) <= MAX_PIE_BINS:
            labels = self.__histogram.keys()
            axes.pie(values, labels=labels, autopct='%4.2f%%')
            return True
        return False

    def draw_histogram(self, axes):
        values = self.__histogram.values()
        if len(values) < 1000 and len(values) > 1:
            labels = self.__histogram.keys()
            axes.hist(self.__data, density=True, bins=range(len(self.__histogram) + 1),
                      rwidth=0.8)


def read_data(filename):
    data = []
    with open(filename, newline='', encoding=ENCODING) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=SEPARATOR)
        headers = reader.fieldnames

        for row in reader:
            data.append([])
            for header in row:
                data[-1].append(row[header].strip())

    return data, headers


if __name__ == "__main__":
    data, headers = read_data(FILENAME)
    print(headers)
    print(len(data))

    columns = {}

    for i in range(len(headers)):
        columns[headers[i]] = UnivariateStats(data, headers, i)

    axSize = ceil(sqrt(len(headers)))
    fig, axes = plt.subplots(axSize, axSize)

    i, j = 0, 0
    for header in columns:
        print(columns[header])
        axes[i, j].set_title(header)
        if not columns[header].draw_pie(axes[i, j]):
            columns[header].draw_histogram(axes[i, j])

        i += 1
        if i >= axSize:
            i = 0
            j += 1

    plt.show()

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


class UnivariateStats:
    def __init__(self, dataframe: pd.DataFrame, max_categorical_values: int, max_pie_bins: int = 10):
        self.dataframe = dataframe
        self.max_categorical_values = max_categorical_values
        self.max_pie_bins = max_pie_bins

        self.infos = {}
        self.datatype = {}

        self.set_datatype()

        self.set_numeric_infos()
        self.set_categorical_infos()

        self.draw_graphics()

    def set_datatype(self):
        for col in self.dataframe:
            self.infos[col] = None
            if df[col].dtype == "int64" or df[col].dtype == "float64":
                if df[col].max() > self.max_categorical_values:
                    self.datatype[col] = 'NUM'
                else:
                    self.datatype[col] = 'CAT'
            elif df[col].dtype == "object":
                self.datatype[col] = 'TXT'

    def set_numeric_infos(self):
        for col in self.dataframe:
            if self.datatype[col] == 'NUM':
                self.infos[col] = self.dataframe[col].skew(), \
                    self.dataframe[col].kurtosis(), \
                    (self.dataframe[col].isna().sum() / len(self.dataframe[col])) * 100

    def set_categorical_infos(self):
        for col in self.dataframe:
            if self.datatype[col] == 'CAT':
                self.infos[col] = self.dataframe[col].unique(), \
                    (self.dataframe[col].isna().sum() / len(self.dataframe[col])) * 100

    def draw_graphics(self):
        for col in self.dataframe:
            if self.datatype[col] == 'CAT' and 1 < self.dataframe[col].count() < self.max_pie_bins:
                self.draw_pie(col)
            elif self.datatype[col] == 'NUM' and (1 < self.dataframe[col].count() < 1000):
                print(col)
                self.draw_histogram(col)

    def draw_pie(self, col):
        unique_values = len(self.dataframe[col].dropna().unique())
        if self.max_pie_bins > unique_values > 1:
            colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, self.dataframe[col].dropna().count()))

            fig, ax = plt.subplots()
            ax.pie(self.dataframe[col].dropna(), colors=colors, radius=3, center=(4, 4),
                   wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

            #
            # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            #        ylim=(0, 8), yticks=np.arange(1, 8))

            return True
        else:
            return False

    def draw_histogram(self, col):
        print(col)
        unique_values = df[col].dropna().unique()
        n_df = df[col].dropna().astype(dtype='int64')
        fig, ax = plt.subplots()
        ax.hist(n_df, bins=int(unique_values.max()) + 1)


    def __str__(self):
        pass


def draw_test(df, col):
    unique_values = len(df[col].dropna().unique())
    print(unique_values)
    n_df = df[col].dropna()
    if 10 > unique_values > 1:
        colors = ['#4CAF50', '#2196F3']
        colors2 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, unique_values))
        print(colors)
        plt.pie(n_df, colors=colors, autopct='%1.1f%%')
        plt.show()
        # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        #        ylim=(0, 8), yticks=np.arange(1, 8))

        return True
    else:
        return False


if __name__ == "__main__":
    FILENAME = './data/usagers-2021.csv'
    ENCODING = 'utf-8'
    SEPARATOR = ';'

    df = pd.read_csv(FILENAME, sep=SEPARATOR, encoding=ENCODING)

    MISSING_VALUES_COLS = ['atm', 'col',
                           'circ', 'vosp',
                           'secu1', 'secu2',
                           'senc', 'secu3',
                           'obs', 'obsm',
                           'choc', 'manv',
                           'prof', 'plan',
                           'motor', 'sexe',
                           'place', 'grav',
                           'trajet', 'locp',
                           'actp', 'etatp']

    for col in df:
        if col in MISSING_VALUES_COLS:
            df[col].replace(-1, np.nan, inplace=True)

    df['actp'].replace('A', 10, inplace=True)
    df['actp'].replace('B', 11, inplace=True)
    df['actp'] = pd.to_numeric(df['actp'])

    data_infos = UnivariateStats(df, 32)

    print(data_infos.infos)
    # draw_test2(df, 'secu3')
    plt.show()
    # print(data_infos.dataframe['secu3'].isna().sum())  # 127797
    # print(data_infos.dataframe['secu3'].isna().sum() / len(data_infos.dataframe['secu3']))
    # print(data_infos.dataframe['secu3'].count())
    # print(len(data_infos.dataframe['secu3']))

    # print(data_infos.dataframe['secu3'].dropna())

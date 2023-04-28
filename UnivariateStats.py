import pandas as pd
import numpy as np
import scipy.stats as stats


class UnivariateStats:
    def __init__(self, dataframe: pd.DataFrame, max_categorical_values: int):
        self.dataframe = dataframe
        self.max_categorical_values = max_categorical_values

        self.infos = {}
        self.datatype = {}

        self.set_datatype()

        self.set_numeric_infos()
        self.set_categorical_infos()

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
        pass

    def __str__(self):
        pass


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
    print(data_infos.dataframe['secu3'].isna().sum()) # 127797
    print(data_infos.dataframe['secu3'].isna().sum() / len(data_infos.dataframe['secu3']))
    print(data_infos.dataframe['secu3'].count())
    print(len(data_infos.dataframe['secu3']))

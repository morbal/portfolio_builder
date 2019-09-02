import os
import pandas as pd
import pandas_datareader as wb
from datetime import timedelta, datetime as dt
from utillies import support


dir_path_str = os.path.dirname(os.path.dirname(__file__))

class DataRequest:

    def __init__(self, symbol_origin='csv'):

        if symbol_origin is 'csv':
            self.input_dir = os.path.join(dir_path_str, r'data/input_symbols.csv')
            self.symbols = pd.read_csv(self.input_dir)['symbols'].tolist()
        elif symbol_origin is 'user':
            self.symbols = []

        self.data_df: pd.DataFrame = pd.DataFrame

    def symbols_input(self, symbol):
        self.symbols.append(symbol)

    def pull_yahoo_data(self, start=(dt.today() - timedelta(days=180)).strftime('%Y-%m-%d'), stop=None):

        assert type(self.symbols) is list, 'Symbols must be of type list! ' + str(type(self.symbols)) + ' was passed.'
        if stop is None:
            stop = dt.today().strftime('%Y-%m-%d')
        else:
            stop = stop
        if len(self.symbols) > 25:
            mod_symbols_list = support.breakdown_list(og_list=self.symbols, sublist_len=24)
            self.data_df = wb.DataReader(mod_symbols_list[0], data_source='yahoo', start=start, end=stop)['Adj Close']
            for i in range(len(mod_symbols_list) - 1):
                try:
                    self.data_df = pd.concat([self.data_df,
                                         wb.DataReader(list(mod_symbols_list[i + 1]), data_source='yahoo',
                                                       start=start,
                                                       end=stop)['Adj Close']], axis=1)
                except KeyError:
                    continue
            self.data_df = pd.concat(
                [self.data_df,
                 wb.DataReader(mod_symbols_list[-1], data_source='yahoo', start=start, end=stop)['Adj Close']],
                axis=1)
            self.data_df = self.data_df.loc[:, ~self.data_df.columns.duplicated()]
        elif 1 < len(self.symbols) <= 24:
            self.data_df = wb.DataReader(self.symbols, data_source='yahoo', start=start, end=stop)['Adj Close']
            self.data_df = self.data_df.loc[:, ~self.data_df.columns.duplicated()]
        elif len(self.symbols) == 1:
            self.data_df = wb.DataReader(self.symbols, data_source='yahoo', start=start, end=stop)['Adj Close']

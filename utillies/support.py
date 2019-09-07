import numpy as np
import pandas as pd
import pandas_datareader as wb

def breakdown_list(og_list, sublist_len):
    mod_list = [og_list[0:sublist_len]]
    for i in range(int(np.ceil(len(og_list) / sublist_len)) - 1):
        mod_list.append(og_list[sublist_len * (i + 1) + 0:sublist_len * (i + 2)])
    return mod_list

def get_log_returns(time_series: list):
    """
    :param time_series: list of time series
    :return: series or data frame of log returns
    """
    if len(time_series) == 1:
        return (time_series[0] - time_series[0].shift(1)) / time_series[0].shift(1)
    elif len(time_series) > 1:
        price_df: pd.DataFrame = pd.DataFrame(time_series).T
        output_df: pd.DataFrame = (price_df - price_df.shift(1)) / price_df.shift(1)
        return output_df.dropna(how='any')


class PortfolioTools():
    def __init__(self):
        self.status: bool = True

    def align_time_series(self, series_list):
        assert type(series_list) is list, 'TypeError: series_list must be list of at least two pd.Series'
        ally_df = series_list[0]

        for s in range(len(series_list)-1):
            ally_df = pd.concat([ally_df, series_list[s+1]], ignore_index=False, axis=1)
        return ally_df.dropna()

    def create_var_cov_matrix(self, series_list):
        assert type(series_list) is list, 'TypeError: price_series must be list of at least two pd.Series'
        log_ret_df: pd.DataFrame = get_log_returns(series_list)
        R = log_ret_df
        var_df: pd.DataFrame = R.var()
        R_var_cov_df: np.cov = np.cov(R.T)

        for i in range(len(R_var_cov_df[0])):
            R_var_cov_df[i][i] = var_df.iloc[i]
        return R_var_cov_df

    def optimize_portfolio(self, turns: int, series_list: list):
        num_assets = len(series_list)
        var_cov_mat = self.create_var_cov_matrix(series_list)
        var_list = list()
        for i in range(turns):
            # Todo make sure W sums up to 1
            W: np.ndarray = np.random.rand(num_assets, 1)
            W_total = sum(W)
            W = W / W_total
            port_var: float = W.T.dot(var_cov_mat).dot(W)[0][0]
            var_list.append((W, port_var))
        min_var: float = min(var_list, key=lambda t: t[1])

        return min_var


'''
tsla = wb.DataReader('TSLA', data_source='yahoo')['Adj Close']
ford = wb.DataReader('F', data_source='yahoo')['Adj Close']
appl = wb.DataReader('AAPL', data_source='yahoo')['Adj Close']
'''

class OptionTools:

    def __init__(self):
        self.type: str = 'call'
        self.price: float = 0
        self.strike: float = 0
        self.position: int = 0
        self.ratio: float = 0
        self.underlying: float = 0
        self.volatility: float = 0
        self.profit: float = 0
        self.parameter_dict: dict = dict()
        self.__call_list__: list = ['Call', 'call', 'c']
        self.__put_list__: list = ['Put', 'put', 'p']

    def calc_profit(self, option_type: str = 'call', price: float = 0, strike: float = 0, position: int = 0,
                    ratio: float = 100, underlying: float = 0):

        self.type = option_type
        self.price = price
        self.strike = strike
        self.position = position
        self.ratio = ratio
        self.underlying = underlying

        if self.type in self.__call_list__ and self.position >= 0:
            self.profit = (max((self.underlying - self.strike), 0) - self.price) * self.position * self.ratio
            return self.profit
        elif self.type in self.__put_list__ and self.position >= 0:
            self.profit = (max((self.strike - self.underlying), 0) - self.price) * self.position * self.ratio
            return self.profit
        elif self.type in self.__call_list__ and self.position < 0:
            self.profit = (self.price - max((self.underlying - self.strike), 0)) * self.position * self.ratio
            return self.profit
        elif self.type in self.__put_list__ and self.position < 0:
            self.profit = (self.price - max((self.strike - self.underlying), 0)) * self.position * self.ratio
            return self.profit
        else:
            return print('Option type is not given correctly.')

    def show_parameters(self):
        self.parameter_dict = {
            'option_type': self.type,
            'price': self.price,
            'strike': self.strike,
            'position': self.position,
            'ratio': self.ratio,
            'volatility': self.volatility,
            'underlying': self.underlying
        }
        print(self.parameter_dict)

    def calc_iv(self):
        return NotImplementedError

    def calc_greeks(self):
        return NotImplementedError


controller_dict: dict = {
    'call_list': ['Call', 'call', 'c'], 'put_list': ['Put', 'put', 'p']
}
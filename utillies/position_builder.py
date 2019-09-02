import numpy as np
from typing import List
import pandas as pd
from utillies.support import OptionTools as ot
# from matplotlib import pyplot as plt

class OptionPosition:

    def __init__(self, opt_type: str = 'call', price: float = 0, strike: float = 0,
                 position: int = 0, volatility: float = 0, maturity: float = 0, pos_id: int = 0, ratio: int = 100):
        self.opt_type: str = opt_type
        self.price: float = price
        self.strike: float = strike
        self.position: int = position
        self.volatility: float = volatility
        self.iv: float = 0
        self.maturity: float = maturity
        self.ratio: int = ratio
        self.pos_id: int = pos_id


class OptionPortfolio:

    def __init__(self):
        self.ot = ot()
        self.portfolio_list: list = []
        self.underlying_price: float = 0
        self.position_count: int = 0
        self.portfolio_df: pd.DataFrame = pd.DataFrame(columns=['type', 'price', 'strike', 'position', 'volatility',
                                                                'maturity', 'profit'])
        self.underlying_dict: dict = {
            'spot': self.underlying_price
        }

    def add_position(self, option_type: str = 'call', price: float = 0, strike: float = 0, position: int = 0,
                     ratio: int = 100):
        ox: OptionPosition = OptionPosition(opt_type=option_type, price=price, strike=strike, position=position,
                                            ratio=ratio, pos_id=self.position_count)
        # Todo calc_iv richtig implementieren
        # ox.iv = ot().calc_iv()
        aux_df: pd.DataFrame = pd.DataFrame(index=[ox.pos_id],
                                            data={'type': ox.opt_type, 'price': ox.price, 'strike': ox.strike,
                                                  'position': ox.position, 'volatility': ox.volatility, 'maturity':
                                                  ox.maturity, 'iv': ox.iv, 'ratio': ox.ratio})
        self.position_count += 1
        self.portfolio_df = pd.concat([self.portfolio_df, aux_df], sort=True)
        self.portfolio_list.append(ox)
        self.add_pnl()

    def drop_position(self, ids_to_drop: List[int] = None):
        self.portfolio_df.drop(ids_to_drop, inplace=True)
        self.portfolio_df.reset_index(inplace=True, drop=True)
        self.position_count = self.portfolio_df.index.to_list()[-1] + 1
        return print('Dropped position(s) with id(s): ' + str(ids_to_drop))

    def change_position(self, id_to_change: int = 0, parameter_to_change: str = 0,
                        new_value: str or int or float = None):
        i = id_to_change
        p = parameter_to_change
        self.portfolio_df.loc[self.portfolio_df.index[i], p] = new_value

    def add_pnl(self):
        for i in range(len(self.portfolio_df)):
            port: pd.DataFrame = self.portfolio_df.iloc[i]
            profit = self.ot.calc_profit(option_type=port['type'], price=port['price'], position=port['position'],
                                      ratio=port['ratio'], underlying=self.underlying_price)
            self.portfolio_df.loc[port.name, 'profit'] = profit

    def set_underlying(self, parameter_to_change: str = 'underlying_price', new_value: str or int or float = None):
        self.underlying_dict[parameter_to_change] = new_value



    # def simulate_positions(self, incr: float = 1):
    #
    #
    #
    #
    # def plot_position(self, id_to_plot: list = None, plot_aggregate: bool = False):
    #
    #     for pos in pos_to_plot:
    #         plt.plot(pos)

op = OptionPortfolio()
op.add_position()
op.add_position()
op.add_position()
hase = op.portfolio_df

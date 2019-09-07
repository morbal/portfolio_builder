import numpy as np


def discount_cf(cf: float or np.array(float) = None, fv: float = None, t: float = None, cont: bool = False):
    NotImplementedError


# def calc_forward(rate: float, spot: float, strike: float, t: float, freq: float = 1, cont: bool = True, div: float = 0):
#     if cont and div == 0:
#         assert freq == 1, print('Continous compounding must not have a frequency given.')
#         value = (spot - strike) * np.exp(-rate * t)
#         price =
#     elif not cont and div == 0:
#         assert freq == 1, print('Continous compounding must not have a frequency given.')
#         value = (spot - strike) * (1 - rate/freq) ** t
#         price =
#     elif cont and div != 0:
#         value = spot * np.exp(-div * (t * freq)) - strike * np.exp(-rate * (t * freq))
#         price =
#     elif not cont and div != 0:
#         value = spot - strike
#         price =
#     return value


def calc_irr(cashflows: np.array, initial_investment: float, t: int = 1, guess: float = 0.1, incr: float = 0.000001,
             prec: float = 0.001):
    cf_tpl: list = [list(i) for i in zip(cashflows, range(1, t+1))]
    irr: float = guess
    value: float = 0
    outcome_list: list = list()

    for cf, t in cf_tpl:
        value += cf / ((1 + irr) ** t)
    value -= initial_investment
    outcome_list.append((irr, value))

    while value > prec:
        value = 0
        irr += incr
        for cf, t in cf_tpl:
            value += cf / ((1 + irr) ** t)
        value -= initial_investment
        outcome_list.append((irr, value))

    while value < -prec:
        value = 0
        irr -= incr
        for cf, t in cf_tpl:
            value += cf / ((1 + irr) ** t)
        value -= initial_investment
        outcome_list.append((irr, value))

    return outcome_list

#Todo build converter
# def interest_converter(rate: float, t: float, convert_to: str = None, conver_from: str = None):



def calc_fwd_rate(rate_1: float, rate_2: float, t_1: int, t_2: int):
    fwd_rate = ((1 + rate_2) ** t_2 / (1 + rate_1) ** t_1) - 1
    return fwd_rate


def calc_zcb(rate: float, spot: float, t: float, freq: float = 1):
    # Todo not done yet
    price = 100 / (1 + (rate/freq)) ** (t * freq)
    return price



from QuantLib import *
from utillies import support as s


class OptionPricing:

    def __init__(self, option_type: str, spot: float, strike: float, volatility: float, start_date: tuple,
                 maturity_date: tuple, earliest_exercise: tuple = None, dividend: float = 0.03,
                 option_style: str = 'eu', rf: float = 0.01):

        self.t0 = start_date
        self.start: Date = Date(self.t0[0], self.t0[1], self.t0[2])
        self.t1 = maturity_date
        self.maturity: Date = Date(self.t1[0], self.t1[1], self.t1[2])
        self.spot_price: float = spot
        self.strike: float = strike
        self.volatility: float = volatility
        self.dividend_rate: float = dividend
        self.option_style: str = option_style

        if option_type in s.controller_dict['call_list']:
            self.option_type: int = Option.Call
        elif option_type in s.controller_dict['put_list']:
            self.option_type: int = Option.Put

        self.rf_rate: float = rf
        self.day_count: Actual365Fixed = Actual365Fixed()
        self.calendar: Germany = Germany()

        Settings.instance().evaluationDate = self.start

        self.payoff: PlainVanillaPayoff = PlainVanillaPayoff(self.option_type, self.strike)

        if self.option_style == 'eu':
            self.exercise: EuropeanExercise = EuropeanExercise(self.maturity)
            self.option: VanillaOption = VanillaOption(self.payoff, self.exercise)
        elif self.option_style == 'us':
            self.tx = earliest_exercise
            self.early_exercise: Date = Date(self.tx[0], self.tx[1], self.tx[2])
            self.exercise: AmericanExercise = AmericanExercise(self.early_exercise, self.maturity)
            self.option: VanillaOption = VanillaOption(self.payoff, self.exercise)
        else:
            print('Unknown option style: Use "eu" or "us" as parameter.')

    def get_bsm_dict(self):

        spot_handle: QuoteHandle = QuoteHandle(SimpleQuote(self.spot_price))
        flat_ts: YieldTermStructureHandle = YieldTermStructureHandle(FlatForward(self.start, self.rf_rate,
                                                                                 self.day_count))
        dividend_yield: YieldTermStructureHandle = \
            YieldTermStructureHandle(FlatForward(self.start, self.dividend_rate, self.day_count))
        flat_vol_ts: BlackVolTermStructureHandle = \
            BlackVolTermStructureHandle(BlackConstantVol(self.start, self.calendar, self.volatility, self.day_count))
        bsm_process: BlackScholesMertonProcess = BlackScholesMertonProcess(spot_handle,
                                                                           dividend_yield,
                                                                           flat_ts,
                                                                           flat_vol_ts)
        if self.option_style == 'eu':
            self.option.setPricingEngine(AnalyticEuropeanEngine(bsm_process))
        elif self.option_style == 'us':
            self.option.setPricingEngine(AnalyticDigitalAmericanEngine(bsm_process))

        bsm_dict: dict = {
            'value': self.option.NPV(),
            'greeks': {
                'delta': self.option.delta(),
                'gamma': self.option.gamma(),
                'theta': self.option.theta(),
                'rho': self.option.rho(),
                'dividend_rho': self.option.dividendRho(),
                'vega': self.option.vega(),
            },
            'elasticity': self.option.elasticity()
        }
        return bsm_dict

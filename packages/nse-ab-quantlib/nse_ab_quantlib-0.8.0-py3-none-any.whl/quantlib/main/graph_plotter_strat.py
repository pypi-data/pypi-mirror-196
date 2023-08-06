#!/usr/bin/env python3

import logging
import argparse
from datetime import datetime

from alphatools.backtesting_app import BackTestingApp
from alphatools.utils.token_manager import TokenManager

from quantlib import instruments

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s {%(pathname)s:%(lineno)d} : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
class GraphPlotterStrat(BackTestingApp):
    def __init__(self, creds):
        # formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)-8s : %(message)s',
        #                               datefmt='%Y-%m-%d %H:%M:%S')
        # handler = logging.StreamHandler(sys.stdout)
        # handler.setFormatter(formatter)
        # self.logger.addHandler(handler)
        # self.logger.setLevel(logging.INFO)
        super().__init__(creds)

    def load_instruments(self, symbol, start_date, end_date):
        self.set_start_date(start_date)
        self.set_end_date(end_date)

        token_manager = TokenManager()
        self.logger.info("Hello world")
        exp_date = instruments.get_kth_expiry(symbol[0], 1, instruments.ExpiryType.MONTHLY)
        token_info = token_manager.get_fut(symbol[0], exp_date)
        token = token_info['token']
        exch_seg = token_info['exch_seg']
        self.add_instrument(token, exch_seg)

        self.load_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--underlying", nargs='+',
                        help="Instrument whose derivatives have to be recorded", required=True)
    parser.add_argument("-s", "--start_date",
                        help="Instrument whose derivatives have to be recorded", required=False,
                        default=datetime.now().strftime('%Y%m%d'))
    parser.add_argument("-e", "--end_date",
                        help="Instrument whose derivatives have to be recorded", required=False,
                        default=datetime.now().strftime('%Y%m%d'))
    args = parser.parse_args()
    start_date = datetime.strptime(args.start_date, '%Y%m%d')
    end_date = datetime.strptime(args.end_date, '%Y%m%d')
    strat = GraphPlotterStrat('/Users/jaskiratsingh/projects/smart-api-creds.ini')
    strat.load_instruments(args.underlying, start_date, end_date)

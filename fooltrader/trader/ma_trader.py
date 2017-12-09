from fooltrader.api import quote
from fooltrader.computing import technical
from fooltrader.trader.trader import Trader


class MaTrader(Trader):
    def __init__(self):
        super().__init__()
        self.universe = '000001'

    def on_time_elapsed(self):
        super().on_time_elapsed()
        current_kdata = quote.get_kdata(security_item=self.universe, the_date=self.event_time)
        if len(current_kdata) > 0:
            the_close = current_kdata['close']
            print(the_close)
            the_ma = technical.ma(self.universe, start=self.event_time, end=self.event_time)['close_ma5'][0]
            print(the_ma)
            if the_close > the_ma and not self.account.get_position(self.universe):
                self.order(security_id=self.universe, amount=100, current_price=the_close)
            else:
                self.order(security_id=self.universe, amount=-100, current_price=the_close)


if __name__ == '__main__':
    from elasticsearch_dsl.connections import connections

    connections.create_connection(hosts=['localhost'], timeout=20)

    MaTrader().run()
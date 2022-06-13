import threading
#####
#subpackage
import subpackage.loggers as loggers
from Business_Logic.super_trend_cal import super_trend_calculate_15m
from Business_Logic.ttmsquze_cal import ttmsqueze_calculate_15m
from Business_Logic.rsi_cal import rsi_15m

if __name__ == '__main__':
    t = threading.Thread(name='super_trend_calculate_15m', target=super_trend_calculate_15m).start()
    t = threading.Thread(name='ttmsqueze_calculate_15m', target=ttmsqueze_calculate_15m).start()
    t = threading.Thread(name='rsi_15m', target=rsi_15m).start()



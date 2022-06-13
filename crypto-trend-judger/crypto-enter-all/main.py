import threading
#####
#subpackage
import subpackage.loggers as loggers
from Business_Logic.strategy_enter import enter_15m

if __name__ == '__main__':
    t = threading.Thread(target=enter_15m,args=('BTCUSDT','15m',15,1,)).start()
    t2 = threading.Thread(target=enter_15m,args=('LTCUSDT','15m',15,1,)).start()
    t4 = threading.Thread(target=enter_15m,args=('TRXUSDT','15m',15,4,)).start()
    

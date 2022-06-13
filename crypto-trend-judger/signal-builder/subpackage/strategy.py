import pandas as pd
import numpy as np
from talib import abstract



def supertrend(df, atr_period=34, multiplier=0.75):
    """
    用atr來做停利停損
    """
    
    high = df['high']
    low = df['low']
    close = df['close']
    
    # calculate ATR
    price_diffs = [high - low, 
                   high - close.shift(), 
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean() 
    # df['atr'] = df['tr'].rolling(atr_period).mean()
    
    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2
    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)
    
    # initialize Supertrend column to True
    supertrend = [True] * len(df)
    
    for i in range(1, len(df.index)):
        curr, prev = i, i-1
        
        # if current close price crosses above upperband
        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]
            
            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan
    # 計算dema25,dema169
    dema25 = abstract.DEMA(df,25).rename('dema25')
    dema40 = abstract.DEMA(df,40).rename('dema40')
    
    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final_Lowerband': final_lowerband,
        'Final_Upperband': final_upperband,
        'dema25': dema25,
        'dema40':dema40,
        'close': close,
        'atr':atr
    }, index=df.index)


def ttmsqueze(df,length,mult,length_KC,mult_KC):
    """
    15分K用:20,2,20,2
    5分K用:20,3,15,3
    """
    

    # parameter setup
    length = length
    mult = mult
    length_KC = length_KC
    mult_KC = mult_KC

    # calculate BB
    m_avg = df['close'].rolling(window=length).mean()
    m_std = df['close'].rolling(window=length).std(ddof=0)
    df['upper_BB'] = m_avg + mult * m_std
    df['lower_BB'] = m_avg - mult * m_std

    # calculate true range
    df['tr0'] = abs(df["high"] - df["low"])
    df['tr1'] = abs(df["high"] - df["close"].shift())
    df['tr2'] = abs(df["low"] - df["close"].shift())
    df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)

    # calculate KC
    range_ma = df['tr'].rolling(window=length_KC).mean()
    df['upper_KC'] = m_avg + range_ma * mult_KC
    df['lower_KC'] = m_avg - range_ma * mult_KC

    # calculate bar value
    highest = df['high'].rolling(window = length_KC).max()
    lowest = df['low'].rolling(window = length_KC).min()
    m1 = (highest + lowest)/2
    df['value'] = (df['close'] - (m1 + m_avg)/2)
    fit_y = np.array(range(0,length_KC))
    df['value'] = df['value'].rolling(window = length_KC).apply(lambda x: 
                              np.polyfit(fit_y, x, 1)[0] * (length_KC-1) + 
                              np.polyfit(fit_y, x, 1)[1], raw=True)
    # check for 'squeeze'
    df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC']) # 布林在KC內
    df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])# 布林在KC外(放大突破)
    return pd.DataFrame({
        'squeeze_off': df['squeeze_off'].astype(int),
        'upper_KC': df['upper_KC'] ,
        'lower_KC': df['lower_KC'],
        'upper_BB':df['upper_BB'],
        'lower_BB':df['lower_BB']
    }, index=df.index)
    
# crypto-trend-judger

[系統展示: BTCUSDT(15m) on Grafana](http://wenwender.hopto.org/d/ovypK7_nzn/bi-te-bi-duo-kong-pan-zheng-pan-duan-qi-pan-shi-pan-duan?orgId=1&from=now-5m&to=now)

![https://wenwender.files.wordpress.com/2022/06/image.png?w=1024](https://wenwender.files.wordpress.com/2022/06/image.png?w=1024)

透過Grafana可視化(資料為幣安 BTCUSDT 合約 6/8-6/10的15分K走勢)

- 紅色:趨勢偏多，可以使用趨勢策略作進出場
- 綠色:趨勢偏空，可以使用趨勢策略作進出場
- 黃色:可能為區間震盪，可以使用區間交易策略(逆勢)

## 系統使用指標

此判斷系統是透過幾個混合的指標來做到盤勢的判斷

- atr(真實波動幅度均值)
- rsi(相對強弱指標)
- Bollinger Band(布林通道)
- Keltner Channel(肯特納通道)

## 環境變數

**Price-quoter**

```python
INFLUXDB_URL   
INFLUXDB_TOKEN 
INFLUXDB_ORG 
BINANCE_API_KEY 
BINANCE_API_SECRET 
```

**Signal-builder**

```python
INFLUXDB_URL   
INFLUXDB_TOKEN 
INFLUXDB_ORG
```

**Trend-judger**

```python
INFLUXDB_URL   
INFLUXDB_TOKEN 
INFLUXDB_ORG
```

## 系統架構

在還沒介紹演算法前，先簡單的介紹整個判斷系統的架構，全部的元件都以***python***撰寫，並以***Container***的方式啟動，彼此可以非同步的運作。

如果交易使用的平台，有開放交易的API，就可以實作在Trader上，我自己目前是使用幣安。

![https://wenwender.files.wordpress.com/2022/06/btc-trend.drawio.png?w=651](https://wenwender.files.wordpress.com/2022/06/btc-trend.drawio.png?w=651)

- Influxdb: 時序型資料庫，有針對Time series類型資料儲存查詢進行優化。
- Price-quoter:透過Binance平台的API取得Bitcoin報價後，存入Influxdb。
- Signal-builder: 從Influxdb取得資料後，計算完需要的技術指標後，寫入Influxdb。
- Trend-judger: 盤勢判斷器的演算法會放在這裡，判斷完目前的盤勢訊號後，除了寫回Influxdb做可視化外，也可以透過MQ與Trader連結做實盤交易的其中之一訊號。

本次實作只有到趨勢判斷並可視化，如果大家有興趣，可以再自行考慮整併進交易系統裡作為訊號之一。

## 程式優化方向

- 寫這個project的時候Clean Code的概念還較薄弱，很多變數的命名較不好，Function也沒有拆乾淨，降低易讀性，補足Clean Code的概念後希望未來能寫更好
- 應該善用@property 和@dataclass來管理資料
- 可以將一些算法重要變數儲存在Redis，未來可以根據環境做動態變化(目前是fix的)
- 專案結構和Module分類可以再思考
- 待補上Docker-compose

## 算法優化方向

- 當量能出現時，應該要縮小KC 通道參數，讓**趨勢判斷能夠延續。**
待量能縮減，再放大通道參數，這樣可以達到在趨勢出現時，不會因為暫時的盤整而停止趨勢判斷。(2022/06/14)

![Untitled](crypto-trend-judger%20c3ded912db8a4b0398c6d75f95d40c96/Untitled.png)
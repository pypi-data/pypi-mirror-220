import time
import pandas as pd
import requests
import json





def ohlc(code: str, timeframe: str, timerange: str):
    """获取日线数据 marketWatch只支持日线级别的

    参数:
        code: STOCK/US/XNAS/AAPL | TMUBMUSD10Y
        timeframe: P1D | P1W
        timerange: P1M P1Y P2Y All

    返回:
        pandas.dataframe

                    open      high      low   close      volume
        time
        2022-07-21  154.500  155.5700  151.940  155.35  65086641.0
        2022-07-22  155.390  156.2800  153.410  154.09  66675406.0
        2022-07-25  154.010  155.0400  152.280  152.95  53623953.0
        2022-07-26  152.265  153.0850  150.800  151.60  55138688.0
        2022-07-27  152.580  157.3300  152.160  156.79  78620688.0
        ...             ...       ...      ...     ...         ...
        2023-07-14  190.230  191.1799  189.630  190.69  41616238.0
        2023-07-17  191.900  194.3200  191.810  193.99  50520160.0
        2023-07-18  193.350  194.3300  192.415  193.73  48353770.0
        2023-07-19  193.100  198.2300  192.650  195.10  80507320.0
        2023-07-20  195.090  196.4700  192.495  193.13  59581196.0

    抛出:

    示例:
        df = MW_GetOHLC('STOCK/US/XNAS/AAPL', 'P1D', 'P1Y')

    """

    req_url = (
        f'https://api-secure.wsj.net/api/michelangelo/timeseries/history?json={{"Step":"{timeframe}","TimeFrame":"{timerange}", '
        '"EntitlementToken":"cecc4267a0194af89ca343805a3e57af","IncludeMockTick":true,"FilterNullSlots":false,'
        '"FilterClosedPoints":true,"IncludeClosedSlots":false,"IncludeOfficialClose":true,"InjectOpen":false,'
        '"ShowPreMarket":false,"ShowAfterHours":false,"UseExtendedTimeFrame":false,"WantPriorClose":true,'
        '"IncludeCurrentQuotes":false,"ResetTodaysAfterHoursPercentChange":false,'
        f'"Series":[{{"Key":"{code}","Dialect":"Charting","Kind":"Ticker","SeriesId":"s1",'
        '"DataTypes":["Open", "High", "Low", "Last", "Volume"]}]}&ckey=cecc4267a0'
    )

    # print(req_url)

    r = requests.get(
        req_url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Content-Type": "application/json, text/javascript, */*; q=0.01",
            "Dylan2010.EntitlementToken": "cecc4267a0194af89ca343805a3e57af",
        },
    )
    # Full Return
    # print(r.text)
    # return r.text

    # Stock UNIX Dates
    datajson = json.loads(r.content)
    times = datajson['TimeInfo']['Ticks']
    # print(times)

    # Stock Prices
    data = datajson['Series'][0]['DataPoints']
    # print(data)

    # temp_df = pd.DataFrame(data, columns=['REPORT_DATE','PUBLISH_DATE', 'VALUE', 'PRE_VALUE'])
    temp_df = pd.DataFrame(data)
    temp_df['time'] = times
    temp_df.columns = ["open", "high", "low", "close", 'volume', 'time']

    temp_df["time"] = pd.to_datetime(temp_df["time"], unit='ms').dt.date
    # temp_df["time"] = pd.to_datetime(temp_df["time"],unit='ms')
    temp_df.set_index("time", inplace=True)
    # print(temp_df.dtypes)
    temp_df.dropna(inplace=True)

    # print(temp_df)
    return temp_df


if __name__ == "__main__":
    df = ohlc('TMUBMUSD03M', 'P1D', 'P1Y')
    print(df)

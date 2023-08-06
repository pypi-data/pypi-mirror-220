import httpx
from cashare.dname import url1
import pandas as pd
import time
def stock_list(token,type:str):
    if type in['us','hk','ca']:
        url = url1 + '/stock/list/'+type+'/'+ token

        r = httpx.get(url,timeout=100)

        return pd.DataFrame(r.json())
    else:
        return "type输入错误"

if __name__ == '__main__':
    df=stock_list(type='hk',token='d9882e4b76023e40f9f07fdced4eb70943i2')
    print(df)
    df = stock_list(type='ca', token='d9882e4b76023e40f9f07fdced4eb70943i2')
    print(df)
    df = stock_list(type='us', token='d9882e4b76023e40f9f07fdced4eb70943i2')
    print(df)
    pass




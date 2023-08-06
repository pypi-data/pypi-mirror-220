import httpx
from cashare.dname import url1
import pandas as pd
import time
from cashare.common.get_data import _retry_get
def u_h_now_data(type,token):
    li = handle_url(type=type, token=token)

    r =_retry_get(li,timeout=100)

    lsss=pd.DataFrame(r.json())
    if r.json() == 'token无效或已超期':
        return r.json()
    else:
        return lsss

def handle_url(type,token):
    g_url=url1+'/us/stock/nowprice/'+type+'/'+token

    return g_url

if __name__ == '__main__':
    ll=u_h_now_data(type='all',token='z9882e4b76023e40fb084c421f588ab864x3')

    print(ll)




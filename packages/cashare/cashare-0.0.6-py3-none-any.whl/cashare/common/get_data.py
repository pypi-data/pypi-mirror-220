import httpx
from cashare.dname import url1
import datetime
import pandas as pd
import dateutil.relativedelta
import time


from tenacity import retry, stop_after_attempt, wait_fixed,retry_if_exception_type

@retry(stop=stop_after_attempt(3),wait=wait_fixed(1),retry_error_callback=lambda exc:True, retry=retry_if_exception_type(Exception))
def _retry_get(url,timeout):
    """
    带重试机制的GET请求函数

    Args:
        url (str): 请求的URL

    Returns:
        Response: 请求的响应对象

    """

    response = httpx.get(url, timeout=timeout)
    response.raise_for_status()
    return response


def generate_data(sk_code,mold,token,end_date:str=None,start_date='19910101',timeout=100):
    """
       获取每日数据的封装函数

       Args:
           sk_code (str): 股票代码
           token (str): 访问令牌
           start_date (str, optional): 起始日期，默认为'1991-01-01'
           end_date (str, optional): 结束日期，默认为当天日期

       Returns:
           DataFrame or str: 返回获取到的每日数据DataFrame，或者错误信息字符串
       """
    today = datetime.date.today().strftime('%Y%m%d')
    if end_date is None or end_date > today:
        end_date = today
    start_date = start_date.replace('-', '')
    end_date = end_date.replace('-', '')
    if start_date > today:
        return "start_date大于现在时间"
    if start_date > end_date:
        return "start_date大于end_date"

    url = _generate_url(sk_code=sk_code, start_date=start_date, end_date=end_date, mold=mold,token=token)
    try:
        response = _retry_get(url,timeout=timeout)
        if isinstance(response, bool) and response:
            return "请求失败,请联系管理员"
        if response.status_code == 200:
            json_data = response.json()
            if json_data == 'token无效或已超期':
                return json_data
            else:
                return pd.DataFrame(json_data)
        else:
            print(333)
            return "请求失败,请联系管理员"
    except httpx.RequestError as e:
        return "网络请求失败：" + str(e)


def _generate_url(sk_code, start_date, end_date, token,mold, limit=10000):
    """
    生成URL的辅助函数

    Args:
        sk_code (str): 股票代码
        start_date (str): 起始日期
        end_date (str): 结束日期
        token (str): 访问令牌
        limit (int, optional): 获取数据的条数，默认为10000
        type (str): 访问令牌

    Returns:
        str: 生成的URL
    """
    url = f"{url1}/stock/{mold}/{sk_code}/{start_date}/{end_date}/{limit}/{token}"
    return url


if __name__ == '__main__':

    df = generate_data(sk_code="000001.sz", token='z9882e4b76023e40ff0ea54667f4c44de2i8', start_date='1990-04-02',
                        end_date='2024-05-02',mold='daily')
    print(df)


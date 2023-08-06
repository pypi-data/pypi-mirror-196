import requests
from . import utils

class ElectricAPI:
    '''
    能源管理平台API
    '''
    _url = 'http://10.50.2.206'
    _headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Referer': 'http://10.50.2.206'
    }

    def __init__(self, session=requests.session(), proxies=None):
        self.session = session
        self.proxies = proxies

    def get(self, url,  **kwargs):
        if (kwargs.get('proxies') is None):
            kwargs['proxies'] = self.proxies
        if (kwargs.get('headers') is None):
            kwargs['headers'] = self._headers
        return self.session.get(self._url + url,  **kwargs)

    def post(self, url,  **kwargs):
        if (kwargs.get('proxies') is None):
            kwargs['proxies'] = self.proxies
        if (kwargs.get('headers') is None):
            kwargs['headers'] = self._headers
        return self.session.post(self._url + url,  **kwargs)

    def getMeter(self,  **kwargs):
        '''
        电表参数查询

        参数`_dc`不起作用且可省略
        '''
        params = kwargs.get('params')
        if (params is not None and params.get('_dc') is None):
            params['_dc'] = utils.timestamp()
        kwargs['params'] = params
        return self.get('/api/charge/query', **kwargs)

    def getRoom(self, **kwargs):
        '''
        获取本人房信息

        参数`_dc`不起作用且可省略
        '''
        params = kwargs.get('params')
        if (params is not None and params.get('_dc') is None):
            params['_dc'] = utils.timestamp()
        kwargs['params'] = params
        return self.get('/api/charge/GetRoom', **kwargs)

    def getBill(self, **kwargs):
        '''
        获取充值账单

        所有参数疑似均不起作用且可省略
        '''
        params = kwargs.get('params')
        default_params = {
            '_dc': utils.timestamp(),
            'page': 1,
            'start': 1,
            'limit': 25
        }
        if (params is not None):
            for key, value in default_params.items():
                if (params.get(key) is None):
                    params[key] = value
        kwargs['params'] = params
        return self.get('/api/charge/user_account', **kwargs)

    def recharge(self, **kwargs):
        '''
        电费充值

        URL参数`_dc`不起作用且可省略
        '''
        params = kwargs.get('params')
        if (params is not None and params.get('_dc') is None):
            params['_dc'] = utils.timestamp()
        kwargs['params'] = params
        data = kwargs.get('data')
        default_data = {
            'building': 'C1',
            'room': 'A301',
            'kwh': 100
        }
        if (data is not None):
            for key, value in default_data.items():
                if (data.get(key) is None):
                    data[key] = value
        kwargs['data'] = data
        return self.post('/api/charge/Submit', **kwargs)

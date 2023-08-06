import requests
from . import utils


class StudentAPI:
    '''
    本科生教学管理系统API

    TODO: 网站返回的结果全是html, 需要进一步处理
    '''
    url = 'https://jw.shiep.edu.cn'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://jw.shiep.edu.cn/eams/home.action'
    }

    def get(self, url,  **kwargs):
        if (kwargs.get('proxies') is None):
            kwargs['proxies'] = self.proxies
        if (kwargs.get('headers') is None):
            kwargs['headers'] = self.headers
        return self.session.get(self.url + url,  **kwargs)

    def post(self, url,  **kwargs):
        if (kwargs.get('proxies') is None):
            kwargs['proxies'] = self.proxies
        if (kwargs.get('headers') is None):
            kwargs['headers'] = self.headers
        return self.session.post(self.url + url,  **kwargs)

    def __init__(self, session=requests.session(), proxies=None):
        self.session = session
        self.proxies = proxies

    def home(self, **kwargs):
        return self.get('/eams/home.action', **kwargs)

    def todayCourse(self, **kwargs):
        '''
        获取今日课表

        参数`_`不起作用且可省略
        '''
        params = kwargs.get('params')
        if (params is not None and params.get('_') is None):
            params['_'] = utils.timestamp()
        kwargs['params'] = params
        return self.get('/eams/studTodayCourse!search.action', **kwargs)

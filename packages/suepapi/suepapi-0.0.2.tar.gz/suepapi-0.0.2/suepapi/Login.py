import requests
from pyquery import PyQuery as pq


class Login:
    session = requests.sessions.Session()
    loginURL = 'https://ids.shiep.edu.cn/authserver/login'
    educationURL = 'https://jw.shiep.edu.cn/eams/home.action'
    energyURL = 'http://10.50.2.206/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    isLogin = False

    def __init__(self, username, password,  service='', rememberMe=False, proxies=None):
        '''
        参数说明

        username: 用户名
        password: 密码
        service: (可选) 要登陆的系统, 可填以下值:
            energy: 登录能源管理平台 (充值电费的网站)
            其它值: 登录教务系统 (本科生教学管理系统)
        rememberMe: 七天内免登录，默认`False`
        proxies: 使用的代理, 格式同`requests`库中的`proxies`参数
        ```'''
        self.username = username
        self.password = password
        self.service = service
        self.rememberMe = rememberMe
        self.proxies = proxies

    def __getArguments(self):
        '''
        获取登录所需的参数, 记录Cookies
        '''
        try:
            url = None
            if self.service == 'energy':
                url = self.energyURL
            else:
                url = self.educationURL
            response = self.session.get(url, headers=self.headers, proxies=self.proxies)
            if (response.status_code != 200):
                raise ConnectionError('获取页面失败，状态码: ', response.status_code)
            doc = pq(response.text)
            args = {
                "lt": doc('input[name="lt"]').attr('value'),
                "dllt": doc('input[name="dllt"]').attr('value'),
                "execution": doc('input[name="execution"]').attr('value'),
                "_eventId": doc('input[name="_eventId"]').attr('value'),
                "rmShown": doc('input[name="rmShown"]').attr('value')
            }
            for key, value in args.items():
                if not isinstance(value, str):
                    raise ValueError("无法获取参数 {} 的值".format(key))
            return args
        except Exception as e:
            print('获取登录所需参数失败', e)

    def __login(self, data):
        '''
        登录
        '''
        data['username'] = self.username
        data['password'] = self.password
        if (self.rememberMe):
            data['rememberMe'] = 'on'
        try:
            if self.service == 'energy':
                data['service'] = self.energyURL
                data['renew'] = 'true'
            else:
                data['service'] = self.educationURL
            response = self.session.post(self.loginURL, headers=self.headers, data=data, proxies=self.proxies)
            if (response.status_code != 200):
                raise ConnectionError('请求出错，状态码:', response.status_code)
            self.isLogin = True
        except Exception as e:
            print('登录失败', e)

    def getSession(self):
        '''
        获取requests的Session

        登录成功返回session, 否则返回None
        '''
        if (self.isLogin):
            return self.session
        else:
            return None

    def start(self):
        '''
        开始登录
        '''
        args = self.__getArguments()
        if (args != None):
            self.__login(args)

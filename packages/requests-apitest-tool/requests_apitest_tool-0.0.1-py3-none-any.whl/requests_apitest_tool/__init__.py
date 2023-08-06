from functools import wraps
import inspect
import requests
from requests import Response
from urllib.parse import urljoin
from requests.cookies import RequestsCookieJar

class HttpRequest(object):
    def __init__(self, url='', method='get', **kwargs):
        self.url = url
        self.method = method
        self.decorator_args = kwargs
        self.func_return = None
        self.func_doc = None
        self.func_im_self = None
        self.session:requests.Session = None

    def __call__(self, func) -> Response:
        self.func = func
        self.is_class = False
        try:
            if inspect.getfullargspec(func).args[0] == 'self':
                self.is_class = True
        except IndexError:
            pass

        @wraps(func)
        def fun_wrapper(*args, **kwargs):
            self.func_return = self.func(*args, **kwargs) or {}
            self.func_im_self = args[0] if self.is_class else object

            try:
                self.func.__doc__ = self.func.__doc__.decode('utf-8')
            except:
                pass
            self.func_doc = (self.func.__doc__ or self.func.__name__).strip()
            self.create_url()
            self.create_session()
            self.session.cookies = getattr(self.func_im_self, 'cookies',RequestsCookieJar())
            self.session.headers.update(getattr(self.func_im_self, 'headers', {}))
            self.decorator_args.update(self.func_return)
            return self.session.request(method=self.method,url=self.url,**self.decorator_args)

        return fun_wrapper

    def _create_url(self):
        """
        生成http请求的url
        """

        # 使用在函数中定义的url变量,如果没有,使用装饰器中定义的
        base_url = getattr(self.func_im_self, 'base_url', '')
        self.url = self.func_return.pop('url', None) or self.url
        self.url = urljoin(base_url, self.url)

    def _create_session(self):
        """
        如果接收到的要变参数中有session,且为Session对象,赋值给session变量, 否则创建一个
        """
        if self.is_class:
            self.session = getattr(self.func_im_self, 'session', None)
            if not isinstance(self.session, requests.Session):
                session = requests.Session()
                setattr(self.func_im_self, 'session', session)
                self.session = session

        elif isinstance(self.func_return.get('session'), requests.Session):
            self.session = self.func_return.get('session')
        else:
            self.session = requests.Session()


http_router = HttpRequest

if __name__ == '__main__':
    pass

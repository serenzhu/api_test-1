import json
import requests

from scripts.handle_log import do_log
from scripts.handle_parameterize import Parameterize
from scripts.handle_yaml import c_yaml


class HandleRequest:
    """
    处理请求
    """
    def __init__(self):
        # 创建Session会话对象
        self.one_session = requests.Session()

    def add_headers(self, headers):
        """
        添加公共请求头
        :param headers: 需要添加的请求头, 为字典类型
        :return:
        """
        # Session会话对象中的headers类似于一个字典
        # 可以将待添加的请求头字典与self.one_session.headers中的请求头(类似字典)进行合并覆盖
        self.one_session.headers.update(headers)

    def send(self, url, method="post", data=None, is_json=True, **kwargs):
        """
        发起请求
        :param url: url地址
        :param method: 请求方法, 通常为get、post、put、delete、patch
        :param data: 传递的参数, 可以传字典、json格式的字符串、字典类型的字符串, 默认为None
        :param is_json: 是否以json的形式来传递参数, 如果为True, 则以json形式来传, 如果为False则以www-form形式来传, 默认为True
        :param kwargs: 可变参数, 可以接收关键字参数, 如headers、params、files等
        :return: None 或者 Response对象
        """
        if isinstance(data, str):   # 判断data是否为str字符串类型, 如果为str类型, 会返回True, 否则返回False
            try:
                # 假设为json字符串, 先使用json.loads转化为字典
                data = json.loads(data)
            except Exception as e:  # 如果不为json字符串会抛出异常, 然后使用eval函数来转化
                do_log.exception(e)
                do_log.info("使用eval函数将数据转换为字典格式")
                data = eval(data)

        # 将传递的method请求方法统一转化为小写
        method = method.lower()

        if method == "get":  # 如果为get请求, 那么传递的data, 默认传查询字符串参数
            res = self.one_session.request(method, url, params=data, **kwargs)
        elif method in ("post", "put", "delete", "patch"):  # 如果为post、put、delete、patch请求
            if is_json:     # 如果is_json为True, 那么以json格式的形式来传参
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:   # 如果is_json为False, 那么以www-form的形式来传参
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print(f"不支持【{method}】请求方法")
        return res

    def request_interface(self, url, method, data):
        # 拼接请求地址
        new_url = c_yaml.read('api', 'prefix') + url
        # 参数化请求地址实例化
        new_url = Parameterize.to_param(new_url)
        # 参数化请求数据实例化
        new_data = Parameterize.to_param(data)
        # 发送请求
        res = self.send(url=new_url, method=method, data=new_data, is_json=True)
        # 返回响应数据
        return res


    def close(self):
        # 调用会话对象的close方法, 是释放资源, 还是可以发起请求的
        self.one_session.close()

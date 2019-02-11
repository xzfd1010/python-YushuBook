import requests


class HTTP:
    # 用于处理一切请求的类，方法应该都是静态方法，不涉及业务，是基础类
    @staticmethod  # staticmethod 没有用到类变量和对象变量
    def get(url, return_json=True):  # restful API 返回 json格式的数据
        r = requests.get(url)
        # 根据状态码处理不同情况
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()  # 返回json格式
        #     else:
        #         return r.text  # 返回字符串
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ''

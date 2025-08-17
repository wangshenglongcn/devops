import time
from .metrics import record_event


# Django 2.0 以后，中间件是一个类，必须实现 __init__ 和 __call__ 方法：
class MetricsMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        print("中间件初始化")

    def __call__(self, request):
        # 到达视图前
        print("请求到达视图前", request.path)

        start = time.time()
        response = self.get_response(request)

        # 到达视图后
        print("视图执行后，响应返回前", response.status_code)
        duration = time.time() - start
        method = request.method  # 请求方法
        status = response.status_code  # 返回码
        path = request.path  # 请求路径

        record_event((method, path, status, duration))

        return response

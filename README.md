## 记录个人django开发流程

```shell
mkdir djangotutorial
python-admin startproject mystie djangotutorial  # 创建名为mysite的项目，位于djangotutorial目录下

cd djangotutorial
python manage.py runserver  # 启动django项目

python manage.py startapp polls  # 创建一个应用
```

### 定义一个视图的流程

这里以polls应用示例：
- 在polls/views.py中创建一个函数，用于显示访问链接时显示的内容

```python
def index(request):
    return HttpResponse("Hello, world.")
```

- 在polls/views.py中创建url信息

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
]
```

- 在项目urls.py中引用polls应用的urls信息

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path参数， route 和 view， include允许引用其他URLconf
    # 子应用的url信息在此定义或者include引用
    path("polls/", include("polls.urls"))
]
```
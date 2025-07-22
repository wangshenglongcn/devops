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

### 数据库

这里暂时使用默认的SQLite

### 创建模型

模型本质上是数据库布局，并包含额外的元数据

编辑polls/models.py

```py
from django.db import models

# Create your models here.
# 每个模型都由一个继承自 django.db.models.Model 的类表示
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_data = models.DateTimeField("data published")

class Choice(models.Model):
    # ForeignKey 定义了一个关系，告诉Django每个Choice都与一个Question相关
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

### 激活模型

在mysite/setting.py INSTALLED_APPS中添加应用配置类，配置类名在应用app.py下

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig'  # 新增
]
```

执行 `python manage.py makemigrations polls`，终端显示数据库表创建成功
```
Migrations for 'polls':
  polls\migrations\0001_initial.py
    + Create model Question
    + Create model Choice
```

打印SQLite数据库内容

```shell
python manage.py sqlmigrate polls 0001
```

当数据库修改后
```shell
# 为模型的改变生成迁移文件
python manage.py makemigrations

# 应用数据库迁移
python manage.py migrate
```

### 管理界面

创建管理员
```shell
python manage.py createsuperuser
```

向管理界面中假如投票应用
```python
from django.contrib import admin

# Register your models here.
from .models import Question

admin.site.register(Question)
```

### 获取访问url中的信息

如下所示，在polls/urls.py中定义
假如url为polls/5/result/, url会先匹配到polls/，然后去掉这段文件，继续匹配
可以匹配到`<int:question_id>/results/`, 就将question_id赋值为5
```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # url匹配是，会将匹配到的int赋值给question_id
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]
```
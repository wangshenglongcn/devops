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

### 写一个有用的视图

每个视图必须做的只有两件事：返回一个HttpResponse对象或者抛出一个异常，如Http404，其余的均自定义

假如我们写一个展示Question最新5条数据的视图，可以使用如下代码：
```python
def index(request):
    question_list = Question.objects.order_by("-pub_date")[:5]
    resp = "\n".join([q.question_text for q in question_list])
    return HttpResponse(resp)
```

但是存在一个问题，我们不可能一直这样手写格式，这时我们需要模板去渲染数据。

#### 使用模板渲染

在polls应用下创建templates/polls目录，将模板放在这个目录下

>虽然我们现在可以将模板文件直接放在 polls/templates 文件夹中（而不是再建立一个 polls 子文件夹），但是这样做不太好。Django 将会选择第一个匹配的模板文件，如果你有一个模板文件正好和另一个应用中的某个模板文件重名，Django 没有办法 区分 它们。我们需要帮助 Django 选择正确的模板，最好的方法就是把他们放入各自的 命名空间 中，也就是把这些模板放入一个和 自身 应用重名的子文件夹里。

```html
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

html文件中使用了django模板语言，参考[Django模板](https://docs.djangoproject.com/zh-hans/5.2/topics/templates/)

而在视图中，进行以下修改
引入的loader用来加载模板；template.render是对象方法，渲染模板
```py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader

def index(request):
    question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"question_list": question_list}
    return HttpResponse(template.render(context, request))
```

由于载入模板，加载对象，并基于模板生成HttpResponse对象是一个很常用的流程，所以django提供了快捷方法：
无需导入 loader 以及 HttpResponse
```py
from django.shortcuts import render
from .models import Question

def index(request):
    question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"question_list": question_list}
    return render(request, "polls/index.html", context)
```

#### 抛出404错误

一种方法是用try-except来捕获并抛出，另一种是使用django定义的快捷函数get_object_or_404

```python
from django.shortcuts import render, get_object_or_404
from .models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

```

也有get_list_or_404，原理类型，列表为空就报404

### 去除硬编码

之前在index.html中链接是硬编码的
```html
<a href="/polls/{{ question.id }}/">{{ question.question_text }}</a>
```

但是，由于在polls.urls中定义了name，所以可以用以下方式：
```html
<a href="{% url 'detail' question.id %}">{{ question.question_text }}</a>
```

### 为url添加命名空间

在实际应用中，一个项目可能不止一个应用，Django如何分辨重名的url呢？

在根URLconf中添加命名空间app_name，如polls/urls.py
```python
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    # url匹配是，会将匹配到的int赋值给question_id
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]
```

配置后，html中使用polls:detail来访问对应url，如
```html
<a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a>
```


### 实现投票页面

### 使用通用视图

detail()和results()视图都很精简，但存在冗余问题，显示投票列表的index()视图也具有类似性。

这些视图反映基本的网络开发中的一个常见情况：根据URL中的参数从数据库中获取数据、载入模板文件然后返回渲染后的模板。
由于这种情况特别常见，Django 提供一种快捷方式，叫做 “通用视图” 系统。

如：ListView 和 DetailView 通用视图分别抽象了 "显示对象列表" 和 "显示特定类型对象的详细页面" 的概念。

按照以下步骤转换成通用视图：
1. 转换URLconf
2. 删除一些旧的、不再需要的视图
3. 基于django的通用视图引入新视图

>一般来说，当编写一个 Django 应用时，你应该先评估一下通用视图是否可以解决你的问题，你应该在一开始使用它，而不是进行到一半时重构代码。

#### 改良URLconf

适配使用通用视图
```python
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # url匹配时，会将匹配到的int赋值给question_id或pk
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
```

#### 改良视图

通用视图都继承自 django.views.generic
ListView 展示一个对象的列表
DetailView 展示一个对象的详细信息

如下所示
```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "question_list"
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
```


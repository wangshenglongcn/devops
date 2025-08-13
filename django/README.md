## 创建项目及应用

```shell
django-admin startproject project_name .
python manage.py startapp app_name
```
本项目中，project_name = mysite, app_name = blog

settings INSTALL_APPS 中添加应用名
```python
INSTALLED_APPS = [
    'blog',
    ...
]
```

## 配置 MySQL 数据库

安装 pymysql，配置 mysite/__init__.py
```python
import pymysql

pymysql.install_as_MySQLdb()

```

部署 mysql，并新建数据表及用户
```shell
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django_user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydb.* TO 'django_user'@'%';
FLUSH PRIVILEGES;
```

mysite/settings.py 下修改数据库配置文件
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydb",
        "USER": "django_user",
        "PASSWORD": "password",
        "HOST": "117.72.175.93",
        "PORT": "3307",
    }
}
```

执行 `python manage.py migrate` 无报错说明成功链接

## 自定义数据库模型

这里定义了标题、作者、内容、发布时间
其中作者配置成多个文章配对一个用户，作者被删除时相关文章也会被删除
```python
from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    title = models.CharField(max_length=200)

    # 配置成多个文章配对一个用户，作者被删除时相关文章也会被删除
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField()


    # 默认排序方式
    class Meta:
        ordering = ['-publish_date']
```

## 配置路由

在 mysite 中 include app 中的 url 配置，在 app 中自定义路由

## 配置视图

在 app 下 views.py 中添加 之前在 urls.py 中用到的 视图模板文件放到 app/templates/app 下


## 前端

前端除了 django 自带的模板语言外，其余格式大部分用 bootstrap 实现

## 适配生产环境

修改 mysite/settings.py

1. DEBUG 改为 False
2. 增加 STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 以便正常执行 python manage.py collectstatic
    无其他适配的话会在跟 manage.py 同级目录下生产 staticfiles 目录
3. 修改 ALLOWED_HOSTS，添加生产环境 IP


## 参考文档

[django官方文档](https://docs.djangoproject.com/zh-hans/5.2/topics/)
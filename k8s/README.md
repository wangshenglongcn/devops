## 语法

关于 Deployment、Service、StatefulSet 等语法可以参考 k8s 官方文档。

## Mysql

由于 MySQL 需要持久化，所以使用 StatefulSet 来部署，并配置持久化卷。

另外 Django 关联 MySQL 需要一个确定的链接，所以这里配合 Headless Service 来固定 DNS。

## Redis

Redis 作为数据库缓存，虽然不需要持久化，但是在部署带哨兵节点的高可用集群时，Django 关联也需要固定的链接。

所以 Redis 也通过 Headless Service + StatefulSet 实现。

## Django Blog


Django Blog 无需持久化，用 Deployment 即可，另外需要暴露端口给外部，所以需要 NodePort 类型 Service 。

原本只有博客的源码，所以要先用 Docker 将其打包成镜像，命令如下：
```shell
cd django
docker build -t django-blog .
```

然后需要注意 Docker 镜像跟 k8s 镜像（containerd）不共享，所以需要额外导入：
```shell
# 打包 docker 镜像
docker save django-blog:latest -o django-blog.tar

# 导入 containerd
ctr images import django-blog.tar

# 查看 k8s 镜像
ctr images list
```

### Django 额外特殊适配

ALLOWED_HOSTS 中添加 Django Service
```python
ALLOWED_HOSTS = [..., "django-service"]
```

由于 Django 访问 MySql、Redis 的方式有变更

访问链接等信息通过参数传递
```yaml
env:
  - name: REDIS_HOST
    value: redis-svc  # Redis 服务的名字
  - name: REDIS_PORT
    value: "6379"  # Redis 默认端口
  - name: REDIS_PASSWORD
    value: "123qwe"  # Redis 密码（如果有）
  - name: DATABASE_HOST
    value: mysql-svc  # 数据库服务的名字
  - name: DATABASE_NAME
    value: mydb
  - name: DATABASE_USER
    value: root
  - name: DATABASE_PASSWORD
    value: password
```

所以 Django settings 文件中需适配，如：
```python
# mysql
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")  # 默认值为localhost
DATABASE_NAME = os.getenv("DATABASE_NAME", "mydb")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 使用 MySQL 数据库
        "NAME": DATABASE_NAME,  # 使用环境变量中的数据库名
        "USER": DATABASE_USER,  # 使用环境变量中的用户名
        "PASSWORD": DATABASE_PASSWORD,  # 使用环境变量中的密码
        "HOST": DATABASE_HOST,  # 使用环境变量中的主机地址
        "PORT": "3306",  # MySQL 默认端口
    }
}

# redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # 默认值为 localhost
REDIS_PORT = os.getenv("REDIS_PORT", "6379")  # 默认 Redis 端口
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")  # 默认没有密码

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",  # 使用 django-redis
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",  # Redis 服务的 URL
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,  # 传入密码（如果有的话）
        },
    }
}
```
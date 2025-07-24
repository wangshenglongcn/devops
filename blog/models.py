from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    """
    settings.AUTH_USER_MODE: Django 内置的用户模型（通常是 auth.User，或者你自定义的用户模型）。用 settings.AUTH_USER_MODEL 可以避免硬编码表名，让项目更灵活
    on_delete=models.CASCADE: 表示当被关联的用户被删除时，这个作者字段对应的记录也会被删除（级联删除）
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)  # 新建对象时，如果没有手动传值，就默认设置为调用timezone.now()的结果
    publish_date = models.DateTimeField(blank=True, null=True) # 设置为空时，这两个建议一起设置，blank表单层面，null数据库层面

    def publish(self):
        self.publish_date = timezone.now()
        self.save()  # 当前对象的最新状态保存到数据库
    
    def __str__(self):
        return self.title

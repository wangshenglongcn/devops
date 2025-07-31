from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Posts(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    # 默认为当前时间
    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        # 指定默认排序方式
        ordering = ['-publish_date']
    
    # 优化后台显示
    def __str__(self):
        return self.title
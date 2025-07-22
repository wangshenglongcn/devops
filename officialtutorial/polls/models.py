from django.db import models

# Create your models here.
# 每个模型都由一个继承自 django.db.models.Model 的类表示
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("data published")

class Choice(models.Model):
    # ForeignKey 定义了一个关系，告诉Django每个Choice都与一个Question相关
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
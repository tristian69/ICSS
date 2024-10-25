from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # User는 django.contrib.auth.models가 제공하는 모델
    modify_date = models.DateTimeField(null=True, blank=True)
    pcode = models.CharField(max_length=10)
    pname = models.TextField()
    unitprice = models.IntegerField(default=0)
    discountrate = models.DecimalField(max_digits=11, decimal_places=2,default=0)
    mainfunc = models.CharField(max_length=100, default="")
    imgfile = models.ImageField(null=True, upload_to="", blank=True) # 이미지 컬럼 추가
    detailfunc = models.CharField(max_length=200, default="")


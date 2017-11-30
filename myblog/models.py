from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar=models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default.png',max_length=200,blank=True,verbose_name='头像')
    class Meta:
        verbose_name='用户'
        verbose_name_plural=verbose_name
        ordering=['-id']
    def __str__(self):
        return self.username

class Category(models.Model):
    name=models.CharField(max_length=20,verbose_name='分类名称')
    index=models.IntegerField(default=999,verbose_name='分类索引')
    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name
        ordering=['index','id']
    def __str__(self):
        return self.name

# class ArticleManager(models.Manager):
#     def distinct_date(self):
#         distinct_date_list = []
#         date_list = self.values('date_publish')
#         for date in date_list:
#             date = date['date_publish'].strftime('%Y/%mwenzhangcundang')
#             if date not in distinct_date_list:
#                 distinct_date_list.append(date)
#         return distinct_date_list

class Article(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    desc=models.CharField(max_length=100,verbose_name='描述')
    content=models.TextField(verbose_name='内容')
    click_count=models.IntegerField(default=0,verbose_name='点击次数')
    is_recommend=models.BooleanField(default='False',verbose_name='是否推荐')
    date_publish=models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    author=models.ForeignKey(User,verbose_name='作者')
    category=models.ForeignKey(Category,blank=True,verbose_name='分类')
    # objects = ArticleManager()

    class Meta:
        verbose_name='文章'
        verbose_name_plural=verbose_name
        ordering=['-date_publish']
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.article.title

class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200,  verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser



class Userprofile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default=u"")
    birday = models.DateTimeField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")), default=u"",verbose_name=u'性别')
    address = models.CharField(max_length=100, default=u"",verbose_name=u'地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name=u'电话')
    image = models.ImageField(upload_to=u"image/%Y/%m",default=u"", max_length=100,verbose_name=u'头像')

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()



class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=60,verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u'验证码类型',max_length=50,choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")))
    send_time = models.DateTimeField(verbose_name=u'发送时间',default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural  = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image=models.ImageField(upload_to="banner/%Y/%m",verbose_name=u'轮播图')
    url=models.URLField(max_length=200,verbose_name=u'访问地址')
    index=models.IntegerField(default=100,verbose_name=u'顺序')
    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural  = verbose_name







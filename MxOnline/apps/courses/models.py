# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.



class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name=u"课程名")
    course_org= models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    teacher=models.ForeignKey(Teacher,verbose_name=u'讲师',null=True,blank=True)
    # detail = models.TextField(verbose_name=u'课程详情')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300,imagePath="course/ueditor/", filePath="course/ueditor/",default='')

    is_banner=models.BooleanField(default=False,verbose_name=u'是否轮播')
    degree = models.CharField(verbose_name=u'难度',default='',choices=(("cj",u"初级"),("zj",u"中级"),("gj",u"高级")),max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面',default='')
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    tag=models.CharField(default="", verbose_name=u'课程标签', max_length=20)
    category=models.CharField(default=u'前端开发',verbose_name=u'课程类别',max_length=20)
    you_know=models.CharField(max_length=300,verbose_name=u'学到',default='')
    teacher_tell=models.CharField(max_length=300,verbose_name=u'老师说',default='')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description=u'章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = u'跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]
      # 获取课程章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __unicode__(self):
         return self.name


class BannerCourse(Course):

    class Meta:
        verbose_name=u'轮播课程'
        verbose_name_plural=verbose_name
        proxy=True




class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name


    def get_lesson_video(self):
        return self.video_set.all()

    def __unicode__(self):
         return self.name



class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100,verbose_name=u"视频名")
    url = models.URLField(max_length=200,default="", verbose_name=u'访问地址')
    video_times = models.IntegerField(default=0,verbose_name=u"时长（分钟）")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

        def __unicode__(self):
            return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u"名称")
    download = models.FileField(upload_to='course/resource/%Y/%m', default="", max_length=200, verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name








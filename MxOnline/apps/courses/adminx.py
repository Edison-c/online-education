# _*_ coding:utf-8 _*_
__author__ = 'edison'
__date__ = '17-12-19 上午12:18'

from .models import Course,Lesson,Video,CourseResource,BannerCourse
from organization.models import CourseOrg

import xadmin
import xlrd



class LessonInline(object):
    model=Lesson
    extra=0


class CourseResourceInline(object):
    model=CourseResource
    extra=0




class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','is_banner','learn_times','students','fav_nums','image','click_nums','add_time','get_zj_nums','go_to']
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name','desc','detail','degree','is_banner','learn_times','students','fav_nums','image','click_nums','add_time']
    ordering = ['-click_nums']
    readonly_fields=['fav_nums']
    exclude=['click_nums']
    inlines=[LessonInline,CourseResourceInline]
    list_editable=['degree','desc']
    style_fields = {"detail":"ueditor"}
    import_excel = True

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)



    def queryset(self):
        qs=super(CourseAdmin,self).queryset()
        qs=qs.filter(is_banner=False)
        return qs


    def save_models(self):
        obj=self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org=obj.course_org
            course_org.course_nums=Course.objects.filter(course_org=course_org).count()
            course_org.save()



xadmin.site.register(Course, CourseAdmin)



class BannerCourseAdmin(object):
    list_display = ['name','desc','detail','degree','is_banner','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name','desc','detail','degree','is_banner','learn_times','students','fav_nums','image','click_nums','add_time']
    ordering = ['-click_nums']
    readonly_fields=['fav_nums']
    exclude=['click_nums']
    inlines=[LessonInline,CourseResourceInline]

    def queryset(self):
        qs=super(BannerCourseAdmin,self).queryset()
        qs=qs.filter(is_banner=True)
        return qs


xadmin.site.register(BannerCourse, BannerCourseAdmin)





class LessonAdmin(object):
    list_display = ['name','course','add_time']
    search_fields = ['name','course']
    list_filter = ['name','course','add_time']

xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name','course']
    list_filter = ['name', 'course', 'add_time']


xadmin.site.register(CourseResource, CourseResourceAdmin)
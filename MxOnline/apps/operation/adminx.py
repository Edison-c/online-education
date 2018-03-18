# _*_ coding:utf-8 _*_
__author__ = 'edison'
__date__ = '17-12-19 上午1:50'

import xadmin

from .models import UserAsk,CourseComments,UserFavorite,UserMessage,Usercourse

class UserAskAdmin(object):
    list_display = ['name', 'course_name', 'mobile', 'add_time']
    search_fields = ['name', 'course_name', 'mobile']
    list_filter = ['name', 'course_name', 'mobile', 'add_time']

xadmin.site.register(UserAsk, UserAskAdmin)


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']

xadmin.site.register(CourseComments, CourseCommentsAdmin)


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']

xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']

xadmin.site.register(UserMessage, UserMessageAdmin)


class UsercourseAdmin(object):
    list_display = ['user', 'course',  'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course',  'add_time']

xadmin.site.register(Usercourse, UsercourseAdmin)




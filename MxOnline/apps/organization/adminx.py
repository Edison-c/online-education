# _*_ coding:utf-8 _*_
__author__ = 'edison'
__date__ = '17-12-19 上午1:26'

from .models import CityDict,CourseOrg,Teacher

import xadmin


class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']

xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'image', 'address', 'city',  'fav_nums', 'image', 'click_nums','add_time']
    search_fields = ['name', 'desc',  'address', 'city',  'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'address', 'city',  'fav_nums', 'image', 'click_nums','add_time']
    relfield_style = 'fk-ajax'
xadmin.site.register(CourseOrg, CityDictAdmin)


class TeacherAdmin(object):
    list_display = ['name','org','work_years','work_company','work_position','point','fav_nums','click_nums','add_time']
    search_fields = ['name','org','work_years','work_company','work_position','point','fav_nums','click_nums']
    list_filter = ['name','org','work_years','work_company','work_position','point','fav_nums','click_nums','add_time']

xadmin.site.register(Teacher, TeacherAdmin)





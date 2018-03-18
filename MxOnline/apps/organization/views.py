# _*_ coding:utf-8 _*_
from django.shortcuts import render
from  django.views.generic import View
from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course
from operation.models import UserFavorite
from .models import Teacher
from django.db.models import Q
import json






# Create your views here.



class OrgView(View):
    def get(self,request):
        # 课程机构
        all_orgs=CourseOrg.objects.all()
        hot_orgs=all_orgs.order_by("-click_nums")[:3]

        seacher_keywords = request.GET.get('keywords', '')

        if seacher_keywords:
            all_orgs = CourseOrg.objects.filter(Q(name__icontains=seacher_keywords)|Q(desc__icontains=seacher_keywords))

        # 城市
        all_citys=CityDict.objects.all()
        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct','')
        if category:
               all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort','')
        if sort=='students':
            all_orgs=all_orgs.order_by('-students')
        elif sort=='course_nums':
            all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()


        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,3,request=request)

        orgs = p.page(page)
        return render(request,"org-list.html",{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })



class AddUserAskView(View):
    # 用户添加咨询
    def post(self,request):
        userask_form=UserAskForm(request.POST)

        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)
            data={"status":"success"}
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            data={"status":"fail","msg":u"填写出错"}
            return HttpResponse(json.dumps(data),content_type='application/json')


class OrgHomeView(View):
    # 机构首页
    def get(self,request,org_id):
        current_page = "home"
        course_org=CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums+=1
        course_org.save()
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
             has_fav=True

        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:3]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav

        })

class OrgCourseView(View):
    def get(self,request,org_id):
        current_page="course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #
        #
        #
        # # Provide Paginator with the request object for complete querystring generation
        #
        # p = Paginator(all_courses,3,request=request)
        #
        # course_page = p.page(page)
        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav


        })


class OrgDescView(View):
    def get(self,request,org_id):
        current_page="desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav

        })



class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teachers': all_teachers,
            'current_page': current_page,
            'has_fav':has_fav

        })


class AddFavView(View):
    def post(self,request):
        # 用户收藏和取消收藏
        fav_id=request.POST.get('fav_id','0')
        fav_type=request.POST.get('fav_type','0')


        if not request.user.is_authenticated():
            # 判断用户登录状态
            data={"status":"fail","msg":u"用户未登录"}
            return HttpResponse(json.dumps(data), content_type='application/json')

        exist_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
             #如果记录已经存在，则用户取消收藏
           exist_records.delete()
           if int(fav_type)==1:
               course=Course.objects.get(id=int(fav_id))
               course.fav_nums-=1
               if course.fav_nums<0:
                   course.fav_nums=0
               course.save()

           elif int(fav_type)==3:
                 teacher=Teacher.objects.get(id=int(fav_id))
                 teacher.fav_nums-=1
                 if teacher.fav_nums<0:
                     teacher.fav_nums=0
                 teacher.save()
           elif int(fav_type)==2:
                 org=CourseOrg.objects.get(id=int(fav_id))
                 org.fav_nums-=1
                 if org.fav_nums<0:
                     org.fav_nums=0
                 org.save()
           data={"status":"fail","msg":u"收藏"}

           return HttpResponse(json.dumps(data), content_type='application/json')

        else:
            user_fav=UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user=request.user
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()

                data = {"status": "success", "msg": u"已收藏"}
                return HttpResponse(json.dumps(data), content_type='application/json')

            else:
                data = {"status": "fail", "msg": u"收藏出错"}

                return HttpResponse(json.dumps(data), content_type='application/json')



class TeacherListView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all().order_by('-add_time')
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        seacher_keywords = request.GET.get('keywords', '')

        if seacher_keywords:
            all_teachers = Course.objects.filter(Q(name__icontains=seacher_keywords)|Q(work_company__icontains=seacher_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')


        teachers_nums=all_teachers.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 3, request=request)

        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'sort': sort,
            'hot_teachers': hot_teachers,
            'teachers_nums':teachers_nums
        })



class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher=Teacher.objects.get(id=int(teacher_id))
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]


        # 增加讲师点击数
        teacher.click_nums += 1
        teacher.save()

        all_courses=Course.objects.filter(teacher=teacher)

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org_id, fav_type=2):
                has_fav_org = True


        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,
            'all_courses':all_courses,
            'hot_teachers':hot_teachers
        })





















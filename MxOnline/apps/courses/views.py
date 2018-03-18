# _*_ coding:utf-8 _*_


# Create your views here.
from django.shortcuts import render
from  django.views.generic import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from operation.models import UserFavorite,CourseComments,Usercourse
from courses.models import CourseResource,Video
from  utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q






class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by('-add_time')
        hot_courses=Course.objects.all().order_by("-click_nums")[:3]

        seacher_keywords=request.GET.get('keywords', '')

        if seacher_keywords:
            all_courses=Course.objects.filter(Q(name__icontains=seacher_keywords)|Q(desc__icontains=seacher_keywords))

      # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })


class CourseDetailView(View):
    # 课程详情页
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums+=1
        course.save()

        has_fav_course=False
        has_fav_org=False
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course=True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org=True


        tag=course.tag
        if tag:
            relate_courses=Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses=[]
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })



class CourseInfoView(LoginRequiredMixin,View):
    # 课程章节信息
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))
        course.students+=1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses=Usercourse.objects.filter(user=request.user,course=course)
        if not  user_courses:
            user_course=Usercourse(user=request.user,course=course)
            user_course.save()

        user_courses = Usercourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = Usercourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses=Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources=CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources':all_resources,
            'relate_courses':relate_courses

        })


class CommentsView(LoginRequiredMixin,View):
    # 课程评论信息
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = Usercourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = Usercourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        all_comments=CourseComments.objects.all().order_by('-add_time')
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments':all_comments,
            'relate_courses': relate_courses

        })



class AddCommentView(View):
    def post(self,request):


        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse("{'status':'fail','msg':u'用户未登录'}", content_type='application/json')

        course_id=request.POST.get('course_id',0)

        comments=request.POST.get('comments','')
        if course_id >0 and comments:
            course_comments= CourseComments()
            course=Course.objects.get(id=int(course_id))
            course_comments.course=course
            course_comments.comments=comments
            course_comments.user=request.user
            course_comments.save()
            return HttpResponse("{'status':'success','msg':u'添加成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':u'添加失败'}", content_type='application/json')


class VideoPlayView(View):
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course=video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = Usercourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = Usercourse(user=request.user, course=course)
            user_course.save()

        user_courses = Usercourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = Usercourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video':video
        })






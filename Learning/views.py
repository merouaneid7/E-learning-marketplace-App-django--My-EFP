import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect , render
from App.models import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  logout

def BASE(request):
    return render(request,'base1.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    

    context = {
        'category' : category,
        'course': course,
        
    }
    return render(request,'Main/home.html',context)

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCources = Course.objects.filter(price = 0).count()
    PaidCources = Course.objects.filter(price__gte = 1).count()
    coursenumber=Course.objects.count()
   

    context = {
        'category':category,
        'level':level,
        'course':course,
        'Freecources':FreeCources,
        'Paidcources':PaidCources,
        'coursenumber':coursenumber,
        
    }
    return render(request,'Main/single_course.html',context)


def CONTACT_US(request):
    return render(request,'Main/contact_us.html')

def ABOUT_US(request):
    return render(request,'Main/about_us.html')

def Search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    context = {
        'course':course,
    }
    return render(request,'Search/search.html',context)

def Course_details(request, slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    course = Course.objects.filter(slug = slug)
    if course.exists():
         course = course.first()
    else :
         return redirect('404')
   
    course_id = Course.objects.get(slug = slug)
    if request.user.is_authenticated:
        try:
            check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
        except UserCourse.DoesNotExist:
             check_enroll = None
    
    d_price=course.price - (course.discount*course.price)/100
    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'd_price':d_price,
    }

    return render(request, 'course/course_details.html', context)


def watch_course(request , slug):
    lecture = request.GET.get('lecture')
    course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)
    print(lecture)
    print(course)
    
    try :
        check_enroll = UserCourse.objects.get(user = request.user , course = course_id)
        video = Video.objects.get(id=lecture)
        if course.exists():
            course = course.first()
        else :
            return redirect('404')
    except UserCourse.DoesNotExist :
        return redirect('404')
    print(video)
    context = {
        'course':course,
        'video':video,
        'lecture':lecture,
        'check_enroll':check_enroll
    }
    return render(request,'course/watch_course.html',context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    
    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def Page_not_found(request):
    return render(request,'error/404.html')


def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    
   
    if course.price == 0 :
        course = UserCourse(
            user = request.user,
            course = course
        )
        course.save()
        messages.success(request,'Course are successfully enrolled')
        return redirect('my-course')
    else:
        context = {
            'course':course
        }
    
    course_id = Course.objects.get(slug = slug)

    try:
        enroll_status = UserCourse.objects.get(user=request.user , course=course_id)
    except UserCourse.DoesNotExist:
        enroll_status = None
    return render(request,'checkout/checkout.html',context)

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    course = Course.objects.get(slug = body['course'])
    course_add = UserCourse(
            user = request.user,
            course = course
        )
    course_add.save()
    messages.success(request,'Course are successfully enrolled')
         
    return JsonResponse('Payment completed!', safe=False)
        
def paymentSuccess(request,slug):
    course = UserCourse.objects.get(slug=slug)
    context ={
        'course':course
    }
    return render(request,'checkout/success.html',context)
	

@login_required(login_url='login')
def my_course(request):
    course = UserCourse.objects.filter(user = request.user)

    context = {
        'course':course,
    }
    return render(request,'course/my_course.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def category_page(request,pk):
    category = Categories.objects.get(id=pk)
    course = Course.objects.filter(category=category)
    context = {
        'course':course,
        'category':category
    }

    return render(request,'course/category.html',context)
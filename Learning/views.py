import json
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect , render
from django.contrib.auth import authenticate , login , logout
from App.form import *
from App.models import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import  logout

from django.contrib.auth.decorators import user_passes_test



    
    


    

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

    context = {
        'category':category,
        'level':level,
        'course':course,
        'Freecources':FreeCources,
        'Paidcources':PaidCources,
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
    else :
        check_enroll = None

    d_price=course.price-((course.price*course.discount)/100)
    
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
        video = Video.objects.filter(id=lecture)
        if course.exists():
            course = course.first()
        else :
            return redirect('404')
    except UserCourse.DoesNotExist :
        return redirect('404')
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
            course = course,
            
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
            course = course,
            has_premium_chatbot_access=True,
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


def formateur_list(request):
    formateurs = Author.objects.all()
    return render(request, 'Formateur/formateur_list.html', {'formateurs': formateurs})

def formateur_detail(request, pk):
    formateur = get_object_or_404(Author, pk=pk)
    return render(request, 'Formateur/formateur_detail.html', {'formateur': formateur})

def formateur_delete(request, pk):
    formateur = get_object_or_404(Author, pk=pk)
    formateur.delete()
    return redirect('formateur_list')


def add_to_group(request, formateur_id):
    # Get the Formateur instance
    formateur = get_object_or_404(Author, pk=formateur_id)
    
    # Create a user account for the Formateur
    user = User.objects.create_user(username=formateur.name, email=formateur.email_author, password='0000')
    formateur.user = user
    formateur.save()
    # Add the user to the Formateur group
    formateur_group = Group.objects.get(name='Formateur')
    formateur_group.user_set.add(user)
    if user.groups.filter(name='Formateur').exists():
        messages.success(request,'Formateur are successfully Add')
        return redirect('formateur_list')
    else:
        # If user was not added to the group, you can handle the error accordingly
        return HttpResponseForbidden("Failed to add Formateur to Formateur group")


def add_course(request):
    if request.method == 'POST':
        # Assuming the user is authenticated
        formateur = request.user.author  # Retrieve the formateur associated with the current user
        
        course_form = CourseForm(request.POST, request.FILES)
        objectif_form = ObjectifForm(request.POST)
        lesson_form = LessonForm(request.POST)
        video_form = VideoForm(request.POST)

        if course_form.is_valid() and objectif_form.is_valid() and lesson_form.is_valid() and video_form.is_valid():
            course = course_form.save(commit=False)
            course.author = formateur  # Assign the current formateur to the course
            course.save()

            objectif = objectif_form.save(commit=False)
            objectif.course = course
            objectif.save()

            lesson = lesson_form.save(commit=False)
            lesson.course = course
            lesson.save()

            video = video_form.save(commit=False)
            video.course = course
            video.lesson = lesson
            video.save()

            return redirect('author_dashboard')  # Redirect to author dashboard after adding all related items
        else:
            print("didn't validate the form")
            print(course_form.errors)
            print(objectif_form.errors)
            print(lesson_form.errors)
            print(video_form.errors)
    else:
        course_form = CourseForm()
        objectif_form = ObjectifForm()
        lesson_form = LessonForm()
        video_form = VideoForm()

    return render(request, 'Formateur/add_course.html', {
        'course_form': course_form,
        'objectif_form': objectif_form,
        'lesson_form': lesson_form,
        'video_form': video_form,
    })
def author_dashboard(request):
    try:
        # Retrieve the Author instance associated with the current user
        author = Author.objects.get(user=request.user)
        print("Author:", author)  # Debugging print
        # Retrieve courses associated with the current author
        courses = Course.objects.filter(author=author)
        print("Courses:", courses)  # Debugging print
    except Author.DoesNotExist:
        # Handle the case where the current user does not have an associated Author instance
        courses = []
    return render(request, 'Formateur/dashboard.html', {'courses': courses})

from django.contrib import admin
from django.urls import path , include
from .import views , user_login
from django.conf import settings
from django.conf.urls.static import static
from .views import add_course, formateur_list, formateur_detail, formateur_delete , add_to_group



urlpatterns = [
    path('admin/', admin.site.urls),

    path('base',views.BASE,name='base'),
    path('',views.HOME , name='home'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('contact', views.CONTACT_US, name='contact_us'),
    path('about', views.ABOUT_US,name='about_us'),
    path('search',views.Search_course , name='search_course'),

    path('courses',views.SINGLE_COURSE, name='courses'),
    path('course/<slug:slug>',views.Course_details,name='course_details'),
    path('my-course',views.my_course, name='my-course'),
    path('course/watch-course/<slug:slug>',views.watch_course, name='watch-course'),
    
    path('accounts/register',user_login.REGISTER , name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin' , user_login.LOGIN , name='doLogin'),
    path('accounts/profile' , user_login.PROFILE , name='profile'),
    path('accounts/profile/update' , user_login.PROFILE_UPDATE, name='profile_update'),
    path('checkout/<slug:slug>', views.checkout , name='checkout'),
    path('complete/', views.paymentComplete , name='complete'),
    path('success/', views.paymentSuccess , name='success'),
    path('complete/', views.paymentComplete , name='complete'),

    path('category/<str:pk>', views.category_page , name='category_page'),
   
    
   
    path('logout/', views.logoutUser ,name='logout'),
    path('404',views.Page_not_found , name='404'),
    

    path('accounts/F_register',user_login.F_registre , name='F_register'),
   
    path('dashboard',views.author_dashboard , name='author_dashboard'),



    path('formateurs', formateur_list, name='formateur_list'),
    path('formateurs/<int:pk>/', formateur_detail, name='formateur_detail'),
    path('formateurs/<int:pk>/delete/', formateur_delete, name='formateur_delete'),
    path('formateurs/<int:formateur_id>/add_to_group/', add_to_group, name='add_to_group'),
    path('add_course', add_course, name='add_course'),

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
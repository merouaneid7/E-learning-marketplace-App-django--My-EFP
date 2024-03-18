from django.shortcuts import redirect , render
from django.contrib.auth.models import User
from django.contrib import messages
from App.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from App.form import AuthorForm
from App.models import Author

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email are Already Exists !')
           return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'Username are Already exists !')
           return redirect('register')
        
        # Check if password and confirm_password match
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match!')
            return redirect('register')
        
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request,'registration/register.html')


def LOGIN(request):
    if request.method == "POST" and 'btnsignin' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
    
    user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
    
    if user!=None:
            if 'remembreme' not in request.POST:
                 request.session.set_expiry(0)
            login(request,user)
            return redirect('home')
    else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')
        

def PROFILE(request):
     return render(request,'registration/profile.html')

def PROFILE_UPDATE(request):
      if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('profile')
     
     
def F_registre(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        name = request.POST.get('name')
        email_author = request.POST.get('email_author')
        phone_author = request.POST.get('phone_author')
        cni =  request.POST.get('cni')
        author_profile =  request.POST.get('author_profile')
        about_author =  request.POST.get('about_author')
        ville= request.POST.get('ville')

        
        if form.is_valid():
            form.save()
            messages.success(request, ' Succsesfull')  # Success message
            return redirect('F_register')
        else:
            messages.error(request, 'remplie tout les champs')  # Error message for missing fields
    else:
        form = AuthorForm()
    
    return render(request, 'Formateur/form_registre.html', {'form': form})
from django.shortcuts import render,redirect
from userauths.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User


# Create your views here.
def registerview(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save() # django checks for signal # post_save # and creates account for new user
            username = form.cleaned_data.get('username')
            messages.success(request, f"Hey {username} your account is created sucessfully.")
           # new_user = authenticate(username=form.cleaned_data['username'])
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password = form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
        
    if request.user.is_authenticated:
        messages.warning(request, f"you are already logged in.")
        return redirect("core:index")
    else:
        form = UserRegistrationForm()

    context = {
        "form":form
    }
    return render(request, "userauths/sign-up.html", context)


def loginview(request):
    if request.method == "POST":
        ##here email is geting as username beacuse of field overiding.
        email = request.POST.get('email') 
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None: # if there is a user
                login(request, user)
                messages.success(request, "you are loggedin")
                return redirect("account:account")
                # return redirect("core:index")
            else:
                messages.warning(request, "username or password doesnt match.")
                return redirect("userauths:login")
        except:
            messages.warning(request, "user does not exist.")
            pass
    if request.user.is_authenticated:
        messages.warning(request, "you have already loggedin")
        return redirect('account:account')

    
    return render(request, "userauths/sign-in.html")


def logoutview(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect("userauths:sign-up")
from django.shortcuts import render,redirect
from django.views import View
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login
from utility.views import render_with_messages
from django.contrib.auth import logout

class SignUp(View):
    def get(self,request):

        return render(request,'signup.html')
    def post(self,request):
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        password1 = request.POST.get('password1', '').strip()
        if '@' not in email:
            return render_with_messages(request, 'signup.html', error_message="Enter valid Email")
        
        if not ( all(i.isdigit() for i in phone_number) and len(phone_number)==10):
            return render_with_messages(request, 'signup.html', error_message="Enter Valid Phone number")
        
        if password and password1 and password != password1:
            return render_with_messages(request, 'signup.html', error_message="Passwords do not match")

        if CustomUser.objects.filter(username=username).exists():
            return render_with_messages(request, 'signup.html', error_message="Username already exists")
        
        if CustomUser.objects.filter(email=email).exists():
            return render_with_messages(request, 'signup.html', error_message="Email already exists")

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render_with_messages(request, 'signup.html', error_message= "Phone number already exists")
        
        user = CustomUser.objects.create(username=username,email=email,phone_number=phone_number)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')




class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('/')  # Redirect to a home page or any other page
        else:
           return render_with_messages(request, 'login.html', error_message= "Invalid email or password")
       
def Logout(request):
    logout(request)  # Logs out the user
    return redirect('login')
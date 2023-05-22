from django.shortcuts import render
from django.http import HttpResponseRedirect
from Accounts.forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as authlogin
from django.contrib.auth.models import User
from Accounts.models import Profile
import json



# Create your views here.

def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user     = authenticate(request,username=username,password=password)

		if user is None:
			return render(request,'registration/login.html',{'error':'Invalid Username or Password'})
		
		authlogin(request,user)
		name    = User.objects.get(username= username)
		red     = HttpResponseRedirect('homepage/')
		return red
	return render(request,'registration/login.html')

def logout_page(request):
	return render(request=request,template_name ='registration/logout.html' )

def sign_up(request):
	form = SignupForm()
	mydict = {'form':form}
	print(mydict)
	if request.method == 'POST':
		if len(request.POST['phone_number']) != 10:
			print('no not valid')

		form1 = SignupForm(request.POST)
		print(form)
		print(type(form))
		if form1.is_valid():
			user = form1.save()
			user.set_password(user.password)
			user.save()
			profile=Profile.objects.create(user=user,phone_number=request.POST['phone_number'])
			profile.save()

		return render(request,'registration/login.html')

	return render(request = request, template_name = 'registration/signup.html' , context = mydict)

@login_required
def change_password(request):
	if request.method == "POST":
		user_name = request.POST.get('username')
		old_pwd   = request.POST.get('old_pwd')
		new_pwd   = request.POST.get('new_pwd')
		conf_pwd  = request.POST.get('conf_pwd')
		
		try:
			user = authenticate(request,username=user_name,password=old_pwd)
			if user is None:
				return render(request,'registration/change_password.html',{'error':'Invalid Username or Old password'})
			if new_pwd != conf_pwd:
				return render(request,'registration/change_password.html',{'error':'Give confirm password same as new password'})
			
			user.password = new_pwd
			user.save()
			user.set_password(user.password)
			user.save()
			logout(request)
			return render(request,'registration/login.html',context = {'error':'Password Successfuly changed, login using new password here!'})

		except Exception as e:
			return render(request,'registration/change_password.html',{'error':'Username is not found, Enter currect Username'})

	return render(request,'registration/change_password.html')


@login_required
def home_page(request):
	return render(request=request,template_name ='registration/homepage.html')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
	if request.method == "POST":
		return login_view(request)

	else:
		if request.user.is_authenticated():
			return render(request, 'pokerapp/home.html')
		return render(request, 'reg/home.html')


# Create your views here.
def login_view(request):
	if request.method == "POST":
		username, password = request.POST.get('username'), request.POST.get('password')
		if username and password:
			if User.objects.filter(username=username).exists():
				u = authenticate(username=username, password = password)
				if u is not None and not u.is_anonymous():
					login(request, u)
					return redirect('home')
		return render(request, 'reg/home.html', {'error':'There was an error logging in the user, please try again. '})
	else:
		return redirect('home')

def register_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']
		email = request.POST['email']
		if User.objects.filter(email = email).exists() \
		or User.objects.filter(username = username).exists() or not password == password2:
			return render(request, 'reg/register.html', {'error':'Username or email already used, or passwords do not match'})
		u = User.objects.create_user(username = username, email=email, password = password)
		user = authenticate( username=username,password=password)
		login(request, user)
		return redirect('home')
	else:
		return render(request, 'reg/register.html')


def logout_view(request):
	logout(request)
	return redirect('home')
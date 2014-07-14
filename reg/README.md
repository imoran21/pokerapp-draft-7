reg
===

This is an app for simple django registration handling.  


INSTRUCTIONS

1) download this repo

1) Create a django project 

django-admin.py startproject myproject . 
2) Copy and paste the 'reg' folder into the same directory as manage.py 

3) open myproject/settings.py 

-add 'reg' to installed apps 


4) open myproject/urls.py 

-add this to urls 

url(r'^reg/', include('reg.urls')), 

if you want the homepage to be the login page, add this line

url(r'^$', 'reg.views.home', name='home'),


if not then you can put your custom home url or include a different app 


5) sync database 

python manage.py sycncdb


now when you do python manage.py runserver and go to the /reg url, you should see the login page, with a link to register




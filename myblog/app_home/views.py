from django.shortcuts import render

# Create your views here.

def get_html_home(req):
    return render(req, "app_home/home.html")
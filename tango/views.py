from django.http import HttpResponse
from django.shortcuts import render
from tango.models import Category


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':category_list}
    return render(request,'tango/index.html',context=context_dict)
    # context_dict = {'message':'This is home page'}
    # return render(request,'tango/index.html',context=context_dict)
    # return HttpResponse("Hello there <br> <a href ='/tango/about'>About</a> ")


def about(request):
    context_dict = {'aboutmessage':'This tutorial has been put together by Aditi'}
    return render(request,'tango/about.html',context=context_dict)
    # return HttpResponse("this is about page <br> <a href = '/tango'>Home</a>")

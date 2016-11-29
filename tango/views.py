from django.http import HttpResponse
from django.shortcuts import render
from tango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    views = Category.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'views':views}
    return render(request,'tango/index.html',context=context_dict)
    # context_dict = {'message':'This is home page'}
    # return render(request,'tango/index.html',context=context_dict)
    # return HttpResponse("Hello there <br> <a href ='/tango/about'>About</a> ")


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None


    return render(request, 'tango/category.html', context=context_dict)


def about(request):
    context_dict = {'aboutmessage':'This tutorial has been put together by Aditi'}
    return render(request,'tango/about.html',context=context_dict)
    # return HttpResponse("this is about page <br> <a href = '/tango'>Home</a>")

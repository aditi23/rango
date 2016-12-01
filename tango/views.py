from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from tango.models import Page, Category
from tango.forms import UserRegisterForm,UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# def index(request):
#     category_list = Category.objects.order_by('-likes')[:5]
#     views = Category.objects.order_by('-views')[:5]
#     context_dict = {'categories':category_list,'views':views}
#     return render(request,'tango/index.html',context=context_dict)
#     # context_dict = {'message':'This is home page'}
#     # return render(request,'tango/index.html',context=context_dict)
#     # return HttpResponse("Hello there <br> <a href ='/tango/about'>About</a> ")


# class IndexView(generic.ListView):
#     template_name = 'tango/index.html'
#     model = Category
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super(Category, self).get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['categories'] = Category.objects.order_by('-likes')[:5]
#         context['views'] = Category.objects.order_by('-views')[:5]
#         return context


class IndexView(LoginRequiredMixin,generic.ListView):
    login_url = '/tango/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'tango/index.html'
    context_object_name = 'categories'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.order_by('-likes')[:5],
            'views': Category.objects.order_by('-views')[:5],
        })
        return context

    # def get_queryset(self):
    #     return Category.objects.order_by('-likes')[:5]


class ShowCategoryView(generic.ListView):
    template_name = 'tango/category.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        print('hello the kwargs are')
        print()
        try:
            print(kwargs)
            context = super(ShowCategoryView, self).get_context_data(**kwargs)
            category = Category.objects.get(slug=self.kwargs['slug'])
            pages = Page.objects.filter(category=category)
            context.update({
                'categories': category,
                'pages': pages,
            })
        except Category.DoesNotExist:
            context = super(ShowCategoryView, self).get_context_data(**kwargs)
            context.update({
                'categories': None,
                'pages': None,
            })
        return context


# def show_category(request, category_name_slug):
#     context_dict = {}
#
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#         pages = Page.objects.filter(category=category)
#         context_dict['pages'] = pages
#         context_dict['category'] = category
#     except Category.DoesNotExist:
#         context_dict['pages'] = None
#         context_dict['category'] = None
#
#     return render(request, 'tango/category.html', context=context_dict)


def about(request):
    context_dict = {'aboutmessage': 'This tutorial has been put together by Aditi'}
    return render(request, 'tango/about.html', context=context_dict)
    # return HttpResponse("this is about page <br> <a href = '/tango'>Home</a>")


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'tango/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/tango')

        return render(request, self.template_name, {'form': form})


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'tango/login.html'
    success_url = '/tango'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
            # return HttpResponseRedirect(self,'/tango',user)

        return render(self.request, self.template_name, {'form': form})

    def form_invalid(self, form):
        print('invalid')
        return render(self.request, self.template_name, {'form': form})


class LogoutView(RedirectView):
    url = '/tango/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request,*args,**kwargs)





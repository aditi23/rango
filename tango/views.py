from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from tango.models import Page, Category, UserProfile
from tango.forms import UserRegisterForm,UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


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
            'views': Category.objects.order_by('views')[:5],
        })
        return context


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


class ProfileView(generic.DetailView):

    template_name = 'tango/profile.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        print('hello the kwargs are')
        print()
        try:
            # print(kwargs['object'].id)
            context = super(ProfileView, self).get_context_data(**kwargs)
            # profile = UserProfile.objects.get(kwargs['object'].id)

            profile = self.request.user.userprofile

            context.update({
                'profileDetails': profile,
            })
        except UserProfile.DoesNotExist:
            context = super(ProfileView, self).get_context_data(**kwargs)
            context.update({
                'profileDetails': None,
            })
        return context


def about(request):
    context_dict = {'aboutmessage': 'This tutorial has been put together by Aditi'}
    return render(request, 'tango/about.html', context=context_dict)


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'tango/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

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
                    return redirect(reverse('index'))

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
            # return redirect(self.success_url)
            return redirect(reverse('index'))
        return self.form_invalid(form)

    def form_invalid(self, form):
        print(
            form.errors
        )
        return super(UserLoginView,self).form_invalid(form)


class LogoutView(RedirectView):
    url = '/tango/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request,*args,**kwargs)


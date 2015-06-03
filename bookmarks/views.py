from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import logout
from bookmarks.forms import *

def main_page(request):
    template = 'main_page.html'
    variables = {
        'head_title': 'Django Bookmarks',
        'page_title': 'Welcome to Django Bookmarks',
        'page_body': 'Where you can store and share bookmarks!'
    }

    return render(request, template, variables)

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested user not found.')

    bookmarks = user.bookmark_set.all()

    template = get_template('user_page.html')

    variables = Context({
        'username': username,
        'bookmarks': bookmarks
    })

    output = template.render(variables)

    return HttpResponse(output)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            return render(request, 'registration/register_success.html')

    else:
        form = RegistrationForm()

    variables = { 'form': form }

    return render(request, 'registration/register.html', variables)
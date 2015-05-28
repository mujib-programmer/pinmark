from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

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
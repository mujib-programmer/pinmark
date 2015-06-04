from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from bookmarks.forms import *
from bookmarks.models import *

def main_page(request):
    template = 'main_page.html'
    variables = {
        'head_title': 'Django Bookmarks',
        'page_title': 'Welcome to Django Bookmarks',
        'page_body': 'Where you can store and share bookmarks!'
    }

    return render(request, template, variables)

def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')

    variables = Context({
        'username': username,
        'bookmarks': bookmarks,
        'show_tags': True
    })

    return render(request, 'user_page.html', variables)

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

@login_required
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)

        if form.is_valid():
            # create or get link.
            link, dummy = Link.objects.get_or_create(
                url=form.cleaned_data.get('url')
            )

            # create or get bookmark
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                link=link
            )

            # update bookmark title
            bookmark.title = form.cleaned_data.get('title')

            # if the bookmark is being updated, clear old tag list.
            if not created:
                bookmark.tag_set.clear()

            # create new tag list
            tag_names = form.cleaned_data.get('tags').split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                bookmark.tag_set.add(tag)

            # save bookmark to database
            bookmark.save()

            return HttpResponseRedirect('/user/%s/' % request.user.username)

        else:
            print(form.errors)

    else:
        form = BookmarkSaveForm()

    variables = {'form': form}

    return render(request, 'bookmark_save.html', variables)
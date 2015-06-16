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

def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = {
        'bookmarks' : bookmarks,
        'tag_name' : tag_name,
        'show_tags' : True,
        'show_user' : True
    }

    return render(request, 'tag_page.html', variables)

def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')

    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].bookmarks.count()

    for tag in tags:
        tag.count = tag.bookmarks.count()

        if tag.count < min_count:
            min_count = tag.count

        if tag.count > max_count:
            max_count = tag.count

    # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)

    if range == 0.0:
        range = 1.0

    # Calculate tag weights.
    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )

    variables = {
        'tags' : tags
    }

    return render(request, 'tag_cloud_page.html', variables)

def search_page(request):
    form = SearchForm()
    bookmarks = []
    show_results = False

    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()

        if query:
            form = SearchForm({'query' : query})
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]

    variables = {
        'form' : form,
        'bookmarks' : bookmarks,
        'show_results' : show_results,
        'show_tags' : True,
        'show_user' : True
    }

    return render(request, 'search.html', variables)

from django.shortcuts import render

def main_page(request):
    template = 'main_page.html'
    variables = {
        'head_title': 'Django Bookmarks',
        'page_title': 'Welcome to Django Bookmarks',
        'page_body': 'Where you can store and share bookmarks!'
    }

    return render(request, template, variables)
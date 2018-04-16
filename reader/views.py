from django.shortcuts import render


def comic_reader(request, *args, **kwargs):
    return render(request, template_name='reader/index.html')

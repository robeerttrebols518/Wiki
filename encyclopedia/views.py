from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

from . import util
markdow = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class Post(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': '3', 'style': 'resize:none; width: 40%'}))
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3' }))

class Search(forms.Form):
    news = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Search'}))

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

def index(request):
    entries = util.list_entries()
    searching = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            news = form.cleaned_data["news"]
            for i in entries:
                if news in entries:
                    page = util.get_entry(news)
                    page_converted = markdow.convert(page)
                    context = {
                        'page': page_converted,
                        'title': news,
                        'form': Search()
                    }
                    return render(request, "encyclopedia/entryPage.html", context)
                if news.lower() in i.lower():
                    searching.append(i)
                    context = {
                        'searching': searching,
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)
        else:
            return request(request, "encyclopedia/index.html", {"form":form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
            })

def entryPage(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdow.convert(page)
        context = {
            'page': page_converted,
            'title': title,
            'form': Search()
        }
        return render(request, "encyclopedia/entryPage.html", context)
    else:
        return render(request, "encyclopedia/errorPage.html", {"message": "Requested page cannot be found.", "form":Search()})


def createPage(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/errorPage.html", {"form": Search(), "message": "The page you are trying to create is exists"})
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdow.convert(page)
                context = {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                }
                return render(request, "encyclopedia/entryPage.html", context)
    else:
        return render(request, "encyclopedia/createPage.html", {"form": Search(), "post": Post()})

def editPage(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        context = {
            'form': Search(),
            'editPage': Edit(initial={'textarea': page}),
            'title': title
        }
        return render(request, "encyclopedia/editPage.html", context)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_converted = markdow.convert(page)
            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }
            return render(request, "encyclopedia/entryPage.html", context)

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdow.convert(page)
        context = {
            'form': Search(),
            'page': page_converted,
            'title': page_random
        }
        return render(request, "encyclopedia/entryPage.html", context)

            

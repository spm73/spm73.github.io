from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse #, HttpResponseRedirect
from django.urls import reverse

from . import util
from markdown2 import Markdown
from random import choice


def index(request) -> HttpResponse:
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title: str) -> HttpResponse:
    content = util.get_entry(title)
    if content is None:
        return render(request, 'encyclopedia/not_found.html', {
            "title": title
        })
    
    return render(request, 'encyclopedia/entry.html', {
        "title": title,
        "md_content": Markdown().convert(content)
    })


def new(request) -> HttpResponse:
    if request.method != 'POST':
        return render(request, 'encyclopedia/new.html')
    
    form = request.POST
    if not form["title"] and not form["content"]:
        return redirect(reverse("encyclopedia:new"))
    elif form["title"] in util.list_entries():
        return render(request, "encyclopedia/new_error.html", {
            "entry": form["title"]
        })
    
    util.save_entry(form["title"], form["content"])
    
    return redirect(reverse("encyclopedia:entry", args=[form["title"]]))


def random_page(request) -> HttpResponse:
    # return HttpResponseRedirect(reverse("encyclopedia:entry", args=[choice(util.list_entries())]))
    return redirect(reverse("encyclopedia:entry", args=[choice(util.list_entries())]))


def search(request) -> HttpResponse:
    if request.method != "POST":
        return redirect(reverse("encyclopedia:index"))
        
    entry_title = request.POST["q"]
    
    if entry_title in util.list_entries():
        return redirect(reverse("encyclopedia:entry", args=[entry_title]))
    elif not entry_title:
        return redirect(reverse("encyclopedia:index"))
    else:
        return render(request, "encyclopedia/search_error.html", {
            "entry_title": entry_title,
            "entries": [entry for entry in util.list_entries() if entry_title in entry]
        })
        

def edit(request, entry_name: str) -> HttpResponse:
    if request.method != "POST":
        return render(request, 'encyclopedia/edit.html', {
            "old_content": util.get_entry(entry_name),
            "title": entry_name
        })
    
    form = request.POST
    util.save_entry(entry_name, form["new_content"])
    
    return redirect(reverse('encyclopedia:entry', kwargs={"title": entry_name}))
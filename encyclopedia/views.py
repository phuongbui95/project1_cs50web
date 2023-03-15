from django.shortcuts import render, redirect
from . import util

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "get_entry": util.get_entry(title),
        "title": title,
        "entries": entries
    })

def search(request):
    # Check if method is GET
    if request.method == "GET":
        query = request.GET.get("q") # get the search query
        if(query in entries):
            return redirect("encyclopedia:entry", title=query) # redirect to a url tag with 'title' as a parameter
        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "q": query
        })
    
    return render(request, "encyclopedia/search.html", {
        "entries": entries,
        "q": None
    })            


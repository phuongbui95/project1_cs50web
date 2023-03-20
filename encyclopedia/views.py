from django.shortcuts import render, redirect
from . import util
import markdown2

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    content = markdown2.markdown(str(util.get_entry(title)))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "get_entry": util.get_entry(title),
        "content": content,
        "entries": entries
    })

def search(request):
    # Check if method is GET
    if request.method == "GET":
        query = request.GET.get("q") # get the search query
        # if the searched query is found in util.list_entries()
        if(query in entries):
             # redirect to a url tag with 'title' as a parameter
            return redirect("encyclopedia:entry", title=query)
        # if not matched any queries in list_entries, redirect to search.html
        else:
            results = []
            for entry in entries:
                if query in entry.lower():
                    results.append(entry)
            
            # if a list of "results" is empty, list the default entries
            if not results: 
                # results = entries
                return redirect("encyclopedia:entry", title=query)
            return render(request, "encyclopedia/search.html", {
                "q": query,
                "entries": results
            })
            
            
    # if not GET any queries, present the search.html
    return render(request, "encyclopedia/search.html", {
        "q": None,
        "entries": entries
        
    })            

def new(request):
    return render(request, "encyclopedia/new.html")
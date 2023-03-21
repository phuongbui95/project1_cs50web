from django import forms
from django.shortcuts import render, redirect

from . import util
import markdown2

# class to store content of New Pages
class NewPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

# class to edit content of Entry Pages
class EditPageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

# index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry's page
def entry(request, title):
    content = markdown2.markdown(str(util.get_entry(title)))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "get_entry": util.get_entry(title),
        "content": content,
        "entries": util.list_entries()
    })

# redirect to Search page if entry is invalid
def search(request):
    # Check if method is GET
    if request.method == "GET":
        query = request.GET.get("q") # get the search query
        # if the searched query is found in util.list_entries()
        if(query in util.list_entries()):
             # redirect to a url tag with 'title' as a parameter
            return redirect("encyclopedia:entry", title=query)
        # if not matched any queries in list_entries, redirect to search.html
        else:
            results = []
            for entry in util.list_entries():
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
        "entries": util.list_entries()
        
    })            

# New page
def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already exists!",
                    "title": title
                    })
            else:
                util.save_entry(title, content)
                return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
                })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewPageForm()
            })
    
# Edit page
def edit(request, title):
    if request.method == "POST":
        # If the new update is saved, redirect to new entry's page
        form = EditPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)
    else:
        # pre-populated with the existing Markdown content of the page
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "content": util.get_entry(title)
        })
    
# delete page
def delete(request, title):
    return render(request, "encyclopedia/delete.html", {
        "title": title,
        "message": util.delete_entry(title)
    })
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def home(req):
    return render_to_response('search/home.html')

def search(req):
    q = req.GET.get('q', None)
    if not q or q.isspace():
        return HttpResponseRedirect('/')
    return render_to_response('search/results.html', {'q': q})

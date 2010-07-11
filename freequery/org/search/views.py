from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from freequery.client import FreequeryClient

def home(req):
    return render_to_response('search/home.html')

def search(req):
    q = req.GET.get('q', None)
    spec = req.GET.get('spec', 'a')
    if not q or q.isspace():
        return HttpResponseRedirect('/')
    fq = FreequeryClient(spec)
    docs = fq.query(q)
    return render_to_response('search/results.html', {'q': q, 'docs': docs})

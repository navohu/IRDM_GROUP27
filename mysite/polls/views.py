from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import Result
from django.views import generic

def search(request):
    if request.POST:
        print request.POST['term']
        # return render_to_response('polls/index.html')
    else:
        return render_to_response('polls/index.html')

def results(request):
    results = Result.objects.all()
    print results
    context = {'result_list': results}
    return render(request, 'polls/index.html', context)
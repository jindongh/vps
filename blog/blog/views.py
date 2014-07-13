from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
 
def home(request):
    #return render_to_response('home.html')
    return HttpResponseRedirect("/weblog/") 


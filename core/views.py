from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# def burito(request):
#     return render(request, 'core/index.html')

def sample(request):
    return render(request, 'core/index.html')



from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world.")


def detail(request, question_id):
    return HttpResponse(f"You're lookint {question_id}")

def results(request, question_id):
    return HttpResponse(f"You're looking at the result of question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}")
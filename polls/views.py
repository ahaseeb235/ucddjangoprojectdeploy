from django.http import HttpResponse
from .models import Question
from django.shortcuts import get_object_or_404, render


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/home.html", context)

def about(request):
    return render(request, 'polls/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'polls/contact.html', {'title': 'contact'})

# to get 404 error
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



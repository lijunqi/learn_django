from django.shortcuts import get_object_or_404, render
from django.http import Http404

# Create your views here.

from django.http import HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # The context is a dictionary mapping template variable names to Python objects.
    context = { 'latest_question_list': latest_question_list, }

    # The render() function takes the request object as its first argument,
    # a template name as its second argument and a dictionary as its optional
    # third argument. It returns an HttpResponse object of the given template
    # rendered with the given context.
    return render(request, 'polls/index.html', context)

# Add a few more views
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist...")

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're lokking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # The context is a dictionary mapping template variable names to Python objects.
    context = { 'latest_question_list': latest_question_list, }

    #*  The render() function takes the request object as its first argument,
    #*  a template name as its second argument and a dictionary as its optional
    #*  third argument. It returns an HttpResponse object of the given template
    #*  rendered with the given context.
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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


#####################################
# Use generic views
#####################################
#*  The ListView generic view uses a default template called
#*  <app name>/<model name>_list.html;
#*  We use template_name to tell ListView to use
#*  our existing "polls/index.html" template.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    #*  The automatically generated context variable is "question_list".
    #*  To override this we provide the context_object_name attribute,
    #*  specifying that we want to use "latest_question_list" instead.
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


#*  By default, the DetailView generic view uses a template called
#*  <app name>/<model name>_detail.html.
#*  In our case, it would use the template "polls/question_detail.html".
#*  The template_name attribute is used to tell Django to use
#*  a specific template name instead of the autogenerated default template name.
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    #! Avoiding race conditions using F()
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #*  Always return an HttpResponseRedirect after successfully dealing
        #*  with POST data. This prevents data from being posted twice if a
        #*  user hits the Back button.
        #*  reverse() give the name of the view that we want to pass control to
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
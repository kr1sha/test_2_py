from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Question, Choice


class IndexView(ListView):
    #latest_question_list = Question.objects.order_by('-published_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #template = loader.get_template('test_app/index.html')
    #context = {'latest_question_list': latest_question_list}
    #return HttpResponse(template.render(context, request))

    #return render(request, 'test_app/index.html', context)

    template_name = 'test_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-published_date')[:5]


#def detail(request, question_id):
    #try:
        #question = Question.objects.get(pk=question_id)
        #context = {'question': question}
    #except Question.DoesNotExist:
        #raise Http404('Question does not exist')

    #question = get_object_or_404(Question, pk=question_id)
    #context = {'question': question}

    #return render(request, 'test_app/detail.html', context)

class DetailView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'test_app/detail.html'


#def result(request, question_id):
#    question = get_object_or_404(Question, id=question_id)
#    return render(request, "test_app/results.html", {'question': question})

class ResultView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'test_app/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    try:
        selected_choices = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'test_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })

    else:
        selected_choices.votes += 1
        selected_choices.save()
        return HttpResponseRedirect(reverse('test:question_results', args=(question.id, )))

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


def get_published_question():
    """
    get_published_question will return the list of published question id
    """
    all_questions = Question.objects.all()
    available_questions_id = []
    for question in all_questions:
        if Question.is_published(question):
            available_questions_id += [question.id]
    return available_questions_id


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(id__in=get_published_question()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


    def get(self, request, *args, **kwargs):
        """
        get will direct the user to the Question if it's currently available.
        It will redirect to the polls page if the question is not available as it's not published or can't be voted.
        """
        try:
            self.object = self.get_object() # try to get the object
        except Http404:
            # In the case the poll page lead to an 404 which means the poll does not available do the following

            messages.error(request, "The poll is not available.")
            # Show the error message that the poll is unavailable

            return redirect('polls:index')
            # redirect to polls page
        else:
            if not self.object.is_published():
                messages.error(request, "The poll is not published yet.")
                return redirect('polls:index')
            elif not self.object.can_vote():
                messages.error(request, "You are currently not allowed to vote in this poll.")
            else:
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)


        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

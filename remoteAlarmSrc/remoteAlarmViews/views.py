# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from remoteAlarm.models import Poll
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from remoteAlarm.models import Choice
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'remoteAlarm/index.html'
    context_object_name = 'latest_poll_list'
    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'remoteAlarm/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'remoteAlarm/results.html'

# ...
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'remoteAlarm/detail.html', {
            'remoteAlarm': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('remoteAlarm:results', args=(p.id,)))
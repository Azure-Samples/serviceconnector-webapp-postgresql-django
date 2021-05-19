from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import psycopg2
import requests
import os

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        questions = list(Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5])
        # questions = self.fetch_data_msi()
        return questions

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

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













        

    # def fetch_data_msi(self):
    #     resource_uri = 'https://ossrdbms-aad.database.windows.net'
    #     identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
    #     identity_header = os.environ["IDENTITY_HEADER"]
    #     client_id = os.environ["Cupertino_DBforPostgreSQL_UserAssignedIdentityClientId"]
    #     token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01&client_id={client_id}"
    #     head_msi = {'X-IDENTITY-HEADER':identity_header}

    #     resp = requests.get(token_auth_uri, headers=head_msi)
    #     access_token = resp.json()['access_token']
    #     questions = []

    #     host = os.environ["Cupertino_DBforPostgreSQL_TargetServiceEndpoint"]
    #     dbname = os.environ["Cupertino_DBforPostgreSQL_SubResourceName"]
    #     user = os.environ["Cupertino_DBforPostgreSQL_Identity"]
    #     sslmode = "require"
    #     conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, access_token, sslmode)
    #     conn = psycopg2.connect(conn_string) 
    #     print("Connection established")

    #     cursor = conn.cursor()

    #     # Fetch all rows from table
    #     cursor.execute("SELECT id, question_text FROM polls_question;")
    #     rows = cursor.fetchall()

    #     # # Print all rows
    #     for row in rows:
    #         question = Question()
    #         question.id = int(row[0])
    #         question.question_text = str(row[1])
    #         questions.append(question)

    #     # Cleanup
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    #     question = Question()
    #     question.id = 1
    #     question.question_text = "msi sample"
    #     questions.append(question)

    #     return questions





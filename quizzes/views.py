from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin, ProcessFormView

from .forms import QuestionForm
from .models import Question, Quiz


class QuizzesListView(ListView):

    queryset = Quiz.objects.filter(is_active=True)
    paginate_by = 5


class QuestionView(DetailView, ProcessFormView, FormMixin):

    form_class = QuestionForm
    template_name = 'quizzes/quiz_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz_id=self.pk)

    def get_object(self):
        user = self.request.user
        user_answers = user.answers.filter(question__quiz_id=self.pk)
        qs = self.get_queryset().exclude(answers__in=user_answers)
        return qs.first()

    def get_current_number(self):
        pks = list(self.get_queryset().values_list('pk', flat=True))
        return {
            'questions_count': len(pks),
            'question_number': pks.index(self.object.pk) + 1
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_current_number())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        answers = form.cleaned_data['answers']
        self.request.user.answers.add(*answers)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['answers'] = self.object.answers
        return kwargs

    def get_success_url(self):
        return reverse('quizzes_detail', kwargs={'pk': self.pk})

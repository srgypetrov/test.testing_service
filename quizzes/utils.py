from .models import Question


def get_user_current_question(user, quiz_id):
    user_answers = user.answers.filter(question__quiz_id=quiz_id)
    qs = Question.objects.filter(quiz_id=quiz_id)
    qs = qs.exclude(answers__in=user_answers)
    return qs.first()


def get_question_number(quiz_id, question_id):
    qs = Question.objects.filter(quiz_id=quiz_id)
    pks = list(qs.values_list('pk', flat=True))
    return {
        'questions_count': len(pks),
        'question_number': pks.index(question_id) + 1
    }
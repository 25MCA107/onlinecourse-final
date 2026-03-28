from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Question, Choice, Submission


def index(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list_bootstrap.html', {'course_list': courses})


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    try:
        Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse('onlinecourse:detail', args=(course.id,)))


@login_required
def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []
    for key in request.POST:
        if key.startswith('choice'):
            choice_ids = request.POST.getlist(key)
            for choice_id in choice_ids:
                selected_choices.append(int(choice_id))

    submission.choices.set(selected_choices)
    submission.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    questions = course.question_set.all()

    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'total_score': total_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

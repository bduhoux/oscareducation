# encoding: utf-8

from django.db import transaction
from django.http import Http404, HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from examinations.models import *
from examinations.models import TestExercice, List_question
from models import *
from promotions.utils import user_is_professor


@user_is_professor
def generator(request, lesson_id, skill_id, test_id):
    form = ArithmeticPolynomialSecondDegree.make_form(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dom = form.cleaned_data['domain']
            image = form.cleaned_data['image']
            range = [int(form.cleaned_data['range_from']), int(form.cleaned_data['range_to'])]
            problem_type = "Arithmetic_Polynomial_Second_degree"
            data = {'problem': problem_type, 'image': image, 'domain': dom,
                    'range': range}
            problem = ProblemGenerator.factory(json.dumps(data))
            exercise = problem.get_context()
            new_test_exercise = TestExercice()
            new_test_exercise.skill_id = skill_id
            new_test_exercise.test_id = test_id
            with transaction.atomic():
                new_test_exercise.added_by = request.user
                new_test_exercise.exercice = exercise
                new_test_exercise.save()
            return render(request, "questions_factory/questions_list.haml",
                          {'questions': problem.gen_questions(5), 'new_test_exercise': new_test_exercise,
                           'test_id': test_id, 'lesson_id': lesson_id})
    return render(request, "questions_factory/settings_problems.haml", {'form': form})


def generator_submit(request, lesson_id, skill_id, test_id):
    if request.method == "POST":
        test_exercise = get_object_or_404(TestExercice, pk=int(request.POST["exercise_id"]))
        question_desc = request.POST["question_description"]
        question_source = request.POST["question_source"]
        question_answer = (request.POST["question_answer"])
        with transaction.atomic():
            question = Question(description=question_desc, answer=question_answer, source=question_source)
            question.save()
        with transaction.atomic():
            link = List_question.objects.create(
                context_id=test_exercise.exercice.id,
                   question_id=question.id,
            )
            link.save()
        return JsonResponse({'msg': 'La question a été ajoutée au test'})
    else:
        return HttpResponseNotFound('<h1>No matches the given query.</h1>')

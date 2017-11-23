# encoding: utf-8

from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader

from models import *
from models.problem_form import GeneratorChoiceForm
from promotions.utils import user_is_professor


def get_form(generator_name, request):
    form = None
    if generator_name == "ArithmeticProblem":
        form = ArithmeticPolynomialSecondDegree.make_form(request.POST or None)
    elif generator_name == "SimpleInterestProblem":
        form = SimpleInterestProblem.make_form(request.POST or None)
    elif generator_name == "StatisticsProblem":
        form = StatisticsProblem.make_form(request.POST or None)
    elif generator_name == "VolumeProblem":
        form = VolumeProblem.make_form(request.POST or None)
    return form


@user_is_professor
def generator(request, lesson_id, skill_id, test_id):
    form = GeneratorChoiceForm(None)
    valid = True
    if request.POST:
        form = get_form(request.POST["generator_name"], request)
        if not form:
            return HttpResponseNotFound('<h1>Erreur 404 : cannot generate this name of problem</h1>')
        if form.is_valid():
            problem = ProblemGenerator.factory(form.cleaned_data)
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
        else:
            valid = False
    return render(request, "questions_factory/settings_problems.haml", {'form': form, 'valid': valid})


@user_is_professor
def generator_choice(request, lesson_id, skill_id, test_id, generator_name):
    """Return partial html content"""
    form = get_form(generator_name, request)
    if not form:
        return HttpResponseNotFound('<h1>Erreur 404 : cannot generate this name of problem</h1>')
    t = loader.get_template("questions_factory/_generator_form.haml")
    c = {'generator_name': generator_name, 'form': form}
    return HttpResponse(t.render(c, request))


@user_is_professor
def generator_submit(request, lesson_id, skill_id, test_id):
    if request.POST:
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
        return HttpResponseNotFound('<h1>Erreur 404</h1>')

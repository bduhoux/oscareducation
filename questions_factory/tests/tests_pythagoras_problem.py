# coding=utf-8
from django.test import TestCase
from examinations.models import *
from questions_factory.models import PythagorasProblem, ProblemGenerator
import math


class ResultTest(TestCase):
    def test_pythagoras_result(self):
        problem = create_problem()
        self.assertTrue(problem.get_sol() == math.sqrt(math.pow(problem.figure[0][1],2) + math.pow(problem.figure[1][1],2)))


class GeneratingQuestionsTests(TestCase):
    # FIXME 
    def TOFIX_test_pythagoras_generation(self):
        problem = create_problem()
        questions = problem.gen_questions(5)
        self.assertTrue(isinstance(problem.get_context(), Context))
        for question in questions:
            self.assertTrue(isinstance(question, Question))
            self.assertTrue(question.description is not None)


class InstanceTests(TestCase):
    def test_generator(self):
        problem = create_problem()
        self.assertTrue(isinstance(problem, PythagorasProblem))

    def test_raw_instance(self):
        problem = PythagorasProblem(4, 14)
        self.assertTrue(isinstance(problem, PythagorasProblem))

    def test_wrong_values(self):
        with self.assertRaises(ValueError):
            PythagorasProblem("yolo", 3)


def create_problem(range_from=1, range_to=20):
    values = {"problem": "Pythgoras_Problem"}
    values["generator_name"] = "PythagorasProblem"
    values["range_from"] = range_from
    values["range_to"] = range_to
    problem = ProblemGenerator.factory(values)
    return problem
# coding=utf-8
from problem_model import *
from problem_form import ArithmeticForm
import random
import numpy
from examinations.models import *
from collections import OrderedDict
import re

from skills.models import Skill


class ArithmeticPolynomialSecondDegree(ProblemModel):
    def __init__(self, domain, image, range, val=None):
        ProblemModel.__init__(self, "Polynomial second degree", domain, image, range)
        if val and len(val) == 3:
            self.val = val
        else:
            self.gen_new_values()

    def gen_new_values(self):
        self.val = list()
        self.gen_values()

    def gen_values(self):
        if self.image == "Integer":
            self.gen_values_from_sol()
        elif self.domain == "Integer":
            for i in range(3):
                self.val.append(random.randint(self.range[0], self.range[1]))
        elif self.domain == "Rational":
            for i in range(3):
                self.val.append(random.uniform(self.range[0], self.range[1]))
        else:
            raise ValueError("Wrong value for domain: ", self.domain)

    def gen_values_from_sol(self):
        # Max_val for value is rng_range³
        # TODO What range should we put ?
        sol = [random.randint(-5, 5), random.randint(-5, 5)]
        sum, prod = sol[0] + sol[1], sol[0] * sol[1]
        # For polynom of type ax²+bx+c
        a = random.randint(-5, 5)
        b = -1 * sum * a
        c = prod * a
        self.val = [a, b, c]

    def get_desc(self):
        return self.desc

    def get_val(self):
        return self.val

    @staticmethod
    def round(list):
        new_list = []
        for x in list:
            if isinstance(x, complex):
                new_list.append(complex("{0:.2f}".format(x)))
            elif isinstance(x, float):
                new_list.append(float("{0:.2f}".format(x)))
        return new_list

    def get_sol(self):
        tmp_sol = numpy.roots(self.val).tolist()
        sol = list()
        if self.image == "Rational" or self.image == "Integer":
            sol = list()
            for root in tmp_sol:
                if not isinstance(root, complex):
                    sol.append(root)
        elif self.image == "Complex":
            sol = tmp_sol
        else:
            raise ValueError("Wrong value for image:", self.image)

        return self.round(sol)

    def new_question(self, sol):
        question_desc = "Calculer les racines de: "
        if self.domain == "Integer":
            equation = ("{:-d}x²{:+d}x{:+d}".format(self.val[0], self.val[1], self.val[2]))
        elif self.domain == "Rational":
            equation = ("{:-0.2f}x²{:+0.2f}x{:+0.2f}".format(self.val[0], self.val[1], self.val[2]))
        equation = self.pretty_polynomial_string(equation)
        question_desc += equation
        if sol.__len__() > 1:
            sol = tuple(sol)
        else:
            sol = sol[0]
        answers = yaml.dump(OrderedDict([("answers", [sol]), ("type", "text")]))
        question = Question(description=question_desc, answer=answers, source="Génerée automatiquement")
        return question

    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            # We only want problems having a solution
            # TODO : Avoid looping
            while not self.get_sol():
                self.gen_new_values()
            questions.append((self.new_question(self.get_sol())))
            # TODO : Check if no two problems the same
            self.gen_new_values()
        return questions

    def get_context(self):
        default_context = self.default_context()
        # TODO Get from db if already Context already exist
        # context, created = Context.objects.get_or_create(defaults=default_context, file_name="generated")
        return default_context

    @staticmethod
    def default_context():
        description = "Calculer les racines $$ x_1, x_2 $$ d'un polyonme du second degré <br/> " \
                      "<b> Attention : </b> les réponses doivent être sous la forme " \
                      "$$ (x_1, x_2) $$ dans l'ordre croissant et arrondis à 2 chiffres après la virgule"
        skill_id = "T4-U5-A1b"
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context

    @staticmethod
    def make_form(post_values):
        return ArithmeticForm(post_values)

    @staticmethod
    # TODO Make it prettier
    def pretty_polynomial_string(string):
        string = re.sub(r"\+-", r"-", string)
        string = "   " + string + "   "
        string = re.sub(r"(\+|-|\s)0x*²*(\+|-|\s)", r"\2", string)
        string = re.sub(r"(\+|-|\s)1(x²*)(\+|-|\s)", r"\2\3", string)
        return string

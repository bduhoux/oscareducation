# coding=utf-8
import random
import numpy
import yaml

from collections import OrderedDict
from examinations.models import *
from questions_factory.models.problem_form import *
from questions_factory.models.problem_models.problem import *
from skills.models import Skill


class StatisticsProblem(Problem) :
    def __init__(self, nb=10, range=(0, 20)):
        self.range = range
        self.values = None
        self.nb = nb
        self.gen_values()

    def gen_values(self):
        self.values = [random.randint(self.range[0],self.range[1]) for _ in range(self.nb)]


    def get_sol(self):
        sol = list()
        average = self.get_average()
        sol.append(float("{0:.2f}".format(average)))
        median = self.get_median()
        sol.append(float("{0:.2f}".format(median)))
        standard_deviation = self.get_standard_deviation()
        sol.append(float("{0:.2f}".format(standard_deviation)))
        return sol


    def gen_questions(self, number_of_questions):
        questions = list()
        for _ in range(number_of_questions):
            questions.append((self.new_question(self.get_sol())))
            self.gen_values()
        return questions

    def new_question(self, sol):
        question_desc = "Voici une série de données recueillies pour chaque jour écoulée durant " + str(self.nb) + " jours : <br/>" \
                        "<table style=""width:100%"", border=1px, text-align=""center""> <tr>"
        n = 1
        for j in self.values:
            question_desc += "<th padding=15px> jour " + str(n) + "</th>"
            n += 1
        question_desc += "</tr>"
        for v in self.values:
            question_desc +=  "<td padding=15px>" + str(v) + "</td>"
        question_desc +="</tr> </table>"

        answers = yaml.dump(OrderedDict([("answers", [sol]), ("type", "text")]))
        question = Question(description=question_desc, answer=answers, source="Génerée automatiquement")
        return question

    @staticmethod
    def make_form(post_values):
        return StatisticsForm(post_values)


    def get_context(self):
        default_context = self.default_context()
        # TODO Get from db if already Context already exist
        # context, created = Context.objects.get_or_create(defaults=default_context, file_name="generated")
        return default_context

    @staticmethod
    def default_context():
        description = "Calculer la moyennne, la médiane et l'écart-type des valeurs données<br/> " \
                      "<b> Attention : </b> les réponses doivent être sous la forme " \
                      "$$ [x_1, x_2, x_3] $$ dans l'ordre suivant : Moyenne ,Médiane, Ecart-Type avec 2 chiffres après la virgule et non arrondis"
        skill_id = "T4-U5-A1b"
        default_context = Context.objects.create(
            file_name="generated",
            skill=Skill.objects.get(code=skill_id),
            context=description,
            added_by=None
        )
        return default_context


    def get_average(self):
        m = numpy.mean(self.values)
        return m

    def get_median(self):
        m = numpy.median(self.values)
        return m

    def get_standard_deviation(self):
        sd = numpy.std(self.values)
        return sd


from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Professor, Student
from django.core.urlresolvers import reverse


class PermissionsTest(TestCase):
    def setUp(self):
        prof = User.objects.create(username="professor")
        prof.set_password("1234")
        prof.save()
        self.prof = Professor.objects.create(user=prof)

        student = User.objects.create(username="student")
        student.set_password("1234")
        student.save()
        self.prof = Student.objects.create(user=student)

    def test_unlogged_go_to_homepage(self):
        c = Client()

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/accounts/login/')
        self.assertEqual(response.status_code, 302)

    def test_redirect_professor(self):
        c = Client()
        c.login(username="professor", password="1234")

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/professor/dashboard/')

    def test_redirect_student(self):
        c = Client()
        c.login(username="student", password="1234")

        response = c.get("/")
        self.assertEqual(response.url, 'http://testserver/student/dashboard/')


class PageLoadTest(TestCase):
    def setUp(self):
        prof = User.objects.create(username="professor")
        prof.set_password("1234")
        prof.save()
        self.prof = Professor.objects.create(user=prof)

        self.c = Client()
        self.c.login(username="professor", password="1234")

    def test_static_pages_load(self):
        self.assertEqual(self.c.get(reverse("professor:dashboard")).status_code, 200)


# exercice_validation_form_validate_exercice
"""     Tests unfinished for promotions but canceled because Celine & Adrien did them. I'll continue if I've time.


class ExerciceFromExerciceTest(TestCase):
    # We set up the paramters of login
    def setUp(self):
        self.c = Client()
        self.c.login(username="prof", password="prof")

    # We test a text question
    def testText(self):
        request = {"questions" : [
        {"type" = "text","instructions":"2+2 = ?","answers"="4"}
        ]}
        self.assertEqual(self.c.exercice_validation_form_validate_exercice(request).yaml.result,'success')

    def testMath(self):

    def testGraph(self):


# exercice_validation_form_submit

class ExerciceSubmitTest(TestCase):
    # We set up the paramters of login
    def setUp(self):
        self.c = Client()
        self.c.login(username="prof", password="prof")

    def testText():
        self.c = Client()
        self.c.login(username="prof", password="prof")

    def testGraph():

"""

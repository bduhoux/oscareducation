from django.test import TestCase,Client



# Create your tests here.

"""
    We create a student with username = eleve.eleve with password = eleve by the teacher 'prof' in class 'Hankar'.
    We create a test with 'prof' for the class '5M4', in our case we have the number 464 of test and normally the eleve.eleve can't access.
    We create a test with 'prof' but not 'mis en ligne', the test 465
    We try to access to a test (28) that we've already passed
    We create a test that the user eleve.eleve didn't begin and we access it for the first time
"""
# pass tests

class passTestsTest(TestCase):
    d

    # We test to access to a test but without logging, the server shall forbid us and send us a 404 error.
    # We take the id of a test already created, 21, in our case.
    def testWithoutLog(self):
        c = Client()
        response = c.get("/test/21/start/")
        self.assertEqual(response.status_code,404)

    # We test to access to a test that the professor hasn't activated.
    def testNotRunnnig(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/test/465/start/")
        self.assertTemplateUsed(response,'examinations/test_closed.haml')

    #
    def testStarted(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/23")
        self.assertTemplateUsed(response,"examinations/pass_test.haml")

    # We test to access to the test page where we've already passed the test.
    def testFinished(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/28")
        self.assertTemplateUsed(response,"examinations/test_finished.haml")

    # We test to access to a test that we didn't finished
    def testRender(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/28")
        self.assertTemplateUsed(response,"examinations/take_exercice.haml")


# skill pedagogic
"""
class skillPedagogicTest(TestCase):
    def setUp(self):
        self.s = Client()
        self.s.login(username="eleve.eleve",password="eleve")
    def testSkill(self):
        response = self.c.get('/pedagogical/skill/S41b/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill2(self):
        response = self.c.get('/pedagogical/skill/S22b/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill3(self):
        response = self.c.get('/pedagogical/skill/S31fII/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill4(self):
        response = self.c.get('/pedagogical/skill/S13aI/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')


"""

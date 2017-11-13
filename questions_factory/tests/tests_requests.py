from django.test import TestCase, RequestFactory
from questions_factory.views import *


class ProblemGenerationRequests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_put_request_on_generator_submit(self):
        request = self.factory.put('/questions_factory/generator/272727/88/9022772/')
        response = generator_submit(request, 222, 222, 222)
        self.assertEqual(response.status_code, 404)


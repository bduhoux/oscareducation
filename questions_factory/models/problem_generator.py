from arithmetic_problem import *
import json


class ProblemGenerator:

    def __init__(self):
        pass

    def factory(json_i):
        global problem, domain, image, range, values
        input = json.loads(json_i)
        problem = input["problem"]
        domain, range, image = input.pop("domain"), input.pop("range"), input.pop("image")
        values = input.pop("val", None)

        if problem == "Arithmetic_Polynomial_Second_degree":
            return ArithmeticPolynomialSecondDegree(domain, image, range, values)
        else:
            raise ValueError('Wrong problem type')

    factory = staticmethod(factory)

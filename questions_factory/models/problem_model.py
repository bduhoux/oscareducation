import abc


class ProblemModel:
    def __init__(self, desc, domain, image, range=(0, 20), val=None):
        self.desc = desc
        self.domain = domain
        self.image = image
        self.range = range

    @abc.abstractmethod
    def get_desc(self):
        """Return the description of the problem"""

    @abc.abstractmethod
    def get_sol(self):
        """Return the solution of the problem"""

    @abc.abstractmethod
    def gen_values(self):
        """Generate new random values for the problem"""

    @abc.abstractmethod
    def make_form(self):
        """Generate the associated form"""

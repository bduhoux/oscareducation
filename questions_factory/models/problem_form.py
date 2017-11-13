# coding=utf-8
from django import forms

DOMAIN_CHOICES = (('Integer', 'Entiers'), ('Rational', 'Rationnels'))
IMAGE_CHOICES = (('Rational', 'Rationnels'), ('Complex', 'Complexes'), ('Integer', 'Entiers'))


class ProblemForm(forms.Form):
    domain = forms.ChoiceField(widget=forms.Select, choices=DOMAIN_CHOICES, label='Domaine')
    image = forms.ChoiceField(widget=forms.Select, choices=IMAGE_CHOICES, label='Image')


class ArithmeticForm(ProblemForm):
    range_from = forms.FloatField(widget=forms.TextInput, required=True, label='Interval inférieur')
    range_to = forms.FloatField(widget=forms.TextInput, required=True, label='Interval supérieur')

    def clean(self):
        cleaned_data = super(ArithmeticForm, self).clean()
        range_from = cleaned_data.get("range_from")
        range_to = cleaned_data.get("range_to")

        # Checking instance to avoid problem with 0 values
        if isinstance(range_from, float) and isinstance(range_to, float):
            if range_from >= range_to:
                msg = "L'interval inférieur ne peut pas être plus grand ou égal au supérieur."
                self.add_error('range_from', msg)
            if (range_to - range_from) < 5:
                msg = "Fournissez un interval de valeurs supérieur ou égal à 5"
                self.add_error('range_from', msg)

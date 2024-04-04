from django import forms


class KISProfileChosingForm(forms.Form):

    id = forms.ChoiceField()
    name = forms.ChoiceField()




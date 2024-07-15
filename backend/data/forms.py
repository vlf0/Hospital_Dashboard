from django import forms
from .kis_data import KISData, MainQueries


class KISProfileChosingForm(forms.Form):
    id = forms.ChoiceField(label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = self.get_id_choices()

    def get_id_choices(self):
        query = [MainQueries.KIS_PROFILES]
        dept_hosp_dataset = next(KISData(query).get_data_generator())
        choices = [(profile[0], f'{str(profile[0])} - Профиль {profile[1]}') for profile in dept_hosp_dataset]
        return choices

from django import forms
from .models import KISProfiles


class KISProfileChosingForm(forms.ModelForm):
    id = forms.ChoiceField(label='')

    class Meta:
        model = KISProfiles
        fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].choices = self.get_id_choices()
        # self.fields['name'].choices = self.get_name_choices()

    def get_id_choices(self):
        profiles = KISProfiles.objects.all()
        choices = [(profile.id, f'{str(profile.id)} - Профиль {profile.name}') for profile in profiles]
        return choices

    # def get_name_choices(self):
    #     profiles = KISProfiles.objects.all()
    #     choices = [(profile.id, profile.name) for profile in profiles]
    #     return choices

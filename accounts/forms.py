from django import forms

from .models import Project


class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date','end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }
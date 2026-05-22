from django import forms

from projects.models import Project
from users.validators import validate_github_url


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Project.STATUS_CHOICES)

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Название проекта обязательно.")
        return name

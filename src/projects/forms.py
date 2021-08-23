from django.forms import ModelForm
from django import forms
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = "__all__"
        fields = [
            "title",
            "featured_image",
            "description",
            "demo_link",
            "source_link",
            "tags",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Project title goes here.'})
        # self.fields['description'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Project description goes here.'})

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django import forms
from .models import Project, Review


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


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
        labels = {"value": "Place your vote", "body": "Add a comment with your vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Project title goes here.'})
        # self.fields['description'].widget.attrs.update({'class' : 'input', 'placeholder' : 'Project description goes here.'})

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})

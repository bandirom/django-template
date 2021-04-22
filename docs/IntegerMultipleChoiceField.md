IntegerMultipleChoiceField(forms.MultipleChoiceField)
==============================

Integer Form representation of `MultipleChoiceField` using `models.JsonField()`

##### Example:
```python

# models.py
from django.db import models

class YourModel(models.Model):
    some_choice_field = models.JSONField(default=list, blank=True)

# choices.py
from django.db.models import IntegerChoices

class YourModelChoice(IntegerChoices):
    ONE = (1, 'One')
    TWO = (2, 'Two')
    Three = (3, 'Three')


# forms.py
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class YourModelForm(forms.ModelForm):
    some_choice_field = IntegerMultipleChoiceField(
        choices=YourModelChoice.choices,
        widget=FilteredSelectMultiple('FieldName', False),
        required=False
    )

    class Meta:
        model = YourModel
        fields = ('id', 'some_choice_field')

# admin.py
from django.contrib import admin

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    form = YourModelForm


```

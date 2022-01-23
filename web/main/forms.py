import json

from django import forms


class IndentedJSONFormField(forms.JSONField):
    """Json form field with indented lines"""

    def prepare_value(self, value):
        if isinstance(value, str):
            return value
        return json.dumps(value, indent=2)


class IntegerMultipleChoiceField(forms.MultipleChoiceField):
    """Integer representation of MultipleChoiceField using JSONField"""

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise forms.ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return [int(val) for val in value]

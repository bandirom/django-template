from django.db.models import JSONField

from .forms import IndentedJSONFormField


class IndentedJSONField(JSONField):
    """JsonField with indented lines"""

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                'form_class': IndentedJSONFormField,
                **kwargs,
            }
        )

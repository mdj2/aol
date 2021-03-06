from django.forms.widgets import RadioSelect
from django.forms.forms import BoundField, Form
from django import forms
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxInput, ClearableFileInput
from django.forms.util import ErrorList
from django.utils.html import format_html, format_html_join
from django.utils.encoding import force_text

# monkey patch the ErrorList so it has a bootstrap css class (text-danger)
ErrorList.as_ul = lambda self: '' if not self else format_html('<ul class="errorlist text-danger">{0}</ul>', format_html_join('', '<li>{0}</li>', ((force_text(e),) for e in self)))

# monkey patch BoundFields so that it has an error_class attribute that returns
# "field-error" or the empty string
BoundField.error_class = lambda self: "has-error" if self.errors else ""

# monkey patch the ModelForm and Form iterators so they add an is_checkbox
# attribute to all checkbox form elements
def model_iter(self):
    for bound_field in super(ModelForm, self).__iter__():
        if isinstance(bound_field.field.widget, CheckboxInput):
            bound_field.is_checkbox = True
        yield bound_field
ModelForm.__iter__ = model_iter

def form_iter(self):
    for bound_field in super(Form, self).__iter__():
        if isinstance(bound_field.field.widget, CheckboxInput):
            bound_field.is_checkbox = True
        yield bound_field
Form.__iter__ = form_iter

class DeletableModelForm(forms.ModelForm):
    """
    This form adds a do_delete field which is checked when the modelform is
    saved. If it is true, the model instance is deleted
    """
    do_delete = forms.BooleanField(required=False, initial=False, label="Delete")

    def __init__(self, *args, **kwargs):
        super(DeletableModelForm, self).__init__(*args, **kwargs)
        # if we are adding a new model (the instance.pk will be None), then
        # there is no reason to have a delete option, since the object hasn't
        # been created yet
        if self.instance.pk is None:
            self.fields.pop("do_delete")

    def save(self, *args, **kwargs):
        if self.cleaned_data.get('do_delete'):
            self.instance.delete()
        else:
            super(DeletableModelForm, self).save(*args, **kwargs)


from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Button
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, Select

from blog.models import Post

from django import forms
from .models import Image


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class PostCreateForm(ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'
    helper.layout = Layout(
        # HTML("<h5>About to create a post</h5>"),
        Field('title', css_class='mb-2'),
        HTML("<hr />"),
        Field('text', css_class='mb-2'),
        HTML("<hr />"),
        'author',
        HTML("<hr />"),
        Field('published_date', css_class='mb-2'),
        Field('image', css_class='mb-2'),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Button('cancel', 'Cancel')
        )
    )

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                # 'style': 'max-width: 300px;',
                'placeholder': 'Title'
            }),
            'text': Textarea(attrs={
                # 'class': "form-control",
                # 'style': 'max-width: 300px;',
                'placeholder': 'Text'
            }),
            'author': Select(attrs={
                'class': "form-control",
                # 'style': 'max-width: 300px;',
                'placeholder': 'Author'
            }),
            'published_date': DateTimePickerInput()

        }


class RegisterForm(UserCreationForm):

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'].lower()).exists():
            raise forms.ValidationError('username already exists')

        return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

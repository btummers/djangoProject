from django.forms import ModelForm, TextInput, Textarea

from blog.models import Post

from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class PostCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        
        super(PostCreateForm, self).__init__(*args, **kwargs)


    class Meta:

        model = Post
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'text': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),
            # 'published_date': forms.CharField(),

        }
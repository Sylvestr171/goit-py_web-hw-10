from django.forms import ModelForm, CharField, TextInput, ModelChoiceField, Select, ValidationError
from .models import Author, Quote


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    born_date = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    born_location = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    description = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    tags = CharField(required=True,widget=TextInput(attrs={'placeholder': 'Наприклад: life, happiness'}))
    author = ModelChoiceField(queryset=Author.objects.all(), to_field_name="id")
    quote = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Quote
        fields = ['tags', 'author', 'quote']
        widgets = {
            'quote': TextInput(attrs={'placeholder': 'Введіть цитату'}),
            'author': Select()
        }

    def clean_tags(self):
            tag_list = [tag.strip() for tag in self.cleaned_data['tags'].split(',') if tag.strip()]
            if not tag_list:
                raise ValidationError("Введіть хоча б один тег.")
            return tag_list  # повертаємо список тегів

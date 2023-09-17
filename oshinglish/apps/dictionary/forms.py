from django import forms
from django.forms import ModelForm

# from django.contrib.auth.forms import UserCreationForm
# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    OshindongaWord,
    WordDefinition,
)

WORD_PAIR_CHOICES = (
    OshindongaWord.objects.all().order_by("word").select_related("english_word")
)  # [:10]


class SearchWordForm(forms.Form):
    ENGLISH = "English"
    OSHINDONGA = "Oshindonga"
    INPUT_LANGUAGE = [
        (ENGLISH, "English"),
        (OSHINDONGA, "Oshindonga"),
    ]
    input_language = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg",
                "id": "inputGroupSelect01",
                "style": "max-width:21%;",
            }
        ),
        choices=INPUT_LANGUAGE,
    )
    search_word = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Search word",
            }
        ),
        max_length=50,
    )


class EnglishWordForm(ModelForm):
    class Meta:
        model = EnglishWord
        # Not recommended (potential security issue if more fields added)
        fields = "__all__"
        widgets = {
            "word": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Enter an English word",
                }
            ),
            "word_case": forms.Select(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        word_case = cleaned_data.get("word_case")
        word = cleaned_data.get("word")
        if word_case == "Abbreviation":
            self.cleaned_data["word"] = word.strip().upper()
        elif word_case == "Proper Noun":
            self.cleaned_data["word"] = word.strip().capitalize()
        else:
            self.cleaned_data["word"] = word.strip().lower()


class OshindongaPhoneticForm(ModelForm):
    class Meta:
        model = OshindongaPhonetic
        fields = "__all__"
        widgets = {
            "oshindonga_word": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Shanga oshitya shOshindonga",
                }
            ),
            "phonetics": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "pronunciation": forms.FileInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        oshindonga_word = cleaned_data.get("oshindonga_word")
        phonetics = cleaned_data.get("phonetics")
        self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().lower()
        # self.cleaned_data['phonetics'] = phonetics.strip()


class OshindongaWordForm(ModelForm):
    english_word = forms.ModelChoiceField(
        queryset=EnglishWord.objects.all().order_by("word"),
        empty_label="Select the English word",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "style": "display:none",
                "id": "englishWords",
            }
        ),
    )
    word_phonetics = forms.ModelChoiceField(
        queryset=OshindongaPhonetic.objects.all().order_by("oshindonga_word"),
        empty_label="Select Oshindonga word phonetics",
        widget=forms.Select(attrs={"class": "form-control form-control-lg mb-2"}),
    )

    class Meta:
        model = OshindongaWord
        fields = "__all__"
        widgets = {
            "word": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Shanga oshitya shOshindonga",
                }
            ),
            "word_case": forms.Select(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        word_case = cleaned_data.get("word_case")
        word = cleaned_data.get("word")
        if word_case == "Abbreviation":
            self.cleaned_data["word"] = word.strip().upper()
        elif word_case == "Proper Noun":
            self.cleaned_data["word"] = word.strip().capitalize()
        else:
            self.cleaned_data["word"] = word.strip().lower()


class WordDefinitionForm(ModelForm):
    word_pair = forms.ModelChoiceField(
        queryset=WORD_PAIR_CHOICES,
        empty_label="Select a word pair to define",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "style": "display:none",
                "id": "word_pairs",
            }
        ),
    )
    synonyms = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control form-control-lg mb-2",
                # "style": "display:none",
                # "id": "synonyms",
            }
        ),
        choices=[
            (pair.id, f"{pair.word} | {pair.english_word.word}")
            for pair in WORD_PAIR_CHOICES
        ],
    )

    plurals = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control form-control-lg mb-2",
                # "style": "display:none",
                # "id": "plurals",
            }
        ),
        choices=[
            (pair.id, f"{pair.word} | {pair.english_word.word}")
            for pair in WORD_PAIR_CHOICES
        ],
    )

    class Meta:
        model = WordDefinition
        fields = "__all__"
        widgets = {
            "part_of_speech": forms.Select(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "onchange": "displayPluralOrTense()",
                }
            ),
            "simple_present": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "present_participle": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "simple_past": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "past_participle": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "english_definition": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Enter the English definition here...",
                }
            ),
            "oshindonga_definition": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Shanga efatululo mOshindonga mpaka...",
                }
            ),
        }


class DefinitionExampleForm(ModelForm):
    definition = forms.ModelChoiceField(
        queryset=WordDefinition.objects.all()
        .order_by("word_pair")
        .select_related("word_pair__english_word"),
        empty_label="Select a definition to exemplify",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "onchange": "displayDefinition()",
            }
        ),
    )

    class Meta:
        model = DefinitionExample
        fields = "__all__"
        widgets = {
            "english_example": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "oshindonga_example": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }


class OshindongaIdiomForm(ModelForm):
    word_pair = forms.ModelChoiceField(
        queryset=OshindongaWord.objects.all().order_by("word"),
        empty_label="Select the word pair",
        widget=forms.Select(attrs={"class": "form-control form-control-lg mb-2"}),
    )

    class Meta:
        model = OshindongaIdiom
        fields = "__all__"
        widgets = {
            "oshindonga_idiom": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "meaning": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }


# class ContributorCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         fields = UserCreationForm.Meta.fields + ("email",)

#     def __init__(self, *args, **kwargs):
#         super(ContributorCreationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs = {
#             'class': 'form-control form-control-lg mb-2', 'placeholder': 'Username'}
#         self.fields['email'].widget.attrs = {
#             'class': 'form-control form-control-lg mb-2', 'placeholder': 'Email address'}
#         self.fields['password1'].widget.attrs = {
#             'class': 'form-control form-control-lg mb-2', 'placeholder': 'Password'}
#         self.fields['password2'].widget.attrs = {
#             'class': 'form-control form-control-lg mb-2', 'placeholder': 'Confirm password'}

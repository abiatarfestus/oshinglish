from django import forms
from django.forms import ModelForm

# from django.contrib.auth.forms import UserCreationForm
# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    PartOfSpeech,
    WordPair,
    WordPairDefinition,
)

WORD_PAIR_CHOICES = (
    WordPair.objects.all()
    .order_by("oshindonga_word")
    .select_related("english_word", "root", "part_of_speech")
)[:10]


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
        fields = ["word", "word_case"]
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
        fields = [
            "word_pair",
            "oshindonga_phonetics",
            "oshindonga_pronunciation",
        ]
        widgets = {
            "word_pair": forms.Select(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "oshindonga_phonetics": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    # "placeholder": "Shanga oshitya shOshindonga",
                }
            ),
            "oshindonga_pronunciation": forms.FileInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        oshindonga_phonetics = cleaned_data.get("oshindonga_phonetics")
        self.cleaned_data["oshindonga_phonetics"] = oshindonga_phonetics.strip()
        # self.cleaned_data['phonetics'] = phonetics.strip()


class WordPairForm(ModelForm):
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
    root = forms.ModelChoiceField(
        queryset=WordPair.objects.all().order_by("oshindonga_word"),
        empty_label="Select the a root word",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "style": "display:none",
                "id": "rootWords",
            }
        ),
    )
    part_of_speech = forms.ModelChoiceField(
        queryset=PartOfSpeech.objects.all().order_by("code"),
        empty_label="Select the a part of speech",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "style": "display:none",
                "id": "partsOfSpeech",
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
            (pair.id, f"{pair.oshindonga_word} | {pair.english_word.word}")
            for pair in WORD_PAIR_CHOICES
        ],
    )

    class Meta:
        model = WordPair
        fields = ["english_word", "oshindonga_word", "root", "synonyms"]
        widgets = {
            "oshindonga_word": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                    "placeholder": "Shanga oshitya shOshindonga",
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        english_word = cleaned_data.get("english_word")
        word_case = english_word.word_case
        oshindonga_word = cleaned_data.get("oshindonga_word")
        if word_case == "Abbreviation":
            self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().upper()
        elif word_case == "Proper Noun":
            self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().capitalize()
        else:
            self.cleaned_data["oshindonga_word"] = oshindonga_word.strip().lower()


class WordPairDefinitionForm(ModelForm):
    word_pair = forms.ModelChoiceField(
        queryset=WORD_PAIR_CHOICES,
        empty_label="Select a word pair to define",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-lg mb-2",
                "style": "display:none",
                "id": "wordPairs",
            }
        ),
    )

    class Meta:
        model = WordPairDefinition
        fields = ["word_pair", "english_definition", "oshindonga_definition"]
        widgets = {
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
        queryset=WordPairDefinition.objects.all()
        .order_by("word_pair")
        .select_related("word_pair__english_word", "root", "part_of_speech"),
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
        fields = ["definition", "english_example", "oshindonga_example"]
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
        queryset=WordPair.objects.all().order_by("oshindonga_word"),
        empty_label="Select the word pair",
        widget=forms.Select(attrs={"class": "form-control form-control-lg mb-2"}),
    )

    class Meta:
        model = OshindongaIdiom
        fields = ["word_pair", "oshindonga_idiom", "meaning"]
        widgets = {
            "oshindonga_idiom": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "meaning": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }

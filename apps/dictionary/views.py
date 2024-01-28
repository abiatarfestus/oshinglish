import json
import random
from json import dumps

from django.conf import settings
from django.db.models import F, Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.utils.html import format_html
from django.views.generic.edit import CreateView, UpdateView

from .forms import (
    DefinitionExampleForm,
    EnglishWordForm,
    OshindongaIdiomForm,
    OshindongaPhoneticForm,
    WordPairForm,
    WordPairDefinitionForm,
)
from .constants import *
from .processors import SearchDefinition


def get_untranslated_words():
    all_english_ids = [word.id for word in ALL_ENGLISH_WORDS]
    all_english_translated_ids = [pair.english_word_id for pair in ALL_WORD_PAIRS]
    untranslated_english_ids = [i for i in all_english_ids if i not in all_english_translated_ids]
    random.shuffle(untranslated_english_ids)
    untranslated_english_words = []
    for i in untranslated_english_ids[:5]:
        untranslated_english_words.append(EnglishWord.objects.get(id=i))
    return untranslated_english_words


def get_undefined_words():
    word_pair_ids = [pair.id for pair in ALL_WORD_PAIRS]
    defined_pair_ids = [definition.word_pair_id for definition in ALL_DEFINITIONS]
    undefined_pair_ids = [i for i in word_pair_ids if i not in defined_pair_ids]
    random.shuffle(undefined_pair_ids)
    undefined_word_pairs = []
    for i in undefined_pair_ids[:5]:
        undefined_word_pairs.append(WordPair.objects.get(id=i))
    return undefined_word_pairs


def get_unexemplified():
    definition_ids = [definition.id for definition in ALL_DEFINITIONS]
    exemplified_definition_ids = [example.definition_id for example in ALL_EXAMPLES]
    unexemplified_definition_ids = [i for i in definition_ids if i not in exemplified_definition_ids]
    random.shuffle(unexemplified_definition_ids)
    unexemplified_definitions = []
    for i in unexemplified_ids[:5]:
        unexemplified_definitons.append(WordPairDefinition.objects.get(id=i))
    return unexemplified_definitions


def search_word(request):
    # Create an instance of the SearchDefinition calss, passing in the request
    search_object = SearchDefinition(request)
    # Call the search_word() method of the created instance/object, which will kickstart the necessary queries
    search_object.search_word()
    # Pass the context of the object/instance and pass it to the context variable of this view
    context = search_object.context
    return render(request, "dictionary/search.html", context)


def search_suggested_word(request, pk):
    word_instance = get_object_or_404(EnglishWord, pk=pk)
    search_object = SearchDefinition(request)
    search_object.search_suggested(word_instance.id)
    context = search_object.context
    return render(request, "dictionary/search.html", context)


def search_with_ajax(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        print(request.GET)
        term = request.GET.get('term')
        field_type = request.GET.get("field")
        if field_type == "english_words":
            results = EnglishWord.objects.filter(word__icontains=term).order_by("word").values("id", "word")
        elif field_type == "roots" or field_type == "synonyms":
            results = WordPair.objects.filter(
                Q(english_word__word__icontains=term) | Q(oshindonga_word__icontains=term)
                ).order_by("oshindonga_word").values("id", "oshindonga_word", "english_word__word")
        elif field_type == "parts_of_speech":
            results = PartOfSpeech.objects.filter(
                Q(english_name__icontains=term) | Q(oshindonga_name__icontains=term)
            ).order_by("english_name").values("id", "english_name", "oshindonga_name")
        elif field_type == "word_pair":
            results = WordPair.objects.filter(
                Q(english_word__word__icontains=term) | Q(oshindonga_word__icontains=term)
                ).order_by("english_word").values("id", "oshindonga_word", "english_word__word", "part_of_speech__english_name")
        # elif field_type == "synonyms":
        #     results = ALL_WORD_PAIRS.filter(oshindonga_word__icontains=term).order_by("oshindonga_word")
        return JsonResponse(list(results), safe=False)
    return JsonResponse({"message": "Only Ajax requests allowed"})


class EnglishWordCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_englishword"
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {
        "operation": "Add a new English word",
        "newly_added_words": ALL_ENGLISH_WORDS[:5],
    }
    success_message = "The word '%(word)s' was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaPhoneticCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_oshindongaphonetic"
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {
        "operation": "Gwedha mo omawi gOshindonga",
        "new_phonetics": ALL_PHONETICS,
        # "random_unphonetised": random_unphonetised,
    }
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_phonetics': oshindonga_words, 'untranslated_words': get_untranslated_words

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordPairCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_wordpair"
    form_class = WordPairForm
    model = WordPair
    extra_context = {
        "operation": "Gwedha mo oshitya shOshindonga oshipe",
        "newly_added_pairs": ALL_WORD_PAIRS[:5],
        "untranslated_english_words": get_untranslated_words,
    }
    success_message = (
        "Oshitya '%(oshindonga_word)s' osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordPairDefinitionCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    # Uses the form class defined in forms.py which allows customization
    permission_required = "dictionary.add_wordpairdefinition"
    form_class = WordPairDefinitionForm
    model = WordPairDefinition
    extra_context = {
        "operation": "Add a new word definition",
        "newly_defined_words": ALL_DEFINITIONS[:5],
        "undefined_words": get_undefined_words,
    }
    success_message = "Definition of '%(word_pair)s' was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# Converting definitions queryset into a dictionary of {id:(engDef,oshDef)} for passing to the context.
q = WordPairDefinition.objects.all()
queryset_dict = dumps(
    {
        q[i].id: (q[i].english_definition, q[i].oshindonga_definition)
        for i in range(len(q))
    }
)


class DefinitionExampleCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_definitionexample"
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {
        "operation": "Add a new definition example",
        "newly_added_examples": ALL_EXAMPLES[:5],
        "unexemplified_definitions": get_unexemplified,
        "definitions_dict": queryset_dict,
    }
    success_message = "Example of '%(definition)s' usage was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaIdiomCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_oshindongaidiom"
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {
        "operation": "Gwedha mo oshipopiwamayele oshipe",
        "newly_added_idioms": ALL_OSHINDONGA_IDIOMS[:5],
        "random_idioms": ALL_OSHINDONGA_IDIOMS.order_by("?")[:10],
    }
    success_message = (
        "Oshipopiwamayele osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# Update class-based views


class EnglishWordUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_english-word"
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {
        "operation": "Update an existing English word",
        "newly_added_words": ALL_ENGLISH_WORDS[:5],
    }
    success_message = (
        "The word '%(word)s' was successfully updated. Thank you for your contribution!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaPhoneticUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_oshindongaphonetic"
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {
        "operation": "Pukulula ewi lyoshitya shOshindonga li li mo nale",
        "new_phonetics": ALL_PHONETICS[:5],
        # "random_unphonetised": random_unphonetised,
    }
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya lundululwa nawa. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordPairUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_wordpair"
    form_class = WordPairForm
    model = WordPair
    extra_context = {
        "operation": "Pukulula oshitya shOshindonga shi li mo nale",
        "newly_added_pairs": ALL_WORD_PAIRS[:5],
        "untranslated_english_words": get_untranslated_words,
    }
    success_message = "Epukululo olyeenda nawa. Tangi ku sho wa gandja!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordPairDefinitionUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    # Uses the form class defined in forms.py which allows customization
    permission_required = "dictionary.change_wordpairdefinition"
    form_class = WordPairDefinitionForm
    model = WordPairDefinition
    success_message = "Definition of '%(word_pair)s' was successfully updated. Thank you for your contribution!"
    extra_context = {
        "operation": "Update an existing word definition",
        "newly_defined_words": ALL_DEFINITIONS[:5],
        "undefined_words": get_undefined_words,
    }

    def get_context_data(self, **kwargs):
        context = super(WordPairDefinitionUpdate, self).get_context_data(**kwargs)
        # context["operation"] = "Update an existing word definition",
        # context["newly_defined_words"] = defined_words,
        # context["undefined_words"] = get_undefined_words,
        return context

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class DefinitionExampleUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_definitionexample"
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {
        "operation": "Update an existing definition example",
        "newly_added_examples": ALL_EXAMPLES[:5],
        "definitions_dict": queryset_dict,
    }
    success_message = "Example of '%(definition)s' usage was successfully updated. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaIdiomUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_oshindongaidiom"
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {"operation": "Pukulula oshipopiwamayele shi li monale"}
    success_message = "Oshipopiwamayele osha lundululwa nawa.Tangi ku sho wa gandja!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# List View
# Templates for displaying List and Detail views
list_view = "dictionary/list_view.html"
detail_view = "dictionary/detail_view.html"


class EnglishWordListView(generic.ListView):
    paginate_by = 50
    model = EnglishWord
    template_name = list_view

    # Override the default get_queryset()
    def get_queryset(self):
        return EnglishWord.objects.all().order_by("word")

    # Add additional context variables
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EnglishWordListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # Default context = english-word_list
        context["heading"] = "List of English words in the dictionary"
        return context


class OshindongaPhoneticListView(generic.ListView):
    paginate_by = 50
    model = OshindongaPhonetic
    template_name = list_view

    def get_queryset(self):
        return OshindongaPhonetic.objects.all().order_by("oshindonga_word")

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticListView, self).get_context_data(**kwargs)
        context["heading"] = "List of Oshindonga phonetics in the dictionary"
        return context


class WordPairListView(generic.ListView):
    paginate_by = 50
    model = WordPair
    template_name = list_view

    def get_queryset(self):
        return WordPair.objects.all().order_by("english_word")

    def get_context_data(self, **kwargs):
        context = super(WordPairListView, self).get_context_data(**kwargs)
        context["heading"] = "List of word pairs in the dictionary"
        return context


class OshindongaIdiomListView(generic.ListView):
    paginate_by = 10
    model = OshindongaIdiom
    template_name = list_view

    def get_queryset(self):
        return OshindongaIdiom.objects.all().order_by("oshindonga_idiom")

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomListView, self).get_context_data(**kwargs)
        context["heading"] = "List of Oshindonga idioms in the dictionary"
        return context


# Detail View


class EnglishWordDetailView(generic.DetailView):
    model = EnglishWord
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(EnglishWordDetailView, self).get_context_data(**kwargs)
        context["heading"] = "English word detail view"
        print(context)
        return context


class OshindongaPhoneticDetailView(generic.DetailView):
    model = OshindongaPhonetic
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Oshindonga phonetic detail view"
        return context


class WordPairDetailView(generic.DetailView):
    model = WordPair
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(WordPairDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Word Pair detail view"
        synonyms = context.get("wordpair").synonyms.all()
        context["synonyms"] = [f"{pair.english_word} | {pair.oshindonga_word}" for pair in synonyms]
        return context


class WordPairDefinitionDetailView(generic.DetailView):
    model = WordPairDefinition
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(WordPairDefinitionDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Word definition detail view"
        return context


class DefinitionExampleDetailView(generic.DetailView):
    model = DefinitionExample
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(DefinitionExampleDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Definition example detail view"
        return context


class OshindongaIdiomDetailView(generic.DetailView):
    model = OshindongaIdiom
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Oshindonga idiom detail view"
        return context

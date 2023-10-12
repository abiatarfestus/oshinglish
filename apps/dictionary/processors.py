import sys

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import F, Q
from django.shortcuts import render

from .forms import SearchWordForm
from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    PartOfSpeech,
    WordPair,
    WordPairDefinition,
    UnfoundWord,
)

WORD_PAIR_QUERYSET = WordPair.objects.all().select_related("english_word")
WORD_PAIR_HISTORY_QUERYSET = WordPair.history.all().select_related(
    "history_user", "english_word"
)
WORD_PAIR_DEFINITION_QUERYSET = WordPairDefinition.objects.all().select_related(
    "word_pair__english_word"
)
WORD_PAIR_DEFINITION_HISTORY_QUERYSET = WordPairDefinition.history.all().select_related(
    "history_user", "word_pair__english_word"
)
# USER_QUERYSET = User.objects.all()


class HistoryRecord:
    """Queries the history model of the datatbase and returns querysets of each model"""

    def __init__(self):
        # A queryset of all history entries from EnglishWord (historicalenglish-word) table (same applies below)
        self.english = []
        self.oshindonga = []
        self.definition = []
        self.example = []
        self.idiom = []
        self.usernames = []  # Holds all usernames from all history entries
        self.unique_usernames = (
            set()
        )  # Holds unique usernames (set) from the usernames list

    def reset_history(self):
        self.english = []
        self.oshindonga = []
        self.definition = []
        self.example = []
        self.idiom = []
        self.usernames = []
        self.unique_usernames = set()
        return

    def english_history(self):
        self.english = EnglishWord.history.all()
        user_ids = []  # Holds user ids of historical_users (created/modifiers)
        for (
            queryset
        ) in (
            self.english
        ):  # Loops through the querysets and take the user id if it's not null/none
            if (
                queryset.history_user_id != None
            ):  # Appends the the user id to user_ids list
                user_ids.append(queryset.history_user_id)
        for (
            user_id
        ) in (
            user_ids
        ):  # Loops through user ids and matches them to users to obtain usernames
            # Holds a user object from the User model
            user = User.objects.get(id=user_id)
            # Appends the username to the usernames list
            self.usernames.append(user.username)
        # Updates the unique_usernames set with usernames
        self.unique_usernames.update(self.usernames)
        # return self.english  # Returns a queryset of EnglishWord historical objects/records
        return

    def oshindonga_history(self):
        self.oshindonga = WORD_PAIR_HISTORY_QUERYSET
        user_ids = []
        for queryset in self.oshindonga:
            if queryset.history_user_id != None:
                user_ids.append(queryset.history_user_id)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        # return self.oshindonga
        return

    def definition_history(self):
        # self.definition = WordPairDefinition.history.all()
        self.definition = WORD_PAIR_DEFINITION_HISTORY_QUERYSET
        user_ids = []
        for queryset in self.definition:
            if queryset.history_user_id != None:
                user_ids.append(queryset.history_user_id)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        # return self.definition
        return

    def example_history(self):
        self.example = DefinitionExample.history.all()
        user_ids = []
        for queryset in self.example:
            if queryset.history_user_id != None:
                user_ids.append(queryset.history_user_id)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        # return self.example
        return

    def idiom_history(self):
        self.idiom = OshindongaIdiom.history.all()
        user_ids = []
        for queryset in self.idiom:
            if queryset.history_user_id != None:
                user_ids.append(queryset.history_user_id)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        # return self.idiom
        return

    def get_contributors(self, num=None):
        self.reset_history()
        self.english_history()
        self.oshindonga_history()
        self.definition_history()
        self.example_history()
        self.idiom_history()
        # Holds a list of tuples of (#of modifications, username)
        contributors = []
        for username in self.unique_usernames:
            contributors.append((self.usernames.count(username), username))

        def getKey(item):
            return item[0]

        # Reverse sorts the list of tuples by 1st tuple item (#of mod..)
        contributors.sort(key=getKey, reverse=True)
        # num determines the #of contributors to display
        top_contributors = contributors[:num]
        return top_contributors

    def get_user_contribution(self, user):
        english_contribution = 0
        oshindonga_contribution = 0
        definition_contribution = 0
        example_contribution = 0
        idiom_contribution = 0
        current_user_id = user.id
        self.reset_history()
        self.english_history()
        self.oshindonga_history()
        self.definition_history()
        self.example_history()
        self.idiom_history()
        for queryset in self.english:
            if queryset.history_user_id == current_user_id:
                english_contribution += 1
        for queryset in self.oshindonga:
            if queryset.history_user_id == current_user_id:
                oshindonga_contribution += 1
        for queryset in self.definition:
            if queryset.history_user_id == current_user_id:
                definition_contribution += 1
        for queryset in self.example:
            if queryset.history_user_id == current_user_id:
                example_contribution += 1
        for queryset in self.idiom:
            if queryset.history_user_id == current_user_id:
                idiom_contribution += 1
        total = (
            english_contribution
            + oshindonga_contribution
            + definition_contribution
            + example_contribution
            + idiom_contribution
        )
        return [
            english_contribution,
            oshindonga_contribution,
            definition_contribution,
            example_contribution,
            idiom_contribution,
            total,
        ]


class SearchDefinition:
    """
    Searches for a word and returns its definition and example if found, otherwise returns no word,
    translation, definition or example found.
    """

    def __init__(self, request):
        self.request = request
        self.history = HistoryRecord()
        self.form = SearchWordForm(self.request.GET)
        self.context = {
            "form": "",
            "searched_word": "",
            "definitions": "",
            "examples": "",
            "suggested_searches": EnglishWord.objects.order_by("?")[:8],
            "top_contributors": self.history.get_contributors(10),
            "idioms": "",
            "total_english": EnglishWord.objects.count(),
            # "total_oshindonga": WordPair.objects.count(),
            "total_oshindonga": WORD_PAIR_QUERYSET.count(),
            # "total_definitions": WordPairDefinition.objects.filter(~Q(oshindonga_definition="") | ~Q(english_definition="")).count(),
            "total_definitions": WORD_PAIR_DEFINITION_QUERYSET.filter(
                ~Q(oshindonga_definition="") | ~Q(english_definition="")
            ).count(),
            # "total_POS_tags": WordPairDefinition.objects.filter(~Q(part_of_speech="")).count(),
            # "total_POS_tags": WORD_PAIR_DEFINITION_QUERYSET.filter(
            #     ~Q(part_of_speech="")
            # ).count(),
            "total_examples": DefinitionExample.objects.count(),
            "total_idioms": OshindongaIdiom.objects.count(),
        }
        # Note: order_by('?') queries may be expensive and slow, depending on the database backend you’re using

    def save_unfound_word(self, word, language):
        """
        Takes in the word searched and the language input of a search that returned no word found and creates a
        new record in the UnfoundWord table or increment the search count if the word already exists.
        """
        try:
            new_unfound = UnfoundWord(word=word.lower(), language=language)
            new_unfound.save()
        except IntegrityError:
            UnfoundWord.objects.filter(word=word.lower(), language=language).update(
                search_count=F("search_count") + 1
            )
            # existing_word.search_count = F('search_count') + 1
            # existing_word.save()
        except:
            print(sys.exc_info()[0], "occurred.")

    def search_examples(self, definitions_pks):
        """
        Takes in a list of pks of found definitions and search if examples exist and return example objects.
        """
        example_querysets = []
        for definition_pk in definitions_pks:
            example_queryset = DefinitionExample.objects.filter(
                definition_id=definition_pk
            )
            # If no definition found, an empty queryset is appended
            example_querysets.append(example_queryset)
        example_objects = []
        no_example_found = "No example found"
        for example_queryset in example_querysets:
            if len(example_queryset) > 0:  # If it's not an empty querset
                # Loop through the queryset to extract objects
                for i in range(len(example_queryset)):
                    example_objects.append(example_queryset[i])
            else:
                example_objects.append(no_example_found)
        self.context["examples"] = example_objects
        # return render(self.request, 'dictionary/search.html', self.context)

    def search_definitions(self, word_pairs_pks):
        """
        Takes in a list pks of word pairs and return a list of pks of all definitions found.
        """
        # ----------Idiom------------#
        idiom_querysets = []
        for pair_pk in word_pairs_pks:
            idiom_queryset = OshindongaIdiom.objects.filter(word_pair_id=pair_pk)
            # If no definition found, an empty queryset is appended
            idiom_querysets.append(idiom_queryset)
        self.context["idioms"] = idiom_querysets

        # ----------Definition------------#
        definition_querysets = []
        for pair_pk in word_pairs_pks:
            # definition_queryset = WordPairDefinition.objects.filter(word_pair_id=pair_pk)
            definition_queryset = WORD_PAIR_DEFINITION_QUERYSET.filter(
                word_pair_id=pair_pk
            )
            # If no definition found, an empty queryset is appended
            definition_querysets.append(definition_queryset)
        definition_objects = []
        no_definition_found = "No definition found"
        for definition_queryset in definition_querysets:
            if len(definition_queryset) > 0:  # If it's not an empty queryset
                for i in range(len(definition_queryset)):
                    definition_objects.append(definition_queryset[i])
            else:
                definition_objects.append(no_definition_found)
        self.context["definitions"] = definition_objects
        self.context["nouns_list"] = ["NN", "NNS", "NNP", "NNPS"]
        self.context["verbs_list"] = ["VB", "VBD", "VBG", "VBN", "VBZ", "VBP"]
        definitions_pks = []
        for i in range(len(definition_objects)):
            if definition_objects[i] != no_definition_found:
                definitions_pks.append(definition_objects[i].id)
        self.search_examples(definitions_pks)

    def search_word_pairs(self, eng_word_pk):
        """
        Using the English word pk (foreignkey id) search for English|Oshindonga pairs and return a list of pks of all pair objects found.
        """
        # Return a queryset of all word pairs with the searched word
        # word_pairs = WordPair.objects.filter(english_word_id=eng_word_pk)
        word_pairs = WORD_PAIR_QUERYSET.filter(english_word_id=eng_word_pk)
        if len(word_pairs) == 0:
            self.context["searched_word"] = [
                "The word you searched is not yet translated into Oshindonga."
            ]
            # return render(self.request, 'dictionary/search.html', self.context)
        else:
            self.context["searched_word"] = word_pairs
            # Extract pk/id of each pair and save them in a list
            word_pairs_pks = [word_pair.id for word_pair in word_pairs]
            self.search_definitions(word_pairs_pks)

    def search_word(self):
        """
        Check if the searched English word exists in the English model. If found return its pk
        """
        # Reset context variables when visiting for the first time or refreshing the page
        # self.context['searched_word'] = ''
        # self.context['definitions'] = ''
        # self.context['examples'] = ''
        # self.form = SearchWordForm(self.request.GET)
        self.context["form"] = self.form
        if self.form.is_valid():
            word = self.form.cleaned_data["search_word"]
            language = self.form.cleaned_data["input_language"]
            if language == "English":
                try:
                    # Search within English model, and if foud:
                    eng_word = EnglishWord.objects.get(word=word)
                    # Get the the id/pk of the word found to be used in Oshindonga model
                    eng_word_pk = eng_word.id
                except EnglishWord.DoesNotExist:
                    self.save_unfound_word(word, language)
                    self.context["searched_word"] = [
                        "The word you searched was not found."
                    ]
                    # render(self.request, 'dictionary/search.html', self.context)
                    return
                self.search_word_pairs(eng_word_pk)
                # return render(self.request, 'dictionary/search.html', self.context)
            else:
                # word_pairs = WordPair.objects.filter(
                #     word=word
                # )  # Search in WordPair using the word
                word_pairs = WORD_PAIR_QUERYSET.filter(
                    word=word
                )  # Search in WordPair using the word
                if len(word_pairs) == 0:
                    self.save_unfound_word(word, language)
                    self.context["searched_word"] = [
                        "Oshitya shi wa kongo ina shi monika."
                    ]
                    # return render(self.request, 'dictionary/search.html', self.context)
                else:
                    self.context["searched_word"] = word_pairs
                    # Extract pk/id of each pair and save them in a list
                    word_pairs_pks = [word_pair.id for word_pair in word_pairs]
                    self.search_definitions(word_pairs_pks)
        # else:
        #     return render(self.request, 'dictionary/search.html', self.context)

    # Search for a suggested word

    def search_suggested(self, pk):
        """
        Search for a word from suggested searches
        """
        # self.form = SearchWordForm(self.request.GET)
        self.context["form"] = self.form
        # Return a queryset of all word pairs with the searched word
        # word_pairs = WordPair.objects.filter(english_word_id=pk)
        word_pairs = WORD_PAIR_QUERYSET.filter(english_word_id=pk)
        if len(word_pairs) == 0:
            self.context["searched_word"] = [
                "The word you searched is not yet translated into Oshindonga."
            ]
            # return render(self.request, 'dictionary/search.html', self.context)
        else:
            self.context["searched_word"] = word_pairs
            # Extract pk/id of each pair and save them in a list
            word_pairs_pks = [word_pair.id for word_pair in word_pairs]
            self.search_definitions(word_pairs_pks)

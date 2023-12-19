"""
Constants to be used in the app, to be imported by views and forms modules.
"""
from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    WordPair,
    WordPairDefinition,
    PartOfSpeech
)

# QuerySets
ALL_ENGLISH_WORDS = EnglishWord.objects.values_list(
    "id",
    "word",
    named=True
)
ALL_WORD_PAIRS = WordPair.objects.values_list(
    "id",
    "english_word__id",
    "english_word__word",
    "oshindonga_word",
    "part_of_speech__english_name",
    "synonyms__oshindonga_word",
    named=True
).prefetch_related(
    "english_word",
    "root",
    "part_of_speech",
    "synonyms"
)
# ALL_OSHINDONGA_WORDS = [pair.oshindonga_word for pair in ALL_WORD_PAIRS]
ALL_DEFINITIONS = WordPairDefinition.objects.only("id", "word_pair").prefetch_related("word_pair")
ALL_EXAMPLES = DefinitionExample.objects.only("id", "definition").prefetch_related("definition")
ALL_PARTS_OF_SPEECH = PartOfSpeech.objects.values_list(
    "id",
    "code",
    "english_name",
    named=True
)
NEW_ENGLISH_WORDS = [word for word in ALL_ENGLISH_WORDS.order_by("-time_added")[:5]]
NEW_WORD_PAIRS = [pair for pair in ALL_WORD_PAIRS.order_by("-time_added")[:5]]
# NEW_OSHINDONGA_WORDS = [ALL_OSHINDONGA_WORDS[:5]]
NEW_PHONETICS = OshindongaPhonetic.objects.prefetch_related(
    "word_pair"
).order_by("-time_added")[:5]
# NEW_PHONETICS = [phonetic for phonetic in ALL_PHONETICS[:5]]
NEW_DEFINITIONS = [definition for definition in ALL_DEFINITIONS.order_by("-time_added")[:5]]
NEW_EXAMPLES = [example for example in ALL_EXAMPLES.order_by("-time_added")[:5]]
NEW_OSHINDONGA_IDIOMS = OshindongaIdiom.objects.prefetch_related("word_pair").order_by("-time_added")[:10]

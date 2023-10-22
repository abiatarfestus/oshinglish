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
)

# QuerySets
ALL_ENGLISH_WORDS = EnglishWord.objects.order_by("-time_added")
ALL_WORD_PAIRS = WordPair.objects.prefetch_related(
    "english_word",
    "root",
    "part_of_speech",
    "synonyms"
).order_by("-time_added")
# ALL_OSHINDONGA_WORDS = [pair.oshindonga_word for pair in ALL_WORD_PAIRS]
ALL_DEFINITIONS = WordPairDefinition.objects.only("id", "word_pair").prefetch_related("word_pair").order_by("-time_added")
ALL_EXAMPLES = DefinitionExample.objects.only("id", "definition").prefetch_related("definition").order_by("-time_added")
NEW_ENGLISH_WORDS = [word for word in ALL_ENGLISH_WORDS[:5]]
NEW_WORD_PAIRS = [pair for pair in ALL_WORD_PAIRS[:5]]
# NEW_OSHINDONGA_WORDS = [ALL_OSHINDONGA_WORDS[:5]]
NEW_PHONETICS = OshindongaPhonetic.objects.prefetch_related(
    "word_pair"
).order_by("-time_added")[:5]
# NEW_PHONETICS = [phonetic for phonetic in ALL_PHONETICS[:5]]
NEW_DEFINITIONS = [definition for definition in ALL_DEFINITIONS[:5]]
NEW_EXAMPLES = [example for example in ALL_EXAMPLES[:5]]
NEW_OSHINDONGA_IDIOMS = OshindongaIdiom.objects.prefetch_related("word_pair").order_by("-time_added")[:10]
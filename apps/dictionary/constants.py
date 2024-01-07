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
ALL_ENGLISH_WORDS = EnglishWord.objects.all().order_by("-time_added")   #.values("id", "word")
ALL_WORD_PAIRS = WordPair.objects.all().order_by("-time_added") #.values("id", "oshindonga_word", "english_word")
ALL_DEFINITIONS = WordPairDefinition.objects.all().order_by("-time_added")  #.values("id", "word_pair")
ALL_EXAMPLES = DefinitionExample.objects.all().order_by("-time_added")  #.values("id", "definition")
ALL_PARTS_OF_SPEECH = PartOfSpeech.objects.all()
ALL_OSHINDONGA_IDIOMS = OshindongaIdiom.objects.all().order_by("-time_added")   #.values("id", "word_pair")
ALL_PHONETICS = OshindongaPhonetic.objects.all().order_by("-time_added")    #.values("id", "word_pair")

from rest_framework import permissions, viewsets

from apps.dictionary.models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    PartOfSpeech,
    WordPair,
    WordPairDefinition,
)

from .serializers import (
    DefinitionExampleSerializer,
    EnglishWordSerializer,
    OshindongaIdiomSerializer,
    OshindongaPhoneticSerializer,
    PartOfSpeechSerializer,
    WordPairDefinitionSerializer,
    WordPairSerializer,
)


class EnglishWordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows English words to be viewed or edited.
    """

    queryset = EnglishWord.objects.all().order_by("word")
    serializer_class = EnglishWordSerializer
    permission_classes = [permissions.IsAuthenticated]


class WordPairViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga words to be viewed or edited.
    """

    queryset = WordPair.objects.all().order_by("oshindonga_word")
    serializer_class = WordPairSerializer
    permission_classes = [permissions.IsAuthenticated]


class OshindongaPhoneticViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga phonetics to be viewed or edited.
    """

    queryset = OshindongaPhonetic.objects.all().order_by("word_pair__oshindonga_word")
    serializer_class = OshindongaPhoneticSerializer
    permission_classes = [permissions.IsAuthenticated]


class WordPairDefinitionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows word pairdefinition to be viewed or edited.
    """

    queryset = WordPairDefinition.objects.all().order_by(
        "word_pair__english_word__word"
    )
    serializer_class = WordPairDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]


class DefinitionExampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows word definition example to be viewed or edited.
    """

    queryset = DefinitionExample.objects.all().order_by("id")
    serializer_class = DefinitionExampleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PartOfSpeechViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows part of speech to be viewed or edited.
    """

    queryset = PartOfSpeech.objects.all().order_by("code")
    serializer_class = PartOfSpeechSerializer
    permission_classes = [permissions.IsAuthenticated]


class OshindongaIdiomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Oshindonga idiom to be viewed or edited.
    """

    queryset = OshindongaIdiom.objects.all().order_by("word_pair__oshindonga_word")
    serializer_class = OshindongaIdiomSerializer
    permission_classes = [permissions.IsAuthenticated]

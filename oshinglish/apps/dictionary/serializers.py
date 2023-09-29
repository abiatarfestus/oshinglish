from rest_framework import serializers

from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    PartOfSpeech,
    WordPair,
    WordPairDefinition,
)


class EnglishWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ["url", "id", "word", "word_case"]


class WordPairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordPair
        fields = [
            "url",
            "id",
            "english_word",
            "oshindonga_word",
            "root",
            "part_of_speech",
            "synonyms",
        ]


class OshindongaPhoneticSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OshindongaPhonetic
        fields = [
            "url",
            "id",
            "word_pair",
            "oshindonga_phonetics",
            "oshindonga_pronunciation",
        ]


class OshindongaIdiomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OshindongaIdiom
        fields = ["url", "id", "word_pair", "oshindonga_idiom", "meaning"]


class WordPairDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WordPairDefinition
        fields = [
            "url",
            "id",
            "word_pair",
            "english_definition",
            "oshindonga_definition",
        ]


class DefinitionExampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefinitionExample
        fields = ["url", "id", "definition", "english_example", "oshindonga_example"]


class PartOfSpeechSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartOfSpeech
        fields = ["url", "id", "code", "english_name", "oshindonga_name", "example"]

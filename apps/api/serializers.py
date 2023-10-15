from rest_framework import serializers

from apps.dictionary.models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    PartOfSpeech,
    WordPair,
    WordPairDefinition,
)


class EnglishWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishWord
        fields = ["id", "word", "word_case"]


class WordPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordPair
        fields = [
            'id',
            "english_word",
            "oshindonga_word",
            "root",
            "part_of_speech",
            "synonyms",
        ]


class OshindongaPhoneticSerializer(serializers.ModelSerializer):
    class Meta:
        model = OshindongaPhonetic
        fields = [
            "id",
            "word_pair",
            "oshindonga_phonetics",
            "oshindonga_pronunciation",
        ]


class OshindongaIdiomSerializer(serializers.ModelSerializer):
    class Meta:
        model = OshindongaIdiom
        fields = ["id", "word_pair", "oshindonga_idiom", "meaning"]


class WordPairDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordPairDefinition
        fields = [
            "id",
            "word_pair",
            "english_definition",
            "oshindonga_definition",
        ]


class DefinitionExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefinitionExample
        fields = [
            "id",
            "definition",
            "english_example",
            "oshindonga_example"
        ]


class PartOfSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfSpeech
        fields = ["id", "code", "english_name", "oshindonga_name", "example"]

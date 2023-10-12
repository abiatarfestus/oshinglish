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
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:english-word-detail',
        read_only=True
    )
    class Meta:
        model = EnglishWord
        fields = ["url", "word", "word_case"]


class WordPairSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:word-pair-detail',
        read_only=True
    )
    english_word = serializers.HyperlinkedRelatedField(
        view_name='dictionary:english-word-detail',
        read_only=True
    )
    root = serializers.HyperlinkedRelatedField(
        view_name='dictionary:word-pair-detail',
        read_only=True
    )
    part_of_speech = serializers.HyperlinkedRelatedField(
        view_name='dictionary:part-of-speech-detail',
        read_only=True
    )
    synonyms = serializers.HyperlinkedRelatedField(
        view_name='dictionary:part-of-speech-detail',
        many=True,
        read_only=True
    )
    class Meta:
        model = WordPair
        fields = [
            'url',
            "english_word",
            "oshindonga_word",
            "root",
            "part_of_speech",
            "synonyms",
        ]

class OshindongaPhoneticSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:oshindonga-phonetic-detail',
        read_only=True
    )
    word_pair = serializers.HyperlinkedRelatedField(
        view_name='dictionary:word-pair-detail',
        read_only=True
    )
    class Meta:
        model = OshindongaPhonetic
        fields = [
            "url",
            "word_pair",
            "oshindonga_phonetics",
            "oshindonga_pronunciation",
        ]


class OshindongaIdiomSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:oshindonga-idiom-detail',
        read_only=True
    )
    word_pair = serializers.HyperlinkedRelatedField(
        view_name='dictionary:word-pair-detail',
        read_only=True
    )
    class Meta:
        model = OshindongaIdiom
        fields = ["url", "word_pair", "oshindonga_idiom", "meaning"]


class WordPairDefinitionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:word-pair-definition-detail',
        read_only=True
    )
    word_pair = serializers.HyperlinkedRelatedField(
        view_name='dictionary:word-pair-detail',
        read_only=True
    )
    class Meta:
        model = WordPairDefinition
        fields = [
            "url",
            "word_pair",
            "english_definition",
            "oshindonga_definition",
        ]


class DefinitionExampleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:definition-example-detail',
        read_only=True
    )
    definition = serializers.HyperlinkedRelatedField(
        view_name='dictionary:word-pair-definition-detail',
        read_only=True
    )
    class Meta:
        model = DefinitionExample
        fields = [
            "url",
            "definition",
            "english_example",
            "oshindonga_example"
        ]


class PartOfSpeechSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dictionary:part-of-speech-detail',
        read_only=True
    )
    class Meta:
        model = PartOfSpeech
        fields = ["url", "code", "english_name", "oshindonga_name", "example"]

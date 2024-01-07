from django.db import models
from django.db.models import F  # For referencing fields on the same model
from django.urls import reverse
from simple_history.models import HistoricalRecords

# Module level functions and variable


class AuthAndTimeTracker(models.Model):
    """
    An abstract base class for adding instance creation and modification time as well as modification history.
    To be inherited by all models.
    """

    time_added = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class EnglishWord(AuthAndTimeTracker):
    """
    A model that adds and modifies English words in the database
    """

    ABBREVIATION = "Abbreviation"
    PROPER_NOUN = "Proper Noun"
    NORMAL = "Normal"
    WORD_CASE = [
        (ABBREVIATION, "Abbreviation"),
        (PROPER_NOUN, "Proper Noun"),
        (NORMAL, "Normal"),
    ]
    word = models.CharField(
        unique=True,
        max_length=50,
        error_messages={
            "unique": "The English word you entered already exists in the dictionary."
        },
    )
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE,
        default=NORMAL,
        help_text="Indicate whether the word you are entering is a normal word, abbretiation or proper noun.",
    )

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        # from django.urls import reverse
        return reverse("dictionary:english-word-detail", args=[str(self.id)])
        # return reverse('dictionary:english-create')


class PartOfSpeech(AuthAndTimeTracker):
    """
    A model for part of speech
    """

    code = models.CharField(max_length=4, blank=False, null=False, unique=True)
    english_name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    oshindonga_name = models.CharField(max_length=50, blank=True, null=True)
    example = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.english_name} | {self.oshindonga_name}"

    def get_absolute_url(self):
        return reverse("dictionary:part-of-speech-detail", args=[str(self.id)])


class WordPair(AuthAndTimeTracker):
    """
    A model that builds word pairs by adding and modifying Oshindonga words.
    """

    # objects = models.Manager()
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    oshindonga_word = models.CharField(unique=False, max_length=50)
    root = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    part_of_speech = models.ForeignKey(
        PartOfSpeech, on_delete=models.SET_NULL, blank=True, null=True
    )
    synonyms = models.ManyToManyField("self")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["english_word", "oshindonga_word", "part_of_speech"],
                name="unique_word_pair",
            )
        ]

    def __str__(self):
        return f"{self.english_word} | {self.oshindonga_word} {[self.id]}"

    def get_absolute_url(self):
        return reverse("dictionary:word-pair-detail", args=[str(self.id)])


class WordPairDefinition(AuthAndTimeTracker):
    """
    A model for word pair definitions.
    """

    word_pair = models.ForeignKey(
        WordPair, on_delete=models.CASCADE, related_name="definitions"
    )
    english_definition = models.CharField(max_length=255, blank=True)
    oshindonga_definition = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.word_pair}: {[self.id]}"

    def get_absolute_url(self):
        return reverse("dictionary:word-definition-detail", args=[str(self.id)])


class DefinitionExample(AuthAndTimeTracker):
    """
    A model that adds and modifies exmples to word definitions.
    """

    definition = models.ForeignKey(WordPairDefinition, on_delete=models.CASCADE)
    english_example = models.CharField(max_length=255)
    oshindonga_example = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % (self.definition)

    def get_absolute_url(self):
        return reverse("dictionary:definition-example-detail", args=[str(self.id)])


class OshindongaIdiom(AuthAndTimeTracker):
    """
    A model that adds and modifies idioms for Oshindonga words.
    """

    word_pair = models.ForeignKey(WordPair, on_delete=models.CASCADE)
    oshindonga_idiom = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.word_pair)

    def get_absolute_url(self):
        return reverse("dictionary:oshindonga-idiom-detail", args=[str(self.id)])


class OshindongaPhonetic(AuthAndTimeTracker):
    """
    A model that adds and modifies Oshindonga word phonetic characteristics in the database.
    """

    word_pair = models.OneToOneField(WordPair, on_delete=models.CASCADE)
    oshindonga_phonetics = models.CharField(max_length=50, null=False, blank=False)
    oshindonga_pronunciation = models.FileField(
        upload_to="oshindonga_pronunciations", blank=True
    )

    def __str__(self):
        return f"{self.word_pair.oshindonga_word} | {self.oshindonga_phonetics}"

    def get_absolute_url(self):
        # from django.urls import reverse
        # url pattern/template not yet implemented
        return reverse("dictionary:phonetic-detail", args=[str(self.id)])
        # return reverse('dictionary:oshindonga-create')


class UnfoundWord(models.Model):
    """
    A model that records words that were searched, but no found in the dictionary.
    """

    word = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    time_searched = models.DateTimeField(auto_now_add=True)
    search_count = models.IntegerField(default=1)
    added_to_dict = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "language"], name="unique_unfound_word"
            )
        ]

    def __str__(self):
        return f"{self.word}: {self.language}"

    def get_absolute_url(self):
        return reverse("dictionary:unfound-word-detail", args=[str(self.id)])

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    PartOfSpeech,
    OshindongaPhonetic,
    WordPair,
    WordPairDefinition,
    UnfoundWord,
)

# Register your models here.

class EnglishWordAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("word", "id")
    ordering = ("word",)
    search_fields = ("word",)


class WordPairAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("english_word", "oshindonga_word", "root", "part_of_speech", "id")
    list_filter = ("part_of_speech",)
    ordering = ("english_word",)
    raw_id_fields = ("english_word", "root", "part_of_speech")
    search_fields = (
        "english_word__word",
        "root__root",
        "part_of_speech__code"
    )


class WordPairDefinitionAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    # inlines = [ReviewInline]
    list_display = ("word_pair", "id")
    list_filter = ("word_pair",)
    ordering = ("word_pair",)
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = (
        "word_pair__english_word__word",
        "word_pair__oshindonga_word__word",
    )


class DefinitionExampleAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("definition", "id")
    ordering = ("definition",)
    raw_id_fields = ("definition",)
    search_fields = (
        "definition__word_pair__english_word__word",
        "definition__word_pair__oshindonga_word",
    )


class OshindongaIdiomAdmin(SimpleHistoryAdmin):
    date_hierarchy = "time_added"
    list_display = ("word_pair", "oshindonga_idiom", "id")
    ordering = ("word_pair",)
    raw_id_fields = ("word_pair",)
    search_fields = (
        "word_pair__english_word__word",
        "word_pair__oshindonga_word",
    )


admin.site.register(EnglishWord, EnglishWordAdmin)
admin.site.register(WordPair, WordPairAdmin)
admin.site.register(WordPairDefinition, WordPairDefinitionAdmin)
admin.site.register(DefinitionExample, DefinitionExampleAdmin)
admin.site.register(OshindongaIdiom, OshindongaIdiomAdmin)
admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)

# admin.site.register(EnglishWord, SimpleHistoryAdmin)
# admin.site.register(OshindongaWord, SimpleHistoryAdmin)
# admin.site.register(WordDefinition, SimpleHistoryAdmin)
# admin.site.register(DefinitionExample, SimpleHistoryAdmin)
# admin.site.register(OshindongaIdiom, SimpleHistoryAdmin)
# admin.site.register(OshindongaPhonetic, SimpleHistoryAdmin)

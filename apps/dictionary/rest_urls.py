from django.urls import include, path
from rest_framework import routers

from . import rest_views

router = routers.DefaultRouter()
# router.register(r"english_words", rest_views.EnglishWordViewSet, basename="english-word")
# router.register(r"oshindonga_words", rest_views.WordPairViewSet, basename="word-pair")
# router.register(r"oshindonga_phonetics", rest_views.OshindongaPhoneticViewSet, basename="oshindonga-phonetic")
# router.register(r"word_pair_definitions", rest_views.WordPairDefinitionViewSet, basename="word-pair-definition")
# router.register(r"definition_examples", rest_views.DefinitionExampleViewSet, basename="definition-example")
# router.register(r"oshindonga_idioms", rest_views.OshindongaIdiomViewSet, basename="oshindonga-idiom")
# router.register(r"parts_of_speech", rest_views.PartOfSpeechViewSet, basename="part-of-speech")
router.register(r"english_words", rest_views.EnglishWordViewSet)
router.register(r"word_pairs", rest_views.WordPairViewSet)
router.register(r"oshindonga_phonetics", rest_views.OshindongaPhoneticViewSet)
router.register(r"word_pair_definitions", rest_views.WordPairDefinitionViewSet)
router.register(r"definition_examples", rest_views.DefinitionExampleViewSet)
router.register(r"oshindonga_idioms", rest_views.OshindongaIdiomViewSet)
router.register(r"parts_of_speech", rest_views.PartOfSpeechViewSet)

app_name = "dictionary"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    # path("search/", rest_views.search_word, name="search"),
    path("search/<int:pk>", rest_views.search_suggested_word, name="search-suggested-word"),
]

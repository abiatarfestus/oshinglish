from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"english_words", views.EnglishWordViewSet, basename="english-word")
router.register(r"word_pairs", views.WordPairViewSet, basename="word-pair")
router.register(r"oshindonga_phonetics", views.OshindongaPhoneticViewSet, basename="oshindonga-phonetic")
router.register(r"word_pair_definitions", views.WordPairDefinitionViewSet, basename="word-pair-definition")
router.register(r"definition_examples", views.DefinitionExampleViewSet, basename="definition-example")
router.register(r"oshindonga_idioms", views.OshindongaIdiomViewSet, basename="oshindonga-idiom")
router.register(r"parts_of_speech", views.PartOfSpeechViewSet, basename="part-of-speech")

app_name = "api"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("root/", include(router.urls)),
    # path("search/<int:pk>", views.search_suggested_word, name="search-suggested-word"),
]

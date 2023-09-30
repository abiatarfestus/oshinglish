from django.urls import include, path
from rest_framework import routers

from . import rest_views

router = routers.DefaultRouter()
router.register(r"english_words", rest_views.EnglishWordViewSet, basename="english-word")
router.register(r"oshindonga_words", rest_views.WordPairViewSet, basename="word-pair")
router.register(r"oshindonga_phonetics", rest_views.OshindongaPhoneticViewSet)

app_name = "dictionary"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    path("search/", rest_views.search_word, name="search"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

from django.urls import path

from . import views

app_name = "dictionary"
urlpatterns = [
    path("search/", views.search_word, name="search"),
    path("search/<int:pk>", views.search_suggested_word, name="search-suggested-word"),
    path("ajax-search/", views.search_with_ajax, name="ajax-search"),
    # Create Views
    path("english/create/", views.EnglishWordCreate.as_view(), name="add-english-word"),
    path(
        "oshindonga-phonetic/create/",
        views.OshindongaPhoneticCreate.as_view(),
        name="add-oshindonga-phonetic",
    ),
    path(
        "word-pair/create/",
        views.WordPairCreate.as_view(),
        name="add-word-pair",
    ),
    path(
        "word-pair-definition/create/",
        views.WordPairDefinitionCreate.as_view(),
        name="add-definition",
    ),
    path(
        "definition-example/create/",
        views.DefinitionExampleCreate.as_view(),
        name="add-definition-example",
    ),
    path(
        "oshindonga-idiom/create/",
        views.OshindongaIdiomCreate.as_view(),
        name="add-oshindonga-idiom",
    ),
    # Update Views
    path(
        "english-word/update/<int:pk>/",
        views.EnglishWordUpdate.as_view(),
        name="update-english-word",
    ),
    path(
        "oshindonga-phonetic/update/<int:pk>/",
        views.OshindongaPhoneticUpdate.as_view(),
        name="update-oshindonga-phonetic",
    ),
    path(
        "word-pair/update/<int:pk>/",
        views.WordPairUpdate.as_view(),
        name="update-word-pair",
    ),
    path(
        "word-pair-definition/update/<int:pk>/",
        views.WordPairDefinitionUpdate.as_view(),
        name="update-definition",
    ),
    path(
        "definition-example/update/<int:pk>/",
        views.DefinitionExampleUpdate.as_view(),
        name="update-definition-example",
    ),
    path(
        "oshindonga-idiom/update/<int:pk>/",
        views.OshindongaIdiomUpdate.as_view(),
        name="update-oshindonga-idiom",
    ),
    # List Views
    path("english-words/", views.EnglishWordListView.as_view(), name="english-words"),
    path(
        "oshindonga-phonetics/",
        views.OshindongaPhoneticListView.as_view(),
        name="oshindonga-phonetics",
    ),
    path(
        "word-pairs/",
        views.WordPairListView.as_view(),
        name="word-pairs",
    ),
    path(
        "oshindonga-idioms/",
        views.OshindongaIdiomListView.as_view(),
        name="oshindonga-idioms",
    ),
    # Detail Views
    path(
        "english-word/<int:pk>",
        views.EnglishWordDetailView.as_view(),
        name="english-word-detail",
    ),
    path(
        "oshindonga-phonetic/<int:pk>",
        views.OshindongaPhoneticDetailView.as_view(),
        name="oshindonga-phonetic-detail",
    ),
    path(
        "word-pair/<int:pk>",
        views.WordPairDetailView.as_view(),
        name="word-pair-detail",
    ),
    path(
        "word-pair-definition/<int:pk>",
        views.WordPairDefinitionDetailView.as_view(),
        name="word-pair-definition-detail",
    ),
    path(
        "definition-example/<int:pk>",
        views.DefinitionExampleDetailView.as_view(),
        name="definition-example-detail",
    ),
    path(
        "oshindonga-idiom/<int:pk>",
        views.OshindongaIdiomDetailView.as_view(),
        name="oshindonga-idiom-detail",
    ),
]

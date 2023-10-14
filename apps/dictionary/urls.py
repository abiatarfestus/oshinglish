from django.urls import path

from . import views

app_name = "dictionary"
urlpatterns = [
    #     path('', views.index, name="index"),
    path("search/", views.search_word, name="search"),
    path("search/<int:pk>", views.search_suggested_word, name="search-suggested-word"),
    # Create Views
    path("english/create/", views.EnglishWordCreate.as_view(), name="english-create"),
    path(
        "oshindonga-phonetic/create/",
        views.OshindongaPhoneticCreate.as_view(),
        name="oshindonga-phonetic-create",
    ),
    path(
        "oshindonga/create/",
        views.WordPairCreate.as_view(),
        name="oshindonga-create",
    ),
    path(
        "definition/create/",
        views.WordPairDefinitionCreate.as_view(),
        name="definition-create",
    ),
    path(
        "example/create/",
        views.DefinitionExampleCreate.as_view(),
        name="example-create",
    ),
    path(
        "oshindonga-idiom/create/",
        views.OshindongaIdiomCreate.as_view(),
        name="oshindonga-idiom-create",
    ),
    # Update Views
    path(
        "english/<int:pk>/update/",
        views.EnglishWordUpdate.as_view(),
        name="english-update",
    ),
    path(
        "oshindonga-phonetic/<int:pk>/update/",
        views.OshindongaPhoneticUpdate.as_view(),
        name="oshindonga-phonetic-update",
    ),
    path(
        "oshindonga/<int:pk>/update/",
        views.WordPairUpdate.as_view(),
        name="oshindonga-update",
    ),
    path(
        "definition/<int:pk>/update/",
        views.WordPairDefinitionUpdate.as_view(),
        name="definition-update",
    ),
    path(
        "example/<int:pk>/update/",
        views.DefinitionExampleUpdate.as_view(),
        name="example-update",
    ),
    path(
        "oshindonga-idiom/<int:pk>/update/",
        views.OshindongaIdiomUpdate.as_view(),
        name="oshindonga-idiom-update",
    ),
    # List Views
    path("english-words/", views.EnglishWordListView.as_view(), name="english-words"),
    path(
        "oshindonga-phonetics/",
        views.OshindongaPhoneticListView.as_view(),
        name="oshindonga-phonetics",
    ),
    path(
        "oshindonga-words/",
        views.WordPairListView.as_view(),
        name="oshindonga-words",
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
        "oshindonga-word/<int:pk>",
        views.WordPairDetailView.as_view(),
        name="oshindonga-word-detail",
    ),
    path(
        "word-definition/<int:pk>",
        views.WordPairDefinitionDetailView.as_view(),
        name="word-definition-detail",
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

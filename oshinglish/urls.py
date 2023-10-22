"""
URL configuration for oshinglish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.dictionary import views as dictionary_views

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("", dictionary_views.search_word, name="search"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("access-denied/", views.access_denied, name="access-denied"),
    path("under-construction/", views.under_construction, name="under-construction"),
    path("dictionary/", include("apps.dictionary.urls")),
    path("users/", include("apps.users.urls")),
    path("api/dictionary/", include("apps.api.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("help/", TemplateView.as_view(template_name="help.html"), name="help"),
    path(
        "privacy-policy/",
        TemplateView.as_view(template_name="oshinglish/privacy_policy.html"),
        name="privacy-policy",
    ),
    path(
        "terms-and-conditions/",
        TemplateView.as_view(template_name="oshinglish/terms_and_conditions.html"),
        name="terms-and-conditions",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

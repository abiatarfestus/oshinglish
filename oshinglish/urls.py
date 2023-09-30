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
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include(rest_urls)),
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("access-denied/", views.access_denied, name="access-denied"),
    path("under-construction/", views.under_construction, name="under-construction"),
    # path("help/", TemplateView.as_view(template_name="onestop/help.html"), name="help"),
    # path(
    #     "privacy-policy/",
    #     TemplateView.as_view(template_name="onestop/privacy_policy.html"),
    #     name="privacy-policy",
    # ),
    # path(
    #     "terms-and-conditions/",
    #     TemplateView.as_view(template_name="onestop/terms_and_conditions.html"),
    #     name="terms-and-conditions",
    # ),
    path("dictionary/", include("apps.dictionary.rest_urls")),
    path("users/", include("apps.users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

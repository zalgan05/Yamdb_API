from django.urls import include, path

from . import views

API_VERSION = "v1"

urlpatterns = [
    path("auth/signup/", views.signup, name="signup"),
]

urlpatterns = [path(f"{API_VERSION}/", include(urlpatterns))]

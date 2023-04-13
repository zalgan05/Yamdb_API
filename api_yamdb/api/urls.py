from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, signup

API_VERSION = "v1"

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path('', include(router.urls)),
]


urlpatterns = [path(f"{API_VERSION}/", include(urlpatterns))]

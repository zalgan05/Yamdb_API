from api.views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    signup,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

API_VERSION = "v1"

router = DefaultRouter()
router.register("categories/", CategoryViewSet)
router.register("genres/", GenreViewSet)  # delete запрос переделать
router.register("titles/", TitleViewSet)  # delete запрос переделать
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path('', include(router.urls)),
]


urlpatterns = [path(f"{API_VERSION}/", include(urlpatterns))]

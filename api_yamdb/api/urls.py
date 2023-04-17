from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    SingleUsersAdminViewSet,
    TitleViewSet,
    UsersAdminViewSet,
    UserSelfViewSet,
    jwt_token,
    signup,
)

API_VERSION = "v1"

router = DefaultRouter()
router.register("users", UserSelfViewSet, basename="user_self")
router.register("users", SingleUsersAdminViewSet)
router.register("users", UsersAdminViewSet)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register("titles", TitleViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/token/", jwt_token, name="jwt_token"),
    path("", include(router.urls)),
]


urlpatterns = [path(f"{API_VERSION}/", include(urlpatterns))]

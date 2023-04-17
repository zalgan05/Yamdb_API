from rest_framework import mixins, viewsets


class ListCreateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class RetrievUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]  # Убран метод PUT


class DestroyViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class AllViewSet(ListCreateViewSet, RetrievUpdateViewSet, DestroyViewSet):
    pass

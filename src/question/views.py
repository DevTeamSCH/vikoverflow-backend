from taggit.models import Tag
from rest_framework import mixins, viewsets, permissions
from . import serializers
from common.mixins import RelativeURLFieldMixin
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import UpdateAPIView, DestroyAPIView



class TagViewSet(
    RelativeURLFieldMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Tag.objects.all()

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj, created = queryset.get_or_create(**filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

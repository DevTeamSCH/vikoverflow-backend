class RelativeURLFieldMixin(object):
    def get_serializer_context(self):
        context = super(RelativeURLFieldMixin, self).get_serializer_context()
        context['request'] = None
        return context

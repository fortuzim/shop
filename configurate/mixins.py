class CustomCharFieldMixin:
    """
    Mixin for custom CharField with max_lenght=100, blank=False and null=False.
    """

    def custom_char_field(self, *args, **kwargs):
        kwargs.setdefault("max_lenght", 100)
        kwargs.setdefault("blank", False)
        kwargs.setdefault("null", False)
        return models.CharField(*args, **kwargs)

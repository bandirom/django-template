from django_filters import rest_framework as filters


class ListCharFilter(filters.BaseInFilter, filters.CharFilter):
    """Filter for django-filter lib.

    ListCharFilter returns: list[str]
    filters.CharFilter returns: str
    """

    pass

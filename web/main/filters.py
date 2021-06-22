from django_filters import rest_framework as filters


class ListCharFilter(filters.BaseInFilter, filters.CharFilter):
    """ Filter for django-filter lib
    ListCharFilter return: list[str]
    filters.CharFilter return: str
    """
    pass

from rest_framework.pagination import PageNumberPagination


class BasePageNumberPagination(PageNumberPagination):
    page_size: int = 10
    page_query_param: str = 'page'
    max_page_size: int = 100
    page_size_query_param: str = 'page_size'

from rest_framework.views import APIView
from settings.utils.pagination import DefaultPagination


class APIViewWithPagination(APIView):
    pagination_class = DefaultPagination
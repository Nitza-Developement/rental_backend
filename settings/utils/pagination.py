from rest_framework import serializers
from drf_spectacular.utils import inline_serializer, OpenApiResponse
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "pageSize"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
    
    @staticmethod
    def paginated_response_schema(serializer_class):
        inner_serializer_class = (
            serializer_class.child
            if hasattr(serializer_class, "child")
            else serializer_class
        )
        return OpenApiResponse(
            response=inline_serializer(
                name=f"Paginated{inner_serializer_class.__class__.__name__}",
                fields={
                    "count": serializers.IntegerField(),
                    "next": serializers.IntegerField(allow_null=True),
                    "previous": serializers.IntegerField(allow_null=True),
                    "results": serializer_class,
                },
            )
        )
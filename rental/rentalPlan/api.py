from drf_spectacular.utils import extend_schema, PolymorphicProxySerializer, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response

from rental.rentalPlan.models import RentalPlan
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from rental.rentalPlan.features import (
    get_rental_plans,
    create_rental_plan,
    get_rental_plan,
    delete_rental_plan,
    update_rental_plan,
)
from rental.rentalPlan.serializer import (
    CreateRentalPlanSerializer,
    RentalPlanSerializer,
    UpdateRentalPlanSerializer,
)
from settings.utils.exceptions import BadRequest400APIException, Unauthorized401APIException, NotFound404APIException
from rental.tenantUser.permissions import IsAdminTenantUser, IsAdminOrStaffTenantUser
from rental.rentalPlan.exceptions import validate_plan_and_handle_errors, ErrorPlanWithNameAlreadyExists, \
    ErrorPlanInvalidName, ErrorPlanInvalidAmount, ErrorPlanInvalidPeriodicity


class ListAndCreateRentalPlansView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='searchText', type=str,
                             description='Matches content in `name`, `periodicity` or `amount` fields, ignoring case ',
                             required=False),
            OpenApiParameter(name='orderBy', type=str, description='You can select between `name`, `periodicity`, `amount` or `pk`',
                             required=False),
            OpenApiParameter(name='asc', type=str, description='Ascending (`True`) or descending (`False`) order',
                             required=False),
        ],
        responses={
            200: RentalPlanSerializer(many=True),
            400: BadRequest400APIException.schema_response(),
            401: Unauthorized401APIException.schema_response()
        }
    )
    def get(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        Endpoint for listing Rental Plan
        """
        search_text = request.query_params.get("searchText", None)
        order_by = request.query_params.get("orderBy", "name")
        asc = request.query_params.get("asc", None)

        try:
            rental_plans_list = get_rental_plans(
                search_text=search_text,
                order_by=order_by,
                asc=False if asc == "False" else True,
            )

            paginator = self.pagination_class()
            paginated_rental_plans = paginator.paginate_queryset(
                rental_plans_list, request
            )
            serialized_list = RentalPlanSerializer(paginated_rental_plans, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    @extend_schema(
        request=CreateRentalPlanSerializer(),
        responses={
            201: RentalPlanSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestRentalPlan",
                serializers=[
                    ErrorPlanWithNameAlreadyExists.schema_serializers(),
                    ErrorPlanInvalidName.schema_serializers(),
                    ErrorPlanInvalidAmount.schema_serializers(),
                    ErrorPlanInvalidPeriodicity.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_rental_plan"
            ),
            401: Unauthorized401APIException.schema_response(),
        }
    )
    def post(self, request):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for creating a Rental Plan.
        """
        serializer = CreateRentalPlanSerializer(data=request.data)
        validate_plan_and_handle_errors(serializer)

        created_rental_plan = create_rental_plan(
            name=serializer.validated_data["name"],
            amount=serializer.validated_data["amount"],
            periodicity=serializer.validated_data["periodicity"],
            tenant=request.user.defaultTenantUser().tenant,
        )

        serialized_rental_plan = RentalPlanSerializer(created_rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_201_CREATED)


class GetUpdateAndDeleteARentalPlanView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAuthenticated(), IsAdminTenantUser()]
        return super().get_permissions()

    def get(self, request, rental_plan_id):
        rental_plan = get_rental_plan(rental_plan_id)

        serialized_rental_plan = RentalPlanSerializer(rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=UpdateRentalPlanSerializer,
        responses={
            200: RentalPlanSerializer,
            400: PolymorphicProxySerializer(
                component_name="BadRequestClient",
                serializers=[
                    ErrorPlanWithNameAlreadyExists.schema_serializers(),
                    ErrorPlanInvalidName.schema_serializers(),
                    ErrorPlanInvalidAmount.schema_serializers(),
                    ErrorPlanInvalidPeriodicity.schema_serializers(),
                    BadRequest400APIException.schema_serializers(),
                ],
                resource_type_field_name="error_client"
            ),
            401: Unauthorized401APIException.schema_response(),
            404: NotFound404APIException.schema_response()
        }
    )
    def put(self, request, rental_plan_id):
        """
        This method requires the user to be authenticated in order to be used.
        Authentication is performed by using a JWT (JSON Web Token) that is included
        in the HTTP request header.

        This endpoint requires the authenticated user to have the administrator, staff
        or owner role.

        Endpoint for editing a Rental Plan.
        """
        try:
            rental_plan=RentalPlan.objects.get(id=rental_plan_id)
        except (TypeError, ValueError, RentalPlan.DoesNotExist):
            raise NotFound404APIException(f"Rental Plan with id {rental_plan_id} doesnt exist")

        serializer = UpdateRentalPlanSerializer(data=request.data,instance=rental_plan)
        validate_plan_and_handle_errors(serializer)

        updated_rental_plan = update_rental_plan(
            rental_plan_id=rental_plan_id,
            name=serializer.validated_data.get("name"),
            amount=serializer.validated_data.get("amount"),
            periodicity=serializer.validated_data.get("periodicity"),
        )
        serialized_rental_plan = RentalPlanSerializer(updated_rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_200_OK)

    def delete(self, request, rental_plan_id):
        delete_rental_plan(rental_plan_id)
        return Response(status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from settings.utils.api import APIViewWithPagination
from rest_framework.permissions import IsAuthenticated
from rental.rentalPlan.features import get_rental_plans, create_rental_plan, get_rental_plan, delete_rental_plan, update_rental_plan
from rental.rentalPlan.serializer import CreateRentalPlanSerializer, RentalPlanSerializer, UpdateRentalPlanSerializer
from settings.utils.exceptions import BadRequest400APIException
from rental.tenantUser.permissions import IsAdminTenantUser, IsAdminOrStaffTenantUser

class ListAndCreateRentalPlansView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminTenantUser]

    def get(self, request):
        search_text = request.query_params.get('searchText', None)
        order_by = request.query_params.get('orderBy', 'name')
        asc = request.query_params.get('asc', None)

        try:
            rental_plans_list = get_rental_plans(
                search_text=search_text,
                order_by=order_by,
                asc=False if asc == 'False' else True
            )

            paginator = self.pagination_class()
            paginated_rental_plans = paginator.paginate_queryset(rental_plans_list, request)
            serialized_list = RentalPlanSerializer(paginated_rental_plans, many=True)
            return paginator.get_paginated_response(serialized_list.data)
        except Exception as e:
            raise BadRequest400APIException(str(e))

    def post(self, request):
        serializer = CreateRentalPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_rental_plan = create_rental_plan(
            name=serializer.validated_data['name'],
            amount=serializer.validated_data['amount'],
            periodicity=serializer.validated_data['periodicity'],
        )

        serialized_rental_plan = RentalPlanSerializer(created_rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_201_CREATED)
    

class GetUpdateAndDeleteARentalPlanView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated(), IsAdminTenantUser()]
        return super().get_permissions()

    def get(self, request, rental_plan_id):
        rental_plan = get_rental_plan(rental_plan_id)

        serialized_rental_plan = RentalPlanSerializer(rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_200_OK)

    def put(self, request, rental_plan_id):
        serializer = UpdateRentalPlanSerializer(data={
            'id': rental_plan_id,
            'name': request.data.get('name'),
            'amount': request.data.get('amount'),
            'periodicity': request.data.get('periodicity'),
        })
        serializer.is_valid(raise_exception=True)

        updated_rental_plan = update_rental_plan(
            rental_plan_id=rental_plan_id,
            name=serializer.validated_data.get('name'),
            amount=serializer.validated_data.get('amount'),
            periodicity=serializer.validated_data.get('periodicity'),
        )
        serialized_rental_plan = RentalPlanSerializer(updated_rental_plan)

        return Response(serialized_rental_plan.data, status=status.HTTP_200_OK)

    def delete(self, request, rental_plan_id):
        delete_rental_plan(rental_plan_id)
        return Response(status=status.HTTP_200_OK)

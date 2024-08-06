from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from settings.utils.api import APIViewWithPagination
from settings.utils.exceptions import BadRequest400APIException

from rental.tenantUser.permissions import IsAdminOrStaffTenantUser
from rental.contract_form.serializer import (
    ContractFormTemplateSerializer,
    UpdateContractFormTemplateSerializer,
    ContractFormSerializer,
    CreateContractFormSerializer,
    CloneContractFormTemplateSerializer,
)

from rental.contract_form.features import (
    get_contract_form_templates,
    create_contract_form_template,
    get_contract_form_template,
    delete_contract_form_template,
    update_contract_form_template,
    get_contract_forms,
    create_contract_form,
    clone_contract_form_template,
    get_contract_form,
    create_contract_form_response,
    create_contract_form_pdf,
)
from rental.contract_form.validators import validate_contract_form_response


class ContractFormTemplateListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request: Request):

        tenant = request.user.defaultTenantUser().tenant
        paginator = self.pagination_class()

        try:
            forms_list = get_contract_form_templates(tenant)

            if request.query_params.get("all"):
                serialized_list = ContractFormTemplateSerializer(forms_list, many=True)
                return Response(serialized_list.data, status=status.HTTP_200_OK)

            paginated_forms = paginator.paginate_queryset(forms_list, request)
            serialized_list = ContractFormTemplateSerializer(paginated_forms, many=True)

            return paginator.get_paginated_response(serialized_list.data)
        except Exception as error:
            raise BadRequest400APIException(str(error)) from error

    def post(self, request):

        serializer = ContractFormTemplateSerializer(data=request.data)

        if serializer.is_valid():

            tenant = request.user.defaultTenantUser().tenant
            user = request.user.defaultTenantUser()

            data = {"tenant": tenant, "user": user}
            data.update(serializer.validated_data)

            form = create_contract_form_template(**data)
            serialized_form = ContractFormTemplateSerializer(form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractFormTemplateGetUpdateAndDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, pk):

        tenant = request.user.defaultTenantUser().tenant
        contract_form = get_contract_form_template(tenant, pk)
        serializer = ContractFormTemplateSerializer(contract_form)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        tenant = request.user.defaultTenantUser().tenant
        contract_form = get_contract_form_template(tenant, pk)

        serializer = UpdateContractFormTemplateSerializer(
            contract_form, data=request.data
        )

        if serializer.is_valid():

            form = update_contract_form_template(
                contract_form, **serializer.validated_data
            )
            serialized_form = ContractFormTemplateSerializer(form)

            return Response(serialized_form.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tenant = request.user.defaultTenantUser().tenant
        delete_contract_form_template(tenant, pk)
        return Response("ok", status=status.HTTP_200_OK)


class ContractFormTemplateCloneView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        tenant = request.user.defaultTenantUser().tenant

        serializer = CloneContractFormTemplateSerializer(
            data=request.data, context={"tenant": tenant}
        )

        if serializer.is_valid():

            form = clone_contract_form_template(serializer.instance)

            serialized_form = ContractFormTemplateSerializer(form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractFormListAndCreateView(APIViewWithPagination):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request):

        tenant = request.user.defaultTenantUser().tenant
        paginator = self.pagination_class()

        try:
            forms_list = get_contract_forms(tenant)
            paginated_forms = paginator.paginate_queryset(forms_list, request)
            serialized_list = ContractFormSerializer(paginated_forms, many=True)

            return paginator.get_paginated_response(serialized_list.data)
        except Exception as error:
            raise BadRequest400APIException(str(error)) from error

    def post(self, request):

        tenant = request.user.defaultTenantUser().tenant

        serializer = CreateContractFormSerializer(
            data=request.data, context={"tenant": tenant}
        )

        if serializer.is_valid():

            user = request.user.defaultTenantUser()

            data = {"tenant": tenant, "user": user}
            data.update(serializer.validated_data)

            form = create_contract_form(**data)
            serialized_form = ContractFormSerializer(form)

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractFormGetView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def get(self, request, pk):

        create_pdf = request.query_params.get("pdf")
        tenant = request.user.defaultTenantUser().tenant
        contract_form = get_contract_form(tenant, pk)
        serializer = ContractFormSerializer(
            contract_form, context={"contract_form_id": pk}
        )

        if create_pdf:
            pdf = create_contract_form_pdf(serializer.data)

            response = HttpResponse(
                content_type="application/pdf",
                headers={
                    "Content-Disposition": 'attachment; filename="contract-form.pdf"'
                },
            )
            response.write(pdf)

            return response

        return Response(serializer.data, status=status.HTTP_200_OK)


class ContractFormFieldResponseCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffTenantUser]

    def post(self, request):

        tenant = request.user.defaultTenantUser().tenant

        try:
            validate_contract_form_response(tenant, request.data.dict())
            contract_form = create_contract_form_response(tenant, request.data.dict())
            serialized_form = ContractFormSerializer(
                contract_form, context={"contract_form_id": contract_form.id}
            )

            return Response(serialized_form.data, status=status.HTTP_201_CREATED)

        except Exception as error:
            raise BadRequest400APIException(str(error)) from error

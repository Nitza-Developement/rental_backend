from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.client.serializer import ClientListSerializer, ClientCreateSerializer, ClientUpdateSerializer
from apps.core.client.features import delete_client, get_client, get_clients, create_client, update_client
from apps.core.client.exceptions import validate_client_and_handle_errors


class ClientListAndCreateView(APIView):

    def get(self, request):
        try:
            clients_list = get_clients()
            serialized_list = ClientListSerializer(clients_list, many=True)
            return Response(serialized_list.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=400, data={"error": str(e)})

    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data)
        validate_client_and_handle_errors(serializer)

        created_client = create_client(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            phone_number=serializer.validated_data['phone_number'],
            tenant=serializer.validated_data['tenant']
        )

        serialized_client = ClientListSerializer(created_client)
        return Response(serialized_client.data, status=status.HTTP_201_CREATED)


class ClientGetUpdateAndDeleteView(APIView):

    def get(self, request, client_id):
        try:
            client = get_client(client_id)
            serialized_client = ClientListSerializer(client)
            return Response(serialized_client.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=400, data={"error": str(e)})

    def put(self, request, client_id):
        serializer = ClientUpdateSerializer(data=request.data)
        validate_client_and_handle_errors(serializer)

        updated_client = update_client(
            client_id=client_id,
            name=serializer.validated_data.get('name'),
            email=serializer.validated_data.get('email'),
            phone_number=serializer.validated_data.get('phone_number'),
            tenant=serializer.validated_data.get('tenant')
        )

        serialized_client = ClientListSerializer(updated_client)
        return Response(serialized_client.data, status=status.HTTP_200_OK)

    def delete(self, request, client_id):
        delete_client(client_id)
        return Response(status=status.HTTP_200_OK)

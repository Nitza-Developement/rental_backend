from rental.client.models import Client
from settings.utils.exceptions import NotFound404APIException


def create_client(tenant, name, email, phone_number):
    client = Client.objects.create(
        tenant=tenant,
        name=name,
        email=email,
        phone_number=phone_number
    )
    return client


def get_clients(tenant):
    return Client.objects.filter(tenant=tenant)


def get_client(client_id):
    try:
        return Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        raise NotFound404APIException(f'Client with ID {client_id} doesnt exists')


def update_client(client_id, name=None, email=None, phone_number=None):
    client = get_client(client_id)
    if client:
        if name:
            client.name = name
        if email:
            client.email = email
        if phone_number:
            client.phone_number = phone_number
        client.save()
    else:
        raise NotFound404APIException(f'Client with ID {client_id} doesnt exists')
    return client


def delete_client(client_id):
    client = get_client(client_id)
    if client:
        client.delete()
        return True
    raise NotFound404APIException(f'Client with ID {client_id} doesnt exists')


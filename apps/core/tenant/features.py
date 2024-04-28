from django.db.models import Q
from apps.core.tenant.models import Tenant
from settings.utils.exceptions import NotFound404APIException


def get_tenants(search_text: str = None,
                order_by: str = None,
                asc: bool = True):

    tenants = Tenant.objects.all()

    if search_text:
        tenants = tenants.filter(
            Q(name__icontains=search_text) |
            Q(email__icontains=search_text))

    if order_by:
        if not asc:
            order_by = '-' + order_by
        tenants = tenants.order_by(order_by)

    return tenants


def get_tenant(tenant_id: str):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
    except Tenant.DoesNotExist:
        raise NotFound404APIException(f'Tenant with id {tenant_id} not found')

    return tenant


def create_tenant(
    email: str,
    name: str,
    isAdmin: bool = False
):

    new_tenant = Tenant.objects.create(email=email, name=name, isAdmin=isAdmin)
    new_tenant.save()
    return new_tenant


def update_tenant(
    tenant_id: str,
    email: str,
    name: str,
    isAdmin: bool = False
):

    try:
        tenant = Tenant.objects.get(id=tenant_id)
    except Tenant.DoesNotExist:
        raise NotFound404APIException(f'Tenant with id {tenant_id} not found')

    if email:
        tenant.email = email

    if name:
        tenant.name = name

    if isAdmin is not None:
        tenant.isAdmin = isAdmin

    tenant.full_clean()
    tenant.save()
    return tenant


def delete_tenant(tenant_id):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.delete()

    except Tenant.DoesNotExist:
        raise NotFound404APIException(f'Tenant with id {tenant_id} not found')

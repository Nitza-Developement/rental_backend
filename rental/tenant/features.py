from django.db.models import Q
from rental.models import TenantUser
from rental.tenant.models import Tenant
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
    ownerId: int,
    isAdmin: bool = False,
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

    if ownerId:
        old_owner = TenantUser.objects.get(role=TenantUser.OWNER)
        if old_owner:
            old_owner.role = TenantUser.STAFF
            old_owner.full_clean()
            old_owner.save()
        tenantUser_to_be_owner = TenantUser.objects.get(id=ownerId)
        tenantUser_to_be_owner.role = TenantUser.OWNER
        tenantUser_to_be_owner.full_clean()
        tenantUser_to_be_owner.save()

    tenant.full_clean()
    tenant.save()
    return tenant


def delete_tenant(tenant_id):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.delete()

    except Tenant.DoesNotExist:
        raise NotFound404APIException(f'Tenant with id {tenant_id} not found')

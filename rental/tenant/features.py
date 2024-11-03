from django.db.models import Q

from rental.models import TenantUser
from rental.tenant.models import Tenant
from settings.utils.exceptions import NotFound404APIException


def get_tenants(search_text: str = None, order_by: str = None, asc: bool = True):

    tenants = Tenant.objects.all()

    if search_text:
        tenants = tenants.filter(
            Q(name__icontains=search_text) | Q(email__icontains=search_text)
        )

    if order_by:
        if not asc:
            order_by = "-" + order_by
        tenants = tenants.order_by(order_by)

    return tenants


def get_tenant(tenant_id: str):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
    except Tenant.DoesNotExist:
        raise NotFound404APIException(f"Tenant with id {tenant_id} not found")

    return tenant


def create_tenant(email: str, name: str, isAdmin: bool = False):

    new_tenant = Tenant.objects.create(email=email, name=name, isAdmin=isAdmin)
    new_tenant.save()
    return new_tenant


def update_tenant_owner(tenant: Tenant, owner: int | None):
    if owner is None:
        return

    old_owners = TenantUser.objects.filter(
        tenant=tenant,
        role=TenantUser.OWNER,
    )
    for old_owner in old_owners:
        old_owner.role = TenantUser.STAFF
        old_owner.full_clean()
        old_owner.save()

    new_owner = TenantUser.objects.filter(
        tenant=tenant,
        id=owner,
    ).first()
    if new_owner is None:
        raise NotFound404APIException(f"Tenant User with id {owner} not found")

    new_owner.role = TenantUser.OWNER
    new_owner.full_clean()
    new_owner.save()


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
        raise NotFound404APIException(f"Tenant with id {tenant_id} not found")

    if email:
        tenant.email = email

    if name:
        tenant.name = name

    if isAdmin is not None:
        tenant.isAdmin = isAdmin

    update_tenant_owner(tenant, ownerId)

    tenant.full_clean()
    tenant.save()
    return tenant


def delete_tenant(tenant_id):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.delete()

    except Tenant.DoesNotExist:
        raise NotFound404APIException(f"Tenant with id {tenant_id} not found")

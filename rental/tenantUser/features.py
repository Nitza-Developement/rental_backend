from rental.user.models import User
from rental.user.features import create_user
from rental.tenantUser.models import TenantUser
from settings.utils.exceptions import NotFound404APIException


def create_tenantUser(
        tenant: str,
        email: str,
        role: str,
        is_default=False):

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = create_user(email)

    tenant_user = TenantUser.objects.create(
        tenant=tenant,
        user=user,
        role=role,
        is_default=is_default
    )
    tenant_user.save()
    return tenant_user


def get_tenantUser(tenant_user_id):
    try:
        return TenantUser.objects.get(id=tenant_user_id)
    except TenantUser.DoesNotExist:
        raise NotFound404APIException(
            f'TenantUser with ID {tenant_user_id} doesnt exists')


def get_tenantUsers():
    return TenantUser.objects.all()


def update_tenantUser(tenant_user_id, role=None, is_default=None):
    tenant_user = get_tenantUser(tenant_user_id)
    if tenant_user:
        if role:
            tenant_user.role = role
        if is_default is not None:
            tenant_user.is_default = is_default
            # Ensure only one TenantUser is set as default
            if is_default:
                TenantUser.objects.filter(tenant=tenant_user.tenant, is_default=True).exclude(
                    id=tenant_user.id).update(is_default=False)
        tenant_user.save()
    else:
        raise NotFound404APIException(
            f'TenantUser with ID {tenant_user_id} doesnt exists')
    return tenant_user


def delete_tenantUser(tenant_user_id):
    tenant_user = get_tenantUser(tenant_user_id)
    print(f'EL USER: {tenant_user.user}')
    if tenant_user:
        tenant_user.delete()
        return True
    raise NotFound404APIException(
        f'TenantUser with ID {tenant_user_id} doesnt exists')

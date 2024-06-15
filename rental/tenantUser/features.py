from rental.user.models import User
from rental.user.features import create_user, delete_user
from rental.tenantUser.models import TenantUser
from settings.utils.exceptions import NotFound404APIException


def create_tenantUser(tenant: str, email: str, role: str, is_default=False):

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = create_user(email)

    tenant_user = TenantUser.objects.create(
        tenant=tenant, user=user, role=role, is_default=is_default
    )
    tenant_user.save()
    return tenant_user


def get_tenantUser(tenant_user_id):
    try:
        return TenantUser.objects.get(id=tenant_user_id)
    except TenantUser.DoesNotExist:
        raise NotFound404APIException(
            f"TenantUser with ID {tenant_user_id} doesnt exists"
        )


def get_tenantUsers(user_requesting: User):

    if not user_requesting.defaultTenantUser().tenant.isAdmin:
        return TenantUser.objects.filter(
            tenant=user_requesting.defaultTenantUser().tenant
        )

    return TenantUser.objects.all()


def update_tenantUser(
    tenant_user_id, role=None, is_default=None, tenant=None, email=None, old_email=None
):
    tenant_user = get_tenantUser(tenant_user_id)
    if tenant_user:
        if role:
            tenant_user.role = role
        if tenant:
            tenant_user.tenant = tenant
        if email:
            user = User.objects.get(email=old_email)
            user.email = email
            user.full_clean()
            user.save()

        if is_default is not None:
            current_default = TenantUser.objects.filter(
                user=tenant_user.user, is_default=True
            ).first()
            current_default.is_default = False
            current_default.save()

            tenant_user.is_default = is_default

        tenant_user.full_clean()
        tenant_user.save()
    else:
        raise NotFound404APIException(
            f"TenantUser with ID {tenant_user_id} doesnt exists"
        )
    return tenant_user


def delete_tenantUser(tenant_user_id):
    tenant_user = get_tenantUser(tenant_user_id)
    if tenant_user.is_default:
        tenant_user.is_default = False
        tenant_user.save()

        new_default_tenantUser = (
            TenantUser.objects.filter(user=tenant_user.user)
            .exclude(id=tenant_user.id)
            .first()
        )
        if new_default_tenantUser:
            new_default_tenantUser.is_default = True
            new_default_tenantUser.full_clean()
            new_default_tenantUser.save()
        else:
            delete_user(tenant_user.user.id)
    if tenant_user:
        tenant_user.delete()
        return True
    raise NotFound404APIException(f"TenantUser with ID {tenant_user_id} doesnt exists")

from rental.user.models import User
from rental.user.features import create_user, delete_user
from rental.tenantUser.models import TenantUser
from settings.utils.exceptions import (
    NotFound404APIException,
    BadRequest400APIException,
)


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
    tenant_user_id, is_default=None,
):
    tenant_user = get_tenantUser(tenant_user_id)
    if is_default is not None:
        if (
                (not is_default)
                and tenant_user.is_default
                and not TenantUser.objects.filter(
                            user=tenant_user.user,
                        ).exclude(
                            pk=tenant_user.pk
                        ).exists()
        ):
            raise BadRequest400APIException(
                "It cannot stop being default because it does not exist for this user, only this tenant owns it."
            )
        if is_default and not tenant_user.is_default:
            TenantUser.objects.filter(
                user=tenant_user.user,
                is_default=True
            ).exclude(
                pk=tenant_user.pk
            ).update(
                is_default=False
            )

            tenant_user.is_default = is_default
            tenant_user.full_clean()
            tenant_user.save()

        elif tenant_user.is_default and not is_default:
            tenant_user_default_now=TenantUser.objects.filter(
                user=tenant_user.user,
                is_default=False
            ).exclude(
                pk=tenant_user.pk
            ).first()



            if tenant_user_default_now:
                tenant_user.is_default = is_default
                tenant_user.full_clean()
                tenant_user.save()

                tenant_user_default_now.is_default=True
                tenant_user_default_now.full_clean()
                tenant_user_default_now.save()


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
            user_id=tenant_user.user.id
            tenant_user.delete()
            delete_user(user_id)
            return True

    tenant_user.delete()
    return True


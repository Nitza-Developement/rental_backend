from apps.core.tenant.models import TenantUser


def create_tenantUser(tenant, user, role, is_default=False):
    tenant_user = TenantUser.objects.create(
        tenant=tenant,
        user=user,
        role=role,
        is_default=is_default
    )
    return tenant_user


def get_tenantUsers(tenant):

    return TenantUser.objects.filter(tenant=tenant)


def get_adminTenant_tenantUsers():

    return TenantUser.objects.filter()


def get_tenant_user(tenant_user_id):
    try:
        return TenantUser.objects.get(id=tenant_user_id)
    except TenantUser.DoesNotExist:
        return None


def update_tenant_user(tenant_user_id, role=None, is_default=None):
    tenant_user = get_tenant_user(tenant_user_id)
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
    return tenant_user


def delete_tenant_user(tenant_user_id):
    tenant_user = get_tenant_user(tenant_user_id)
    if tenant_user:
        tenant_user.delete()
        return True
    return False

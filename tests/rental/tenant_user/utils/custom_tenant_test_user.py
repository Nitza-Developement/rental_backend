from attrs import define

from rental.tenantUser.models import TenantUser


@define
class CustomTenantTestUser:
    tenant_user: TenantUser
    password: str

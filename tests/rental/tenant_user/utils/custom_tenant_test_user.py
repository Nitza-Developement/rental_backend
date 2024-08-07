from typing import List

from attrs import define

from rental.tenantUser.models import TenantUser


@define
class CustomTenantTestUser:
    default_tenant_user: TenantUser
    password: str
    list_tenant_user: List[TenantUser] = []

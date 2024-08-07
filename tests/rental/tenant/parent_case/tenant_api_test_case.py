from tests.rental.auth.parent_case.auth_api_test_case import AuthAPITestCase
from tests.rental.tenant.mixin.tenant_mixin import TenantMixin
from tests.rental.tenant_user.mixins.tenant_user_mixin import TenantUserMixin


class TenantApiTestCase(AuthAPITestCase, TenantMixin, TenantUserMixin):
    pass

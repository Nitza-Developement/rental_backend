from rental.tenantUser.models import TenantUser
from tests.rental.auth.utils.custom_test_user import CustomTestUser
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)
from tests.rental.vehicle.mixins.vehicle_mixin import VehicleMixin


class VehicleApiTestCase(TenantApiTestCase, VehicleMixin):
    def setUp(self):
        super().setUp()
        self.custom_tenant_user_staff: CustomTenantTestUser = (
            self.create_tenant_user(role=TenantUser.STAFF)
        )
        self.custom_staff: CustomTestUser = CustomTestUser(
            user=self.custom_tenant_user_staff.default_tenant_user.user,
            password=self.custom_tenant_user_staff.password,
        )

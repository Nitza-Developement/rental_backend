from rental.tenantUser.models import TenantUser
from tests.rental.auth.utils.custom_test_user import CustomTestUser
from tests.rental.client.mixins.client_mixin import ClientMixin
from tests.rental.contract.mixins.contract_mixin import ContractMixin
from tests.rental.note.mixins.note_mixin import NoteMixin
from tests.rental.rental_plan.mixins.rental_plan_mixin import RentalPlanMixin
from tests.rental.tenant.parent_case.tenant_api_test_case import (
    TenantApiTestCase,
)
from tests.rental.tenant_user.utils.custom_tenant_test_user import (
    CustomTenantTestUser,
)
from tests.rental.toll_due.mixins.toll_due_mixin import TollDueMixin
from tests.rental.vehicle.mixins.vehicle_mixin import VehicleMixin


class ContractApiTestCase(
    TenantApiTestCase,
    ClientMixin,
    RentalPlanMixin,
    VehicleMixin,
    TollDueMixin,
    NoteMixin,
    ContractMixin,
):
    def setUp(self):
        super().setUp()
        self.custom_tenant_user_staff: CustomTenantTestUser = (
            self.create_tenant_user(role=TenantUser.STAFF)
        )
        self.custom_staff: CustomTestUser = CustomTestUser(
            user=self.custom_tenant_user_staff.default_tenant_user.user,
            password=self.custom_tenant_user_staff.password,
        )

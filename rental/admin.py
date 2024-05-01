from django.contrib import admin
from django.contrib.auth.models import Group
from rental.models import User, Tenant, TenantUser, Client, Vehicle, VehiclePlate, VehiclePicture

admin.site.site_title = "Fleet Admin Site"
admin.site.site_header = "Administration Panel"
admin.site.index_title = "Dashboard"

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_superuser', 'date_joined']
    search_fields = ('name', 'email')
    date_hierarchy = 'date_joined'


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'user', 'tenant')
    search_fields = ('id', 'user__name', 'tenant__name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'tenant')


class TenantUserInline(admin.TabularInline):
    model = TenantUser
    extra = 0


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 0


class VehiclePlateInline(admin.TabularInline):
    model = VehiclePlate
    extra = 0


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'isAdmin')
    search_fields = ('name', 'email')
    date_hierarchy = 'date_joined'
    inlines = [TenantUserInline, ClientInline, VehicleInline]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'active_plate', 'type', 'year', 'make',
                    'model', 'trim', 'vin', 'nickname', 'spare_tires', 'status')
    search_fields = ('id', 'nickname', 'model', 'vin', 'status')
    inlines = [VehiclePlateInline]

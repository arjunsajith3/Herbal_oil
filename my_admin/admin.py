from django.contrib import admin

from my_admin.models import Customer

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin

from django.contrib.auth.models import User


# -----------------User_Customer------------------------#

class CustomerInline(admin.TabularInline):
    model = Customer


class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)

    list_display = ('username',)


admin.site.unregister(User)

admin.site.register(User, UserAdmin)

# -----------------------End--------------------------------#


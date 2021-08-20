from django.contrib import admin
from .models import CustomUser, Assistant, Doctor, UsersProfile, UserAccountSettings, \
                    UserGeneralSettings, MailingCredential, ContactRequest, Chat, \
                    Message, Product, Plan, Subscription
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserAdmin(BaseUserAdmin):
    """
        DOCSTRING:
        UserAdmin class inherits from BaseUserAdmin, used to update the forms used in the creation and update of the
        CustomUser model.
    """
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (('Title Info', {'fields': ('roll', )}),)
    add_fieldsets = ((None, {'fields': ('username', 'password1', 'password2', 'roll'), }, ), )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Assistant)
admin.site.register(Doctor)
admin.site.register(UsersProfile)
admin.site.register(UserAccountSettings)
admin.site.register(UserGeneralSettings)
admin.site.register(MailingCredential)
admin.site.register(ContactRequest)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Product)
admin.site.register(Plan)
admin.site.register(Subscription)

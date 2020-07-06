from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Following
# Register your models here.

class UsersAdmin(UserAdmin):
    list_display = ('email','username','gender','is_admin')
    list_display_links = ('email','username',)
    list_editable = ('gender',)
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('email','first_name','last_name')
    filter_horizontal = ()
    list_filter       = ('gender',"country",)
    fieldsets         = ()
  

admin.site.register(User, UsersAdmin)

admin.site.register(Following)
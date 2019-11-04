from django.contrib.admin import AdminSite

# from django.contrib.auth.admin import GroupAdmin, UserAdmin
# from django.contrib.auth.models import Group, User


class TANMTAdminSite(AdminSite):
    site_title = 'The All New Magic Tortoise - Administration'
    site_header = 'The All New Magic Tortoise - Administration'
    index_title = 'The All New Magic Tortoise - Administration'


tanmt_admin = TANMTAdminSite()
# tanmt_admin.register(Group, GroupAdmin)
# tanmt_admin.register(User, UserAdmin)

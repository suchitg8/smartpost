from django.contrib import admin
from simply_posted_accounts.models import User, UserAdmin

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
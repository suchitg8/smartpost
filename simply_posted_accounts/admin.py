from django.contrib import admin
from simply_posted_accounts.models import User, UserAdmin
from simply_posted_calendar.models import Publication

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Publication)

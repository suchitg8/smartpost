from django.contrib import admin
from simply_posted_accounts.models import User, UserAdmin ,ContentProvider , DBform

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(ContentProvider)
class ContentProviderAdmin(admin.ModelAdmin):
    list_display = (
        'email','id','first_name','last_name', 'password', 'active'
    )
    search_fields = [
        'email'
    ]
    list_editable = ('active', )
    list_filter = ('active',)

@admin.register(DBform)
class DBformAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'playful_title', 'corporate_title', 'blog_link' ,'image_link','category','contentprovider'
    )
    search_fields = [
        'playful_title','corporate_title'
    ]

    list_filter = ('contentprovider',)
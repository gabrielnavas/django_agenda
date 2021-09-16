from django.contrib import admin

from .models import Category, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'phone',
                    'email', 'date', 'category', 'is_show')
    list_display_links = ('name',)
    list_per_page = 15
    search_fields = ('name', 'last_name', 'phone')
    list_editable = ('phone', 'is_show')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category)

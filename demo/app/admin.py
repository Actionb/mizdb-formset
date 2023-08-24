from django.contrib import admin

from .models import Contact, PhoneNumber


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    class PhoneNumberInline(admin.StackedInline):
        model = PhoneNumber

    inlines = [PhoneNumberInline]

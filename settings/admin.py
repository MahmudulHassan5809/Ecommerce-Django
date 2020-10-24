from django.contrib import admin
from .models import SiteInfo, ContactUs, Banner, AboutUs, SiteAd
# Register your models here.


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_phone', 'site_email']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(SiteInfo, SiteInfoAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone_number', 'solved']
    list_filter = ['solved']
    list_editable = ['solved']
    search_fields = ['phone_number', 'name']


admin.site.register(ContactUs, ContactUsAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    search_fields = ['title']
    list_filter = ['active']
    list_editable = ['active']
    list_perpage = 20


admin.site.register(Banner, BannerAdmin)


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(AboutUs, AboutUsAdmin)


class SiteAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'link','active']
    search_fields = ['title']
    list_filter = ['active']
    list_editable = ['active']
    list_perpage = 20


admin.site.register(SiteAd, SiteAdAdmin)

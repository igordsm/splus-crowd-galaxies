from django.contrib import admin
from .models import GalaxyImage, GalaxyClassification, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
    can_delete = False
    model = Profile
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request,obj)


class ImageClassifications(admin.TabularInline):
    model = GalaxyClassification
    extra = 0
    can_delete = True
    #readonly_fields = ('user', 'galaxy_type')
    

class GalaxyImageAdmin(admin.ModelAdmin):
    class Media:
        js = [
            'https://code.jquery.com/jquery-3.2.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.12/jquery.mask.js',
            'js/image_admin.js'
        ]
    model = GalaxyImage
    list_filter = ['tutorial_image']

    inlines = [ImageClassifications]

admin.site.register(GalaxyImage, GalaxyImageAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

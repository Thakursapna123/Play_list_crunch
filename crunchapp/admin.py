from django.contrib import admin
from .models import *


@admin.register(userProfile)
class PlayList_userProfile(admin.ModelAdmin):
    list_display = ('id',)



@admin.register(UserUniqueToken)
class PlayList_UserUniqueToken(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(AdminPeopleCommentedTemplate)
class PlayList_AdminPeopleCommentedTemplate(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(AdminBannerTemplate)
class PlayList_AdminBannerTemplate(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(prices)
    


    
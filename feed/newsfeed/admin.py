from django.contrib.gis.admin import OSMGeoAdmin
from .models import Activity
from django.contrib import admin
from feed.users.models import User
# Register your models here.


@admin.register(User)
class UserAdmin(OSMGeoAdmin):
    list_display = ('id','location', 'username','profile_picture')


@admin.register(Activity)
class ActivityAdmin(OSMGeoAdmin):
    list_display = ('user','post_type', 'location')



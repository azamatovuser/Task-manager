from django.contrib import admin
from apps.account.models import Account, Friend


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name')


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'friend')
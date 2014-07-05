from django.contrib import admin
from base.models import MoneyAccount, AccountHolder, AccountEntry


# Register your models here.
admin.site.register(AccountHolder)
admin.site.register(MoneyAccount)
admin.site.register(AccountEntry)
from .models import (Customer, Account,
                         Action, Transaction,
                         Transfer, Interest)

from django.contrib import admin

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Interest)